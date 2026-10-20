import unittest
from exemplos import (pares, potencia, acordo_brinquedo, ataque_brinquedo,
                      limite_oaep, acordo_real, intermediario, derivar)


class ExemplosTest(unittest.TestCase):
    def test_01_pares(self):
        self.assertEqual(pares(8), 28)
        self.assertEqual(pares(10), 45)

    def test_02_entrada(self):
        for n in (0, 1, -2, 3.5, True):
            with self.assertRaises(ValueError):
                pares(n)

    def test_03_potencia(self):
        self.assertEqual(potencia(5, 6, 23)[0], 8)

    def test_04_varias_potencias(self):
        for base in range(-3, 8):
            for exp in range(20):
                self.assertEqual(potencia(base, exp, 23)[0], pow(base, exp, 23))

    def test_05_acordo(self):
        self.assertEqual(acordo_brinquedo(), (8, 19, 2, 2))

    def test_06_intermediario_manual(self):
        self.assertEqual(ataque_brinquedo(), (21, 18, 18, 7, 7))

    def test_07_oaep(self):
        self.assertEqual(limite_oaep(), 190)

    def test_08_limite_invalido(self):
        with self.assertRaises(ValueError):
            limite_oaep(256)

    def test_09_acordo_real(self):
        r = acordo_real()
        self.assertTrue(all(v for k, v in r.items() if k != "pacote_bytes"))
        self.assertEqual(r["pacote_bytes"], 24)

    def test_10_intermediario_real(self):
        self.assertTrue(all(intermediario().values()))

    def test_11_derivacao_repetivel(self):
        # Entrada fixa e publica apenas para testar a funcao de derivacao.
        self.assertEqual(derivar(bytes(32), b"sal", b"a"),
                         derivar(bytes(32), b"sal", b"a"))

    def test_12_contexto(self):
        self.assertNotEqual(derivar(bytes(32), b"sal", b"a"),
                            derivar(bytes(32), b"sal", b"b"))


if __name__ == "__main__":
    unittest.main()
