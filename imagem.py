from printavel import Printavel
import requests
import hashlib

class Imagem(Printavel):
	"""docstring for Imagem"""
	def __init__(self, url):
		super(Imagem, self).__init__()
		self.url = url

	def salvar(self):
		req = requests.get(self.url)
		img_data = req.content
		self.size 	 = req.headers['Content-length']
		with open("tmp.jpg", 'wb') as handler:
			handler.write(img_data)
		self.nomearquivo = self.md5()
		with open("imgs/{}.jpg".format(self.nomearquivo), 'wb') as handler:
			handler.write(img_data)
		return """
				INSERT INTO `cicigugu`.`images` (
				        `field_index`,
				        `model`,
				        `foreign_key`,
				        `field`,
				        `filename`,
				        `size`,
				        `mime`
				)
				VALUES
				        (
				                0,
				                'blocks',
				                ?,
				                'image',
				                ?,
				                ?,
				                'image/jpeg'
				        );
				"""
	def valores(self, block_id):
		return (block_id, self.nomearquivo, self.size)
		
	def md5(self):
	    hash_md5 = hashlib.md5()
	    with open("tmp.jpg", "rb") as f:
	        for chunk in iter(lambda: f.read(4096), b""):
	            hash_md5.update(chunk)
	    return hash_md5.hexdigest()