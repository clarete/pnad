Intro
=====

O projeto **pnad2013** tem o propósito de facilitar o acesso aos dados
sobre a população Brasileira publicados pelo
[IBGE](http://www.ibge.gov.br/home/estatistica/populacao/trabalhoerendimento/pnad2013/microdados.shtm).
+Ao invés de requerer programas como SAS ou as linguagens
+como [R](http://www.r-project.org/), utiliza a linguagem [Python](http://python.org) e  a biblioteca
 [Pandas](https://pypi.python.org/pypi/pandas).

Instalação
==========

É necessário ter o Python instalado, além disso, é sugerido o
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/) para
isolamento de ambientes.

Abra o terminal e digite:

```bash
$ pip install -r requirements.txt
```

Execução
========

Conversão do arquivo de entrada (Input)
---------------------------------------

Como citado, o IBGE disponibiliza esses dados para o software
[GNU R](http://www.r-project.org/) e outros programas
proprietários. Porém, o script que gera o output final precisa da
descrição da estrutura do arquivo `Dados/PES2013.txt` no pacote
disponibilizado pelo IBGE.

O arquivo de input `Input/input PES2013.txt` compatível com o programa
proprietário SAS foi manualmente convertido pra um formato menos
complexo e está disponível nesse mesmo repositório, chamado
`input.txt`.

Para converter o arquivo de dados, execute:

```bash
$ python convert.py input.2013.txt <pacote-do-IBGE>/Dados/PES2013.txt > PES2013.csv
```

Output
------

Para obter um CSV com os campos Região, Faixa etária, Renda, N, Peso e
N * P, execute no terminal:

```bash
$ python pnad.py PES2013.csv > output.csv
```

Licensa
-------

Este software está licensiado sob GPLv3.
