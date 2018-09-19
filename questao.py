from urllib.request import urlopen,build_opener
from bs4 import BeautifulSoup
from alternativa import Alternativa
from assunto import Assunto
from texto import Texto
import re
from conexao import conectar, desconectar
import string

class Questao(object):
	"""Classe para receber o HTML de cada questao e prepara para salvar no banco"""
	def __init__(self, link, ano_id):
		super(Questao, self).__init__()
		self.link = link
		self.alternativas = []
		self.assuntos = []
		self.textos = []
		self.fazerConexao()
		self.salvar(ano_id)

	def salvar(self, ano_id):
		conn = conectar()
		c = conn.cursor()
		c.execute("INSERT INTO questoes(numero, ano_id, comentario, enunciado) VALUES (?,?,?,?)", (self.numero, ano_id, self.comentario, self.enunciado))
		questao_id = c.lastrowid
		for ass in self.assuntos:
			c.execute(ass.salvar(), ass.valores(questao_id))
		for tex in self.textos:
			c.execute(tex.salvar(), tex.valores(questao_id))
		for alt in self.alternativas:
			c.execute(alt.salvar(), alt.valores(questao_id))
		conn.commit()
		desconectar(conn)

	def fazerAlternativas(self, alternativas, resposta):
		i = 0
		for alt in alternativas:
			self.alternativas.append(Alternativa(alt, string.ascii_uppercase[i], resposta))
			i += 1

	def fazerAssuntos(self, assuntos):
		for ass in assuntos:
			self.assuntos.append(Assunto(ass))

	def fazerTextos(self, textos):
		for tex in textos:
			self.textos.append(Texto(tex))

	def fazerConexao(self):
		conseguiu = False
		opener = build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		while not(conseguiu): # enquanto nao conseguiu acessar por time out, vai continuar tentando
			try:
				request = opener.open(self.link, timeout = 60)
				conseguiu = True
			except Exception as e:
				print("{} time out, tentando novamente".format(self.link))
			else:
				html = BeautifulSoup(request.read(), "html.parser")
				try:
					self.comentario = html.select("#single-question > div.single-wrapper > div.comments > div.text > p")[0].text.strip()
				except Exception as e:
					self.comentario = ""
				resposta   		    = html.select("div.answer > p")[0].text.strip()
				try:
					self.enunciado  = html.select("div.enunciation")[0].text.strip()
				except Exception as e:
					pass
				self.numero		= re.sub("\D", "", (html.select("#single-question > div.highlight > h1")[0].text.strip()))
				self.fazerAlternativas(html.select("#single-question > div.single-wrapper > ol > li"), resposta)
				self.fazerAssuntos(html.select("#single-question > div.single-wrapper > div.question-info > div.subjects > p"))
				self.fazerTextos(html.select("div.enunciation"))
