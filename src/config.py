class Configuracoes:
    """
    Gerencia as configurações do sistema para recomendações
    de mídias e limites de listas personalizadas.
    """

    def __init__(
        self,
        nota_min_recomendacao=7.0,
        limite_listas_personalizadas=10
    ):
        self.nota_min_recomendacao = nota_min_recomendacao
        self.limite_listas_personalizadas = limite_listas_personalizadas

    def Mostrar_config(self):
        """Exibe as configurações atuais."""
        print("\n===== CONFIGURAÇÕES =====")
        print(
            f"Nota mínima para recomendação: "
            f"{self.nota_min_recomendacao}"
        )
        print(
            f"Limite de listas personalizadas: "
            f"{self.limite_listas_personalizadas}"
        )

    def Nota_min_recomendado(self):
        """Consulta ou altera a nota mínima recomendada."""
        while True:
            try:
                nota = float(
                    input(
                        "Nova nota mínima para recomendação (0 a 10): "
                    ).strip().replace(",", ".")
                )

                if not 0 <= nota <= 10:
                    print("A nota deve estar entre 0 e 10.")
                    continue

                self.nota_min_recomendacao = nota
                return True

            except ValueError:
                print("Digite uma nota numérica válida.")

    def Limite_lista(self):
        """Consulta ou altera o limite de listas personalizadas."""
        while True:
            try:
                limite = int(
                    input(
                        "Novo limite de listas personalizadas: "
                    ).strip()
                )

                if limite < 0:
                    print("O limite não pode ser negativo.")
                    continue

                self.limite_listas_personalizadas = limite
                return True

            except ValueError:
                print("Digite um número inteiro válido.")
