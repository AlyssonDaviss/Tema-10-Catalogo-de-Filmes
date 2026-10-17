
import json
import os

class CadastrarLista:
    """Gerencia a persistência das listas personalizadas."""

    def __init__(self, arquivo=None):
        if arquivo is None:
            raiz_projeto = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            arquivo = os.path.join(
                raiz_projeto, "data", "listas.json"
            )

        self.arquivo = arquivo
        diretorio = os.path.dirname(self.arquivo)

        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        if not os.path.exists(self.arquivo):
            self.salvar_dados({})

    def carregar_dados(self):
        """Carrega as listas salvas no JSON."""
        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            return dados if isinstance(dados, dict) else {}

        except (json.JSONDecodeError, OSError):
            return {}

    def salvar_dados(self, dados):
        """Salva as listas no JSON."""
        try:
            diretorio = os.path.dirname(self.arquivo)

            if diretorio:
                os.makedirs(diretorio, exist_ok=True)

            with open(self.arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(
                    dados,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except OSError as erro:
            return f"Erro ao salvar listas: {erro}"

    def criar_lista(self, id_usuario, nome, tipo):
        """Cria uma lista personalizada para o usuário."""
        if id_usuario is None:
            return "É necessário informar o usuário."

        if not isinstance(nome, str) or not nome.strip():
            return "O nome da lista não pode ser vazio."

        if not isinstance(tipo, str) or not tipo.strip():
            return "O tipo da lista não pode ser vazio."

        dados = self.carregar_dados()
        usuario = str(id_usuario)
        listas_usuario = dados.setdefault(usuario, {})

        for lista in listas_usuario.values():
            if lista.get("nome", "").casefold() == nome.strip().casefold():
                return "Já existe uma lista com esse nome."

        numeros = []

        for identificador in listas_usuario:
            try:
                numeros.append(int(identificador))
            except (ValueError, TypeError):
                continue

        novo_id = str(max(numeros, default=0) + 1).zfill(4)

        listas_usuario[novo_id] = {
            "nome": nome.strip(),
            "tipo": tipo.strip(),
            "conteudo": []
        }

        resultado = self.salvar_dados(dados)

        if resultado is not True:
            return resultado

        return novo_id

    def listar_listas(self, id_usuario):
        """Retorna as listas pertencentes ao usuário."""
        dados = self.carregar_dados()
        return dados.get(str(id_usuario), {})

    def obter_lista(self, id_usuario, id_lista):
        """Retorna uma lista específica ou None."""
        listas = self.listar_listas(id_usuario)
        return listas.get(str(id_lista).zfill(4))

    def adicionar_na_lista(
        self, id_usuario, id_lista, id_midia
    ):
        """Adiciona o ID de uma mídia a uma lista."""
        dados = self.carregar_dados()
        usuario = str(id_usuario)
        identificador = str(id_lista).zfill(4)

        lista = dados.get(usuario, {}).get(identificador)

        if lista is None:
            return "Lista não encontrada."

        midia = str(id_midia)

        if midia in lista["conteudo"]:
            return "Essa mídia já está na lista."

        lista["conteudo"].append(midia)

        resultado = self.salvar_dados(dados)

        if resultado is not True:
            return resultado

        return True

    def remover_da_lista(
        self, id_usuario, id_lista, id_midia
    ):
        """Remove o ID de uma mídia de uma lista."""
        dados = self.carregar_dados()
        usuario = str(id_usuario)
        identificador = str(id_lista).zfill(4)

        lista = dados.get(usuario, {}).get(identificador)

        if lista is None:
            return "Lista não encontrada."

        midia = str(id_midia)

        if midia not in lista["conteudo"]:
            return "Essa mídia não está na lista."

        lista["conteudo"].remove(midia)

        resultado = self.salvar_dados(dados)

        if resultado is not True:
            return resultado

        return True

    def apagar_lista(self, id_usuario, id_lista):
        """Exclui uma lista personalizada."""
        dados = self.carregar_dados()
        usuario = str(id_usuario)
        identificador = str(id_lista).zfill(4)

        listas_usuario = dados.get(usuario, {})

        if identificador not in listas_usuario:
            return "Lista não encontrada."

        del listas_usuario[identificador]

        resultado = self.salvar_dados(dados)

        if resultado is not True:
            return resultado

        return True
