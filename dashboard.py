import streamlit as st
import plotly.express as px
import pandas as pd
import io
from utils import card_indicador  # função personalizada de card estilizado

def render_dashboard(df):
    st.markdown("<h1 style='text-align: center; color: white;'>📊 Painel Logístico - Coordenadores</h1>", unsafe_allow_html=True)

    # Conversão de datas e numéricos
    df["Data Formatada"] = pd.to_datetime(df["Data Formatada"], format="%d/%m/%Y", errors="coerce")
    colunas_numericas = ["DS Num", "Utilizacao BSC Num", "Utilizacao Diario de Bordo", "Carros em Manutencao", "Sem Motorista", "Rotas"]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filtros
    st.sidebar.header("🎯 Filtros")
    coordenadores = st.sidebar.multiselect("👤 Coordenador", sorted(df["Coordenador"].dropna().unique()))
    bases = st.sidebar.multiselect("📍 Base", sorted(df["Base"].dropna().unique()))
    data_min = df["Data Formatada"].min()
    data_max = df["Data Formatada"].max()
    data_inicio, data_fim = st.sidebar.date_input("📅 Intervalo de Data", [data_min, data_max])

    df_filtrado = df[(df["Data Formatada"] >= pd.to_datetime(data_inicio)) & (df["Data Formatada"] <= pd.to_datetime(data_fim))]
    if coordenadores:
        df_filtrado = df_filtrado[df_filtrado["Coordenador"].isin(coordenadores)]
    if bases:
        df_filtrado = df_filtrado[df_filtrado["Base"].isin(bases)]

    df_validado_ds = df_filtrado[df_filtrado["DS Num"] > 0]
    df_validado_util = df_filtrado[df_filtrado["Utilizacao BSC Num"] > 0]
    ultimo_dia = df_filtrado["Data Formatada"].max()
    df_ultimo_dia = df_filtrado[df_filtrado["Data Formatada"] == ultimo_dia]

    # Indicadores principais
    st.markdown("### 🔍 Indicadores Gerais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_indicador("Rotas", int(df_filtrado["Rotas"].sum()), "🛣️")
    with col2:
        media_ds = f"{df_validado_ds['DS Num'].mean():.2f}" if not df_validado_ds.empty else "N/A"
        card_indicador("DS Médio (%)", media_ds, "🎯")
    with col3:
        media_util = f"{df_validado_util['Utilizacao BSC Num'].mean():.2f}" if not df_validado_util.empty else "N/A"
        card_indicador("Utilização Média (%)", media_util, "📊")
    with col4:
        card_indicador("Sem Motorista", int(df_ultimo_dia['Sem Motorista'].sum()), "⚠️")

    col5, col6 = st.columns(2)
    with col5:
        card_indicador("Utilização Diário de Bordo", int(df_filtrado["Utilizacao Diario de Bordo"].sum()), "📘")
    with col6:
        card_indicador("Carros em Manutenção", int(df_ultimo_dia["Carros em Manutencao"].sum()), "🛠️")

    # Gráfico de barras - DS ordenado por média
    st.markdown("### 📊 Delivery Success por Coordenador")
    if not df_validado_ds.empty:
        df_ordenado = (
            df_validado_ds
            .groupby("Coordenador", as_index=False)["DS Num"]
            .mean()
            .sort_values(by="DS Num", ascending=False)
        )

        grafico = px.bar(
            df_ordenado,
            x="Coordenador",
            y="DS Num",
            color="Coordenador",
            text="DS Num",
            template="plotly_dark",
            color_discrete_sequence=["#16a34a", "#22c55e", "#4ade80"]
        )
        grafico.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        grafico.update_layout(
            xaxis_title="Coordenador",
            yaxis_title="DS Num",
            font=dict(color="white"),
            plot_bgcolor='#111827',
            paper_bgcolor='#111827'
        )
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.warning("Nenhum dado válido encontrado para gerar o gráfico.")

    # Exportar
    st.markdown("### 📥 Exportar Dados Filtrados")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Dados Filtrados')
    st.download_button(
        label="📄 Baixar Excel",
        data=output.getvalue(),
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
