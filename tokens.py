"""
Especificação léxica da linguagem simplificada do robô (T1).

Este módulo não sabe nada sobre COMO o texto é varrido (isso é
responsabilidade do lexer.py) - ele só descreve O QUE existe na
linguagem: quais palavras são reservadas, o formato de um token
reconhecido e o erro que o lexer pode levantar.

Separar isso do autômato permite reaproveitar a especificação em
outras fases do compilador (ex.: o analisador sintático do T3 também
vai precisar saber quais são os tokens).
"""

from collections import namedtuple

PALAVRAS_RESERVADAS = {
    "programa": "TK_PROGRAMA",
    "inicio": "TK_INICIO",
    "fim": "TK_FIM",
    "repetir": "TK_REPETIR",
    "se": "TK_SE",
    "senao": "TK_SENAO",
    "mover": "TK_MOVER",
    "limpar": "TK_LIMPAR",
    "direita": "TK_DIREITA",
    "esquerda": "TK_ESQUERDA",
    "voltar_base": "TK_VOLTAR_BASE",
    "sujo": "TK_SUJO",
    "obstaculo": "TK_OBSTACULO",
}

Token = namedtuple("Token", ["tipo", "lexema", "linha", "coluna"])


class ErroLexico(Exception):
    """Erro léxico: caractere que não pertence a nenhum token da linguagem."""

    def __init__(self, caractere, linha, coluna):
        self.caractere = caractere
        self.linha = linha
        self.coluna = coluna
        super().__init__(
            f"ERRO léxico: caractere inválido '{caractere}' na linha {linha}, coluna {coluna}"
        )