from sqlite3 import Error
import sqlite3
sql_ano = """
                CREATE TABLE IF NOT EXISTS anos (
                    id integer PRIMARY KEY,
                    ano integer NOT NULL,
                    ultimoinserido text DEFAULT "",
                    concluido bool default 0
                ); """
sql_questao = """
                CREATE TABLE IF NOT EXISTS questoes (
                    id integer PRIMARY KEY,
                    numero integer NOT NULL,
                    ano_id integer NOT NULL,
                    comentario text,
                    enunciado text,
                    FOREIGN KEY (ano_id) REFERENCES anos (id)
                );
                """
sql_assunto = """
    			CREATE TABLE IF NOT EXISTS assuntos (
                    id integer PRIMARY KEY,
                    questao_id integer NOT NULL,
                    texto text NOT NULL,
                    FOREIGN KEY (questao_id) REFERENCES questoes (id)
                );
    			"""
sql_textos = """
                CREATE TABLE IF NOT EXISTS textos (
                    id integer PRIMARY KEY,
                    texto text,
                    questao_id integer,
                    image bool default 0,
                    FOREIGN KEY (questao_id) REFERENCES questoes (id)
                );
                """
sql_alternativas = """
                CREATE TABLE IF NOT EXISTS alternativas (
                    id integer PRIMARY KEY,
                    texto text,
                    questao_id integer,
                    letra text,
                    correta bool default 0,
                    FOREIGN KEY (questao_id) REFERENCES questoes (id)
                );
                """
def conectar():
    """ Conecta, se não existe cria. """
    try:
        conn = sqlite3.connect("db.db")
        criarTabela(conn, sql_ano)
        criarTabela(conn, sql_assunto)
        criarTabela(conn, sql_questao)
        criarTabela(conn, sql_textos)
        criarTabela(conn, sql_alternativas)
        return conn
    except Error as e:
        print(e)
    return None


def desconectar(conn):
    conn.close()


def criarTabela(conn, sql):
    """ Cria uma tabela no database Conn
    :param conn: Connection object
    :param sql: sql a ser executado
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


