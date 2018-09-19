import sqlite3
from sqlite3 import Error
from urllib.request import urlopen,build_opener
from bs4 import BeautifulSoup
import re


sql_ano = """
                CREATE TABLE IF NOT EXISTS anos (
                    id integer PRIMARY KEY,
                    ano integer NOT NULL,
                    ultimoinserido integer DEFAULT 0
                ); """
sql_questao = """
                CREATE TABLE IF NOT EXISTS questoes (
                    id integer PRIMARY KEY,
                    numero integer NOT NULL,
                    ano_id integer NOT NULL,
                    resposta text,
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
                    texto text NOT NULL,
                    fonte text,
                    questao_id integer,
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




primeiroEnem = 2009
ultimoEnem = 2017
if __name__ == '__main__':
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM anos ORDER BY ano DESC LIMIT 1')
    ultimoAno = ultimoEnem
    for row in c:
        ultimoAno = row[1]
    anos = list(range(primeiroEnem, ultimoAno + 1))[::-1]
    for ano in anos:
    	url = "https://descomplica.com.br/gabarito-enem/questoes/{}/".format(ano)
    	opener = build_opener()
    	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    	questoes = []
    	try:
    		request = opener.open(url, timeout = 60)
    	except Exception as e:
    		print(url + " Timed Out!")
    	else:
    		HTML = BeautifulSoup(request.read(), "html.parser")
    		for questao in HTML.select("#main-content > div.questions-gallery > div.gallery a"):
    			nome = questao.select("div > div.info > div.label")
    			nome = re.sub("\D", "", (nome[0].text.strip()))
    			if(nome != ""):
    				questoes.append(questao.get("href"))
    		print(questoes)
    		print(len(questoes))

    desconectar(conn)
