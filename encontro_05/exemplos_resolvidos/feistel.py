"""Rede de Feistel didática usada no Encontro 5.

A função de rodada é deliberadamente simples: F(R, K) = (R + K) mod 2^n.
Ela torna as contas fáceis de acompanhar, mas não produz uma cifra segura.
"""

from __future__ import annotations

from collections.abc import Iterable


def _mascara(bits_metade: int) -> int:
    if type(bits_metade) is not int or not 1 <= bits_metade <= 16:
        raise ValueError("bits_metade deve ser um inteiro entre 1 e 16")
    return (1 << bits_metade) - 1


def _validar_valor(nome: str, valor: int, mascara: int) -> None:
    if type(valor) is not int or not 0 <= valor <= mascara:
        raise ValueError(f"{nome} deve estar entre 0 e {mascara}")


def _normalizar_subchaves(
    subchaves: Iterable[int], bits_metade: int
) -> tuple[int, ...]:
    mascara = _mascara(bits_metade)
    resultado = tuple(subchaves)
    if not resultado:
        raise ValueError("informe ao menos uma subchave")
    for indice, subchave in enumerate(resultado, start=1):
        _validar_valor(f"subchave {indice}", subchave, mascara)
    return resultado


def funcao_rodada(metade: int, subchave: int, bits_metade: int = 8) -> int:
    """Calcula F(R, K) = (R + K) mod 2^bits_metade."""

    mascara = _mascara(bits_metade)
    _validar_valor("metade", metade, mascara)
    _validar_valor("subchave", subchave, mascara)
    return (metade + subchave) & mascara


def rodada(
    esquerda: int, direita: int, subchave: int, bits_metade: int = 8
) -> tuple[int, int]:
    """Aplica (L, R) -> (R, L XOR F(R, K))."""

    mascara = _mascara(bits_metade)
    _validar_valor("esquerda", esquerda, mascara)
    _validar_valor("direita", direita, mascara)
    valor_f = funcao_rodada(direita, subchave, bits_metade)
    return direita, esquerda ^ valor_f


def desfazer_rodada(
    esquerda_saida: int,
    direita_saida: int,
    subchave: int,
    bits_metade: int = 8,
) -> tuple[int, int]:
    """Recupera (L, R) a partir de (L', R') sem calcular F inversa."""

    mascara = _mascara(bits_metade)
    _validar_valor("esquerda de saída", esquerda_saida, mascara)
    _validar_valor("direita de saída", direita_saida, mascara)
    direita = esquerda_saida
    esquerda = direita_saida ^ funcao_rodada(
        esquerda_saida, subchave, bits_metade
    )
    return esquerda, direita


def separar_bloco(bloco: int, bits_metade: int = 8) -> tuple[int, int]:
    """Separa um bloco de 2n bits em duas metades de n bits."""

    mascara = _mascara(bits_metade)
    _validar_valor("bloco", bloco, (1 << (2 * bits_metade)) - 1)
    return (bloco >> bits_metade) & mascara, bloco & mascara


def recompor_bloco(
    esquerda: int, direita: int, bits_metade: int = 8
) -> int:
    """Recompõe um bloco a partir das metades esquerda e direita."""

    mascara = _mascara(bits_metade)
    _validar_valor("esquerda", esquerda, mascara)
    _validar_valor("direita", direita, mascara)
    return (esquerda << bits_metade) | direita


def trilha_cifragem(
    bloco: int, subchaves: Iterable[int], bits_metade: int = 8
) -> list[dict[str, int]]:
    """Devolve os valores de entrada, F e saída de cada rodada."""

    chaves = _normalizar_subchaves(subchaves, bits_metade)
    esquerda, direita = separar_bloco(bloco, bits_metade)
    trilha: list[dict[str, int]] = []
    for numero, subchave in enumerate(chaves, start=1):
        valor_f = funcao_rodada(direita, subchave, bits_metade)
        nova_esquerda, nova_direita = rodada(
            esquerda, direita, subchave, bits_metade
        )
        trilha.append(
            {
                "rodada": numero,
                "subchave": subchave,
                "esquerda_entrada": esquerda,
                "direita_entrada": direita,
                "valor_f": valor_f,
                "esquerda_saida": nova_esquerda,
                "direita_saida": nova_direita,
            }
        )
        esquerda, direita = nova_esquerda, nova_direita
    return trilha


def cifrar(bloco: int, subchaves: Iterable[int], bits_metade: int = 8) -> int:
    """Aplica todas as rodadas na ordem informada."""

    chaves = _normalizar_subchaves(subchaves, bits_metade)
    esquerda, direita = separar_bloco(bloco, bits_metade)
    for subchave in chaves:
        esquerda, direita = rodada(esquerda, direita, subchave, bits_metade)
    return recompor_bloco(esquerda, direita, bits_metade)


def decifrar(bloco: int, subchaves: Iterable[int], bits_metade: int = 8) -> int:
    """Desfaz as rodadas usando as subchaves em ordem inversa."""

    chaves = _normalizar_subchaves(subchaves, bits_metade)
    esquerda, direita = separar_bloco(bloco, bits_metade)
    for subchave in reversed(chaves):
        esquerda, direita = desfazer_rodada(
            esquerda, direita, subchave, bits_metade
        )
    return recompor_bloco(esquerda, direita, bits_metade)


def distancia_hamming(primeiro: int, segundo: int) -> int:
    """Conta as posições binárias diferentes entre dois inteiros não negativos."""

    if type(primeiro) is not int or type(segundo) is not int:
        raise TypeError("os valores devem ser inteiros")
    if primeiro < 0 or segundo < 0:
        raise ValueError("os valores não podem ser negativos")
    return (primeiro ^ segundo).bit_count()


def medir_avalanche(
    bloco: int,
    subchaves: Iterable[int],
    bit_invertido: int,
    bits_metade: int = 8,
) -> dict[str, int | float]:
    """Cifra duas entradas vizinhas e mede a diferença entre as saídas."""

    total_bits = 2 * bits_metade
    if type(bit_invertido) is not int or not 0 <= bit_invertido < total_bits:
        raise ValueError(f"bit_invertido deve estar entre 0 e {total_bits - 1}")
    chaves = _normalizar_subchaves(subchaves, bits_metade)
    separar_bloco(bloco, bits_metade)
    bloco_alterado = bloco ^ (1 << bit_invertido)
    saida = cifrar(bloco, chaves, bits_metade)
    saida_alterada = cifrar(bloco_alterado, chaves, bits_metade)
    diferentes = distancia_hamming(saida, saida_alterada)
    return {
        "bloco": bloco,
        "bloco_alterado": bloco_alterado,
        "saida": saida,
        "saida_alterada": saida_alterada,
        "bits_diferentes": diferentes,
        "percentual": 100 * diferentes / total_bits,
    }

