"""Exemplo 6 resolvido. Estado em memória: NÃO é um protocolo de produção."""
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from modelo import cabecalho, nonce


def alterar(dados, posicao):
    copia = bytearray(dados)
    copia[posicao] ^= 1
    return bytes(copia)


def receber(aes, n, pacote, aad, usuario_esperado, aceitas):
    """O conjunto pertence a UMA chave/sessão. Não é persistente nem concorrente."""
    if len(n) != 12 or len(aad) != 7 or len(pacote) < 16:
        raise ValueError('formato inválido')
    mensagem = aes.decrypt(n, pacote, aad)  # Nada é exibido antes do sucesso.
    usuario = int.from_bytes(aad[1:3], 'big')
    sequencia = int.from_bytes(aad[3:7], 'big')
    if aad[0] != 1 or usuario != usuario_esperado:
        raise ValueError('contexto inesperado')
    # Nesta demonstração, a operação é permitida para o usuário esperado.
    # Uma aplicação real precisa de sua própria política de autorização.
    identidade = (usuario, sequencia)
    if identidade in aceitas:
        raise ValueError('repetição')
    aceitas.add(identidade)
    return mensagem


def main():
    print('EXEMPLO 6 — Enunciado: cifrar nota=8.5, adulterar campos e distinguir replay de falha de etiqueta.')
    aes = AESGCM(AESGCM.generate_key(bit_length=128))
    n, aad, mensagem = nonce(), cabecalho(), b'nota=8.5'
    # Chave nova e apenas UMA cifração por execução: nonce fixo só neste laboratório.
    pacote = aes.encrypt(n, mensagem, aad)
    print('1. C||T:', pacote.hex(' '), '; comprimento:', len(pacote))
    assert aes.decrypt(n, pacote, aad) == mensagem
    print('2. A decifração intacta recupera', mensagem.decode('ascii'))
    casos = [
        ('C', aes, n, alterar(pacote, 0), aad),
        ('T', aes, n, alterar(pacote, -1), aad),
        ('AAD', aes, n, pacote, alterar(aad, 2)),
        ('nonce', aes, alterar(n, 0), pacote, aad),
        ('chave', AESGCM(AESGCM.generate_key(bit_length=128)), n, pacote, aad),
    ]
    for campo, objeto, n_teste, c_teste, a_teste in casos:
        try:
            objeto.decrypt(n_teste, c_teste, a_teste)
        except InvalidTag:
            print('3. Alteração isolada de', campo, '=> InvalidTag; não usar mensagem.')
        else:
            raise AssertionError('alteração aceita')
    aceitas = set()
    try:
        receber(aes, n, pacote, aad, 18, aceitas)
    except ValueError as erro:
        print('4. Usuário esperado 18:', erro, '(etiqueta intacta).')
    else:
        raise AssertionError('contexto incorreto aceito')
    assert receber(aes, n, pacote, aad, 17, aceitas) == mensagem
    assert aes.decrypt(n, pacote, aad) == mensagem
    print('5. A biblioteca ainda abre a cópia intacta; a política registra a primeira aceitação.')
    try:
        receber(aes, n, pacote, aad, 17, aceitas)
    except ValueError as erro:
        print('6. Segunda recepção pela aplicação:', erro)
    else:
        raise AssertionError('repetição aceita')
    print('Interpretação: autenticação, contexto esperado e controle de repetição são verificações distintas.')


if __name__ == '__main__':
    main()
