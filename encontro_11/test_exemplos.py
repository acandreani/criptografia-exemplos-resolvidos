import unittest
import exemplos as e


class TestRSA(unittest.TestCase):
    def test_chave(self):
        k = e.chave_pequena()
        self.assertEqual((k['n'], k['phi'], k['d']), (55, 40, 27))

    def test_bezout(self):
        g, x, y, _ = e.euclides(3, 40)
        self.assertEqual(g, 1)
        self.assertEqual(3*x+40*y, 1)

    def test_inverso_inexistente(self):
        with self.assertRaises(ValueError):
            pow(10, -1, 40)

    def test_cifra(self):
        self.assertEqual(e.ida_volta()['c'], 13)

    def test_todos_representantes(self):
        for m in range(55):
            self.assertEqual(e.ida_volta(m)['recuperada'], m)

    def test_nao_coprimo(self):
        self.assertEqual(e.nao_coprimo()['c'], 15)
        self.assertEqual(e.nao_coprimo()['recuperada'], 5)

    def test_limites(self):
        for m in [-1, 55, 56, True, 1.5]:
            with self.assertRaises(ValueError):
                e.rsa_bruto(m, 3, 55)

    def test_potencias(self):
        for base in range(55):
            for expoente in [0, 1, 3, 27]:
                self.assertEqual(e.potencia(base, expoente, 55)[0], pow(base, expoente, 55))

    def test_maleabilidade(self):
        self.assertEqual(e.maleabilidade(), dict(c=13, repetido=13, alterado=49, recuperado=14))

    def test_primo_comum(self):
        self.assertEqual(e.primo_compartilhado(), dict(p=5, q1=11, q2=17, d1=27, d2=43))

    def test_esquemas(self):
        r = e.esquemas()
        self.assertEqual(r.pop('limite'), 190)
        self.assertEqual(r.pop('cifra_bytes'), 256)
        self.assertTrue(all(r.values()), r)

    def test_expoente_invalido(self):
        with self.assertRaises(ValueError):
            e.potencia(2, -1, 55)


if __name__ == '__main__':
    unittest.main()
