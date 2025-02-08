import pandas as pd
import streamlit as st

from aux_app_04 import requisitar_filmes


@st.cache_data
def read_data() -> pd.DataFrame:
    return requisitar_filmes()


df: pd.DataFrame = read_data()

filtro_1, filtro_2 = st.columns(2)

ano_lancamento = filtro_1.multiselect('Ano de Lançamento:', df['Ano de Lançamento'].unique())
indicacao_idade = filtro_2.multiselect('Indicação de Idade:', df['Indicação de Idade'].unique())

if len(ano_lancamento) != 0:
    df = df.query(f'`Ano de Lançamento` in {ano_lancamento}')

if len(indicacao_idade) != 0:
    df = df.query(f'`Indicação de Idade` in {indicacao_idade}')



st.subheader(f'Os {df.shape[0]} melhores filmes do IMDb')

# show informations basics

columns = st.columns(3)

for i, (_, j) in enumerate(df.iterrows()):
    with columns[i % 3]:  # Alternando entre as colunas (0, 1, 2)
        with st.container(border=True):
            st.write(f"**{j['Título']}**")
            st.image(j['Capa'])
            a, b = st.columns(2)
            a.write(f"Ano: {j['Ano de Lançamento']}")
            b.write(f"Duração: {j['Duração']} min")

            a.write(f"Classificação: {j['Indicação de Idade']}")
            b.write(f"IMDb: {j['Avaliação do IMDb']}⭐")
