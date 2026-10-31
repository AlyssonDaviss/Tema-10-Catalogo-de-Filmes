"""Ponto de entrada.

  python main.py                      abre o menu interativo
  python main.py <grupo> <ação> ...   executa um subcomando (veja: python main.py -h)
"""

import sys
import shlex

from src.cli import EXEMPLOS, executar, nomes_grupos
from src.services.comandos import Comandos, mostrar_mensagem
from src.menu import Menu


def _boas_vindas():
    """Tela inicial do terminal de comandos: como pedir ajuda e por onde começar."""
    print("\nMODO COMANDOS")
    print("  ajuda                  lista todos os comandos")
    print(f"  ajuda <grupo>          detalha um grupo ({', '.join(nomes_grupos())})")
    print("  ajuda <grupo> <ação>   detalha um comando, ex.: ajuda midia adicionar")
    print("  sair                   encerra")
    print("\nPara começar:")
    for exemplo in EXEMPLOS:
        print(f"  {exemplo}")
    print()


def _terminal_comandos(pasta=None):
    """Mantém o modo CLI ativo e aceita vários comandos na mesma execução."""
    # O shlex entende aspas como parte dos argumentos, como acontece no shell.
    # Se a entrada estiver incompleta, mostramos o erro e mantemos o terminal aberto.
    _boas_vindas()
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
        try:
            argumentos = shlex.split(texto, posix=True)
        except ValueError as erro:
            mostrar_mensagem(f"Erro ao interpretar o comando: {erro}")
            continue
        if argumentos and argumentos[0].casefold() in {"help", "comandos"}:
            argumentos[0] = "ajuda"
        try:
            executar(argumentos, pasta)
        except SystemExit:
            # Um comando inválido ou --help não encerra a sessão interativa.
            continue
        except (KeyboardInterrupt, EOFError):
            print("\nComando interrompido.")


def _escolher_interface(pasta=None):
    # As duas interfaces chamam a mesma camada de regras do sistema.
    while True:
        # Cada opção é apresentada como uma tela separada das respostas anteriores.
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
