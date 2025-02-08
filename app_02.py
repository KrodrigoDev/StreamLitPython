import streamlit as st
import time
import pymysql.cursors


def connection() -> pymysql.Connection:
    """Conecta ao MySQL e retorna a conexão."""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456789',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.Error as erro:
        st.error(f"Erro ao conectar ao banco de dados: {erro}")
        return None


def create_database():
    """Cria o banco de dados e a tabela caso não existam."""
    conn = connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS streamlit")
            cursor.execute("USE streamlit")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    firstname VARCHAR(50) NOT NULL,
                    lastname VARCHAR(50) NOT NULL,
                    date_birthday DATE NOT NULL,
                    password_user VARCHAR(255) NOT NULL
                )
            """)
        conn.commit()
    except pymysql.Error as error:
        st.error(f"Erro ao criar o banco/tabela: {error}")
    finally:
        conn.close()


def insert_one_register(first_name, last_name, date_birthday, password):
    """Insere um novo usuário no banco."""
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='streamlit',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO user (firstname, lastname, date_birthday, password_user)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, date_birthday, password))
        conn.commit()
        st.success("Usuário cadastrado com sucesso!")
    except pymysql.Error as error:
        st.error(f"Erro ao inserir os dados: {error}")
    finally:
        conn.close()


# UI no Streamlit
st.subheader("Adicionar Usuário")

with st.form("form_easy"):
    c1, c2 = st.columns(2)
    first_name = c1.text_input("Nome:")
    last_name = c2.text_input("Sobrenome:")
    date_birthday = st.date_input("Data de Nascimento:")
    password = st.text_input("Senha:", type="password")

    submit = st.form_submit_button("Cadastrar")

    if submit:
        with st.spinner("Carregando..."):
            time.sleep(2)
            create_database()  # Criar banco e tabela, se necessário
            insert_one_register(first_name, last_name, date_birthday, password)
