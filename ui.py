import streamlit as st
from io import BytesIO
import pandas as pd

def file_uploaders():
    """Componentes de upload de arquivos"""
    st.header('Upload dos Arquivos')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Planilha Anterior')
        file_old = st.file_uploader('Carregue a planilha anterior (ex: SNV_202501A.xls)', 
                                  type=['xls', 'xlsx'], key='old')
    
    with col2:
        st.subheader('Planilha Recente')
        file_new = st.file_uploader('Carregue a planilha mais recente (ex: SNV_202504A.xls)', 
                                  type=['xls', 'xlsx'], key='new')
    
    return file_old, file_new

def display_results(result):
    """Exibe os resultados e opção de exportação"""
    if not result.empty:
        st.header('Diferenças Encontradas (ANTIGA =====> NOVA)')
        st.dataframe(result)
        
        # Opção para exportar como Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result.to_excel(writer, index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="Exportar como Excel",
            data=excel_data,
            file_name='diferencas_snv.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.info('Nenhuma diferença encontrada entre as planilhas.')