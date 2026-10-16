
from src.user import Usuario
from repositories.cadastrar_pessoa import CadastrarUsuario
from repositories.cadastrar_midia import CadastrarMidia
from src.midia import Midia, Serie, Episodio


user = input("Diga o Usuário: ")
pin = input("Diga a senha: ")

usuario = Usuario(user, pin)
cadastro_usuario = CadastrarUsuario()

resultado = cadastro_usuario.autenticar(usuario)

if resultado == "sucesso":
    print("Login realizado com sucesso!")

elif resultado == "senha_incorreta":
    print("Senha incorreta.")
    exit()

else:
    if not cadastro_usuario.cadastrar(usuario):
        print("Não foi possível cadastrar o usuário.")
        exit()

    print("Usuário cadastrado com sucesso!")

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
        exit()

    if tipo == "série":
        tipo = "serie"

    midia = Midia(
        titulo,
        tipo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        status
    )

    cadastro_midia = CadastrarMidia()
    id_midia = cadastro_midia.cadastrar_midia(midia)

    if not id_midia:
        print("Mídia já cadastrada ou tipo inválido.")
        exit()

    print("Mídia cadastrada com sucesso!")

    if tipo == "filme":
        duracao = input("Duração: ")

        resultado = cadastro_midia.atualizar_duracao(
            id_midia, duracao
        )

    elif tipo == "serie":
        serie = Serie(
            titulo, tipo, genero, ano,
            classificacao_indicativa, elenco, status,
            0, 0,
            id=id_midia
        )

        while True:
            temporada = serie.registrar_temporadas()

            id_temporada = cadastro_midia.cadastrar_temporada(
                id_midia, temporada
            )

            if not isinstance(id_temporada, str) or not id_temporada.isdigit():
                print(id_temporada)
                break

            # Guarda o ID gerado pelo repositório.
            temporada._id = id_temporada

            while True:
                titulo_ep = input("Título do episódio: ")
                duracao_ep = input("Duração do episódio: ")
                data_ep = input("Data de lançamento: ")

                episodio = Episodio(
                    titulo_ep,
                    duracao_ep,
                    data_ep
                )

                resultado = cadastro_midia.registrar_episodio(
                    id_midia,
                    id_temporada,
                    episodio
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
