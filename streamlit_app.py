import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def converter_runtime_minutos_int(runtime):
    minutos = int(runtime.replace(' min', ''))
    return minutos

def converter_formato_m_para_hh_mm(runtime):
    minutos = runtime
    horas = minutos // 60
    minutos_restantes = minutos % 60
    return f"{horas}h e {minutos_restantes} min"

def criar_recortes(menor_ano, maior_ano, tamanho_recorte):
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


def calcular_media_notas_por_genero(df, recorte, ordenacao):
    cont_generos = df['Genre'].value_counts()
    filtro_generos = cont_generos[cont_generos > recorte].index
    df_filtrado = df[df['Genre'].isin(filtro_generos)]
    df_generos_IMDB = df_filtrado.groupby('Genre')['IMDB_Rating'].mean()
    df_generos_Meta = df_filtrado.groupby('Genre')['Meta_score'].mean()
    df_nota_por_generos = pd.concat([df_generos_IMDB, df_generos_Meta], axis=1).reset_index()
    df_nota_por_generos = df_nota_por_generos.rename(columns={"Meta_score": "media_Meta", "IMDB_Rating": "media_IMDB"})
    return df_nota_por_generos.sort_values(by=ordenacao, ascending=False)


df = pd.read_csv("imdb_top_1000.csv")


df['IMDB_Rating'] = df['IMDB_Rating'] * 10
df = df.dropna()
df['Gross'] = df['Gross'].str.replace(',', '').astype('float64').astype(int)
df['Runtime'] = df['Runtime'].apply(converter_runtime_minutos_int)
df['Formated_Runtime'] = df['Runtime'].apply(converter_formato_m_para_hh_mm)
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce').dropna().astype(int)

st.title("Análise de Dados IMDb")

st.subheader("Informações Gerais do Dataset")
st.write(f"O dataset possui {df.shape[0]} filmes")
st.subheader("Exemplos de filmes")
n_filmes = 8
df_filmes = df.head(n_filmes)


colunas = st.columns(8)  


for i, row in df_filmes.iterrows():
    coluna = colunas[i % 8]  
    with coluna:
        st.image(row['Poster_Link'], caption=row['Series_Title'])
        st.write("")

st.subheader("Média de notas por recortes de anos:")

tamanho_recorte = st.slider("Selecione o tamanho do recorte (anos):", 1, 20, 3)
menor_ano = st.number_input("Ano inicial:", value=int(1980))
maior_ano = st.number_input("Ano final:", value=int(df['Released_Year'].max()))

df_media_anual = criar_recortes(menor_ano, maior_ano, tamanho_recorte)


fig, ax = plt.subplots()
i = np.arange(len(df_media_anual['recorte_anual']))
ax.bar(i, df_media_anual['media_IMDB'], 0.35, label='IMDB')
ax.bar(i + 0.35, df_media_anual['media_Meta'], 0.35, label='Meta')
ax.set_xticks(i + 0.35 / 2)
ax.set_xticklabels(df_media_anual['recorte_anual'], rotation=45)
ax.legend()
st.pyplot(fig)


def calcular_media_notas_por_genero(df, recorte, ordenacao):
    cont_generos = df['Genre'].value_counts()
    filtro_generos = cont_generos[cont_generos > recorte].index
    cont_generos_filtrado = cont_generos[cont_generos > recorte]
    df_filtrado = df[df['Genre'].isin(filtro_generos)]

    
    df_generos_IMDB = df_filtrado.groupby('Genre')['IMDB_Rating'].mean()
    df_generos_Meta = df_filtrado.groupby('Genre')['Meta_score'].mean()
    df_nota_por_generos = pd.concat([df_generos_IMDB, df_generos_Meta, cont_generos_filtrado], axis=1)
    df_nota_por_generos = df_nota_por_generos.reset_index()
    df_nota_por_generos = df_nota_por_generos.rename(
        columns={"Meta_score": "media_Meta", "IMDB_Rating": "media_IMDB", "count": "quantidade"}
    )
    df_nota_por_generos = df_nota_por_generos.sort_values(by=ordenacao, ascending=False)

    return df_nota_por_generos

