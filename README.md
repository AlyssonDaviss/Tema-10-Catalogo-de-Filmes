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

Classe: Usuário

Atributos:
  - Login
  - Senha

Classe: Mídia

Classe: Mídia

Atributos:
- Título
- Tipo
- Gênero
- Ano
- Classificação_Indicativa
- Elenco
- Status

Classe: Filme (herda de Mídia)

Atributos:
  - Duração

Classe: Série (herda de Mídia)
  - nº Temporadas
  - nº Episódios
  - Data de lançamento
  - Nota (opcional)

Classe: Temporada (Se relaciona com Série e Episódio)
  - Titulo
  - nº Episódios
  - Data de lançamento
  - Nota (opcional)

Classe: Episódio (Se relaciona com Temporada)
  - nº Episódio
  - Título
  - Duração
  - Data de lançamento
  - Status de visualização
  - Nota (opcional)

Classe: Avaliação (se relaciona com Usuário e Mídia)

  - Nota
  - Comentário


### Obs. 

    * Dividi Série, Temporada e Episódio, pois cada um possui características próprias que são melhores representadas separadamente.
    
    * Duração não participa de Mídia, pois não é compatível com a estrutura de série (temporadas e episódios), e sim com episódios e filmes.
      - Da mesma forma, subdividi os atributos de Série entre Episódio e Temporada, pois não é usual saber a duração de uma série inteira
      assim como outros atributos.

    * A nota média da série e a nota geral do catálogo são calculadas automaticamente a partir das avaliações registradas.


