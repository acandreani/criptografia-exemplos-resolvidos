"""Testes da implementação de referência."""

import unittest

from feistel import (
    cifrar,
    decifrar,
    desfazer_rodada,
    distancia_hamming,
    medir_avalanche,
    rodada,
    separar_bloco,
    trilha_cifragem,
)


class TestFeistel(unittest.TestCase):
    def test_exemplo_de_duas_rodadas(self) -> None:
        self.assertEqual(cifrar(0b00100101, [3, 2], bits_metade=4), 0b10101001)

    def test_decifra_exemplo_de_duas_rodadas(self) -> None:
        self.assertEqual(decifrar(0b10101001, [3, 2], bits_metade=4), 0b00100101)

    def test_rodada_e_inversao(self) -> None:
        saida = rodada(0xA5, 0x6C, 0x31)
        self.assertEqual(desfazer_rodada(*saida, 0x31), (0xA5, 0x6C))

    def test_ida_e_volta_com_entradas_variadas(self) -> None:
        subchaves = [3, 17, 91, 201]
        for bloco in [0x0000, 0x0001, 0x1234, 0x8000, 0xFFFF]:
            with self.subTest(bloco=hex(bloco)):
                self.assertEqual(decifrar(cifrar(bloco, subchaves), subchaves), bloco)

    def test_saida_permanece_em_16_bits(self) -> None:
        for bloco in range(0, 1 << 16, 997):
            self.assertLessEqual(cifrar(bloco, [3, 17, 91, 201]), 0xFFFF)

    def test_trilha_tem_uma_entrada_por_rodada(self) -> None:
        trilha = trilha_cifragem(0x1234, [3, 17, 91, 201])
        self.assertEqual([etapa["rodada"] for etapa in trilha], [1, 2, 3, 4])

    def test_distancia_do_exemplo_de_avalanche(self) -> None:
        self.assertEqual(distancia_hamming(0b01101101, 0b11000110), 5)

    def test_medida_de_avalanche_fica_no_intervalo(self) -> None:
        resultado = medir_avalanche(0x1234, [3, 17, 91, 201], 0)
        self.assertGreaterEqual(resultado["bits_diferentes"], 0)
        self.assertLessEqual(resultado["bits_diferentes"], 16)
        self.assertGreaterEqual(resultado["percentual"], 0)
        self.assertLessEqual(resultado["percentual"], 100)

    def test_rejeita_bloco_fora_do_intervalo(self) -> None:
        for bloco in [-1, 1 << 16]:
            with self.subTest(bloco=bloco), self.assertRaises(ValueError):
                separar_bloco(bloco)

    def test_rejeita_lista_vazia_de_subchaves(self) -> None:
        with self.assertRaises(ValueError):
            cifrar(0x1234, [])


if __name__ == "__main__":
    unittest.main()

