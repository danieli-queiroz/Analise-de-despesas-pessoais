from google.colab import files
import pandas as pd

def upload_arquivo():
    print("Faça upload do arquivo CSV com os dados financeiros:")
    uploaded = files.upload()
    return list(uploaded.keys())[0]  # retorna o nome do arquivo enviado

def carregar_dados(nome_arquivo):
    df = pd.read_csv(nome_arquivo, parse_dates=['Data'])
    df.columns = df.columns.str.strip().str.title()
    return df

def visualizar_dados(df):
    print("Primeiras linhas do DataFrame:")
    print(df.head())

def verificar_tipos_ausentes(df):
    print("\n Informações gerais:")
    print(df.info())
    print("\n Valores ausentes por coluna:")
    print(df.isnull().sum())

def limpar_e_transformar(df):
    print("\n Iniciando limpeza e transformação dos dados...")
    
    # Padroniza a coluna Valor
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    
    # Cria colunas Ano e Mês
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month

    # Remove duplicatas
    df = df.drop_duplicates()

    print("Limpeza finalizada!")
    return df

def main():
    nome_arquivo = upload_arquivo()  # Faça upload do arquivo
    if nome_arquivo.lower() != "dataset.csv":
        print("Você subiu um arquivo diferente de 'dataset.csv'.")
        print(f"Renomeie o arquivo para 'dataset.csv' ou altere o código para: {nome_arquivo}")
    
    df = carregar_dados("dataset.csv")
    visualizar_dados(df)
    verificar_tipos_ausentes(df)
    df = limpar_e_transformar(df)

    print("\n Dados após limpeza:")
    print(df.head())

if __name__ == "__main__":
    main()


