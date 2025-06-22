import streamlit as st
import pandas as pd
import plotly.express as px

def render_temporal(df):
    st.markdown("<h1 style='text-align: center; color: white;'>📈 Evolução Temporal - Delivery Success</h1>", unsafe_allow_html=True)

    df["Data Formatada"] = pd.to_datetime(df["Data Formatada"], format="%d/%m/%Y", errors="coerce")
    df["DS Num"] = pd.to_numeric(df["DS Num"], errors="coerce")

    # Filtros
    st.sidebar.header("🎯 Filtros")
    coordenadores = st.sidebar.multiselect("👤 Coordenador", sorted(df["Coordenador"].dropna().unique()))
    bases = st.sidebar.multiselect("📍 Base", sorted(df["Base"].dropna().unique()))
    data_min = df["Data Formatada"].min()
    data_max = df["Data Formatada"].max()
    data_inicio, data_fim = st.sidebar.date_input("📅 Intervalo de Data", [data_min, data_max])

    df_filtrado = df[
        (df["Data Formatada"] >= pd.to_datetime(data_inicio)) &
        (df["Data Formatada"] <= pd.to_datetime(data_fim)) &
        (df["DS Num"] > 0)
    ]
    if coordenadores:
        df_filtrado = df_filtrado[df_filtrado["Coordenador"].isin(coordenadores)]
    if bases:
        df_filtrado = df_filtrado[df_filtrado["Base"].isin(bases)]

    st.markdown("### 📊 Evolução Diária do Delivery Success")
    df_agrupado = df_filtrado.groupby(["Data Formatada", "Coordenador"], as_index=False)["DS Num"].mean()

    if df_agrupado.empty:
        st.warning("Nenhum dado disponível para o período selecionado.")
    else:
        fig = px.line(
            df_agrupado,
            x="Data Formatada",
            y="DS Num",
            color="Coordenador",
            markers=True,
            template="plotly_dark",
            title="Média diária do DS por Coordenador",
            color_discrete_map={
                "Jonathas": "#1d4ed8",
                "Sabrina": "#3b82f6",
                "Érica": "#4ade80"
            }
        )
        fig.update_layout(
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(color="white"),
            xaxis_title="Data Formatada",
            yaxis_title="DS Num"
        )
        st.plotly_chart(fig, use_container_width=True)
