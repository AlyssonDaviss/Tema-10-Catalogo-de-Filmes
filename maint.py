
from src.user import Usuario
from src.cli import CLI
from repositories.cadastrar_pessoa import CadastrarUsuario

# Login ou cadastro
user = input("Diga o Usuário: ").strip()
pin = input("Diga a senha: ").strip()

usuario = Usuario(user, pin)
cadastro_usuario = CadastrarUsuario()

resultado = cadastro_usuario.autenticar(usuario)

if resultado == "sucesso":
    print("Login realizado com sucesso!")

elif resultado == "senha_incorreta":
    print("Senha incorreta.")
    raise SystemExit

else:
    if not cadastro_usuario.cadastrar(usuario):
        print("Não foi possível cadastrar o usuário.")
        raise SystemExit

    print("Usuário cadastrado com sucesso!")


# Recupera o ID real do usuário
id_usuario = cadastro_usuario.obter_id(user)

if id_usuario is None:
    print("Não foi possível identificar o ID do usuário.")
    raise SystemExit


# Inicia a interface do sistema
cli = CLI(id_usuario=id_usuario)
cli.Executar()
