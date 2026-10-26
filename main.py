"""Ponto de entrada.

  python main.py                      abre o menu interativo
  python main.py <grupo> <ação> ...   executa um subcomando (veja: python main.py -h)
"""

import sys
import shlex

from src.cli import executar, criar_parser
from src.comandos import Comandos
from src.menu import Menu


def _mostrar_comandos():
    """Exibe modelos de comandos que podem ser copiados e colados."""
    print("""
COMANDOS PARA COPIAR E COLAR
(Substitua os valores entre < > pelos dados desejados.)

Conta:
  usuario entrar <login>
  usuario quem
  usuario sair

Mídias:
  midia adicionar --tipo filme --titulo "Matrix" --genero "Ficção" --ano 1999 --classificacao 14 --duracao 136
  midia adicionar --tipo serie --titulo "Dark" --genero "Suspense" --ano 2017 --classificacao 16
  midia listar
  midia listar --tipo filme
  midia listar --busca "Matrix"
  midia avaliar <ID> <NOTA>
  midia atualizar-status <ID> "ASSISTIDO"
  midia recomendar
  midia remover <ID>
  midia relatorio top
  midia relatorio geral
  midia relatorio notas --por genero
  midia relatorio tempo

Séries:
  serie adicionar-temporada <ID> --episodios 10 --duracao 45
  serie adicionar-episodio <ID> -t 1 -n 1 --titulo "Piloto" --duracao 45
  serie atualizar-status <ID> "ASSISTINDO"
  serie episodios <ID>

Listas e favoritos:
  usuario criar-lista "Quero assistir"
  usuario adicionar-favorito <ID>
  usuario adicionar-na-lista "Quero assistir" <ID>
  usuario listas
  usuario historico

Outros:
  config mostrar
  exemplos
  ajuda
  sair

Digite os comandos sem escrever "python main.py" antes deles.
""")


def _terminal_comandos(pasta=None):
    """Mantém o modo CLI ativo e aceita vários comandos na mesma execução."""
    _mostrar_comandos()
    while True:
        try:
            texto = input("\ncatálogo> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAté logo!")
            return 0
        if not texto:
            continue
        if texto.casefold() in {"sair", "exit", "quit"}:
            print("Até logo!")
            return 0
        if texto.casefold() in {"ajuda", "help", "comandos"}:
            _mostrar_comandos()
            continue
        try:
            argumentos = shlex.split(texto, posix=True)
            executar(argumentos, pasta)
        except SystemExit:
            # Um comando inválido ou --help não encerra a sessão interativa.
            continue
        except (KeyboardInterrupt, EOFError):
            print("\nComando interrompido.")


def _escolher_interface(pasta=None):
    while True:
        print("\n=== CATÁLOGO DE FILMES E SÉRIES ===")
        print("1. Menu guiado (escolher opções com números)")
        print("2. CLI com comandos (digitar ou copiar e colar comandos)")
        print("0. Sair")
        escolha = input("Qual interface deseja usar? ").strip()
        if escolha == "1":
            Menu(Comandos(pasta)).iniciar()
            return 0
        if escolha == "2":
            return _terminal_comandos(pasta)
        if escolha == "0":
            print("Até logo!")
            return 0
        print("Opção inválida. Escolha 1, 2 ou 0.")


def main(argv=None, pasta=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        if argv:
            return executar(argv, pasta)
        return _escolher_interface(pasta)
    except (KeyboardInterrupt, EOFError):
        print("\nAté logo!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
