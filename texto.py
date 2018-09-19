from printavel import Printavel
class Texto(Printavel):
	"""docstring for Texto"""
	def __init__(self, texto):
		self.imagem = False
		self.texto = ""
		self.source = ""
		if(texto.get("class")[0] == "text"):
			self.texto = texto.select(".cont")[0].text
			try:
				self.fonte = texto.select(".source")[0].text
			except Exception as e:
				pass
		elif(texto.get("class")[0] == "enunciation"):
			self.texto = texto.p.text
		else:
			self.imagem = True
			self.texto = texto.select("div > img")[0].get("src")

	def __repr__(self):
		if(not(self.imagem)):
			return self.texto + self.fonte
		else:
			return super(Texto, self).__repr__()

	def salvar(self):
		return "INSERT INTO textos(questao_id, texto, image) VALUES (?,?,?)"

	def valores(self, questao_id):
		return (questao_id, self.texto, self.imagem)
