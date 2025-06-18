import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

from dashboard import render_dashboard
from evolucao_temporal import render_temporal

# Configuração da página
st.set_page_config(page_title="Painel Logístico", layout="wide")

# Escopo necessário para acessar o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = st.secrets["google_service_account"]  # já é um dicionário válido
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Nome da planilha e aba
SHEET_NAME = "Planilha_KPIs_Coordenadores RJ MG ES SP JUNHO"
worksheet = client.open(SHEET_NAME).sheet1

# Lê os dados e transforma em DataFrame
sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.sidebar.title("📊 Navegação")
pagina = st.sidebar.radio("Escolha a página:", ["Dashboard Geral", "Evolução Temporal"])

if pagina == "Dashboard Geral":
    render_dashboard(df)
elif pagina == "Evolução Temporal":
    render_temporal(df)
