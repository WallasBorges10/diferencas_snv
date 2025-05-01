# app.py
import streamlit as st
from config import setup_page
from ui import file_uploaders, display_results
from data_processor import process_data
import pandas as pd

def main():
    # Configuração inicial
    setup_page()
    
    # Upload de arquivos
    file_old, file_new = file_uploaders()
    
    # Processamento dos dados
    if file_old and file_new:
        try:
            df_old = pd.read_excel(file_old)
            df_new = pd.read_excel(file_new)
            
            with st.spinner('Processando as planilhas...'):
                result = process_data(df_old, df_new)
            
            st.success('Processamento concluído!')
            display_results(result)
            
        except Exception as e:
            st.error(f'Ocorreu um erro ao processar os arquivos: {e}')
    elif file_old or file_new:
        st.warning('Por favor, carregue ambos os arquivos para comparação.')

if __name__ == '__main__':
    main()