import datetime

import streamlit as st

bar = st.sidebar


bar.selectbox('Select between: ', ['One', 'Two', 'Three'])
period_date = bar.slider(label='date', min_value=datetime.date(2017, 1, 1, ), max_value=datetime.date.today(),
                         value=(datetime.date(2017, 1, 1, ), datetime.date.today()))

text_input = st.text_area('Write here: ')

with st.expander('open text'):
    st.write(text_input)
    st.write(period_date[0])

with st.container(border=True):
    a, b, c = st.container(border=True).columns(3)

    a.subheader('Metrics one')
    b.subheader('Metrics two')
    c.subheader('Metrics three')
    for i in range(2):
        a, b, c = st.container().columns(3)
        a.metric(label="Temperature", value="70 °F", delta="1.2 °F", border=True)

        b.metric(label="Temperature", value="70 °F", delta="1.2 °F", border=True)

        c.metric(label="Temperature", value="70 °F", delta="1.2 °F", border=True)
