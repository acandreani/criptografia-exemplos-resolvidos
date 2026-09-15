"""Operações internas do AES para acompanhar contas; não é uma cifra completa."""


def byte(valor):
    """Rejeita entradas fora do domínio; não trunca silenciosamente."""
    if type(valor) is not int or not 0 <= valor <= 255:
        raise ValueError("Cada byte deve ser um inteiro entre 0 e 255")
    return valor


def xtime(a):
    """Multiplica por 02 no corpo do AES: módulo x^8+x^4+x^3+x+1."""
    byte(a)
    deslocado = a << 1
    return deslocado ^ 0x11B if a & 0x80 else deslocado


def parcelas(a, b):
    """Retorna (bit, potência vezes a, selecionada) para os oito bits de b."""
    byte(a)
    byte(b)
    etapas = []
    for i in range(8):
        etapas.append((i, a, bool(b & (1 << i))))
        a = xtime(a)
    return etapas


def gf_mul(a, b):
    """Soma por XOR as parcelas selecionadas pelos bits do multiplicador."""
    resultado = 0
    for _, parcela, selecionada in parcelas(a, b):
        if selecionada:
            resultado ^= parcela
    return resultado


def estado(bloco):
    """Recebe 16 bytes em ordem de entrada e retorna quatro linhas."""
    if len(bloco) != 16:
        raise ValueError("O estado exige exatamente 16 bytes")
    return [[byte(bloco[4 * c + r]) for c in range(4)] for r in range(4)]


def shift_rows(s):
    """Nova matriz: linha r gira r posições à esquerda, sem alterar s."""
    if len(s) != 4 or any(len(linha) != 4 for linha in s):
        raise ValueError("O estado deve ter quatro linhas de quatro bytes")
    linhas = [[byte(a) for a in linha] for linha in s]
    return [linha[r:] + linha[:r] for r, linha in enumerate(linhas)]


MATRIZ = ((2, 3, 1, 1), (1, 2, 3, 1), (1, 1, 2, 3), (3, 1, 1, 2))


def produtos_coluna(coluna):
    if len(coluna) != 4:
        raise ValueError("MixColumns recebe quatro bytes por coluna")
    return [[gf_mul(k, a) for k, a in zip(linha, coluna)] for linha in MATRIZ]


def mix_column(coluna):
    """Calcula as quatro saídas, preservando a ordem de cima para baixo."""
    return [p[0] ^ p[1] ^ p[2] ^ p[3] for p in produtos_coluna(coluna)]
