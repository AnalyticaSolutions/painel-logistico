import streamlit as st
import plotly.express as px
import pandas as pd
import io

def render_dashboard(df):
    st.title("📊 Painel Logístico - Coordenadores")

    # Conversão de colunas
    df["Data Formatada"] = pd.to_datetime(df["Data Formatada"], format="%d/%m/%Y", errors="coerce")

    colunas_numericas = [
        "DS Num", "Utilizacao BSC Num", "Utilizacao Diario de Bordo",
        "Carros em Manutencao", "Sem Motorista", "Rotas"
    ]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filtros
    st.sidebar.header("Filtros")
    coordenadores = st.sidebar.multiselect("Coordenador", sorted(df["Coordenador"].dropna().unique()))
    bases = st.sidebar.multiselect("Base", sorted(df["Base"].dropna().unique()))
    data_min = df["Data Formatada"].min()
    data_max = df["Data Formatada"].max()
    data_inicio, data_fim = st.sidebar.date_input("Intervalo de Data", [data_min, data_max])

    df_filtrado = df[
        (df["Data Formatada"] >= pd.to_datetime(data_inicio)) &
        (df["Data Formatada"] <= pd.to_datetime(data_fim))
    ]
    if coordenadores:
        df_filtrado = df_filtrado[df_filtrado["Coordenador"].isin(coordenadores)]
    if bases:
        df_filtrado = df_filtrado[df_filtrado["Base"].isin(bases)]

    df_validado_ds = df_filtrado[df_filtrado["DS Num"] > 0]
    df_validado_util = df_filtrado[df_filtrado["Utilizacao BSC Num"] > 0]

    # Indicadores principais
    st.markdown("### Indicadores Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rotas", int(df_filtrado["Rotas"].sum()))
    col2.metric("DS Médio (%)", f"{df_validado_ds['DS Num'].mean():.2f}" if not df_validado_ds.empty else "N/A")
    col3.metric("Utilização Média (%)", f"{df_validado_util['Utilizacao BSC Num'].mean():.2f}" if not df_validado_util.empty else "N/A")

    col4, col5, col6 = st.columns(3)
    col4.metric("Utilização Diário de Bordo", int(df_filtrado["Utilizacao Diario de Bordo"].sum()))
    col5.metric("Carros em Manutenção", int(df_filtrado["Carros em Manutencao"].sum()))
    col6.metric("Sem Motorista", int(df_filtrado["Sem Motorista"].sum()))

    # Gráfico de barras
    st.markdown("### Delivery Success por Coordenador")
    if not df_validado_ds.empty:
        grafico = px.bar(
            df_validado_ds,
            x="Coordenador",
            y="DS Num",
            color="Coordenador",
            title="DS (%) por Coordenador",
            text="DS Num"
        )
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.warning("Nenhum dado válido encontrado para gerar o gráfico.")

    # Exportar dados
    st.markdown("### 📥 Exportar Dados Filtrados")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Dados Filtrados')
    processed_data = output.getvalue()
    st.download_button(
        label="📄 Baixar Excel",
        data=processed_data,
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
