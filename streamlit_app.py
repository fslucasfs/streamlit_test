import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar e limpar os dados
def load_and_clean_data():
    df = pd.read_csv("imdb_top_1000.csv")
    
    # Ajuste nas colunas
    df['IMDB_Rating'] = df['IMDB_Rating'] * 10
    df['Gross'] = df['Gross'].str.replace(',', '')
    df['Gross'] = df['Gross'].astype('float64')
    df['Gross'] = df['Gross'].replace(np.nan, 0)
    df['Gross'] = df['Gross'].astype(int)
    df = df.dropna()  # Remove linhas com valores nulos

    # Convertendo formato de Runtime
    def converter_formato_m_para_hh_mm(runtime):
        minutos = int(runtime.replace(' min', ''))
        horas = minutos // 60
        minutos_restantes = minutos % 60
        return f"{horas}h e {minutos_restantes} min"

    df['Runtime'] = df['Runtime'].apply(converter_formato_m_para_hh_mm)

    # Convertendo o ano de lançamento
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
    df = df.dropna(subset=['Released_Year'])
    df['Released_Year'] = df['Released_Year'].astype(int)

    return df

# Função para criar recortes de 20 anos e calcular médias
def criar_recortes(menor_ano, maior_ano, tamanho_recorte, df):
    results = []
    for ano in range(menor_ano, maior_ano + 1, tamanho_recorte):
        ultimo_ano = min(ano + tamanho_recorte - 1, maior_ano)
        recorte_ano = df[(df['Released_Year'] >= ano) & (df['Released_Year'] <= ultimo_ano)]

        if not recorte_ano.empty:
            media_IMDB = recorte_ano['IMDB_Rating'].mean()
            media_Meta = recorte_ano['Meta_score'].mean()
            quantidade_filmes = recorte_ano.shape[0]
            results.append({'recorte_anual': f'{ano}-{ultimo_ano}', 'media_IMDB': media_IMDB, 'media_Meta': media_Meta, 'quantidade': quantidade_filmes})

    df_media_anual = pd.DataFrame(results)
    df_media_anual = df_media_anual.sort_values(by='recorte_anual', ascending=False)
    return df_media_anual

# Função para gerar gráficos comparando notas IMDB e Meta_score
def plot_comparacao_media_notas(df_media_anual):
    fig, ax = plt.subplots(figsize=(12, 6))
    largura_barra = 0.35
    i = np.arange(len(df_media_anual['recorte_anual']))
    barra_1 = ax.bar(i, df_media_anual['media_IMDB'], largura_barra, label='Média IMDB')
    barra_2 = ax.bar(i + largura_barra, df_media_anual['media_Meta'], largura_barra, label='Média Meta_score')

    ax.set_xlabel('Recorte Anual')
    ax.set_ylabel('Média das Notas')
    ax.set_title('Comparação das Médias de Notas IMDB e Meta_score por Recorte Anual')
    ax.set_xticks(i + largura_barra / 2)
    ax.set_xticklabels(df_media_anual['recorte_anual'], rotation=30, ha='right')
    ax.legend(bbox_to_anchor=(1.2, 1.05))

    plt.tight_layout()
    st.pyplot(fig)

# Função para calcular a média das notas por gênero
def calcular_media_notas_por_genero(df, recorte=10, ordenacao='media_Meta'):
    cont_generos = df['Genre'].value_counts()
    filtro_generos = cont_generos[cont_generos > recorte].index
    cont_generos_filtrado = cont_generos[cont_generos > recorte]
    df_filtrado = df[df['Genre'].isin(filtro_generos)]

    df_generos_IMDB = df_filtrado.groupby('Genre')['IMDB_Rating'].mean()
    df_generos_Meta = df_filtrado.groupby('Genre')['Meta_score'].mean()
    df_nota_por_generos = pd.concat([df_generos_IMDB, df_generos_Meta, cont_generos_filtrado], axis=1)
    df_nota_por_generos = df_nota_por_generos.reset_index()
    df_nota_por_generos = df_nota_por_generos.rename(columns={"Meta_score": "media_Meta", "IMDB_Rating": "media_IMDB", "count": "quantidade"})
    df_nota_por_generos = df_nota_por_generos.sort_values(by=ordenacao, ascending=False)

    return df_nota_por_generos

# Função para gerar gráfico de barras por gênero
def plot_comparacao_por_genero(df_media_genero):
    fig, ax = plt.subplots(figsize=(12, 6))
    largura_barra = 0.35
    i = np.arange(len(df_media_genero['Genre']))
    barra_1 = ax.bar(i, df_media_genero['media_IMDB'], largura_barra, label='Média IMDB')
    barra_2 = ax.bar(i + largura_barra, df_media_genero['media_Meta'], largura_barra, label='Média Meta')

    ax.set_xlabel('Gênero')
    ax.set_ylabel('Média das Notas')
    ax.set_title('Comparação das Médias de Notas IMDB e Meta_score por Gênero de filme')
    ax.set_xticks(i + largura_barra / 2)
    ax.set_xticklabels(df_media_genero['Genre'], rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.2, 1.05))

    plt.tight_layout()
    st.pyplot(fig)

# Função principal do app
def main():
    st.title('Análise de Filmes IMDB')

    # Carregar e limpar os dados
    df = load_and_clean_data()

    st.subheader("Informações Gerais do Dataset")
    st.write(f"O dataset possui {df.shape[0]} filmes e {df.shape[1]} colunas.")
    st.subheader("Exemplos de filmes")
    n_filmes = 20
    df_filmes = df.head(n_filmes)

    # Exibindo os filmes em 4 colunas
    colunas = st.columns(8)  # Cria 4 colunas

    # Iterando pelos filmes e colocando nas colunas
    for i, row in df_filmes.iterrows():
        coluna = colunas[i % 8]  # Ciclando pelas 4 colunas
        with coluna:
            st.image(row['Poster_Link'], caption=row['Series_Title'], use_column_width=True)
            st.write("")

    # Seção para análise por ano
    st.subheader("Análise por Ano")
    menor_ano = df['Released_Year'].min()
    maior_ano = df['Released_Year'].max()

    recorte = st.slider("Escolha o tamanho do recorte de anos", min_value=1, max_value=50, value=20, step=1)
    df_media_anual = criar_recortes(menor_ano, maior_ano, recorte, df)
    plot_comparacao_media_notas(df_media_anual)

    # Seção para análise por gênero
    st.subheader("Análise por Gênero")
    recorte_genero = st.slider("Escolha o número mínimo de filmes para incluir no gênero", min_value=5, max_value=50, value=10, step=1)
    ordenacao = st.selectbox("Escolha a métrica de ordenação", ['media_Meta', 'media_IMDB'])
    df_media_genero = calcular_media_notas_por_genero(df, recorte_genero, ordenacao)
    plot_comparacao_por_genero(df_media_genero)

if __name__ == "__main__":
    main()
