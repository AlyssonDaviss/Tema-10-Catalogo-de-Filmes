"""Persistência das configurações individuais dos usuários em data/dados.json."""

import json
import os
from pathlib import Path


class CadastrarConfiguracoes:
    """Carrega e salva configurações sem sobrescrever os outros dados do usuário."""

    CONFIGURACOES_PADRAO = {
        "nota_min_recomendacao": 7.0,
        "limite_listas_personalizadas": 10,
    }

    def __init__(self, caminho_arquivo=None):
        raiz_projeto = Path(__file__).resolve().parent.parent
        self.caminho_arquivo = Path(
            caminho_arquivo or raiz_projeto / "data" / "dados.json"
        )

    def _carregar_dados(self):
        if not self.caminho_arquivo.exists():
            return {}

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except json.JSONDecodeError as erro:
            raise ValueError(
                f"O arquivo {self.caminho_arquivo} contém JSON inválido."
            ) from erro

        if not isinstance(dados, dict):
            raise ValueError("O arquivo de usuários deve conter um objeto JSON.")
        return dados

    def _salvar_dados(self, dados):
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo_temporario = self.caminho_arquivo.with_suffix(
            self.caminho_arquivo.suffix + ".tmp"
        )

        try:
            with arquivo_temporario.open("w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
                arquivo.write("\n")
            os.replace(arquivo_temporario, self.caminho_arquivo)
        finally:
            if arquivo_temporario.exists():
                arquivo_temporario.unlink()

    @staticmethod
    def _encontrar_usuario(dados, id_usuario):
        """Aceita IDs em texto ou número, sem alterar o formato já salvo."""
        id_texto = str(id_usuario)
        if id_texto in dados:
            return id_texto
        if id_texto.isdigit() and int(id_texto) in dados:
            return int(id_texto)
        return None

    def obter_ou_criar(self, id_usuario):
        """Retorna as configurações do usuário e grava os padrões se necessário."""
        if id_usuario is None:
            raise ValueError("É necessário informar o ID do usuário.")

        dados = self._carregar_dados()
        chave_usuario = self._encontrar_usuario(dados, id_usuario)
        if chave_usuario is None:
            raise KeyError(
                f"O usuário de ID {id_usuario!r} não foi encontrado em "
                f"{self.caminho_arquivo}."
            )

        usuario = dados[chave_usuario]
        if not isinstance(usuario, dict):
            raise ValueError(f"Os dados do usuário {id_usuario!r} são inválidos.")

        configuracoes_salvas = usuario.get("configuracoes")
        if not isinstance(configuracoes_salvas, dict):
            configuracoes_salvas = {}

        configuracoes = self.CONFIGURACOES_PADRAO.copy()
        configuracoes.update(configuracoes_salvas)

        # Persiste os padrões apenas quando há algo novo a gravar.
        if usuario.get("configuracoes") != configuracoes:
            usuario["configuracoes"] = configuracoes
            self._salvar_dados(dados)

        return configuracoes.copy()

    def salvar_configuracoes(self, id_usuario, configuracoes):
        """Salva as duas configurações e mantém intactos os demais dados."""
        if id_usuario is None:
            return False
        if not isinstance(configuracoes, dict):
            raise TypeError("As configurações devem ser fornecidas em um dicionário.")

        try:
            nota = float(configuracoes["nota_min_recomendacao"])
            limite = int(configuracoes["limite_listas_personalizadas"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("Os valores das configurações são inválidos.")

        if not 0 <= nota <= 10:
            raise ValueError("A nota mínima deve estar entre 0 e 10.")
        if limite < 0:
            raise ValueError("O limite de listas não pode ser negativo.")

        dados = self._carregar_dados()
        chave_usuario = self._encontrar_usuario(dados, id_usuario)
        if chave_usuario is None:
            raise KeyError(f"O usuário de ID {id_usuario!r} não foi encontrado.")

        usuario = dados[chave_usuario]
        if not isinstance(usuario, dict):
            raise ValueError(f"Os dados do usuário {id_usuario!r} são inválidos.")

        # Preserva chaves futuras adicionadas às configurações.
        configuracoes_atuais = usuario.get("configuracoes", {})
        if not isinstance(configuracoes_atuais, dict):
            configuracoes_atuais = {}
        configuracoes_atuais.update({
            "nota_min_recomendacao": nota,
            "limite_listas_personalizadas": limite,
        })
        usuario["configuracoes"] = configuracoes_atuais
        self._salvar_dados(dados)
        return True
