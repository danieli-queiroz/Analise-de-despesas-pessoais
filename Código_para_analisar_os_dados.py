import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ajustes visuais dos gráficos
sns.set_theme(style="whitegrid", palette="pastel")

def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv)
    df.columns = df.columns.str.strip().str.title()

    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
        df['Ano'] = df['Data'].dt.year
        df['Mes'] = df['Data'].dt.month
    return df

def calcular_receita_despesa(df):
    receita_total = df[df['Tipo'] == 'Receita']['Valor'].sum()
    despesa_total = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    print(f"Receita total: R${receita_total}")
    print(f"Despesa total: R${despesa_total}")
    return receita_total, despesa_total

def saldo_liquido_mensal(df):
    resumo_mensal = df.groupby(['Ano', 'Mes', 'Tipo'])['Valor'].sum().unstack().fillna(0)
    resumo_mensal['Saldo Líquido'] = resumo_mensal['Receita'] - resumo_mensal['Despesa']
    print(resumo_mensal[['Receita', 'Despesa', 'Saldo Líquido']])
    return resumo_mensal

def top5_categorias(df):
    top5 = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(5)
    print(top5)
    top5.plot(kind='bar', title='Top 5 Categorias de Gasto')
    plt.ylabel('Valor gasto (R$)')
    plt.tight_layout()
    plt.show()

def distribuicao_por_categoria(df):
    gastos = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum()
    porcentagem = (gastos / gastos.sum()) * 100
    print(porcentagem)
    porcentagem.plot(kind='pie', autopct='%1.1f%%', figsize=(7,7), title='Distribuição de Gastos por Categoria')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def essencial_vs_nao(df):
    essenciais = ['Moradia', 'Alimentação', 'Transporte', 'Saúde','Educação']
    df['Essencial'] = df['Categoria'].apply(lambda x: 'Essencial' if x in essenciais else 'Não Essencial')
    resumo = df[df['Tipo'] == 'Despesa'].groupby('Essencial')['Valor'].sum()
    print(resumo)
    resumo.plot(kind='barh', title='Gastos: Essencial vs Não Essencial')
    plt.xlabel('Valor (R$)')
    plt.tight_layout()
    plt.show()

def media_mensal_gastos(df):
    media = df[df['Tipo'] == 'Despesa'].groupby(['Ano', 'Mes'])['Valor'].sum().mean()
    print(f"Gasto médio mensal: R${media:.2f}")

def poupanca_mensal(resumo_mensal):
    resumo_mensal['% Poupança'] = (resumo_mensal['Saldo Líquido'] / resumo_mensal['Receita']) * 100
    print(resumo_mensal[['Saldo Líquido', '% Poupança']])
    return resumo_mensal

def grafico_resumo_mensal(resumo_mensal):
    resumo_mensal[['Receita', 'Despesa', 'Saldo Líquido']].plot(kind='bar', figsize=(10,6), title='Resumo Financeiro Mensal')
    plt.ylabel('R$')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def sazonalidade_categorias(df):
    sazonalidade = df[df['Tipo'] == 'Despesa'].groupby(['Categoria', 'Ano', 'Mes'])['Valor'].sum().reset_index()
    sazonalidade_pivot = sazonalidade.pivot_table(index='Categoria', columns='Mes', values='Valor', aggfunc='sum').fillna(0)
    print("Sazonalidade de gastos por categoria:")
    print(sazonalidade_pivot)
    plt.figure(figsize=(10, 6))
    sns.heatmap(sazonalidade_pivot, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.5)
    plt.title('Sazonalidade de Gastos por Categoria (R$ por Mês)')
    plt.xlabel('Mês')
    plt.ylabel('Categoria')
    plt.tight_layout()
    plt.show()

def grafico_essencial_mensal(df):
    df_despesas = df[df['Tipo'] == 'Despesa']
    essencial_mensal = df_despesas.groupby(['Ano', 'Mes', 'Essencial'])['Valor'].sum().reset_index()
    plt.figure(figsize=(10,6))
    sns.barplot(data=essencial_mensal, x='Mes', y='Valor', hue='Essencial')
    plt.title('Gastos Mensais: Essenciais vs Não Essenciais')
    plt.ylabel('Total Gasto (R$)')
    plt.xlabel('Mês')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def variacao_percentual(df):
    df_despesas = df[df['Tipo'] == 'Despesa']
    cat_mensal = df_despesas.groupby(['Categoria', 'Ano', 'Mes'])['Valor'].sum().reset_index()
    cat_mensal['Data'] = pd.to_datetime(cat_mensal['Ano'].astype(str) + '-' + cat_mensal['Mes'].astype(str))
    cat_mensal = cat_mensal.sort_values(['Categoria', 'Data'])
    cat_mensal['Variação (%)'] = cat_mensal.groupby('Categoria')['Valor'].pct_change() * 100
    plt.figure(figsize=(12,6))
    sns.lineplot(data=cat_mensal, x='Data', y='Variação (%)', hue='Categoria', marker='o')
    plt.title('Variação % Mensal por Categoria')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def desvio_padrao(df):
    df_despesas = df[df['Tipo'] == 'Despesa']
    variabilidade = df_despesas.groupby(['Categoria', 'Mes'])['Valor'].sum().reset_index()
    desvio = variabilidade.groupby('Categoria')['Valor'].std().sort_values(ascending=False)
    print("Desvio padrão dos gastos por categoria:")
    print(desvio)

def gasto_acumulado(df):
    df_despesas = df[df['Tipo'] == 'Despesa']
    acumulado = df_despesas.groupby(['Categoria', 'Ano', 'Mes'])['Valor'].sum().reset_index()
    acumulado['Data'] = pd.to_datetime(acumulado['Ano'].astype(str) + '-' + acumulado['Mes'].astype(str))
    acumulado = acumulado.sort_values(['Categoria', 'Data'])
    acumulado['Gasto Acumulado'] = acumulado.groupby('Categoria')['Valor'].cumsum()
    plt.figure(figsize=(12,6))
    sns.lineplot(data=acumulado, x='Data', y='Gasto Acumulado', hue='Categoria')
    plt.title('Gasto Acumulado por Categoria ao Longo do Ano')
    plt.xticks(rotation=45)
    plt.ylabel('Total Acumulado (R$)')
    plt.tight_layout()
    plt.show()

def main():
    df = carregar_dados('dataset.csv')
    
    calcular_receita_despesa(df)
    resumo = saldo_liquido_mensal(df)
    top5_categorias(df)
    distribuicao_por_categoria(df)
    essencial_vs_nao(df)
    media_mensal_gastos(df)
    resumo = poupanca_mensal(resumo)
    grafico_resumo_mensal(resumo)
    sazonalidade_categorias(df)
    grafico_essencial_mensal(df)
    variacao_percentual(df)
    desvio_padrao(df)
    gasto_acumulado(df)

if __name__ == "__main__":
    main()




