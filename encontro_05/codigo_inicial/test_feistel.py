"""Testes do código inicial; eles passam à medida que os TODOs são resolvidos."""

import unittest

from feistel import (
    cifrar,
    decifrar,
    desfazer_rodada,
    distancia_hamming,
    rodada,
    separar_bloco,
)


class TestFeistel(unittest.TestCase):
    def test_separa_bloco(self) -> None:
        self.assertEqual(separar_bloco(0x1234), (0x12, 0x34))

    def test_rodada_e_inversao(self) -> None:
        saida = rodada(0xA5, 0x6C, 0x31)
        self.assertEqual(desfazer_rodada(*saida, 0x31), (0xA5, 0x6C))

    def test_exemplo_de_duas_rodadas(self) -> None:
        self.assertEqual(cifrar(0b00100101, [3, 2], bits_metade=4), 0b10101001)

    def test_ida_e_volta_com_entradas_variadas(self) -> None:
        subchaves = [3, 17, 91, 201]
        for bloco in [0x0000, 0x0001, 0x1234, 0x8000, 0xFFFF]:
            with self.subTest(bloco=hex(bloco)):
                self.assertEqual(decifrar(cifrar(bloco, subchaves), subchaves), bloco)

    def test_distancia_do_exemplo_de_avalanche(self) -> None:
        self.assertEqual(distancia_hamming(0b01101101, 0b11000110), 5)


if __name__ == "__main__":
    unittest.main()

