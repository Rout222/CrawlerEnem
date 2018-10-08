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
\t Link
\t\t {}
\t Blocos
\t\t {}
\t Enunciado
\t\t {}
\t Alternativas
\t\t {}
\t Assuntos
\t\t {}
		""".format(self.link, self.blocks, self.enunciado, self.alternativas, self.assuntos)

	def fazerEnunciado(self, div):
		return div.text

	def salvar(self, ano_id):
		conn = conectar()
		c = conn.cursor()
		c.execute("INSERT INTO `cicigugu`.`questions` ( `number`, `comment`, `enunciation`, `year_id`, `theme_id`, `question_group_id` ) VALUES ( %s, %s, %s, %s, 1, 1 );", (self.numero, self.comentario, self.enunciado, ano_id))
		questao_id = c.lastrowid
		for tex in self.blocks:
			blockid = tex.salver(questao_id)
			c.execute("INSERT INTO `cicigugu`.`blocks_questions` (`block_id`, `question_id`) VALUES (%s,%s);", (blockid, questao_id))
		for alt in self.alternativas:
			altid = alt.salvar(questao_id)
		for assunto in self.assuntos:
			c.execute("SELECT `id` FROM `cicigugu`.`block_types` WHERE `title` =  '{}';".format(self.valor))
			idtype = c.fetchone()
			if(idtype):
				idtype = idtype[0]
			else:
				c.execute("INSERT INTO `cicigugu`.`block_types` (`title`) VALUES ('{}');".format(self.valor))
				idtype = c.lastrowid
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
				if(block.get("class") == ["image-wrapper"]):
					self.blocks.append(Bloco(block.div.img["src"], True, "imagem"))
				elif(block.get("class") in [["text"]]):
					for text in block.children:
						if(type(text) == element.Tag):
							if(text.get("class") == ["source"]):
								self.blocks.append(Bloco(text.text.strip(), True, "fonte"))
							elif(text.get("class") == ["cont"]):
								for t in text.children:
									if(type(t) == element.Tag):
										if(len(t.text) > 0):
											if (t.get("style") == "text-align: center;"):
												self.blocks.append(Bloco(t.text, True, "titulo"))
											else:
												self.blocks.append(Bloco(t.text))
				elif(block.get("class") in [["enunciation"]]):
					for text in block.children:
						if(type(text) == element.Tag):
							self.blocks.append(Bloco(text.text))
				elif(block.name == 'p'):
					for x in block.children:
						if(type(x) == element.Tag):
							self.blocks.append(Bloco(x.text, True, x.name))
						else:
							self.blocks.append(Bloco(x))

				else:
					print("Tipo desconhecido {}".format(block.get("class")))

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
					self.enunciado  = self.fazerEnunciado(html.select("#single-question > div.single-wrapper > div.enunciation")[0])
				except Exception as e:
					self.enunciado = ""
				self.numero		= re.sub("\D", "", (html.select("#single-question > div.highlight > h1")[0].text.strip()))
				self.fazerAlternativas(html.select("#single-question > div.single-wrapper > ol > li"), resposta)
				self.fazerAssuntos(html.select("#single-question > div.single-wrapper > div.question-info > div.subjects > p"))
				for b in html.select("#single-question > div.highlight")[0]:
					if(type(b) == element.Tag):
						if(b.get("id") == None and b.get("class") not in [['question-number']]):
							self.fazerBlocks(b)
