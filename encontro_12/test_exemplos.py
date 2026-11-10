"""Testes dos exemplos resolvidos; nao sao o gabarito do laboratorio."""
import unittest
from exemplos import (P, Q, elementos, publica, validar_publica, acordo,
                      compartilhado, intermediario, cifrar, decifrar, elgamal,
                      falhas, validacao, serializar, derivar, biblioteca)


class ExemplosTest(unittest.TestCase):
    def test_01_ordem(self):
        self.assertEqual([v for _, v in elementos()], [1,2,4,8,16,9,18,13,3,6,12,1])
        self.assertEqual(len({v for _, v in elementos()[:-1]}), Q)

    def test_02_dh(self):
        self.assertEqual(acordo(), {'A':16,'B':8,'s_alice':2,'s_bob':2})

    def test_03_todos_acordos(self):
        for a in range(1, Q):
            for b in range(1, Q):
                r = acordo(a,b)
                self.assertEqual(r['s_alice'], r['s_bob'])
                self.assertTrue(validar_publica(r['A']))

    def test_04_expoentes_invalidos(self):
        for a in (0,11,-1,True,1.5,'4'):
            with self.assertRaises(ValueError): publica(a)

    def test_05_intermediario(self):
        r = intermediario()
        self.assertEqual((r['U_para_alice'],r['V_para_bob']), (4,9))
        self.assertEqual((r['s_alice'],r['s_mallory_alice']), (3,3))
        self.assertEqual((r['s_bob'],r['s_mallory_bob']), (16,16))

    def test_06_elgamal(self):
        self.assertEqual(elgamal(), {'y':8,'c1':16,'s':2,'c2':12,'inverso_s':12,'recuperada':6})
        self.assertEqual(cifrar(6,5), (9,4))

    def test_07_todas_mensagens(self):
        for _, m in elementos()[:-1]:
            for x in range(1,Q):
                for k in range(1,Q):
                    self.assertEqual(decifrar(*cifrar(m,k,publica(x)),x),m)

    def test_08_entrada_invalida(self):
        for m in (0,5,23,-1,True):
            with self.assertRaises(ValueError): cifrar(m)
        with self.assertRaises(ValueError): decifrar(1,12)
        with self.assertRaises(ValueError): decifrar(16,0)

    def test_09_reuso(self):
        r=falhas()
        self.assertEqual((r['c1_repetido'],r['c2'],r['d2'],r['razao'],r['m2_recuperada']), (16,12,18,13,9))

    def test_10_maleabilidade(self):
        self.assertEqual(falhas()['decifracao_alterada'],1)
        self.assertEqual(falhas()['c2_alterado'],2)

    def test_11_publicas(self):
        self.assertEqual(validacao()['aceitos'],[2,3,4,6,8,9,12,13,16,18])
        for y in (0,1,5,22,23,-1,True,2.0):
            self.assertFalse(validar_publica(y))
            with self.assertRaises(ValueError): compartilhado(y,4)

    def test_12_pequena_ordem(self):
        self.assertEqual(validacao()['segredos_com_22'],[22,1,22,1])
        self.assertEqual(validacao()['segredos_com_1'],[1,1,1,1])

    def test_13_codificacao(self):
        self.assertNotEqual(serializar([b'ab',b'c']),serializar([b'a',b'bc']))

    def test_14_kdf(self):
        s,sal=bytes(range(32)),bytes(16)
        self.assertEqual(derivar(s,sal,b'A'),derivar(s,sal,b'A'))
        self.assertNotEqual(derivar(s,sal,b'A'),derivar(s,sal,b'B'))
        self.assertEqual(len(derivar(s,sal,b'A')),32)

    def test_15_biblioteca(self):
        r=biblioteca()
        self.assertEqual((r.pop('segredo_bytes'),r.pop('chave_bytes'),r.pop('cifra_bytes')), (32,32,24))
        self.assertTrue(all(r.values()),r)


if __name__ == '__main__':
    unittest.main()
