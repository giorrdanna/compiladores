import sys

from lexer import Lexer


PROGRAMA_EXEMPLO = """
programa limpeza
inicio
    // programa de limpeza com desvio de obstaculo
    repetir 3 {
        mover;
        se sujo {
            limpar;
        }
        direita;
    }
    se obstaculo {
        direita;
    } senao {
        mover;
    }
    voltar_base;
fim
"""

PROGRAMA_COM_ERRO = """
programa teste
inicio
    mover @;
    se sujo # limpar;
fim
"""


def imprimir_resultado(tokens, erros):
    print(f"{'LINHA':<7}{'COLUNA':<9}{'LEXEMA':<16}{'TOKEN'}")
    print("-" * 52)
    for tok in tokens:
        lexema_exibido = tok.lexema if tok.lexema else "<<EOF>>"
        print(f"{tok.linha:<7}{tok.coluna:<9}{lexema_exibido:<16}{tok.tipo}")

    if erros:
        print("\nErros léxicos encontrados:")
        for e in erros:
            print(f"  - {e}")
    else:
        print("\nNenhum erro léxico encontrado.")


def rodar(nome, codigo):
    print("=" * 60)
    print(nome)
    print("=" * 60)
    lexer = Lexer(codigo)
    tokens, erros = lexer.tokenizar()
    imprimir_resultado(tokens, erros)
    print()


def ler_codigo_do_terminal():
    """
    Lê linhas digitadas pelo usuário até encontrar uma linha vazia.
    Retorna o código digitado como uma única string, pronta para o Lexer.
    """
    print("Digite o código do robô (finalize com uma linha vazia):\n")
    linhas = []
    while True:
        try:
            linha = input()
        except EOFError:
            # Também aceita Ctrl+D / Ctrl+Z como forma de encerrar
            break
        if linha == "":
            break
        linhas.append(linha)
    return "\n".join(linhas)


def modo_interativo():
    codigo = ler_codigo_do_terminal()
    print()
    rodar("RESULTADO DA ANÁLISE LÉXICA", codigo)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            rodar("PROGRAMA VÁLIDO (com extensão de obstáculo e comentário)", PROGRAMA_EXEMPLO)
            rodar("PROGRAMA COM ERROS LÉXICOS PROPOSITAIS", PROGRAMA_COM_ERRO)
        else:
            caminho = sys.argv[1]
            with open(caminho, encoding="utf-8") as f:
                codigo = f.read()
            rodar(f"ARQUIVO: {caminho}", codigo)
    else:
        modo_interativo()


if __name__ == "__main__":
    main()