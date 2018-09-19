link = "https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/take-car-just-anyplace-oil-change-may-regret-road-nesse-texto-publi/?cor=azul"
numero = 5
import sqlite3
from sqlite3 import Error
from urllib.request import urlopen,build_opener
from bs4 import BeautifulSoup
import re

opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
request = opener.open(link, timeout = 60)
HTML = BeautifulSoup(request.read(), "html.parser")
comentario = HTML.select("#single-question > div.single-wrapper > div.comments > div.text > p")[0].text.strip()
resposta = HTML.select("#single-question > div.single-wrapper > div.question-info > div.answer > p")[0].text.strip()
enunciado = HTML.select("#single-question > div.single-wrapper > div.enunciation > p")[0].text.strip()
alternativas = []
for alternativa in HTML.select("#single-question > div.single-wrapper > ol > li"):
	alternativas.append(alternativa.text)
assuntos = []
for assunto in HTML.select("#single-question > div.single-wrapper > div.question-info > div.subjects > p"):
	assuntos.append(assunto.text)
textos = []
for texto in HTML.select("#single-question > div.highlight > div.cont-list > div"):
	if(texto.get("class")[0] == "text"):
		if(texto.select(".cont")[0].text != ""):
			textos.append([texto.select(".cont")[0].text, 0])
		if(texto.select(".source")[0].text != ""):
			textos.append([texto.select(".source")[0].text, 0])
	else:
		textos.append([texto.select("div > img")[0].get("src"), 1])	
print(textos)