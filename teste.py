from questao import Questao

a = Questao("https://descomplica.com.br/gabarito-enem/questoes/2017/primeiro-dia/no-conto-de-galeano-experssao-ni-le-va-ni-le-viene-encerra-uma-opiniao/?cor=azul", 555)
for alt in a.textos:
	print(alt)