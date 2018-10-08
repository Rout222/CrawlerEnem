from printavel import Printavel
from bloco import Bloco

class Alternativa(Printavel):
	"""docstring for alternativa"""
	def __init__(self, alternativa, letra, resposta):
		if(alternativa.img == None):
			self.texto = Bloco(alternativa.text)
		else:
			self.texto = Bloco(alternativa.img['src'], True, "imagem")
		self.letra = letra
		self.resposta = self.letra == resposta[-1]

	def __repr__(self):
		return self.letra + ") " + str(self.texto) + (" (Resposta correta)" if self.resposta else "")

	def salvar(self, questaoid):
		conn = conectar()
		c = conn.cursor()
		sql = "INSERT INTO `cicigugu`.`alternatives` ( `letter`, `correct`, `question_id` ) VALUES ( '{}', {}, {} );".format(self.letra, self.resposta, questaoid)
		c.execute(sql)
		altid = c.lastrowid
		blockid = self.texto.salvar()
		c.execute("INSERT INTO `cicigugu`.`alternatives_blocks` (`alternative_id`, `block_id` ) VALUES ({}, {} );".format(altid, blockid))
		c.execute(sql)
		conn.commit()
		desconectar(conn)


