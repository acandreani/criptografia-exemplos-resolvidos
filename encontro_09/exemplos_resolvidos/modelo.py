"""Formatos e contas dos exemplos 1–5; não implementa criptografia."""
import math


def inteiro(valor, tamanho):
    if type(valor) is not int or not 0 <= valor < 2 ** (8 * tamanho):
        raise ValueError("inteiro fora da faixa do campo")
    return valor.to_bytes(tamanho, "big")


def cabecalho(usuario=17, sequencia=9):
    return b"\x01" + inteiro(usuario, 2) + inteiro(sequencia, 4)


def nonce(prefixo=7, contador=9):
    return inteiro(prefixo, 4) + inteiro(contador, 8)


def codificar(a, b):
    return inteiro(len(a), 1) + a + inteiro(len(b), 1) + b


def decodificar(dados):
    campos = []
    posicao = 0
    for _ in range(2):
        if posicao >= len(dados):
            raise ValueError("comprimento ausente")
        tamanho = dados[posicao]
        posicao += 1
        if posicao + tamanho > len(dados):
            raise ValueError("campo truncado")
        campos.append(dados[posicao:posicao + tamanho])
        posicao += tamanho
    if posicao != len(dados):
        raise ValueError("bytes excedentes")
    return tuple(campos)


def tamanhos(mensagem, aad=7):
    if any(type(x) is not int or x < 0 for x in (mensagem, aad)):
        raise ValueError("comprimentos devem ser inteiros não negativos")
    # Apenas contabilidade para a interface AESGCM com nonce de 12 bytes.
    return mensagem, mensagem + 16, aad + 12 + mensagem + 16


def colisao(q, bits):
    """Retorna lambda e aproximação de aniversário; não é limite GCM."""
    if type(q) is not int or q < 0 or type(bits) is not int or not 1 <= bits <= 256:
        raise ValueError("q >= 0 e 1 <= bits <= 256, inteiros")
    if q > 2 ** bits:
        return float("inf"), 1.0  # Colisão certa: mais amostras que valores.
    intensidade = q * (q - 1) / (2 * 2 ** bits)
    return intensidade, -math.expm1(-intensidade)


def etiqueta(tentativas, bits):
    if (type(tentativas) is not int or tentativas < 0
            or type(bits) is not int or not 1 <= bits <= 256):
        raise ValueError("tentativas >= 0 e 1 <= bits <= 256, inteiros")
    return min(1.0, tentativas / 2 ** bits)
