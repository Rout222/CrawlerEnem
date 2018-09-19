from printavel import Printavel
class Alternativa(Printavel):
	"""docstring for alternativa"""
	def __init__(self, alternativa, letra, resposta):
		self.texto = alternativa.text
		self.letra = letra
		self.resposta = self.letra == resposta[-1]

	def __repr__(self):
		return self.letra + ") " + super(Alternativa, self).__repr__() + (" (Resposta correta)" if self.resposta else "")

	def salvar(self):
		return "INSERT INTO alternativas(texto, questao_id, letra, correta) VALUES(?,?,?,?)"

	def valores(self, questao_id):
		return (self.texto, questao_id, self.letra, self.resposta)


