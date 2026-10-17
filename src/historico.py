
from datetime import datetime
from repositories.cadastrar_historico import CadastrarHistorico


class Histórico_de_visualização:
    """Representa um registro do histórico de visualização."""

    def __init__(
        self,
        midia,
        data=None,
        hora=None,
        nota=None,
        status=None,
        comentario=""
    ):
        self.__midia = str(midia)

        agora = datetime.now()
        self.__data = data or agora.strftime("%Y-%m-%d")
        self.__hora = hora or agora.strftime("%H:%M:%S")

        self.__nota = nota
        self.__status = status
        self.__comentario = comentario

    def Salvar_historico(self, id_usuario):
        registro = {
            "midia": self.__midia,
            "data": self.__data,
            "hora": self.__hora,
            "nota": self.__nota,
            "status": self.__status,
            "comentario": self.__comentario
        }

        repositorio = CadastrarHistorico()
        return repositorio.registrar_historico(
            id_usuario,
            registro
        )

    def Registrar_data_hora(self):
        agora = datetime.now()
        self.__data = agora.strftime("%Y-%m-%d")
        self.__hora = agora.strftime("%H:%M:%S")

        return self.__data, self.__hora
