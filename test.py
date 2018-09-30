from questao import Questao
from bloco import Bloco
from bs4 import BeautifulSoup, element
import re

link1 = "https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/no-dia-em-que-foram-colhidos-os-dados-meteorologicos-apresentados-qual-fator-climatico-foi/?cor=azul"
link2 = "https://descomplica.com.br/gabarito-enem/questoes/2017/segundo-dia/toxicidade-de-algumas-substancias-e-normalmente-representada-por-um-indice-conhecido-como-dl50/?cor=azul"
link3 = "https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/o-consumidor-seculo-xxi-chamado-de-novo-consumidor-social-tende-se-comportar-modo/?cor=azul"
link4 = "https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/para-algunos-hombres-el-virus-del-papiloma-humano-hpv-es-algo-muy-lejano-se-olvidan/?cor=azul"
a = Questao(link1, 1)
print(a)