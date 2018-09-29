from printavel import Printavel
import requests


class Imagem(Printavel):
	"""docstring for Imagem"""
	def __init__(self, url):
		super(Imagem, self).__init__()
		self.url = url
		self.nomearquivo = "asd4as65d4as65.jpg"
		img_data = requests.get(self.url).content
		with open('asd4as65d4as65.jpg', 'wb') as handler:
			handler.write(img_data)

		