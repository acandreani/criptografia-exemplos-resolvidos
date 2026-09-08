"""Código inicial: complete os pontos marcados com TODO.

Use os testes como especificação executável. Esta cifra é apenas didática.
"""

from collections.abc import Iterable


def funcao_rodada(metade: int, subchave: int, bits_metade: int = 8) -> int:
    """Calcule F(R, K) = (R + K) mod 2^bits_metade."""

    # TODO 1
    raise NotImplementedError


def rodada(
    esquerda: int, direita: int, subchave: int, bits_metade: int = 8
) -> tuple[int, int]:
    """Aplique (L, R) -> (R, L XOR F(R, K))."""

    # TODO 2
    raise NotImplementedError


def desfazer_rodada(
    esquerda_saida: int,
    direita_saida: int,
    subchave: int,
    bits_metade: int = 8,
) -> tuple[int, int]:
    """Recupere (L, R) a partir de (L', R')."""

    # TODO 3: não calcule uma função inversa de F.
    raise NotImplementedError


def separar_bloco(bloco: int, bits_metade: int = 8) -> tuple[int, int]:
    """Separe o bloco em duas metades de bits_metade bits."""

    # TODO 4: use deslocamento à direita e uma máscara.
    raise NotImplementedError


def recompor_bloco(
    esquerda: int, direita: int, bits_metade: int = 8
) -> int:
    """Recomponha o bloco a partir das duas metades."""

    # TODO 5: use deslocamento à esquerda e OU bit a bit.
    raise NotImplementedError


def cifrar(bloco: int, subchaves: Iterable[int], bits_metade: int = 8) -> int:
    """Aplique as rodadas na ordem informada."""

    # TODO 6
    raise NotImplementedError


def decifrar(bloco: int, subchaves: Iterable[int], bits_metade: int = 8) -> int:
    """Desfaça as rodadas usando as subchaves em ordem inversa."""

    # TODO 7
    raise NotImplementedError


def distancia_hamming(primeiro: int, segundo: int) -> int:
    """Conte os bits 1 de primeiro XOR segundo."""

    # TODO 8: use o método bit_count de um inteiro.
    raise NotImplementedError

