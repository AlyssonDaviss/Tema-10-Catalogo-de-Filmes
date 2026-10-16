
from src.user import Usuario
from repositories.cadastrar_pessoa import *
from src.midia import *

user = input("Diga o Usuário: ")
pin = input("Diga a senha: ")

usuario = Usuario(user, pin)
cadastro = CadastrarUsuario()

if cadastro.cadastrar(usuario):
    print("Usuário cadastrado com sucesso!")
else:
    print("Usuário já cadastrado.")
    exit()

print("Menu")
print("1 - Cadastrar mídia")
print("2 - Sair")

r = int(input("Opção: "))

if r == 1:
    titulo = input("Título da mídia: ")
    tipo = input("Tipo (filme/série): ").lower()
    genero = input("Gênero: ")
    ano = input("Ano de lançamento: ")
    classificacao_indicativa = input("Classificação indicativa: ")
    elenco = input("Elenco (opcional): ")
    status = input("Status: ")

    if tipo not in ("filme", "serie", "série"):
        print("Tipo de mídia inválido.")
    else:
        if tipo == "série":
            tipo = "serie"

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

                while True:
                    titulo_ep = input("Título do episódio: ")
                    duracao_ep = input("Duração do episódio: ")
                    data_ep = input("Data de lançamento: ")

                    e1 = Episodio(
                        titulo_ep,
                        duracao_ep,
                        data_ep
                    )

                    resultado = temporada.registrar_episodios(
                        s1.obter_id(),
                        temporada.obter_id(),
                        e1
                    )

                    if resultado is True:
                        print("Episódio cadastrado.")
                    else:
                        print(resultado)
                        break

                    continuar_ep = input(
                        "Registrar outro episódio? (s/n): "
                    ).lower()

                    if continuar_ep != "s":
                        break

                continuar = input(
                    "Registrar outra temporada? (s/n): "
                ).lower()

                if continuar != "s":
                    break

elif r == 2:
    print("Saindo...")

else:
    print("Opção inválida.")
