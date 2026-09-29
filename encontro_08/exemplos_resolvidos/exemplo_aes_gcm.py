"""Exemplo 6: operação autenticada de biblioteca, não um protocolo completo.

secrets: biblioteca padrão; token_bytes(n): n bytes aleatórios.
cryptography: pacote externo; AESGCM: interface AES-GCM.
generate_key: gera chave; encrypt: cifra e anexa etiqueta; decrypt: verifica.
InvalidTag: exceção de falha de autenticação; try/except trata essa falha.
bytes([n]): byte de valor n; ^: XOR; fatias [:1] e [1:]: partes dos dados.
"""
import secrets
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    print("ENUNCIADO: proteja nota=10.0, autentique turma=8 e rejeite alteração.")
    # Chave nova em cada execução; não imprima nem salve a chave no exemplo.
    chave = AESGCM.generate_key(bit_length=128)
    nonce = secrets.token_bytes(12)
    aes = AESGCM(chave)
    mensagem, aad = b"nota=10.0", b"turma=8"
    # Uma única cifração com esta chave e nonce. Os testes abaixo só decifram.
    pacote = aes.encrypt(nonce, mensagem, aad)
    print("1. Chave de 128 bits e nonce de 12 bytes gerados para esta execução.")
    print(f"2. {len(mensagem)} bytes cifrados + 16 de etiqueta = {len(pacote)} bytes.")
    print(f"   Com nonce separado: {len(pacote) + len(nonce)} bytes, sem AAD e cabeçalhos.")
    recuperado = aes.decrypt(nonce, pacote, aad)
    assert recuperado == mensagem
    print("3. Mensagem autenticada:", recuperado.decode("ascii"))
    alterado = bytes([pacote[0] ^ 1]) + pacote[1:]
    for nome, dados, associados in [("byte cifrado alterado",alterado,aad),
                                   ("dados associados alterados",pacote,b"turma=9")]:
        try:
            aes.decrypt(nonce, dados, associados)
        except InvalidTag:
            print("4. Rejeição confirmada:", nome)
        else:
            raise AssertionError("A verificação deveria falhar")
    print("Nonce aleatório requer política de colisões se a chave for reutilizada.")
    print("Este exemplo não gerencia armazenamento, renovação de chaves ou repetição de mensagens.")


if __name__ == "__main__":
    main()
