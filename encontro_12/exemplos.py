"""Sete exemplos resolvidos; somente laboratorio local, sem seguranca operacional.

O grupo p=23,q=11,g=2 e propositalmente minusculo. Nenhum acesso a rede.
O exemplo de biblioteca NAO autentica participantes e NAO implementa protocolo.
"""
import argparse
import secrets
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

P, Q, G = 23, 11, 2


def inteiro(x, minimo, maximo):
    if type(x) is not int or not minimo <= x <= maximo:
        raise ValueError(f'Use inteiro no intervalo [{minimo}, {maximo}]')
    return x


def elementos():
    """Exemplo 1: tabela de expoentes 0..11, inclusive retorno a identidade."""
    return [(i, pow(G, i, P)) for i in range(Q + 1)]


def validar_publica(y):
    """Somente para o grupo FIXO conhecido (23,11,2), nao valida grupos gerais."""
    return type(y) is int and 2 <= y <= P - 2 and pow(y, Q, P) == 1


def publica(a):
    return pow(G, inteiro(a, 1, Q - 1), P)


def compartilhado(y, a):
    inteiro(a, 1, Q - 1)
    if not validar_publica(y):
        raise ValueError('Valor publico fora do subgrupo nao trivial')
    return pow(y, a, P)


def acordo(a=4, b=3):
    """Exemplo 2: A=16,B=8,s=2. As privadas sao entradas DIDATICAS."""
    A, B = publica(a), publica(b)
    return {'A': A, 'B': B, 's_alice': compartilhado(B, a),
            's_bob': compartilhado(A, b)}


def intermediario(a=4, b=3, u=2, v=5):
    """Exemplo 3: duas conexoes locais; publicas falsas ainda passam validacao."""
    A, B, U, V = (publica(x) for x in (a, b, u, v))
    return {'U_para_alice': U, 'V_para_bob': V,
            's_alice': compartilhado(U, a), 's_mallory_alice': compartilhado(A, u),
            's_bob': compartilhado(V, b), 's_mallory_bob': compartilhado(B, v)}


def cifrar(m=6, k=4, y=8):
    """Exemplo 4: ElGamal elementar. k explicito serve SO a reproducao das contas."""
    inteiro(m, 1, P - 1)
    if pow(m, Q, P) != 1:
        raise ValueError('Mensagem deve ser elemento do grupo, inclusive 1')
    s = compartilhado(y, k)
    return publica(k), m * s % P


def decifrar(c1, c2, x=3):
    inteiro(c2, 1, P - 1)
    if pow(c2, Q, P) != 1:
        raise ValueError('Segundo componente fora do grupo')
    s = compartilhado(c1, x)
    return c2 * pow(s, -1, P) % P


def elgamal(m=6, k=4):
    c1, c2 = cifrar(m, k)
    s = pow(8, k, P)
    return {'y': 8, 'c1': c1, 's': s, 'c2': c2,
            'inverso_s': pow(s, -1, P), 'recuperada': decifrar(c1, c2)}


def falhas():
    """Exemplo 5: reuso e maleabilidade, ambos com valores validos no grupo."""
    c1, c2 = cifrar(6, 4)
    _, d2 = cifrar(9, 4)
    razao = d2 * pow(c2, -1, P) % P
    alterado = c2 * 4 % P
    return {'c1_repetido': c1, 'c2': c2, 'd2': d2, 'razao': razao,
            'm2_recuperada': 6 * razao % P, 'c2_alterado': alterado,
            'decifracao_alterada': decifrar(c1, alterado)}


def validacao():
    """Exemplo 6: o calculo inseguro aparece separado da funcao que rejeita."""
    return {'aceitos': [y for y in range(P) if validar_publica(y)],
            'cinco_elevado_q': pow(5, Q, P),
            'segredos_com_22': [pow(22, a, P) for a in range(1, 5)],
            'segredos_com_1': [pow(1, a, P) for a in range(1, 5)]}


def serializar(campos):
    """Comprimento de 4 bytes antes de cada campo evita concatenacao ambigua."""
    return b''.join(len(c).to_bytes(4, 'big') + c for c in campos)


def publica_bytes(privada):
    return privada.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def derivar(segredo, sal, info):
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=sal, info=info).derive(segredo)


def biblioteca():
    """Exemplo 7: publicas, HKDF e uma unica mensagem AES-GCM; sem identidade."""
    a, b = X25519PrivateKey.generate(), X25519PrivateKey.generate()
    sa, sb = a.exchange(b.public_key()), b.exchange(a.public_key())
    contexto = serializar([b'curso12-v1', b'Alice', b'Bob',
                          publica_bytes(a), publica_bytes(b)])
    sal = secrets.token_bytes(16)
    info = serializar([contexto, b'Alice->Bob'])
    ka, kb = derivar(sa, sal, info), derivar(sb, sal, info)
    reversa = derivar(sa, sal, serializar([contexto, b'Bob->Alice']))
    nonce, aad, msg = secrets.token_bytes(12), b'tipo=nota;seq=1', b'nota=8.5'
    cifra = AESGCM(ka).encrypt(nonce, msg, aad)
    recuperada = AESGCM(kb).decrypt(nonce, cifra, aad)
    adulterada = bytes([cifra[0] ^ 1]) + cifra[1:]
    rejeicoes = []
    for texto, dados in [(adulterada, aad), (cifra, b'tipo=nota;seq=2')]:
        try:
            AESGCM(kb).decrypt(nonce, texto, dados)
        except InvalidTag:
            rejeicoes.append(True)
        else:
            rejeicoes.append(False)
    try:
        a.exchange(X25519PublicKey.from_public_bytes(bytes(32)))
    except ValueError:
        rejeitou_nula = True
    else:
        rejeitou_nula = False
    # Nao imprimir privadas, segredo compartilhado nem chaves derivadas.
    return {'segredos_iguais': sa == sb, 'segredo_bytes': len(sa),
            'chaves_iguais': ka == kb, 'chave_bytes': len(ka),
            'direcoes_separadas': ka != reversa, 'abertura_correta': recuperada == msg,
            'adulteracao_rejeitada': rejeicoes[0], 'aad_errado_rejeitado': rejeicoes[1],
            'publica_nula_rejeitada': rejeitou_nula, 'cifra_bytes': len(cifra)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exemplo', type=int, choices=range(1, 8))
    parser.add_argument('--a', type=int, default=4)
    parser.add_argument('--b', type=int, default=3)
    parser.add_argument('--mensagem', type=int, default=6)
    parser.add_argument('--k', type=int, default=4)
    args = parser.parse_args()
    funcoes = {1: elementos, 2: lambda: acordo(args.a, args.b),
               3: intermediario, 4: lambda: elgamal(args.mensagem, args.k),
               5: falhas, 6: validacao, 7: biblioteca}
    for i in ([args.exemplo] if args.exemplo else range(1, 8)):
        print(f'Exemplo {i}: {funcoes[i]()}')


if __name__ == '__main__':
    main()
