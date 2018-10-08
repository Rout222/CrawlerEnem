from printavel import Printavel
from conexao import conectar, desconectar
from urllib.request import urlopen,build_opener
from bs4 import BeautifulSoup
from questao import Questao
import re
from tqdm import tqdm

class Ano(Printavel):
	"""docstring for Ano"""
	def __init__(self, ano):
		super(Ano, self).__init__()
		self.ano = ano
		conn = conectar()
		c = conn.cursor()
		c.execute("SELECT ultimoinserido, id, concluido FROM years WHERE value = " + str(self.ano))
		row = c.fetchone()
		if(row != None):
			self.id = row[1]
			self.ultimoinserido = row[0]
			self.concluido = row[2]
		else:
			c.execute("INSERT INTO years(value) VALUES (" + str(self.ano) + ")")
			self.ultimoinserido = ""
			self.concluido = False
			self.id = c.lastrowid
			conn.commit()
		if(not(self.concluido)):
			self.pegarQuestoes()
		desconectar(conn)

	def atualizar(self, link):
		conn = conectar()
		c = conn.cursor()
		c.execute("UPDATE years SET ultimoinserido = %s WHERE id = %s", (link, str(self.id)))
		conn.commit()
		desconectar(conn)
		self.ultimoinserido = link

	def concluir(self):
		conn = conectar()
		c = conn.cursor()
		c.execute("UPDATE `cicigugu`.`years` SET `concluido` = 1 WHERE `id` = {}", self.id)
		conn.commit()
		desconectar(conn)

	def pegarQuestoes(self):
		url = "https://descomplica.com.br/gabarito-enem/questoes/{}/".format(self.ano)
		opener = build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		conseguiu = False
		try:
			while(not(conseguiu)):
				request = opener.open(url, timeout = 60)
				conseguiu = True
		except Exception as e:
			print(url + " Timed Out!")
		else:
			html = BeautifulSoup(request.read(), "html.parser")
			achou = False
			if (self.ultimoinserido == ""):
				achou = True
			for questao in tqdm(html.select("#main-content > div.questions-gallery > div.gallery a"), desc='Enem de '+str(self.ano), position=1, leave=False):
				if(not(achou)):
					if(questao.get("href") == self.ultimoinserido):
						achou = True
				else:
					numero = questao.select("div > div.info > div.label")
					numero = re.sub("\D", "", (numero[0].text.strip()))
					if(numero != ""):
						Questao(questao.get("href"), self.id)
						self.atualizar(questao.get("href"))
			self.concluir()