import pandas as pd

def prepare_dataframe(df, origem):
    """Prepara um dataframe individual"""
    df.columns = df.iloc[1]
    df = df.iloc[2:, :]
    df['_origem'] = origem
    return df

def find_differences(group):
    """Função para agregar diferenças mantendo a ordem ANTIGA -> NOVA"""
    result = {}
    for col in group.columns:
        if col == '_origem':
            valores = sorted(group[col].unique(), key=lambda x: 0 if x == 'ANTIGA' else 1)
            result[col] = ' =====> '.join(valores)
        else:
            valores = []
            seen = set()
            for v in group[col]:
                if v not in seen:
                    seen.add(v)
                    valores.append(str(v))
            result[col] = ' =====> '.join(valores) if len(valores) > 1 else valores[0]
    return pd.Series(result)

def normalize_numeric_columns(df, cols):
    """
    Normaliza colunas numéricas:
    - troca vírgula por ponto
    - converte para float
    - arredonda para 1 casa decimal
    - devolve já com ponto como separador
    """
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '.', regex=False)  # vírgula -> ponto
            )
            # Converte para número e arredonda
            df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
    return df

def process_data(df_old, df_new):
    """Processa os dataframes e encontra as diferenças"""
    
    # Preparar os dataframes
    df_old = prepare_dataframe(df_old, 'ANTIGA')
    df_new = prepare_dataframe(df_new, 'NOVA')

    # 🔧 Normalizar colunas com números decimais
    cols_float = ['km_ini', 'km_fim', 'extensao']
    df_old = normalize_numeric_columns(df_old, cols_float)
    df_new = normalize_numeric_columns(df_new, cols_float)

    # Concatenar (antiga primeiro)
    df = pd.concat([df_old, df_new], axis=0)

    # Encontrar linhas com diferenças
    df_diff = df.iloc[:, :-1][~df.iloc[:, :-1].duplicated(keep=False)].sort_values('Código')
    codigos_com_diff = df_diff['Código'].drop_duplicates()

    # Agrupar e aplicar a função de diferenças
    df_dif = df.groupby('Código', as_index=False).apply(find_differences)

    # Filtrar apenas códigos com diferenças
    duplicados = df[df.duplicated('Código', keep=False)]
    diferencas = df_dif[df_dif['Código'].isin(duplicados['Código'].unique())]
    diferencas = diferencas[diferencas['Código'].isin(codigos_com_diff)]

    return diferencas.drop(columns='_origem')
