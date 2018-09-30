from urllib.request import urlopen,build_opener
from bs4 import BeautifulSoup, element
from alternativa import Alternativa
from assunto import Assunto
from bloco import Bloco
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
		self.blocks = []
		self.fazerConexao()
		self.salvar(ano_id)

	def __repr__(self):
		return """
(Questao) com
\t Blocos
\t\t {}
\t Enunciado
\t\t {}
\t Alternativas
\t\t {}
\t Assuntos
\t\t {}
		""".format(self.blocks, self.enunciado, self.alternativas, self.assuntos)

	def fazerEnunciado(self, div):
		return div.text

	def salvar(self, ano_id):
		return ''
		conn = conectar()
		c = conn.cursor()
		c.execute("INSERT INTO questoes(numero, ano_id, comentario, enunciado) VALUES (?,?,?,?)", (self.numero, ano_id, self.comentario, self.enunciado))
		questao_id = c.lastrowid
		blocksinseridos = []
		for tex in self.blocks:
			c.execute(tex.salvar(), tex.valores())
			b_id = c.lastrowid
			if(tex.imagem):
				c.execute(tex.salvarImagem(), tex.valoresImagem(b_id))
			c.execute("INSERT INTO `cicigugu`.`blocks_questions` (`block_id`, `question_id`) VALUES (?,?);", (questao_id, b_id))
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

	def fazerBlocks(self, div):
		for block in div.children:
			if(type(block) == element.Tag):
				if(block["class"] == ["image-wrapper"]):
					self.blocks.append(Bloco(block.div.img["src"], False, True, False))
				if(block["class"] == ["text"]):
					for text in block.children:
						if(type(text) == element.Tag):
							if(text["class"] == ["source"]):
								self.blocks.append(Bloco(text.text.strip(), True, False, False))
							elif(text["class"] == ["cont"]):
								for t in text.children:
									if(type(t) == element.Tag):
										if(len(t.text) > 0):
											if (t.get("style") == "text-align: center;"):
												self.blocks.append(Bloco(t.text, False, False, True))
											else:
												self.blocks.append(Bloco(t.text, False, False, False))

							else:
								raise BaseException

	def fazerConexao(self):
		conseguiu = False
		opener = build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		while not(conseguiu): # enquanto nao conseguiu acessar por time out, vai continuar tentando
			try:
				request = opener.open(self.link, timeout = 5)
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
					self.enunciado  = self.fazerEnunciado(html.select("div.enunciation")[0])
				except Exception as e:
					self.enunciado = ""
				self.numero		= re.sub("\D", "", (html.select("#single-question > div.highlight > h1")[0].text.strip()))
				self.fazerAlternativas(html.select("#single-question > div.single-wrapper > ol > li"), resposta)
				self.fazerAssuntos(html.select("#single-question > div.single-wrapper > div.question-info > div.subjects > p"))
				self.fazerBlocks(html.select("#single-question > div.highlight > div.cont-list")[0])
