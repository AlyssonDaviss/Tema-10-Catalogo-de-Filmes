# Tema-10-Catalogo-de-Filmes

## Descrição do projeto e objetivo

<p>TotalView é um sistema em linha de comando (CLI) para gerenciar um catálogo pessoal de filmes e séries, com avaliações, status de visualização, temporadas/episódios, histórico e relatórios de consumo de mídia. Além disso, possibilita acompanhar o progresso de séries e comparar avaliações entre mídias.</p>

<p>Objetivamos o gerenciamento de mídias, permitindo cadastrar, acompanhar e avaliar filmes e séries, organizar listas e favoritos, registrar o histórico de visualização e gerar relatórios personalizados sobre o consumo e as avaliações do catálogo.</p>

## Estrutura planejada de classes

<details>
<summary>UML Textual Simplificado</summary>

**Classe: Usuario**

Atributos:
- Login
- Senha
- Listas personalizadas (inclui Favoritos)
- Histórico de visualização

Métodos:
+ Criar_lista()
+ Adicionar_favorito()
+ Apagar_lista()
+ Registrar_conclusao()
+ Remover_registros()

**Classe: Comandos (services)**

Métodos:
+ Entrar() / Sair()
+ Adicionar_midia()
+ Listar()
+ Avaliar()
+ Atualizar_status()
+ Editar_midia()
+ Remover()
+ Recomendar()
+ Adicionar_temporada() / Adicionar_episodio()
+ Criar_lista() / Adicionar_favorito()
+ Relatorio()
+ Definir_config()

**Interfaces: CLI (src/cli.py) e Menu (src/menu.py)**

Ambas apenas leem a entrada e chamam a classe Comandos.

**Classe: Midia (abstrata)**

Atributos:
- Título
- Gênero
- Ano
- Classificação_indicativa
- Elenco[]

Métodos:
+ Definir_status()
+ Avaliar()
+ __str__() / __repr__() / __eq__() / __hash__() / __lt__()

**Classe: AssistivelMixin**

Atributos:
- Duração (> 0)
- Status
- Nota (0 a 10)

Métodos:
+ Minutos_assistidos()

**Classe: Filme (herda de AssistivelMixin e Midia)**

Métodos:
+ Definir_status()
+ Avaliar()

**Classe: Serie (herda de Midia)**

Atributos:
- Temporadas[]
- Status (calculado a partir dos episódios)

Métodos:
+ Criar_temporada()
+ Adicionar_episodio()
+ Definir_status()
+ Avaliar()
+ __len__()

**Classe: Temporada**

Atributos:
- Número
- Episódios[]

Métodos:
+ Adicionar_episodio()
+ Nota_media()
+ __len__()

**Classe: Episodio (usa AssistivelMixin)**

Atributos:
- Temporada
- Número
- Título
- Data de lançamento

**Classe: ListaPersonalizada**

Atributos:
- Nome
- Mídias[] (IDs, sem duplicatas)

Métodos:
+ Adicionar()
+ Remover()
+ __len__() / __contains__()

**Classe: RegistroHistorico**

Atributos:
- Mídia (ID)
- Descrição
- Minutos
- Data e hora da conclusão

**Classe: Configuracoes**

Atributos:
- Nota mínima para recomendação
- Limite de listas personalizadas por usuário
- Multiplicador de duração
- Casas decimais do arredondamento das horas

Métodos:
+ Horas()
+ Definir()

**Módulo: relatorio (funções)**

+ Nota_geral()
+ Media_por() (gênero ou tipo)
+ Minutos_por_tipo()
+ Top()
+ Series_mais_assistidas()
+ Minutos_por_periodo() (semana ou mês)

**Persistência: repositories (JSON), reunidos em repositories/dados.py**

+ CadastrarMidia, CadastrarUsuario (listas e histórico), CadastrarConfiguracoes, CadastrarSessao

</details>

<details>
<summary>Ver a estrutura</summary>

```mermaid
classDiagram
    class Usuario {
        -String login
        -String senha
        -ListaPersonalizada[] listas
        -RegistroHistorico[] historico
        +criar_lista()
        +adicionar_favorito()
        +apagar_lista()
        +registrar_conclusao()
    }

    class Comandos {
        +adicionar_midia()
        +listar()
        +avaliar()
        +atualizar_status()
        +editar_midia()
        +remover()
        +recomendar()
        +adicionar_temporada()
        +adicionar_episodio()
        +criar_lista()
        +relatorio()
    }

    class Midia {
        <<abstract>>
        -String titulo
        -String genero
        -int ano
        -String classificacao
        -String[] elenco
        +definir_status()
        +avaliar()
        +__eq__()
        +__lt__()
    }

    class AssistivelMixin {
        <<mixin>>
        -float duracao
        -Status status
        -float nota
    }

    class Filme {
        +definir_status()
        +avaliar()
    }

    class Serie {
        -Temporada[] temporadas
        +criar_temporada()
        +adicionar_episodio()
        +definir_status()
        +avaliar()
        +__len__()
    }

    class Temporada {
        -int numero
        -Episodio[] episodios
        +adicionar_episodio()
        +__len__()
    }

    class Episodio {
        -int temporada
        -int numero
        -String titulo
        -Date data_lancamento
    }

    class ListaPersonalizada {
        -String nome
        -int[] midias
        +adicionar()
        +remover()
    }

    class RegistroHistorico {
        -int midia_id
        -String descricao
        -float minutos
        -DateTime concluido_em
    }

    class Configuracoes {
        -float nota_minima_recomendado
        -int limite_listas
        -float multiplicador_duracao
        -int casas_decimais
        +horas()
    }

    class Relatorio {
        <<funções>>
        +nota_geral()
        +media_por()
        +minutos_por_tipo()
        +top()
        +series_mais_assistidas()
        +minutos_por_periodo()
    }

    class Status {
        <<enumeration>>
        NAO_ASSISTIDO
        ASSISTINDO
        ASSISTIDO
    }

    class Repositorios {
        <<repositories/dados.py>>
        +CadastrarMidia
        +CadastrarUsuario
        +CadastrarConfiguracoes
    }

    %% Herança
    Midia <|-- Filme
    Midia <|-- Serie
    AssistivelMixin <|-- Filme
    AssistivelMixin <|-- Episodio

    %% Relações
    Serie "1" *-- "*" Temporada : Possui
    Temporada "1" *-- "*" Episodio : Possui
    Usuario "1" *-- "*" ListaPersonalizada : Possui
    Usuario "1" *-- "*" RegistroHistorico : Mantém
    ListaPersonalizada "*" --> "*" Midia : Contém (IDs)
    RegistroHistorico "*" --> "1" Midia : Registra
    AssistivelMixin --> Status

    %% Camadas
    Comandos --> Midia : Gerencia
    Comandos --> Usuario : Gerencia
    Comandos --> Relatorio : Usa
    Comandos --> Configuracoes : Consulta
    Comandos --> Repositorios : Persiste
```

