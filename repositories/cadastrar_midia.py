"""Persistência das mídias (com temporadas e episódios) em data/midia_dic.json."""

from repositories.base import RepositorioJson
from src.midia import Midia


class CadastrarMidia(RepositorioJson):
    """Persistência e consulta de filmes e séries."""
    def __init__(self, pasta=None):
        super().__init__("midia_dic.json", pasta)

    def listar(self):
        """Todas as mídias, ordenadas por ID."""
        try:
            midias = [Midia.de_dict(d) for d in self.carregar().values()]
        except (TypeError, KeyError) as erro:
            raise ValueError(
                "midia_dic.json usa um formato incompatível ou contém campos ausentes."
            ) from erro
        return sorted(midias, key=lambda m: m.id)

    def obter(self, id_midia):
        try:
            return Midia.de_dict(self.carregar()[str(int(id_midia))])
        except (KeyError, ValueError):
            raise ValueError(f"Mídia {id_midia} não encontrada.") from None

    def cadastrar(self, midia):
        """Cadastra a mídia; rejeita o mesmo título + tipo + ano."""
        dados = self.carregar()
        existentes = [Midia.de_dict(d) for d in dados.values()]
        if any(m.chave == midia.chave for m in existentes):
            raise ValueError(
                f"Já existe {midia.tipo.lower()} '{midia.titulo}' de {midia.ano}."
            )
        midia.id = max((m.id for m in existentes), default=0) + 1
        dados[str(midia.id)] = midia.para_dict()
        self.salvar(dados)
        return midia

    def salvar_midia(self, midia):
        """Grava alterações e impede duplicidade de título, tipo e ano."""
        dados = self.carregar()
        if str(midia.id) not in dados:
            raise ValueError(f"Mídia {midia.id} não encontrada.")
        for id_existente, registro in dados.items():
            if id_existente == str(midia.id):
                continue
            existente = Midia.de_dict(registro)
            if existente.chave == midia.chave:
                raise ValueError(
                    f"Já existe {midia.tipo.lower()} '{midia.titulo}' de {midia.ano}."
                )
        dados[str(midia.id)] = midia.para_dict()
        self.salvar(dados)

    def remover(self, id_midia):
        dados = self.carregar()
        midia = self.obter(id_midia)
        del dados[str(midia.id)]
        self.salvar(dados)
        return midia
