import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dashboard import render_dashboard
from evolucao_temporal import render_temporal

# Configuração da página
st.set_page_config(page_title="Painel Logístico", layout="wide")

# Autenticação Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_key.json", scope)
client = gspread.authorize(creds)

# Nome da planilha e aba
spreadsheet_name = "Planilha_KPIs_Coordenadores RJ MG ES SP JUNHO"
worksheet_name = "Base_Tratada"

# Leitura dos dados
sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Navegação
st.sidebar.title("📊 Navegação")
pagina = st.sidebar.radio("Escolha a página:", ["Dashboard Geral", "Evolução Temporal"])

if pagina == "Dashboard Geral":
    render_dashboard(df)
elif pagina == "Evolução Temporal":
    render_temporal(df)
