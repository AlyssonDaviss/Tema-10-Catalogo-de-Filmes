# Tema-10-Catalogo-de-Filmes

## Descrição do projeto e objetivo

<p>  TotalView é um sistema em linha de comando (CLI) para gerenciar um catálogo pessoal de 
filmes e séries, com avaliações, status de visualização, temporadas/episódios, histórico e 
relatórios de consumo de mídia. Além disso possibilita acompanhar o progresso de séries e 
comparar avaliações entre mídias.</>p

<p>  TotalView objetiva o gerenciamento de mídias, permitindo cadastrar, acompanhar e avaliar 
filmes e séries, organizar listas e favoritos, registrar o histórico de visualização e gerar 
relatórios personalizados sobre o consumo e as avaliações do catálogo.</p>

## Estrutura planejada de classes

<details>
<summary>Clique para expandir</summary>

Classe: Usuário

Atributos:
  - Login
  - Senha

Métodos:
  + Fazer_login()

Classe: CLI

Atributos:
  - Comando
  - Argumentos

Métodos:
  + Executar()
  + Processar_comando()
  + Mostrar_ajuda()

Classe: Comandos

Métodos:
  + Cadastrar()
  + Listar()
  + Buscar()
  + Avaliar()
  + Remover()
  + Criar_lista()
  + Gerar_relatorio()
  + Mostrar_config()

Classe: Mídia

Atributos:
  - Título
  - Tipo
  - Gênero
  - Ano
  - Classificação_Indicativa
  - Elenco[]
  - Status

Métodos:
  + Cadastrar_Midia()
  + Impedir_Duplicidade()
  + Registrar_status()

Classe: Filme (herda de Mídia)

Atributos:
  - Duração

Métodos:
  + Registrar_duração()

Classe: Série (herda de Mídia)

Atributos:
  - nº Temporadas
  - nº Episódios
  - Nota (opcional)

Métodos:
  + Registrar_temporadas()
  + Atualizar_status()

Classe: Temporada (Se relaciona com Série e Episódio)

Atributos:
  - Titulo
  - nº Episódios
  - Data de lançamento
  - Nota (opcional)

Métodos:
  + Registrar_episodios()

Classe: Episódio (Se relaciona com Temporada e Avaliação)

Atributos:
  - nº Episódio
  - Título
  - Duração
  - Data de lançamento
  - Status de visualização
  - Nota (opcional)

Métodos:
  + Registrar_status()

Classe: Avaliação (se relaciona com Usuário, Mídia e Episódio)

Atributos:
  - Nota
  - Comentário

Métodos:
  + Gerar_media()
  + Registrar_nota()
  + Registrar_comentario()
  
Classe: Histórico de visualização (se relaciona com Usuário e Mídia)

Atributos:
  - Mídia
  - Data
  - Hora

Métodos:
  + Salvar_historico()
  + Registrar_data_hora()

Classe: Lista (se relaciona com Usuário e Mídia)

Atributos:
  - Nome
  - Tipo
  - Conteúdo[]

Métodos:
  + Criar_lista()
  + Adicionar_na_lista()
  + Remover_na_lista()
  + Apagar_lista()

Classe: Relatório

Métodos:
  + Gerar_media_geral_catalogo()
  + Gerar_relatorio()
  + Media_genero()
  + Tempo_total_tipo()
  + Top_10()
  + Serie_maior_numero_ep_assistidos()

Classe: Configurações

Atributos:
  - Nota Mínima para a Recomendação
  - Limite de listas personalizadas por usuário

Métodos:
  + Mostrar_config()
  + Nota_min_recomendado()
  + Limite_lista()

</details>

<details>
<summary>Ver a estrutura</summary>

classDiagram

    class Usuario {
        -String login
        -String senha
        +fazerLogin()
    }

    class CLI {
        -String comando
        -String argumentos
        +executar()
        +processarComando()
        +mostrarAjuda()
    }

    class Comandos {
        +cadastrar()
        +listar()
        +buscar()
        +avaliar()
        +remover()
        +criarLista()
        +gerarRelatorio()
        +mostrarConfig()
    }

    class Midia {
        -String titulo
        -String tipo
        -String genero
        -int ano
        -String classificacaoIndicativa
        -String[] elenco
        -String status
        +cadastrarMidia()
        +impedirDuplicidade()
        +registrarStatus()
    }

    class Filme {
        -int duracao
        +registrarDuracao()
    }

    class Serie {
        -int numeroTemporadas
        -int numeroEpisodios
        -float nota
        +registrarTemporadas()
        +atualizarStatus()
    }

    class Temporada {
        -String titulo
        -int numeroEpisodios
        -Date dataLancamento
        -float nota
        +registrarEpisodios()
    }

    class Episodio {
        -int numeroEpisodio
        -String titulo
        -int duracao
        -Date dataLancamento
        -String statusVisualizacao
        -float nota
        +registrarStatus()
    }

    class Avaliacao {
        -float nota
        -String comentario
        +gerarMedia()
        +registrarNota()
        +registrarComentario()
    }

    class HistoricoVisualizacao {
        -Midia midia
        -Date data
        -Time hora
        +salvarHistorico()
        +registrarDataHora()
    }

    class Lista {
        -String nome
        -String tipo
        -Midia[] conteudo
        +criarLista()
        +adicionarNaLista()
        +removerNaLista()
        +apagarLista()
    }

    class Relatorio {
        +gerarMediaGeralCatalogo()
        +gerarRelatorio()
        +mediaGenero()
        +tempoTotalTipo()
        +top10()
        +serieMaiorNumeroEpAssistidos()
    }

    class Configuracoes {
        -float notaMinimaRecomendacao
        -int limiteListasPersonalizadas
        +mostrarConfig()
        +notaMinRecomendado()
        +limiteLista()
    }

    %% Herança
    Midia <|-- Filme : Herda de
    Midia <|-- Serie : Herda de

    %% Relações
    Serie "1" --> "*" Temporada : Possui
    Temporada "1" --> "*" Episodio : Possui

    Usuario "1" --> "*" Avaliacao : Realiza
    Midia "1" --> "*" Avaliacao : Recebe
    Episodio "1" --> "*" Avaliacao : Recebe

    Usuario "1" --> "*" HistoricoVisualizacao : Possui
    Midia "1" --> "*" HistoricoVisualizacao : Registrada

    Usuario "1" --> "*" Lista : Possui
    Lista "*" --> "*" Midia : Contem

    CLI --> Comandos : Executa
    Comandos --> Midia : Gerencia
    Comandos --> Avaliacao : Gerencia
    Comandos --> Lista : Gerencia
    Comandos --> Relatorio : Gera
    Comandos --> Configuracoes : Consulta

</details>

### Decisões de Desing. 

    - Dividi Série, Temporada e Episódio, pois cada um possui características próprias que são melhores representadas separadamente.
    
    - Duração não participa de Mídia, pois não é compatível com a estrutura de série (temporadas e episódios), e sim com episódios e filmes.
      - Da mesma forma, subdividi os atributos de Série entre Episódio e Temporada, pois não é usual saber a duração de uma série inteira
      assim como outros atributos.

    - A nota média da série e a nota geral do catálogo são calculadas automaticamente a partir das avaliações registradas.

    - Como Favoritos é um tipo de lista, não vejo motivo para criá-la como uma subclasse, então coloquei como um tipo.


