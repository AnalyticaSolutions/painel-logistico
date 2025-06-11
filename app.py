import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel Logístico", layout="wide")
st.title("📦 Painel Logístico - Mercado Livre")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    caminho = "data/Planilha_KPIs.csv"
    df = pd.read_csv(caminho)
    return df

df = carregar_dados()

# Filtros interativos
st.sidebar.header("Filtros")
bases = st.sidebar.multiselect("Base", options=df["Base"].dropna().unique())
coordenadores = st.sidebar.multiselect("Coordenador", options=df["Coordenador"].dropna().unique())
datas = st.sidebar.multiselect("Data", options=df["Data"].dropna().unique())

df_filtrado = df.copy()
if bases:
    df_filtrado = df_filtrado[df_filtrado["Base"].isin(bases)]
if coordenadores:
    df_filtrado = df_filtrado[df_filtrado["Coordenador"].isin(coordenadores)]
if datas:
    df_filtrado = df_filtrado[df_filtrado["Data"].isin(datas)]

# KPIs principais
st.subheader("🔢 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Rotas", df_filtrado["Rotas"].sum())
col2.metric("Média de DS (%)", f'{df_filtrado["DS (%)"].str.replace(",", ".").str.rstrip("%").astype(float).mean():.1f}%')
col3.metric("Carros sem Motorista", df_filtrado["Sem Motorista"].sum())

df_filtrado["DS_float"]
col4.metric("Carros em Manutenção", df_filtrado["Carros em manutenção"].sum())

df_filtrado["DS_float"] = (
    df_filtrado["DS (%)"]
    .astype(str)
    .str.replace(",", ".")
    .str.replace("%", "")
    .astype(float)
)

df_ds_base = df_filtrado.groupby("Base", as_index=False)["DS_float"].mean()

st.subheader("📈 Desempenho médio por Base (% DS)")
fig = px.bar(
    df_ds_base,
    x="Base",
    y="DS_float",
    text_auto=".1f",
    labels={"DS_float": "DS (%)"},
    title=("Média de DS (%) por Base"),
    color="DS_float",
    color_continuous_scale="Blues"
)
fig.update_layout(xaxis_title="Base", yaxis_title="DS (%)")
st.plotly_chart(fig, use_container_width=True)

# Exibir tabela com os dados
st.subheader("📋 Tabela de Dados Filtrados")
st.dataframe(df_filtrado)
