import streamlit as st

def setup_page():
    """Configurações iniciais da página"""
    st.set_page_config(layout="wide")
    st.title('Comparador de Planilhas SNV')
    st.write('Esta aplicação compara duas planilhas SNV (uma anterior e uma mais recente) e mostra as diferenças encontradas.')