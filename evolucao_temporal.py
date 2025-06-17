import streamlit as st
import pandas as pd
import plotly.express as px

def render_temporal(df):
    st.title("📈 Evolução Temporal - Delivery Success")

    # Conversão
    df["Data Formatada"] = pd.to_datetime(df["Data Formatada"], format="%d/%m/%Y", errors="coerce")
    df["DS Num"] = pd.to_numeric(df["DS Num"], errors="coerce")

    # Filtros
    st.sidebar.header("Filtros")
    coordenadores = st.sidebar.multiselect("Coordenador", sorted(df["Coordenador"].dropna().unique()))
    bases = st.sidebar.multiselect("Base", sorted(df["Base"].dropna().unique()))
    data_min = df["Data Formatada"].min()
    data_max = df["Data Formatada"].max()
    data_inicio, data_fim = st.sidebar.date_input("Intervalo de Data", [data_min, data_max])

    # Aplicar filtros
    df_filtrado = df[
        (df["Data Formatada"] >= pd.to_datetime(data_inicio)) &
        (df["Data Formatada"] <= pd.to_datetime(data_fim)) &
        (df["DS Num"] > 0)
    ]
    if coordenadores:
        df_filtrado = df_filtrado[df_filtrado["Coordenador"].isin(coordenadores)]
    if bases:
        df_filtrado = df_filtrado[df_filtrado["Base"].isin(bases)]

    # Agrupar por Coordenador + Data para obter a média do dia
    df_agrupado = (
        df_filtrado
        .groupby(["Data Formatada", "Coordenador"], as_index=False)["DS Num"]
        .mean()
    )

    # Gráfico
    if df_agrupado.empty:
        st.warning("Nenhum dado disponível para o período e filtros selecionados.")
    else:
        st.markdown("### DS (%) por Data (média por Coordenador)")
        fig = px.line(
            df_agrupado,
            x="Data Formatada",
            y="DS Num",
            color="Coordenador",
            markers=True,
            title="Evolução do Delivery Success por Coordenador (média diária)"
        )
        st.plotly_chart(fig, use_container_width=True)
