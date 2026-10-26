"""Lista personalizada de mídias (guarda apenas os IDs, sem duplicatas)."""


class ListaPersonalizada:
    def __init__(self, nome, midias=()):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome da lista não pode ser vazio.")
        self.nome = nome.strip()
        self._midias = []
        for id_midia in midias:
            self.adicionar(id_midia)

    @property
    def midias(self):
        return list(self._midias)

    def adicionar(self, id_midia):
        if id_midia in self._midias:
            raise ValueError(f"A mídia {id_midia} já está na lista '{self.nome}'.")
        self._midias.append(id_midia)

    def remover(self, id_midia):
        if id_midia not in self._midias:
            raise ValueError(f"A mídia {id_midia} não está na lista '{self.nome}'.")
        self._midias.remove(id_midia)

    def __len__(self):
        return len(self._midias)

    def __contains__(self, id_midia):
        return id_midia in self._midias

    def para_dict(self):
        return {"nome": self.nome, "midias": self.midias}

    @classmethod
    def de_dict(cls, dados):
        return cls(dados["nome"], dados["midias"])
