"""Testes dos valores e relações usados nos exemplos do Encontro 6."""

import unittest

from calculos import (
    em_anos,
    probabilidade_colisao,
    tempo_medio,
    tempo_pior_caso,
    tempo_transmissao,
    volume_bytes,
)


class TestCalculos(unittest.TestCase):
    def test_pior_caso_e_caso_medio(self) -> None:
        self.assertEqual(tempo_pior_caso(56, 1e12), 2 * tempo_medio(56, 1e12))

    def test_um_bit_a_mais_dobra_o_tempo(self) -> None:
        self.assertEqual(tempo_medio(57, 1e12), 2 * tempo_medio(56, 1e12))

    def test_paralelismo_perfeito_divide_por_dois(self) -> None:
        self.assertEqual(tempo_medio(56, 1e12, 2), tempo_medio(56, 1e12) / 2)

    def test_razao_128_para_56_bits(self) -> None:
        self.assertEqual(tempo_medio(128, 1e12) / tempo_medio(56, 1e12), 2**72)

    def test_aniversario_em_2_32_blocos(self) -> None:
        probabilidade = probabilidade_colisao(2**32, 64)
        self.assertAlmostEqual(probabilidade, 0.39346934, places=6)

    def test_volume_e_transmissao(self) -> None:
        self.assertEqual(volume_bytes(2**32, 64), 2**35)
        self.assertAlmostEqual(
            tempo_transmissao(2**32, 1e9, 64), 2**35 * 8 / 1e9
        )

    def test_conversao_para_anos(self) -> None:
        self.assertAlmostEqual(em_anos(365.25 * 24 * 60 * 60), 1)

    def test_rejeita_parametros_invalidos(self) -> None:
        with self.assertRaises(ValueError):
            tempo_medio(0, 1e12)
        with self.assertRaises(ValueError):
            volume_bytes(1, 7)


if __name__ == "__main__":
    unittest.main()

