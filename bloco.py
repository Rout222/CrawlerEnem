from printavel import Printavel
from imagem import Imagem
class Bloco(Printavel):
	"""docstring for Bloco"""
	def __init__(self, texto, fonte, imagem, titulo):
		super(Bloco, self).__init__()
		self.texto = texto
		self.fonte = fonte
		self.imagem = imagem
		self.titulo = titulo
		if imagem:
			self.img    = Imagem(texto)

	def __repr__(self):
		if self.imagem:
			return "(imagem) " + self.texto
		elif self.fonte:
			return "(fonte) " + self.texto
		elif self.titulo:
			return "(titulo) " + self.texto
		else:
			return "(texto) " + self.texto

	def save(self):
		return """
			INSERT INTO `cicigugu`.`blocks` (
			        `text`,
			        `block_type_id`
			)
			VALUES
		        (
		                ?,
		                ?
		        );
		"""
	def valores(self):
		t = 1
		if self.imagem:
			t = 2
		elif self.fonte:
			t = 3
		elif self.titulo:
			t = 4
		return (self.texto, t)

	def salvarImagem(self):
		if(self.imagem):
			return self.img.salvar()

	def valoresImagem(self, id_bloco):
		if(self.imagem):
			return self.img.valores(id_bloco)