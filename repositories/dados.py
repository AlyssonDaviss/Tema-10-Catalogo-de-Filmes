"""Módulo de persistência (JSON): ponto único para salvar e carregar os dados.

- CadastrarMidia:         mídias, temporadas e episódios (data/midia_dic.json)
- CadastrarUsuario:       usuários, listas e histórico (data/dados.json, listas.json, historico.json)
- CadastrarConfiguracoes: settings.json
- popular:                seed de filmes e séries pré-cadastrados
"""

from repositories.cadastrar_config import CadastrarConfiguracoes
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_pessoa import CadastrarUsuario
from src.services.seed import popular

__all__ = ["CadastrarConfiguracoes", "CadastrarMidia", "CadastrarUsuario", "popular"]
