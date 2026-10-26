"""Leitura e gravação de JSON, compartilhadas por todos os repositórios."""

import json
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DATA = RAIZ / "data"


class RepositorioJson:
    """Persistência comum baseada em arquivos JSON."""
    def __init__(self, arquivo, pasta=None):
        self.caminho = Path(pasta or PASTA_DATA) / arquivo

    def carregar(self):
        """Devolve o conteúdo (um dict); arquivo ausente equivale a {}."""
        if not self.caminho.exists():
            return {}
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError as erro:
            raise ValueError(f"{self.caminho.name} contém JSON inválido: {erro}") from None
        if not isinstance(dados, dict):
            raise ValueError(f"{self.caminho.name} deve conter um objeto JSON.")
        return dados

    def salvar(self, dados):
        """Grava em arquivo temporário e troca, para nunca deixar JSON pela metade."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        temporario = self.caminho.with_suffix(".tmp")
        temporario.write_text(
            json.dumps(dados, indent=4, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        os.replace(temporario, self.caminho)
