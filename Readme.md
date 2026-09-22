# Compilador 1 — INF0033 (UFG)

Repositório com os trabalhos práticos da disciplina **Compilador 1**, do curso de Engenharia da Computação da UFG (Instituto de Informática), sob orientação do professor **Rubens de Castro Pereira**.

**Equipe:** Ana Beatriz Borges Cordeiro e Giordanna Santos

## Sobre a disciplina

Os trabalhos são sequenciais: cada um constrói uma fase de um compilador para uma **linguagem simplificada de controle de um robô de limpeza**, criada especificamente para a disciplina. A ideia é que cada fase reaproveite a anterior — o analisador léxico do T2 alimenta a análise sintática do T3, e assim por diante.

## Trabalhos

| Trabalho | Descrição | Status |
|---|---|---|
| **T1** — Especificação Léxica | Definição dos 18 tokens + `TK_EOF` da linguagem do robô, incluindo a extensão de detecção e desvio de obstáculos | ✅ Concluído |
| **T2** — Analisador Léxico | Implementação do lexer como máquina de estados (autômato), em Python | ✅ Concluído |
| **T3** — Análise Sintática | *(a definir pelo professor)* | 🔜 Planejado |
| T4+ | *(a definir)* | 🔜 Planejado |

> À medida que novos trabalhos forem entregues, adicione uma linha na tabela acima e uma seção correspondente abaixo.

## A linguagem do robô

DSL (linguagem de domínio específico) imperativa: comandos de movimento (`mover`, `direita`, `esquerda`, `voltar_base`), limpeza (`limpar`), sensores (`sujo`, `obstaculo`), estruturas de controle (`repetir`, `se`/`senao`) e blocos delimitados por `{ }`. Exemplo:

```
programa rotina_limpeza
inicio
    repetir 2 {
        mover;
        se sujo { limpar; }
        se obstaculo { esquerda; } senao { direita; }
    }
    voltar_base;
fim
```

## T2 — Analisador Léxico

### Estrutura

```
tokens.py   -> especificação léxica (palavras reservadas, Token, ErroLexico)
lexer.py    -> o autômato de estados (classe Lexer)
main.py     -> ponto de entrada (interativo, arquivo ou exemplos fixos)
```

### Como rodar

Requisito: Python 3.x

```bash
python main.py                 # modo interativo: digite o código no terminal
python main.py arquivo.txt     # roda o lexer sobre um arquivo
python main.py --demo          # roda os exemplos de demonstração embutidos
```

### Saída esperada

Uma tabela com `LINHA`, `COLUNA`, `LEXEMA` e `TOKEN` para cada elemento reconhecido, seguida da lista de erros léxicos encontrados (caractere, linha e coluna) — ou a confirmação de que nenhum erro foi encontrado.

