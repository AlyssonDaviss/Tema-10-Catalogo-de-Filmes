
from src.user import Usuario
from repositories.cadastrar_pessoa import CadastrarUsuario
from repositories.cadastrar_midia import CadastrarMidia
from src.midia import Midia, Serie, Episodio


# Login ou cadastro
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


# Menu principal
print("\nMenu")
print("1 - Cadastrar mídia")
print("2 - Sair")

r = input("Opção: ")

if r == "1":
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
        titulo, tipo, genero, ano,
        classificacao_indicativa, elenco, status
    )

    cadastro_midia = CadastrarMidia()
    id_midia = cadastro_midia.cadastrar_midia(midia)

    if not id_midia:
        print("Mídia já cadastrada ou tipo inválido.")
        exit()

    print("Mídia cadastrada com sucesso!")

    # Cadastro de filme
    if tipo == "filme":
        duracao = input("Duração: ")

        resultado = cadastro_midia.atualizar_duracao(
            id_midia, duracao
        )

        if resultado is True:
            print("Duração cadastrada.")
        else:
            print(resultado)

    # Cadastro de série
    elif tipo == "serie":
        serie = Serie(
            titulo, tipo, genero, ano,
            classificacao_indicativa, elenco, status,
            id=id_midia
        )

        while True:
            dados = cadastro_midia.carregar_dados()

            temporadas_existentes = dados.get(
                str(id_midia), {}
            ).get("temporadas", {})

            numero_temporada = len(temporadas_existentes) + 1

            numero_episodios = int(
                input("Número de episódios da temporada: ")
            )

            data_lancamento = input(
                "Data de lançamento da temporada: "
            )

            temporada = serie.registrar_temporadas(
                numero_temporada,
                numero_episodios,
                data_lancamento
            )

            id_temporada = cadastro_midia.cadastrar_temporada(
                id_midia, temporada
            )

            if (
                not isinstance(id_temporada, str)
                or not id_temporada.isdigit()
            ):
                print(id_temporada)
                break

            temporada.definir_id(id_temporada)

            # Cadastro automático dos episódios
            duracao_media = input(
                "Duração média dos episódios: "
            )

            for numero in range(1, numero_episodios + 1):
                episodio = Episodio.criar_automatico(
                    numero, duracao_media
                )

                resultado = cadastro_midia.registrar_episodio(
                    id_midia,
                    id_temporada,
                    episodio
                )

                if resultado is not True:
                    print(resultado)
                    break

                print(f"Episódio {numero} cadastrado.")

            else:
                print(
                    f"{numero_episodios} episódios cadastrados automaticamente."
                )

            continuar = input(
                "Registrar outra temporada? (s/n): "
            ).lower()

            if continuar != "s":
                break

elif r == "2":
    print("Saindo...")

else:
    print("Opção inválida.")
