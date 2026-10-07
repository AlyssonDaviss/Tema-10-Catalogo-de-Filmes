dados = {
  usuario: "Alysson",
  senha: "123456",
  historico: ["0001", "0002", "0003"],
  listas: [{
    favoritos: ["0001", "0002"],
    assistir_mais_tarde: ["0003"]
  }],
  midias: [{
    "0001": {
        nota: 4.5,
        comentarios: ["Ótimo filme!", "Adorei a atuação do elenco."]
    },
    "0002": {
        nota: 3.8,
        comentarios: ["Divertido, mas poderia ser melhor."]
    },
    "0003": {
        nota: 4.2,
        comentarios: ["Emocionante e bem dirigido."]
    },
    "0004": {
        nota: 4.7,
        comentarios: ["Série envolvente e com ótimos episódios."],
        episodios: [
            {
                id: "0004-01",
                nota: 4.5,
                comentarios: ["Episódio inicial promissor."]
            },
            {
                id: "0004-02",
                nota: 4.8,
                comentarios: ["Episódio emocionante e cheio de reviravoltas."]
            }
        ]
    }
  }]
};

export default dados;