import unittest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from modelo import cabecalho, nonce
from exemplo_aead import alterar, receber


class Autenticacao(unittest.TestCase):
    def setUp(self):
        self.aes = AESGCM(AESGCM.generate_key(bit_length=128))
        self.n, self.a = nonce(), cabecalho()
        self.c = self.aes.encrypt(self.n, b'nota=8.5', self.a)
        self.aceitas = set()

    def test_recuperacao(self):
        self.assertEqual(len(self.c), 24)
        self.assertEqual(receber(self.aes,self.n,self.c,self.a,17,self.aceitas), b'nota=8.5')

    def test_adulteracoes(self):
        for n,c,a in [(self.n,alterar(self.c,0),self.a),
                      (self.n,alterar(self.c,-1),self.a),
                      (alterar(self.n,0),self.c,self.a),
                      (self.n,self.c,alterar(self.a,2))]:
            with self.assertRaises(InvalidTag):
                receber(self.aes,n,c,a,17,self.aceitas)
            self.assertFalse(self.aceitas)
        outra = AESGCM(AESGCM.generate_key(bit_length=128))
        with self.assertRaises(InvalidTag):
            outra.decrypt(self.n,self.c,self.a)

    def test_contexto(self):
        with self.assertRaisesRegex(ValueError, 'contexto'):
            receber(self.aes,self.n,self.c,self.a,18,self.aceitas)
        self.assertFalse(self.aceitas)
        self.assertEqual(receber(self.aes,self.n,self.c,self.a,17,self.aceitas), b'nota=8.5')

    def test_repeticao_e_proxima(self):
        receber(self.aes,self.n,self.c,self.a,17,self.aceitas)
        self.assertEqual(self.aes.decrypt(self.n,self.c,self.a), b'nota=8.5')
        with self.assertRaisesRegex(ValueError, 'repetição'):
            receber(self.aes,self.n,self.c,self.a,17,self.aceitas)
        n, a = nonce(contador=10), cabecalho(sequencia=10)
        c = self.aes.encrypt(n, b'nota=9.0', a)  # Nova cifração, novo nonce.
        self.assertEqual(receber(self.aes,n,c,a,17,self.aceitas), b'nota=9.0')

    def test_formato(self):
        with self.assertRaisesRegex(ValueError, 'formato'):
            receber(self.aes,self.n,self.c,b'',17,self.aceitas)
        self.assertFalse(self.aceitas)


if __name__ == '__main__':
    unittest.main()
