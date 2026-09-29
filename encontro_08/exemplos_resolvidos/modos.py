"""Modelo de quatro bits, reversível mas inseguro. Não é AES."""


def validar(x, limite=16):
    if type(x) is not int or not 0 <= x < limite:
        raise ValueError(f"Esperado inteiro entre 0 e {limite - 1}")
    return x


def e(x, k=3):
    return (validar(x) + validar(k)) % 16


def d(y, k=3):
    return (validar(y) - validar(k)) % 16


def ecb(blocos, k=3):
    validar(k)
    return [e(m, k) for m in blocos]


def cbc_etapas(blocos, iv, k=3):
    """Retorna tuplas (mensagem, anterior, entrada da cifra, saída)."""
    validar(iv)
    validar(k)
    etapas = []
    anterior = iv
    for m in blocos:
        entrada = validar(m) ^ anterior
        c = e(entrada, k)
        etapas.append((m, anterior, entrada, c))
        anterior = c
    return etapas


def cbc(blocos, iv, k=3):
    return [linha[3] for linha in cbc_etapas(blocos, iv, k)]


def dec_cbc(blocos, iv, k=3):
    validar(iv)
    validar(k)
    saida = []
    anterior = iv
    for c in blocos:
        saida.append(d(c, k) ^ anterior)
        anterior = c
    return saida


def ctr_etapas(blocos, nonce, inicio=0, k=3):
    """Dois bits de nonce e dois de contador. Nunca permite retorno a zero."""
    validar(nonce, 4)
    validar(inicio, 4)
    validar(k)
    if len(blocos) > 4 - inicio:
        raise ValueError("contador esgotado: a entrada da cifra se repetiria")
    etapas = []
    for i, m in enumerate(blocos):
        contador = inicio + i
        t = (nonce << 2) | contador
        fluxo = e(t, k)
        etapas.append((contador, t, fluxo, validar(m) ^ fluxo))
    return etapas


def ctr(blocos, nonce, inicio=0, k=3):
    return [linha[3] for linha in ctr_etapas(blocos, nonce, inicio, k)]


def preencher(dados, tamanho=16):
    """PKCS #7 para demonstrar comprimentos, não autenticação."""
    if type(tamanho) is not int or not 1 <= tamanho <= 255:
        raise ValueError("Tamanho de bloco inválido")
    p = tamanho - len(dados) % tamanho
    return dados + bytes([p]) * p


def remover(dados, tamanho=16):
    if type(tamanho) is not int or not 1 <= tamanho <= 255:
        raise ValueError("Tamanho de bloco inválido")
    if not dados or len(dados) % tamanho:
        raise ValueError("Preenchimento inválido")
    p = dados[-1]
    if not 1 <= p <= tamanho or dados[-p:] != bytes([p]) * p:
        raise ValueError("Preenchimento inválido")
    return dados[:-p]
