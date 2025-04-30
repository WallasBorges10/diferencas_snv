import streamlit as st
import pandas as pd
from io import BytesIO

# Configuração da página para layout wide
st.set_page_config(layout="wide")

def process_data(df_old, df_new):
    # Processando os dataframes (ajustando cabeçalhos e removendo linhas desnecessárias)
    df_new.columns = df_new.iloc[1]
    df_new = df_new.iloc[2:, :]
    df_old.columns = df_old.iloc[1]
    df_old = df_old.iloc[2:, :]
    
    # Concatenando os dataframes
    df = pd.concat([df_old, df_new], axis=0)
    
    # Encontrando diferenças
    df_diff = df[~df.duplicated(keep=False)].sort_values('Código')
    codigos = df_diff['Código'].drop_duplicates()
    
    # Função para agregar diferenças
    def agrega_diferencas(col):
        return ' ============> '.join(set(map(str, col)))
    
    # Agrupando por código e agregando diferenças
    df_dif = df.groupby('Código', as_index=False).agg(agrega_diferencas)
    
    # Filtrando apenas códigos com diferenças
    duplicados = df[df.duplicated('Código', keep=False)]
    diferencas = df_dif[df_dif['Código'].isin(duplicados['Código'].unique())]
    diferencas = diferencas[diferencas['Código'].isin(codigos)]
    
    return diferencas

# Configuração da página
st.title('Comparador de Planilhas SNV')
st.write('Esta aplicação compara duas planilhas SNV (uma anterior e uma mais recente) e mostra as diferenças encontradas.')

# Upload dos arquivos
st.header('Upload dos Arquivos')
col1, col2 = st.columns(2)

with col1:
    st.subheader('Planilha Anterior')
    file_old = st.file_uploader('Carregue a planilha anterior (ex: SNV_202501A.xls)', type=['xls', 'xlsx'], key='old')

with col2:
    st.subheader('Planilha Recente')
    file_new = st.file_uploader('Carregue a planilha mais recente (ex: SNV_202504A.xls)', type=['xls', 'xlsx'], key='new')

# Processamento dos dados
if file_old and file_new:
    try:
        df_old = pd.read_excel(file_old)
        df_new = pd.read_excel(file_new)
        
        with st.spinner('Processando as planilhas...'):
            result = process_data(df_old, df_new)
        
        st.success('Processamento concluído!')
        
        # Mostrando o resultado
        st.header('Diferenças Encontradas')
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
        
    except Exception as e:
        st.error(f'Ocorreu um erro ao processar os arquivos: {e}')
elif file_old or file_new:
    st.warning('Por favor, carregue ambos os arquivos para comparação.')