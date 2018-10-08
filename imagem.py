from printavel import Printavel
import requests
import hashlib
from conexao import conectar, desconectar
class Imagem(Printavel):
	"""docstring for Imagem"""
	def __init__(self, url):
		super(Imagem, self).__init__()
		self.url = url

	def salvar(self, blockid):
		req = requests.get(self.url)
		img_data = req.content
		self.size 	 = req.headers['Content-length']
		with open("tmp.jpg", 'wb') as handler:
			handler.write(img_data)
		self.nomearquivo = self.md5()
		with open("imgs/{}.jpg".format(self.nomearquivo), 'wb') as handler:
			handler.write(img_data)
		conn = conectar()
		c = conn.cursor()
		sql = "INSERT INTO `cicigugu`.`images` ( `field_index`, `model`, `foreign_key`, `field`, `filename`, `size`, `mime` ) VALUES ( 0, 'blocks', {}, 'image', '{}', {}, 'image/jpeg' );".format(blockid, self.nomearquivo, self.size)
		c.execute(sql)
		conn.commit()
		desconectar(conn)
			
	def md5(self):
	    hash_md5 = hashlib.md5()
	    with open("tmp.jpg", "rb") as f:
	        for chunk in iter(lambda: f.read(4096), b""):
	            hash_md5.update(chunk)
	    return hash_md5.hexdigest()