</details>

## Estrutura de pastas

```text
main.py            ponto de entrada (menu guiado ou CLI com subcomandos)
src/
  cli.py, menu.py  interfaces (entrada e saída de tela)
  domain/          classes e regras de negócio: midia, user, listas, historico, config
  services/        lógica de aplicação: comandos, relatorio, seed
repositories/      acesso e persistência dos dados (JSON); dados.py reúne os repositórios
data/              arquivos JSON gerados pelos repositórios
tests/             testes automatizados
```

## Como executar

Requisitos: Python 3.10 ou superior. O sistema em si não precisa de bibliotecas externas.

```text
python main.py                            abre a escolha entre menu guiado e CLI com comandos
python main.py <grupo> <ação> [opções]    executa um subcomando direto
```

Os dados são gravados em `data/` e as configurações em `settings.json`.

## Como rodar os testes

```text
pip install -r requirements.txt
python -m pytest
```

## Exemplos de uso

```text
python main.py usuario entrar Davi
python main.py midia adicionar --tipo filme --titulo Matrix --genero "Ficção" --ano 1999 --classificacao 14 --duracao 136
python main.py midia adicionar --tipo serie --titulo Dark --genero "Suspense" --ano 2017 --classificacao 16
python main.py serie adicionar-temporada 2 --episodios 10 --duracao 50
python main.py serie adicionar-episodio 2 -t 2 -n 1 --titulo "Piloto" --duracao 45
python main.py midia atualizar-status 1 assistido
python main.py midia avaliar 1 9.5
python main.py midia listar --status assistido
python main.py usuario criar-lista "Para assistir"
python main.py usuario adicionar-favorito 1
python main.py midia relatorio top
python main.py midia relatorio notas --por genero
python main.py midia relatorio tempo
python main.py midia relatorio periodo --por semana
```

## Como pedir ajuda na CLI

```text
python main.py ajuda                    todos os comandos, um por linha
python main.py ajuda midia              comandos do grupo com seus argumentos
python main.py ajuda midia adicionar    detalhes de um comando
```

No terminal de comandos (opção 2 ao abrir `python main.py`) basta digitar `ajuda`, `ajuda midia` etc., sem o prefixo `python main.py`. O guia é gerado a partir dos próprios subcomandos, então não existe uma lista de comandos escrita à mão para manter.

### Decisões de Design

```text
- Dividi Série, Temporada e Episódio, pois cada um possui características próprias que são melhores representadas separadamente.

- Duração não participa de Mídia, pois não é compatível com a estrutura de série inteira. A duração é utilizada em filmes e episódios.

- O status de uma série pode ser definido a partir dos episódios. Ao alterar o status de um nível superior, a alteração é repassada aos itens abaixo dele.

- A nota média da série e da temporada é calculada a partir das avaliações dos episódios correspondentes, sem precisar solicitar uma nota para cada episódio quando a avaliação é feita pelo escopo inteiro.

- Como Favoritos é um tipo de lista, não vejo motivo para fazer ela como uma subclasse. Por isso, ela é tratada como uma organização das mídias do usuário.

- O histórico registra o tempo assistido. Quando uma mídia volta para o status de não assistida, o registro correspondente deve ser removido para manter os relatórios corretos.

- As listas personalizadas possuem um limite configurável por usuário. As configurações também definem a nota mínima para recomendação e o multiplicador utilizado na conversão de minutos para horas.

- A CLI utiliza subcomandos para executar as operações. O menu guiado oferece uma alternativa para quem prefere navegar pelas opções sem precisar conhecer todos os comandos.

- Os dados são persistidos em arquivos JSON por meio dos repositórios, separando o armazenamento das regras de negócio.

- O tempo assistido soma apenas mídias com status ASSISTIDO, como pede a regra de negócio. Uma série só entra no total quando todos os episódios estão concluídos.

- Os relatórios de notas (geral, por gênero e tipo, e top) consideram apenas mídias finalizadas (ASSISTIDO). O relatório de séries mais assistidas é a exceção, pois conta episódios assistidos.

- No menu guiado, as temporadas e os episódios avulsos ficam em Mídias > Séries: temporadas e episódios. A data de lançamento é opcional (AAAA-MM-DD, Enter para pular), como o --lancamento da CLI.

- O módulo dados.py da especificação é representado por repositories/dados.py, que reúne os repositórios em um único ponto de acesso, evitando duplicar código.

- O arredondamento das horas é configurável pela chave casas_decimais do settings.json.
```
