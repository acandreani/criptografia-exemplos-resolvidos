"""Cálculos reproduzidos nos exemplos resolvidos do Encontro 6.

Este módulo trabalha com modelos de ordem de grandeza. Ele não implementa DES,
3DES ou AES e não deve ser usado para avaliar a segurança de uma implantação
real. Todos os valores de ``bits_seguranca`` são tratados como uma estimativa
do trabalho de um ataque genérico.
"""

from __future__ import annotations

import math

SEGUNDOS_ANO = 365.25 * 24 * 60 * 60


def _validar_pos_int(nome: str, valor: int) -> None:
    if type(valor) is not int or valor <= 0:
        raise ValueError(f"{nome} deve ser um inteiro positivo")


def _validar_positivo(nome: str, valor: float) -> None:
    if valor <= 0:
        raise ValueError(f"{nome} deve ser positivo")


def tentativas_media(bits_seguranca: int) -> int:
    """Aproxima a média por M/2; a média exata sem repetição é (M+1)/2.

    Aqui M = 2**bits_seguranca, com posição uniforme da chave correta.
    Para um nível abstrato de segurança, é apenas um modelo comparativo.
    """

    _validar_pos_int("bits_seguranca", bits_seguranca)
    return 2 ** (bits_seguranca - 1)


def tentativas_pior_caso(bits_seguranca: int) -> int:
    """Retorna o tamanho completo do espaço de busca: ``2**bits``."""

    _validar_pos_int("bits_seguranca", bits_seguranca)
    return 2**bits_seguranca


def tempo_medio(
    bits_seguranca: int,
    testes_por_segundo: float,
    maquinas: int = 1,
) -> float:
    """Estima o tempo médio de busca, supondo divisão perfeita do trabalho."""

    _validar_positivo("testes_por_segundo", testes_por_segundo)
    _validar_pos_int("maquinas", maquinas)
    return tentativas_media(bits_seguranca) / (testes_por_segundo * maquinas)


def tempo_pior_caso(
    bits_seguranca: int,
    testes_por_segundo: float,
    maquinas: int = 1,
) -> float:
    """Estima o tempo do pior caso com as mesmas hipóteses do caso médio."""

    _validar_positivo("testes_por_segundo", testes_por_segundo)
    _validar_pos_int("maquinas", maquinas)
    return tentativas_pior_caso(bits_seguranca) / (
        testes_por_segundo * maquinas
    )


def em_anos(segundos: float) -> float:
    """Converte segundos em anos de 365,25 dias."""

    _validar_positivo("segundos", segundos)
    return segundos / SEGUNDOS_ANO


def probabilidade_colisao(
    amostras: int,
    bits_bloco: int = 64,
) -> float:
    """Aproxima repetições em amostras independentes uniformes com reposição.

    Não calcula a probabilidade de quebra do DES nem de colisão entre entradas
    distintas de uma permutação fixa. math.expm1(x) calcula exp(x)-1 com melhor
    precisão perto de zero; -expm1(-a) equivale a 1-exp(-a).
    """

    _validar_pos_int("amostras", amostras)
    _validar_pos_int("bits_bloco", bits_bloco)
    espaco = 2**bits_bloco
    expoente = -(amostras * (amostras - 1)) / (2 * espaco)
    return -math.expm1(expoente)


def volume_bytes(blocos: int, bits_bloco: int = 64) -> int:
    """Converte uma quantidade de blocos em bytes."""

    _validar_pos_int("blocos", blocos)
    _validar_pos_int("bits_bloco", bits_bloco)
    if bits_bloco % 8:
        raise ValueError("bits_bloco deve ser múltiplo de 8")
    return blocos * (bits_bloco // 8)


def tempo_transmissao(
    blocos: int,
    bits_por_segundo: float,
    bits_bloco: int = 64,
) -> float:
    """Converte o volume de blocos em tempo de transmissão."""

    _validar_positivo("bits_por_segundo", bits_por_segundo)
    return volume_bytes(blocos, bits_bloco) * 8 / bits_por_segundo


def cenarios(
    taxa: float = 1e12,
    maquinas: int = 1,
) -> list[dict[str, float | int | str]]:
    """Monta os três cenários comparados no texto do aluno."""

    return [
        {
            "nome": "DES",
            "bits_seguranca": 56,
            "segundos": tempo_medio(56, taxa, maquinas),
        },
        {
            "nome": "3DES (força estimada)",
            "bits_seguranca": 112,
            "segundos": tempo_medio(112, taxa, maquinas),
        },
        {
            "nome": "AES-128",
            "bits_seguranca": 128,
            "segundos": tempo_medio(128, taxa, maquinas),
        },
    ]
