"""Histórico de visualização: conclusão de um filme ou episódio, com data e hora."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RegistroHistorico:
    """Registro de uma visualização concluída."""
    midia_id: int
    descricao: str
    minutos: float
    concluido_em: datetime

    def para_dict(self):
        return {
            "midia_id": self.midia_id,
            "descricao": self.descricao,
            "minutos": self.minutos,
            "concluido_em": self.concluido_em.isoformat(timespec="seconds"),
        }

    @classmethod
    def de_dict(cls, d):
        return cls(
            d["midia_id"], d["descricao"], d["minutos"],
            datetime.fromisoformat(d["concluido_em"]),
        )
