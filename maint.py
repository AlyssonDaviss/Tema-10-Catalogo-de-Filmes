from src.user import Usuario
from src.midia import *

user = input("Diga o Usuário: ")
pin = input("Diga a senha: ")

# loop para validação de login()

usuario = Usuario(user, pin)
usuario.cadastrar()

# CLI

print("Menu")
print("1 cadastrar midia")
print("2 sair")
r = int(input())

if r == 1:
    titulo = input("Título da mídia: ")
    tipo = input("Tipo (filme/série): ").lower()
    genero = input("Gênero: ")
    ano = input("Ano de lançamento: ")
    classificacao_indicativa = input("Classificação indicativa: ")
    elenco = input("Elenco: ")
    status = input("Status: ")

    m1 = Midia(
     titulo,
     tipo,
     genero,
     ano,
     classificacao_indicativa,
     elenco,
     status
    )

m1.Cadastrar_Midia()

if tipo == "filme":
    duracao = input("Duração: ")

    f1 = Filme(
        titulo, genero, ano,
        classificacao_indicativa, elenco, status,
        duracao, m1.obter_id()
    )

    f1.registrar_duracao()

elif tipo == "serie":
    s1 = Serie(
        titulo, tipo, genero, ano,
        classificacao_indicativa, elenco, status,
        0, 0,
        id=m1.obter_id()
    )

    while True:
        temporada = s1.registrar_temporadas()
        s1.cadastrar_temporada(temporada)

        continuar = input("Registrar outra temporada? (s/n): ").lower()

        if continuar != "s":
            break

print(True)


