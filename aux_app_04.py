#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd


def requisitar_filmes():
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

    # Definindo headers para evitar bloqueio
    headers = {"User-Agent": "Mozilla/5.0"}

    # Fazendo a requisição
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando a lista de elementos
    lista_filmes = soup.find('ul',
                             class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-e22973a9-0 khSCXM compact-list-view ipc-metadata-list--base')

    # Encontrando todos os itens de filme dentro da lista
    itens_filmes = lista_filmes.find_all('li')

    df = estruturar_dataframe(itens_filmes)
    return df


def estruturar_dataframe(listagem_filmes) -> pd.DataFrame:
    capa = []
    titulos = []
    anos = []
    duracoes = []
    indicacoes = []
    avaliacoes = []

    # Iterando sobre cada item de filme
    for item_filme in listagem_filmes:
        # Título

        titulos.append(item_filme.find(class_='ipc-title__text').text[3:].replace('.', '').strip())

        imgs = item_filme.find_all('img')

        # Extraindo os links (src) de cada imagem
        for img in imgs:
            capa.append(img['src'])

        # Encontrar todos os elementos dentro de item_filme com a classe específica
        elementos = item_filme.find_all(class_='sc-d5ea4b9d-6 hBxwRe cli-title-metadata')

        if elementos:
            spans = elementos[0].find_all("span")  # Pega todos os <span> dentro do div
            if spans:
                ano = int(spans[0].text.strip())  # Pega apenas o primeiro span, que contém o ano
                anos.append(ano)

                duracao = spans[1].text
                duracoes.append(duracao)

                indicacao = spans[2].text
                indicacoes.append(indicacao)

        # Avaliação do IMDb
        avaliacoes.append(item_filme.find(class_='sc-d5ea4b9d-1 cVWRWO').text)

    # Criando um DataFrame usando pandas
    df_filmes = pd.DataFrame({
        'Capa': capa,
        'Título': titulos,
        'Ano de Lançamento': anos,
        'Duração': duracoes,
        'Indicação de Idade': indicacoes,
        'Avaliação do IMDb': avaliacoes
    })

    return df_filmes
