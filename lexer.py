"""
Autômato de estados do analisador léxico.

Estados:
  S0 - estado inicial (decide para onde ir a partir do próximo caractere)
  S1 - lendo um identificador ou palavra reservada
  S2 - lendo um número
  S3 - viu '/', aguardando confirmar se é início de comentário ('//')
  S4 - dentro de um comentário de linha (ignorado até a quebra de linha)

Convenção de comentários adotada: "// até o fim da linha".
"""

from tokens import PALAVRAS_RESERVADAS, Token, ErroLexico


# ---------------------------------------------------------------------------
# Funções auxiliares (classes de caracteres, iguais às classes usadas
# nas expressões regulares da especificação: [a-zA-Z], [0-9], etc.)
# ---------------------------------------------------------------------------

def eh_letra(c):
    return c is not None and (("a" <= c <= "z") or ("A" <= c <= "Z"))


def eh_digito(c):
    return c is not None and ("0" <= c <= "9")


def eh_letra_digito_ou_underscore(c):
    return eh_letra(c) or eh_digito(c) or c == "_"


def eh_espaco_ou_tab(c):
    return c == " " or c == "\t"


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

class Lexer:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def peek(self):
        """Olha o caractere atual sem consumi-lo. None se chegou ao fim."""
        if self.pos >= len(self.codigo):
            return None
        return self.codigo[self.pos]

    def avancar(self):
        """Consome o caractere atual e atualiza linha/coluna."""
        c = self.codigo[self.pos]
        self.pos += 1
        if c == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return c

    def proximo_token(self):
        """
        Executa o autômato a partir de S0 até reconhecer um único token
        (ou levantar ErroLexico).
        """
        estado = "S0"
        lexema = ""
        linha_ini, coluna_ini = self.linha, self.coluna

        while True:
            c = self.peek()

            # ---------------- S0: estado inicial ----------------
            if estado == "S0":
                linha_ini, coluna_ini = self.linha, self.coluna

                if c is None:
                    return Token("TK_EOF", "", linha_ini, coluna_ini)

                elif eh_espaco_ou_tab(c) or c == "\n":
                    self.avancar()
                    continue

                elif eh_letra(c):
                    lexema += self.avancar()
                    estado = "S1"

                elif eh_digito(c):
                    lexema += self.avancar()
                    estado = "S2"

                elif c == "{":
                    self.avancar()
                    return Token("TK_ABRE_CHAVE", c, linha_ini, coluna_ini)

                elif c == "}":
                    self.avancar()
                    return Token("TK_FECHA_CHAVE", c, linha_ini, coluna_ini)

                elif c == ";":
                    self.avancar()
                    return Token("TK_PONTO_VIRGULA", c, linha_ini, coluna_ini)

                elif c == "/":
                    self.avancar()
                    estado = "S3"

                else:
                    self.avancar()
                    raise ErroLexico(c, linha_ini, coluna_ini)

            # ---------------- S1: identificador / palavra reservada ----------------
            elif estado == "S1":
                if eh_letra_digito_ou_underscore(c):
                    lexema += self.avancar()
                else:
                    tipo = PALAVRAS_RESERVADAS.get(lexema, "TK_ID")
                    return Token(tipo, lexema, linha_ini, coluna_ini)

            # ---------------- S2: número ----------------
            elif estado == "S2":
                if eh_digito(c):
                    lexema += self.avancar()
                else:
                    return Token("TK_NUM", lexema, linha_ini, coluna_ini)

            # ---------------- S3: viu '/', confirma comentário ----------------
            elif estado == "S3":
                if c == "/":
                    self.avancar()
                    estado = "S4"
                else:
                    # '/' isolado não é um lexema válido na linguagem
                    raise ErroLexico("/", linha_ini, coluna_ini)

            # ---------------- S4: dentro de comentário de linha ----------------
            elif estado == "S4":
                if c is None:
                    return Token("TK_EOF", "", self.linha, self.coluna)
                elif c == "\n":
                    self.avancar()
                    estado = "S0"
                    lexema = ""
                else:
                    self.avancar()

    def tokenizar(self):
        """
        Roda o lexer até o fim do código-fonte.
        Retorna (tokens, erros). Em caso de erro, o autômato se recupera
        reiniciando em S0 a partir do próximo caractere, permitindo
        reportar mais de um erro na mesma execução.
        """
        tokens = []
        erros = []

        while True:
            try:
                tok = self.proximo_token()
            except ErroLexico as e:
                erros.append(e)
                continue

            tokens.append(tok)
            if tok.tipo == "TK_EOF":
                break

        return tokens, erros