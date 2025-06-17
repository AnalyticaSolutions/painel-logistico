import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Escopo necessário para acessar o Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carrega o segredo do arquivo `secrets.toml`
google_secrets = st.secrets["google_service_account"]
creds_dict = dict(google_secrets)  # converte para dict normal
creds_json = json.loads(json.dumps(creds_dict))  # garante que está no formato certo

# Autentica com o Google
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Nome da planilha e aba
SHEET_NAME = "Planilha_KPIs_Coordenadores RJ MG ES SP JUNHO"
worksheet = client.open(SHEET_NAME).sheet1

# Lê os dados e transforma em DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Mostra os dados
st.title("Painel Logístico")
st.write("Dados carregados com sucesso:")
st.dataframe(df)
