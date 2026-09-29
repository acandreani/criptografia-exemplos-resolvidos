import itertools
import unittest
from modos import e, d, ecb, cbc, dec_cbc, ctr, preencher, remover


class Modos(unittest.TestCase):
    def test_exemplos(self):
        self.assertEqual(ecb([6]*3), [9]*3)
        self.assertEqual(cbc([6]*3,5), [6,3,8])
        self.assertEqual(ctr([6]*3,2), [13,10,11])

    def test_permutacoes(self):
        for k in range(16):
            self.assertEqual(len({e(x,k) for x in range(16)}),16)
            for x in range(16):
                self.assertEqual(d(e(x,k),k), x)

    def test_inversas_todos_pares(self):
        for par in itertools.product(range(16),repeat=2):
            m = list(par)
            for iv in range(16):
                self.assertEqual(dec_cbc(cbc(m,iv),iv),m)
            for nonce in range(4):
                self.assertEqual(ctr(ctr(m,nonce),nonce),m)

    def test_limites(self):
        self.assertEqual(len(ctr([0]*4,0)),4)
        self.assertEqual(len(ctr([0],0,3)),1)
        for m,n,i in [([0]*5,0,0),([0]*2,0,3),([0],4,0),([0],0,-1),([16],0,0)]:
            with self.assertRaises(ValueError):
                ctr(m,n,i)
        with self.assertRaises(ValueError):
            cbc([0],16)

    def test_reuso_e_alteracao(self):
        p,q,s = 0x41,0x42,0xA6
        c,outro = p ^ s, q ^ s
        self.assertEqual((c,outro),(0xE7,0xE4))
        self.assertEqual(c ^ outro,p ^ q)
        self.assertEqual(p ^ c ^ outro,q)
        self.assertEqual((c ^ 1) ^ s,0x40)

    def test_preenchimento(self):
        for n in range(65):
            m = bytes(range(n))
            saida = preencher(m)
            self.assertEqual(len(saida)%16,0)
            self.assertEqual(remover(saida),m)
        self.assertEqual(preencher(b'A'*20)[-12:],bytes([12])*12)
        self.assertEqual(preencher(b'A'*16)[-16:],bytes([16])*16)
        for dados in [b'',b'A',b'A'*15+b'\x00',b'A'*14+b'\x01\x02']:
            with self.assertRaises(ValueError):
                remover(dados)


if __name__ == '__main__':
    unittest.main()
