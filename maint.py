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
    print(True)



