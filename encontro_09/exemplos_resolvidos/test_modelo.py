import unittest
from modelo import cabecalho, nonce, codificar, decodificar, tamanhos, colisao, etiqueta


class Contas(unittest.TestCase):
    def test_registro(self):
        self.assertEqual(cabecalho(), bytes.fromhex('01 00 11 00 00 00 09'))
        self.assertEqual(tamanhos(8), (8, 24, 43))
        self.assertEqual(tamanhos(0), (0, 16, 35))
        with self.assertRaises(ValueError):
            tamanhos(-1)

    def test_serializacao(self):
        self.assertEqual(codificar(b'ab', b'c').hex(), '0261620163')
        self.assertEqual(codificar(b'a', b'bc').hex(), '0161026263')
        for a, b in [(b'ab', b'c'), (b'a', b'bc'), (b'', b''), (b'a'*255, b'b')]:
            self.assertEqual(decodificar(codificar(a,b)), (a,b))
        for entrada in (b'', b'\x02a', b'\x00', b'\x00\x00x'):
            with self.assertRaises(ValueError):
                decodificar(entrada)
        with self.assertRaises(ValueError):
            codificar(b'x'*256, b'')

    def test_nonce(self):
        self.assertEqual(nonce().hex(), '000000070000000000000009')
        self.assertEqual(nonce(contador=10)[-1], 10)
        self.assertEqual(nonce(2**32-1, 2**64-1), b'\xff'*12)
        for p, c in [(-1,0), (2**32,0), (0,-1), (0,2**64)]:
            with self.assertRaises(ValueError):
                nonce(p,c)

    def test_probabilidades(self):
        intensidade, p = colisao(2**32,96)
        self.assertAlmostEqual(intensidade / 2**-33, 1, places=8)
        self.assertAlmostEqual(p / intensidade, 1, places=8)
        self.assertAlmostEqual(colisao(2**16,32)[1], 0.393465, places=6)
        self.assertEqual(colisao(1,96), (0,0))
        self.assertEqual(colisao(17,4)[1], 1)
        self.assertEqual(etiqueta(2**20,32), 2**-12)
        self.assertEqual(etiqueta(2**20,128), 2**-108)
        self.assertEqual(etiqueta(10,1), 1)
        for q,bits in [(-1,32), (1,0), (1,257)]:
            with self.assertRaises(ValueError):
                colisao(q,bits)


if __name__ == '__main__':
    unittest.main()