def grafico_media_genero(df_media_genero):
    fig, ax = plt.subplots(figsize=(16, 9))  

    largura_barra = 0.5
    i = np.arange(len(df_media_genero['Genre']))

    
    ax.bar(i, df_media_genero['media_IMDB'], largura_barra, label='Média IMDB')
    ax.bar(i + largura_barra, df_media_genero['media_Meta'], largura_barra, label='Média Meta')

    
    ax.set_xlabel('Gênero', fontsize=16)
    ax.set_ylabel('Média das Notas', fontsize=16)
    ax.set_title('Comparação das Médias de Notas IMDB e Meta_score por Gênero de Filme', fontsize=16)
    ax.set_xticks(i + largura_barra / 2)
    ax.set_xticklabels(df_media_genero['Genre'], rotation=45, ha='right', fontsize=16)
    ax.legend(bbox_to_anchor=(1.2, 1.05), fontsize=16)

    
    plt.tight_layout()
    return fig


recorte = st.slider("Número mínimo de filmes por gênero:", 1, 100, 10)
ordenacao = st.selectbox("Ordenar por:", ["media_IMDB", "media_Meta"])

df_media_genero = calcular_media_notas_por_genero(df, recorte, ordenacao)

st.subheader("Gráfico de médias por gênero:")
grafico = grafico_media_genero(df_media_genero)
st.pyplot(grafico)





def calcular_media_notas_por_diretor(df, ordenacao, recorte=5):
    cont_diretores = df['Director'].value_counts()
    filtro_diretores = cont_diretores[cont_diretores > recorte].index
    df_filtrado = df[df['Director'].isin(filtro_diretores)]

    df_media = df.groupby('Director', observed=True).agg(
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean')
    )

    df_media['quantidade'] = cont_diretores
    return df_media.sort_values(by=ordenacao, ascending=False)


def media_gross_diretor(df, recorte=5):
    cont_diretores = df['Director'].value_counts()
    filtro_diretores = cont_diretores[cont_diretores > recorte].index
    df_filtrado = df[df['Director'].isin(filtro_diretores)]

    df_media = df_filtrado.groupby('Director', observed=True).agg(
        media_Gross=('Gross', 'mean'),
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean')
    )

    df_media['quantidade'] = cont_diretores
    return df_media.sort_values(by='media_Gross', ascending=False)


def medias_e_generos_diretor(df, recorte=5):
    cont_diretores = df['Director'].value_counts()
    filtro_diretores = cont_diretores[cont_diretores > recorte].index
    df_filtrado = df[df['Director'].isin(filtro_diretores)]

    df_media = df.groupby('Director', observed=True).agg(
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean'),
        media_Gross=('Gross', 'mean'),
        genero_mais_frequente=('Genre', lambda x: x.value_counts().index[0])
    )

    df_media['quantidade'] = cont_diretores
    return df_media.sort_values(by='media_IMDB', ascending=False)

st.subheader("Análise de médias e gêneros mais frequentes")


def calcular_media_notas_por_intervalo(df, ordenacao):
    cont_duracao = df['duracao'].value_counts()

    df_media = df.groupby('duracao', observed=True).agg(
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean')
    )

    df_media['quantidade'] = cont_duracao
    df_media = df_media.reset_index()
    df_media = df_media.sort_values(by=ordenacao, ascending=False)
    return df_media


def media_gross_duracao(df):
    cont_duracao = df['duracao'].value_counts()

    df_media = df.groupby('duracao', observed=True).agg(
        media_Gross=('Gross', 'mean'),
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean')
    )

    df_media['quantidade'] = cont_duracao
    df_media = df_media.reset_index()
    df_media = df_media.sort_values(by='media_Gross', ascending=False)
    return df_media


def medias_e_generos_duracao(df):
    cont_duracao = df['duracao'].value_counts()

    df_media = df.groupby('duracao', observed=True).agg(
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean'),
        media_Gross=('Gross', 'mean'),
        genero_mais_frequente=('Genre', lambda x: x.value_counts().index[0])
    )

    df_media['quantidade'] = cont_duracao
    df_media = df_media.reset_index()
    return df_media.sort_values(by='media_IMDB', ascending=False)


st.subheader("Ajuste os intervalos de duração com o slider")
min_duracao, max_duracao = st.slider(
    "Defina os limites mínimo e máximo para as durações dos filmes",
    int(df['Runtime'].min()), int(df['Runtime'].max()), (60, 240)
)

step = st.slider("Escolha o tamanho de cada faixa (minutos)", 10, 60, 30)


bins = list(range(min_duracao, max_duracao + step, step))
labels = [f"{bins[i]} a {bins[i + 1]} minutos" for i in range(len(bins) - 1)]
df['duracao'] = pd.cut(df['Runtime'], bins=bins, labels=labels, right=False)


