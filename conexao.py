import mysql.connector
def conectar():
    """ Conecta, se não existe cria. """
    try:
        conn = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='cicigugu')
        return conn
    except Error as e:
        print(e)
    return None


def desconectar(conn):
    conn.close()
