import unittest
from aes_operacoes import xtime, gf_mul, estado, shift_rows, mix_column


def referencia(a, b):
    """Produto polinomial direto e divisão longa: algoritmo independente."""
    p = 0
    for i in range(8):
        if b & (1 << i):
            p ^= a << i
    for grau in range(14, 7, -1):
        if p & (1 << grau):
            p ^= 0x11B << (grau - 8)
    return p


class ExemplosAES(unittest.TestCase):
    def test_estado_shift(self):
        s = estado(list(range(16)))
        self.assertEqual(s[0], [0, 4, 8, 12])
        self.assertEqual(shift_rows(s), [[0,4,8,12], [5,9,13,1], [10,14,2,6], [15,3,7,11]])
        self.assertEqual(s[1], [1,5,9,13])

    def test_xor(self):
        self.assertEqual([a ^ b for a,b in zip([0x3A,0x7C,0x10,0xF0], [0x0F,1,0xAA,0x55])], [0x35,0x7D,0xBA,0xA5])

    def test_xtime(self):
        for a, esperado in [(0x57,0xAE), (0xAE,0x47), (0x80,0x1B), (0,0)]:
            self.assertEqual(xtime(a), esperado)

    def test_produto_fips(self):
        self.assertEqual(gf_mul(0x57,0x13), 0xFE)

    def test_coluna_fips(self):
        self.assertEqual(mix_column([0xD4,0xBF,0x5D,0x30]), [4,0x66,0x81,0xE5])

    def test_todos_produtos(self):
        for a in range(256):
            for b in range(256):
                self.assertEqual(gf_mul(a,b), referencia(a,b), (a,b))

    def test_entradas_invalidas(self):
        for a in [-1, 256, 1.5, True]:
            with self.assertRaises(ValueError):
                xtime(a)
        with self.assertRaises(ValueError):
            estado([0]*15)
        with self.assertRaises(ValueError):
            mix_column([0]*3)


if __name__ == "__main__":
    unittest.main()
