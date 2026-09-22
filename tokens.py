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