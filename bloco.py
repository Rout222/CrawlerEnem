from printavel import Printavel
from imagem import Imagem
class Blocos(Printavel):
	"""docstring for Blocos"""
	def __init__(self, texto, fonte, imagem):
		super(Blocos, self).__init__()
		self.texto = texto
		self.fonte = fonte
		self.imagem = imagem
		if imagem > 0:
			self.img    = Imagem(texto)

	def __repr__(self):
		return "Este bloco é uma imagem com o link " + self.texto
teste = Blocos("https://d2q576s0wzfxtl.cloudfront.net/2017/11/08151500/questao03.ing_.enem-2017.png", False, True)
print(teste)

		