from printavel import Printavel
class Assunto(Printavel):
	"""docstring for Assunto"""
	def __init__(self, assunto):
		self.texto = assunto.text

	def salvar(self):
		return "INSERT INTO assuntos(questao_id, texto) VALUES (?,?)"

	def valores(self, questao_id):
		return (questao_id, self.texto)
		