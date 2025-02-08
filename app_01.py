import pandas as pd
import streamlit as st
import pathlib
import json

st.markdown("""
# Exibidor de arquivo

### Suba seu arquivo e vejamos o que acontece
""")

files = pathlib.Path('files')

if not files.exists():
    files.mkdir()

file = st.file_uploader(
    'put your file here:',
    type=['csv', 'json', 'py', 'png', 'jpg']
)

if file:
    print(file.type)
    match file.type.split('/'):
        case 'application', 'json':
            st.json(json.load(file))
        case 'text', 'csv':
            df = pd.read_csv(file, sep=';', encoding='latin1')
            st.dataframe(df)
            df['ano'] = df['ano'].astype(str)
            df.set_index('ano', inplace=True)
            st.bar_chart(df)
        case 'image', 'jpeg':
            st.image(file)
else:
    st.error('Ainda não tenho arquivo')


with st.form("my_form"):
    name = st.text_input('Name', type="default")
    passowrd = st.text_input('Password', type='password')
    submit = st.form_submit_button('submit')

    if submit:
        st.write(f'{name} {passowrd}')
