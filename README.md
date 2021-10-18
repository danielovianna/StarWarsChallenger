# Star Wars Challenger

O "Desafio Star Wars" consiste em criar uma rest API em Python usando FastApi, MongoDB, documentação Swagger e consumindo a [swapi](https://swapi.dev) .

## Antes de Instalar

Verifique se sua máquina possui o instalador de pacotes [pip](https://pypi.org/help/). É necessário também ter o [MongoDB](https://www.mongodb.com/) instalado e rodando na máquina.

## Instalação
```bash
# Instalando todos os requirementos:
pip install -r requeriments.txt

# Iniciando o programa:
uvicorn index:app --reload
```

Você pode testar no seu browser no endereço http://localhost:8000 mas será melhor aproveitado pela documentação Swagger gerada em [http://localhost:8000/docs](http://localhost:8000/docs)
O mongoDB criará a base de dados (starwars) e as collections (planet e film) automaticamente assim que a primeira inclusão for feita.

## Funcionamento

A API possui um cadastro completo (CRUD) com leitura, inserção, atualização e exclusão dos seguintes dados: Planets e Films. Cada planeta possui nome, clima, diâmetro, população e os filmes que participa. O filmes possuem nome e data de lançamento. Ao inserir um planeta o programa verifica se o planeta existe na swapi e caso exista ele importará os dados desse planeta da swapi, caso não exista o planeta é inserido normalmente. Durante a inclusão do planeta também é verificado se os filmes incluídos também existem na swapi e caso existam o programa importará os filmes automaticamente inserindo eles na base de dados, caso não exista um novo filme é inserido normalmente. Note que, durante a inclusão do planeta, é feito o relacionamento por _id dos filmes automaticamente ao planeta. Existem diversas outras validações como por exemplo: planetas e filmes repetidos, data de lançamento inválida e etc.


##### Nota: Toda a programação e comentários foram feitos em inglês.

## Demonstração
Uma demonstração do funcionamento do aplicativo pode ser vista nesse [video](https://youtu.be/5RtqacUagks).

## Autor
Daniel de Oliveira Vianna