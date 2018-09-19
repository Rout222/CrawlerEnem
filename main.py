from ano import Ano
from tqdm import tqdm

primeiroEnem = 2009
ultimoEnem = 2017
if __name__ == '__main__':
    ultimoAno = ultimoEnem
    anos = list(range(primeiroEnem, ultimoAno + 1))[::-1]
    for ano in tqdm(anos, desc='Enem Todo', position=0):
    	Ano(ano) 
