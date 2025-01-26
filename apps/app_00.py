# imports
import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date, timedelta, datetime
from typing import List


@st.cache_data
def load_data(tickets_enterprises: List) -> pd.DataFrame:
    tickets = ' '.join(tickets_enterprises)

    df_actions = yf.Tickers(tickets)
    df_actions = df_actions.history(period='1d', start=date.today() - timedelta(1825), end=date.today())

    # conceito de multi-indices
    df_actions = df_actions['Close']

    # algumas cryptos não existiam em deerminado período, para tratar isso optei por colocar zero
    df_actions.fillna(0, inplace=True)

    for ticket in tickets_enterprises:
        # conversão do valor de fechamento das criptos para real com cotação do dólar do dia 25
        df_actions[ticket] = df_actions[ticket].apply(lambda x: round(x * 5.91, 2))

    return df_actions


@st.cache_data
def load_tickets() -> pd.DataFrame:
    actions = pd.read_csv('../files/cryptocurrencies.csv')

    return actions


@st.cache_data
def load_main() -> pd.DataFrame:
    df_tickets = load_tickets()
    df_actions = load_data(df_tickets['Ticker'])

    names = dict(zip(df_tickets['Ticker'], df_tickets['Name']))
    df_actions.rename(columns=names, inplace=True)

    return df_actions


df = load_main()

# views
st.title(f"""
Update of crypto closing prices over the years
""")

# side bar (barra lateral).
# obs: para add qualquer elemento na side bar basta chamar a propriedade antes do metódo desejado
st.sidebar.header('filters')

# filter actions (exemplo do filtro dentro do side bar)
actions_selecet = st.sidebar.multiselect('Select crypto to view: ', df.columns)

if actions_selecet:
    df = df[actions_selecet]

# filter dates
date_initial = df.index.min().to_pydatetime()
date_final = df.index.max().to_pydatetime()

# existe o paramentro step para definir a tempo em que desejamos passar o tempo. obs ele usa o timedelta() da lib
# datetime
date_filter = st.sidebar.slider('Select the period', min_value=date_initial, max_value=date_final,
                                value=(date_initial, date_final))

# filtrando por linhas
df = df.loc[date_filter[0]:date_filter[1]]

# mostrando o gráfico
st.line_chart(df)

# mostrando a perfomance das criptos ao longo do tempo
text_actions = ''

# caso não esteja selecionado nenhuma cripto será mostrado a perfomance de todas
if len(actions_selecet) == 0:
    actions_selecet = df.columns

for action in actions_selecet:
    # (VALOR FINAL - VALOR INCIAL)
    perfomance_action = float((df[action].iloc[-1] - df[action].iloc[0]))

    if perfomance_action > 0:
        text_actions += f'  \n{action}: :green[R${perfomance_action:.2f}]'
    elif perfomance_action <= 0:
        text_actions += f'  \n{action}: :red[R${perfomance_action:.2f}]'

st.write(f"""
### Perfomance of crypto
The performance of cryptocurrencies between {datetime.strftime(date_filter[0], '%Y-%m-%d')} and {datetime.strftime(date_filter[1], '%Y-%m-%d')} :

{text_actions}
""")
