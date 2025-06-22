import streamlit as st

def card_indicador(titulo, valor, icone):
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #065f46, #16a34a);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            color: white;
            text-align: center;
            margin-bottom: 10px;">
            <div style="font-size: 20px;">{icone} <strong>{titulo}</strong></div>
            <div style="font-size: 36px; font-weight: bold;">{valor}</div>
            <div style="font-size: 14px; margin-top: 5px;">📈 Progresso semanal</div>
        </div>
    """, unsafe_allow_html=True)