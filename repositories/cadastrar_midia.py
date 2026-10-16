
import json
from pathlib import Path


class CadastrarMidia:
    def __init__(self):
        self.caminho = (
            Path(__file__).resolve().parent.parent
            / "data" / "midia_dic.json"
        )

    def carregar_dados(self):
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar_dados(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def gerar_id(self, dados):
        ids = [int(i) for i in dados if i.isdigit()]
        return str(max(ids, default=0) + 1).zfill(4)

    def cadastrar_midia(self, midia):
        dados = self.carregar_dados()

        for item in dados.values():
            if item["titulo"].casefold() == midia.titulo.casefold():
                return False

        novo_id = self.gerar_id(dados)

        if midia.tipo == "filme":
            dados[novo_id] = {
                "tipo": midia.tipo,
                "titulo": midia.titulo,
                "genero": midia.genero,
                "duracao": ""
            }

        elif midia.tipo == "serie":
            dados[novo_id] = {
                "tipo": midia.tipo,
                "titulo": midia.titulo,
                "genero": midia.genero,
                "temporadas": {}
            }

        else:
            return False

        self.salvar_dados(dados)
        return novo_id

    def atualizar_duracao(self, id_midia, duracao):
        dados = self.carregar_dados()
        id_midia = str(id_midia)

        if id_midia not in dados:
            return "ID não cadastrado."

        dados[id_midia]["duracao"] = duracao
        self.salvar_dados(dados)
        return True

    def cadastrar_temporada(self, id_serie, temporada):
        dados = self.carregar_dados()
        id_serie = str(id_serie)

        if id_serie not in dados:
            return "ID não cadastrado."

        temporadas = dados[id_serie].setdefault("temporadas", {})
        novo_id = self.gerar_id(temporadas)

        temporadas[novo_id] = {
            "titulo": temporada.obter_titulo(),
            "numero_episodios": temporada.obter_numero_episodios(),
            "data_lancamento": temporada.obter_data_lancamento(),
            "episodios": {}
        }

        self.salvar_dados(dados)
        return novo_id

    def registrar_episodio(self, id_serie, id_temporada, episodio):
        dados = self.carregar_dados()

        id_serie = str(id_serie)
        id_temporada = str(id_temporada)

        if id_serie not in dados:
            return "Série não cadastrada."

        temporadas = dados[id_serie].get("temporadas", {})

        if id_temporada not in temporadas:
            return "Temporada não cadastrada."

        temporada = temporadas[id_temporada]
        episodios = temporada.setdefault("episodios", {})

        if len(episodios) >= temporada["numero_episodios"]:
            return "Limite de episódios atingido."

        novo_id = self.gerar_id(episodios)

        episodios[novo_id] = {
            "numero_episodio": len(episodios) + 1,
            "titulo": episodio.obter_titulo(),
            "duracao": episodio.obter_duracao(),
            "data_lancamento": episodio.obter_data_lancamento()
        }

        self.salvar_dados(dados)
        return True
