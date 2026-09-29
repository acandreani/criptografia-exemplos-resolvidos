"""Execute separadamente: requer cryptography, sem pular testes silenciosamente."""
import unittest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Autenticacao(unittest.TestCase):
    def test_recuperacao_tamanho_adulteracao(self):
        # Valores fixos só para este teste: nunca reutilize esta chave em dados reais.
        chave,nonce = bytes(16),bytes(12)
        aes = AESGCM(chave)
        mensagem,aad = b"nota=10.0",b"turma=8"
        c = aes.encrypt(nonce,mensagem,aad)
        self.assertEqual(len(c),25)
        self.assertEqual(aes.decrypt(nonce,c,aad),mensagem)
        casos = [(bytes([c[0]^1])+c[1:],aad,nonce),
                 (c[:-1]+bytes([c[-1]^1]),aad,nonce),
                 (c,b"turma=9",nonce),
                 (c,aad,bytes([1])+nonce[1:])]
        for dados,associados,n in casos:
            with self.assertRaises(InvalidTag):
                aes.decrypt(n,dados,associados)


if __name__ == '__main__':
    unittest.main()
