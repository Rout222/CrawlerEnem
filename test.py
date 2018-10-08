from questao import Questao
from bloco import Bloco
from bs4 import BeautifulSoup, element
import re

links = ["https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/no-dia-em-que-foram-colhidos-os-dados-meteorologicos-apresentados-qual-fator-climatico-foi/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2017/segundo-dia/toxicidade-de-algumas-substancias-e-normalmente-representada-por-um-indice-conhecido-como-dl50/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/o-consumidor-seculo-xxi-chamado-de-novo-consumidor-social-tende-se-comportar-modo/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/para-algunos-hombres-el-virus-del-papiloma-humano-hpv-es-algo-muy-lejano-se-olvidan/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2017/segundo-dia/agua-para-o-abastecimento-de-um-predio-e-armazenada-em-um-sistema-formado-por-dois-reservatorios/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2016/primeiro-dia/uma-ambulancia-a-em-movimento-retilineo-e-uniforme-aproxima-se-de-um-observador-o-em-repouso/?cor=azul","https://descomplica.com.br/gabarito-enem/questoes/2016/primeiro-dia/o-benzeno-um-importante-solvente-para-a-industria-quimica-e-obtido-industrialmente/?cor=azul"]
# print(Questao(links[5], 1))


for l in links:
	print(Questao(l, 1))
	