# %% bibliotecas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf

st.set_page_config(page_title="Dados do Tesouro Direto",page_icon="💰", layout="wide")
@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
# %% Funções

def busca_titulos_td():
  '''
  Função que retorna todos os títulos do Tesouro
  Ela agrega os títulos por Nome e Data de Vencimento usando o Multindex do Pandas.
  '''
  url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
  df = pd.read_csv(url, sep=';', decimal = ',')
  df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], dayfirst=True)
  df['Data Base']       = pd.to_datetime(df['Data Base'], dayfirst=True)
  multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
  df = df.set_index(multi_indice).iloc[: , 3:]  
  return df

def busca_vendas_tesouro():
  ''' 
  Função de busca das vendas 
  '''
  url = "https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv"
  df  = pd.read_csv(url, sep=';', decimal=',')
  df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], dayfirst=True)
  df['Data Venda']       = pd.to_datetime(df['Data Venda'], dayfirst=True)
  multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
  df = df.set_index(multi_indice).iloc[: , 3:]  
  return df

def busca_recompras_tesouro():
  url = "https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv"
  df  = pd.read_csv(url, sep=';', decimal=',')
  df['Vencimento do Titulo'] = pd.to_datetime(df['Vencimento do Titulo'], dayfirst=True)
  df['Data Resgate']       = pd.to_datetime(df['Data Resgate'], dayfirst=True)
  multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
  df = df.set_index(multi_indice).iloc[: , 3:]  
  return df

#%%
st.title("💰 Dados do Tesouro Direto")

titulos = busca_titulos_td()
titulos.sort_index(inplace=True)

tipos_titulos = tipos_titulos = titulos.index.droplevel(level=1).droplevel(level=1).drop_duplicates().to_list()
tipos_titulos.sort(reverse=True)
TipoTesouro = st.sidebar.selectbox('Tipo Tesouro', tipos_titulos)

# %% Selecionar data e tipo de tesouro
DatasVenc = titulos.loc[(TipoTesouro)].index.droplevel(level=1).drop_duplicates()
DatasVenc = DatasVenc.sort_values(ascending=False)

Vencimento = st.sidebar.selectbox('Data Vencimento', DatasVenc[DatasVenc > '2020-12-31'].strftime('%Y-%m-%d'))

preco = titulos.loc[(TipoTesouro, Vencimento)]


fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=("Preço Unitário", "Taxa"),
    column_widths=[0.6, 0.4]
    )

trace1 = go.Scatter(
    x=preco.index.values,
    y=preco['PU Base Manha'],
    name="Preço Uniário",
    hoverinfo = 'y',
    marker=dict(
            color='MediumBlue',
            size=5
            ),
    showlegend = False
    )
trace2 = go.Scatter(
    x=preco.index.values,
    y=preco['Taxa Venda Manha'],
    name="Taxa",
    hoverinfo = 'y',
    marker=dict(
            color='mediumvioletred',
            size=5
            ),
    showlegend = False
    )
fig.add_trace(trace1, row=1, col=1)
fig.add_trace(trace2, row=1, col=2)

fig.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=20, b=0),
    hovermode="x unified") 

st.header(TipoTesouro+' '+ Vencimento)
st.plotly_chart(fig, use_container_width=True)


#%%
trace3 = go.Scatter(
    x=preco.index.values,
    y=preco['PU Compra Manha'],
    name="Preço Compra",
    marker=dict(
            color='lightseagreen',
            size=5
            )
    )
trace4 = go.Scatter(
    x=preco.index.values,
    y=preco['PU Venda Manha'],
    name="Preço Venda",
    marker=dict(
            color='Tomato',
            size=5
            )
    )

fig2 = go.Figure(
    data=[trace3, trace4]
)


fig2.update_layout(
    margin=dict(l=0, r=0, t=20, b=0),
    hovermode="x unified")

st.header('Preço de Compra e Venda')
st.plotly_chart(fig2, use_container_width=True)

# Footer
footer="""<style>
a:link , a:visited{
color: gray;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: Tomato;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
#MainMenu {visibility: hidden;}
</style>
<div class="footer">
<p>Made in <a href='https://https://streamlit.io'><img src='https://avatars3.githubusercontent.com/u/45109972?s=400&v=4' style='width:25px;height:25px'></a>
by <a style='display: block; text-align: center;' href="http://vitor.tk/" target="_blank">/home/vitor</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)