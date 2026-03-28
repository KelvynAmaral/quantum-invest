import pandas as pd
import streamlit as st

@st.cache_data
def load_excel_data(file_path='cotacoes_ibrx11.xlsx'):
    try:
        sel = pd.read_excel(file_path, sheet_name='Selecao_Carteira')
        cot = pd.read_excel(file_path, sheet_name='Cotacoes')
        ret = pd.read_excel(file_path, sheet_name='Retorno')
        cot['Data'] = pd.to_datetime(cot['Data'])
        ret['Data'] = pd.to_datetime(ret['Data'])
        return sel, cot, ret
    except Exception as e:
        st.error(f"Erro Crítico nos Dados: {e}")
        return None, None, None