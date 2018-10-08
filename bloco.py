from printavel import Printavel
from imagem import Imagem
from conexao import conectar, desconectar

class Bloco(Printavel):
	"""docstring for Bloco"""
	def __init__(self, texto, custom = False, valor = 'texto'):
		super(Bloco, self).__init__()
		self.texto = texto
		self.custom = custom
		self.valor = valor
		if self.custom and self.valor == "imagem":
			self.img = Imagem(texto)

	def __repr__(self):
		if self.custom:
			return "\n\t("+self.valor+") " + self.texto
		else:
			return "\n\t(texto) " + self.texto

	def salvar(self, idquestao):
		conn = conectar()
		c = conn.cursor()
		c.execute("SELECT `id` FROM `cicigugu`.`block_types` WHERE `title` =  '{}';".format(self.valor))
		idtype = c.fetchone()
		if(idtype):
			idtype = idtype[0]
		else:
			c.execute("INSERT INTO `cicigugu`.`block_types` (`title`) VALUES ('{}');".format(self.valor))
			idtype = c.lastrowid
		c.execute("INSERT INTO `cicigugu`.`blocks` (`text`,`block_type_id`) VALUES ( '{}', '{}');".format(self.texto, idtype))
		blockid = c.lastrowid
		if(self.valor == 'imagem'):
			self.img.salvar(blockid)
		conn.commit()
		desconectar(conn)
		return blockid