st.subheader("Frequência de filmes por duração")
duracao_counts = df['duracao'].value_counts().sort_index()
fig, ax = plt.subplots()
duracao_counts.plot(kind='bar', ax=ax)
ax.set_title("Frequência de Filmes por Faixa de Duração")
ax.set_ylabel("Quantidade de Filmes")
ax.set_xlabel("Duração")
plt.xticks(rotation=45)
st.pyplot(fig)


st.subheader("Média Meta Score por Duração")
tabela_meta = calcular_media_notas_por_intervalo(df, 'media_Meta')
fig, ax = plt.subplots()
ax.bar(tabela_meta['duracao'], tabela_meta['media_Meta'])
ax.set_title("Média Meta Score por Faixa de Duração")
ax.set_ylabel("Meta Score")
ax.set_xlabel("Duração")
plt.xticks(rotation=45)
st.pyplot(fig)


st.subheader("Média IMDB por Duração")
tabela_imdb = calcular_media_notas_por_intervalo(df, 'media_IMDB')
fig, ax = plt.subplots()
ax.bar(tabela_imdb['duracao'], tabela_imdb['media_IMDB'], color='orange')
ax.set_title("Média IMDB por Faixa de Duração")
ax.set_ylabel("IMDB")
ax.set_xlabel("Duração")
plt.xticks(rotation=45)
st.pyplot(fig)


st.subheader("Gross Médio por Duração")
tabela_gross = media_gross_duracao(df)
fig, ax = plt.subplots()
ax.bar(tabela_gross['duracao'], tabela_gross['media_Gross'], color='green')
ax.set_title("Gross Médio por Faixa de Duração")
ax.set_ylabel("Gross Médio")
ax.set_xlabel("Duração")
plt.xticks(rotation=45)
st.pyplot(fig)






def get_all_stars_count(df):
    all_stars = pd.concat([df['Star1'], df['Star2'], df['Star3'], df['Star4']])
    return all_stars.value_counts()

def calcular_media_notas_por_estrela(df, recorte, ordenacao):
    cont_estrelas = get_all_stars_count(df)
    filtro_estrelas = cont_estrelas[cont_estrelas > recorte].index
    df_filtrado = df[df[['Star1', 'Star2', 'Star3', 'Star4']].apply(
        lambda row: any(star in filtro_estrelas for star in row), axis=1)]

    df_long = df_filtrado.melt(
        id_vars=['IMDB_Rating', 'Meta_score'],
        value_vars=['Star1', 'Star2', 'Star3', 'Star4'],
        value_name='estrela'  
    )

    df_media = df_long.groupby('estrela').agg(
        media_IMDB=('IMDB_Rating', 'mean'),
        media_Meta=('Meta_score', 'mean')
    )

    df_media['quantidade'] = cont_estrelas
    df_media = df_media.loc[filtro_estrelas]
    df_media = df_media.reset_index()
    df_media = df_media.rename(columns={"index": "estrela"})
    df_media = df_media.sort_values(by=ordenacao, ascending=False)

    return df_media


st.title("Análise de Estrelas do Cinema")

recorte = st.slider("Mínimo de Filmes por Estrela", 5, 20, 5)
ordenacao = st.selectbox("Ordenar por", ["media_Meta", "media_IMDB"])

st.header("Média de Notas por Estrela")
df_media = calcular_media_notas_por_estrela(df, recorte, ordenacao)

if ordenacao in df_media.columns:
    st.subheader("Gráfico de Médias")
    plt.figure(figsize=(10, 5))
    plt.bar(df_media['estrela'], df_media[ordenacao])  
    plt.xticks(rotation=90)
    plt.ylabel(ordenacao)
    plt.title("Médias das Estrelas")
    st.pyplot(plt)
else:
    st.error(f"A coluna '{ordenacao}' não foi encontrada no DataFrame. Verifique as configurações.")


recorte = 10

st.subheader("Tabela ordenada por Meta Score")
tabela_meta = calcular_media_notas_por_diretor(df, 'media_Meta', recorte)
st.dataframe(tabela_meta)


st.subheader("Tabela ordenada por IMDB")
tabela_imdb = calcular_media_notas_por_diretor(df, 'media_IMDB', recorte)
st.dataframe(tabela_imdb)

st.subheader("Tabela analisando gêneros mais frequentes")
tabela_generos = medias_e_generos_diretor(df, recorte)
st.dataframe(tabela_generos)
