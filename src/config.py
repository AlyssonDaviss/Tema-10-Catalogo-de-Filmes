"""Configurações do sistema (valores lidos de settings.json)."""

from dataclasses import asdict, dataclass, replace


@dataclass
class Configuracoes:
    nota_minima_recomendado: float = 7.0
    limite_listas: int = 10
    # horas = minutos * multiplicador_duracao (padrão: 1/60)
    multiplicador_duracao: float = 1 / 60
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
        if self.multiplicador_duracao <= 0:
            raise ValueError("O multiplicador de duração deve ser positivo.")
        if not 0 <= self.casas_decimais <= 6:
            raise ValueError("As casas decimais devem estar entre 0 e 6.")

    def horas(self, minutos):
        """Converte minutos em horas com o arredondamento configurado."""
        return round(minutos * self.multiplicador_duracao, self.casas_decimais)

    def definir(self, chave, valor):
        """Devolve uma cópia com a chave alterada (e validada)."""
        if chave not in asdict(self):
            raise ValueError(f"Configuração desconhecida: '{chave}'.")
        return replace(self, **{chave: valor})
