"""Configurações do sistema (valores lidos de settings.json)."""

from dataclasses import asdict, dataclass, replace


@dataclass
class Configuracoes:
    """Configurações validadas do catálogo."""
    nota_minima_recomendado: float = 7.0
    limite_listas: int = 10
    # horas = minutos * multiplicador_duracao (padrão: 1/60)
    multiplicador_duracao: float = 1 / 60
    # casas decimais do arredondamento das horas
    casas_decimais: int = 2

    def __post_init__(self):
        try:
            self.nota_minima_recomendado = float(self.nota_minima_recomendado)
            self.limite_listas = int(self.limite_listas)
            self.multiplicador_duracao = float(self.multiplicador_duracao)
            self.casas_decimais = int(self.casas_decimais)
        except (TypeError, ValueError):
            raise ValueError("Valor de configuração inválido.") from None
        if not 0 <= self.nota_minima_recomendado <= 10:
            raise ValueError("A nota mínima deve estar entre 0 e 10.")
        if self.limite_listas < 0:
            raise ValueError("O limite de listas não pode ser negativo.")
        if self.casas_decimais < 0:
            raise ValueError("As casas decimais não podem ser negativas.")
        if self.multiplicador_duracao <= 0:
            raise ValueError("O multiplicador de duração deve ser positivo.")

    def horas(self, minutos, casas_decimais=None):
        """Converte minutos em horas; o arredondamento vem de settings.json."""
        casas = self.casas_decimais if casas_decimais is None else casas_decimais
        return round(minutos * self.multiplicador_duracao, casas)

    def definir(self, chave, valor):
        """Devolve uma cópia com a chave alterada (e validada)."""
        if chave not in asdict(self):
            raise ValueError(f"Configuração desconhecida: '{chave}'.")
        return replace(self, **{chave: valor})
