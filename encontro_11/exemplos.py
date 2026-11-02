"""Seis resolucoes de RSA. Inteiros pequenos sao inseguros; uso local didatico."""
import argparse
import math
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def euclides(a, b):
    """MDC e coeficientes x,y com a*x+b*y=MDC; guarda as divisoes."""
    r0, r1, x0, x1, y0, y1 = a, b, 1, 0, 0, 1
    passos = []
    while r1:
        q, resto = divmod(r0, r1)
        passos.append((r0, q, r1, resto))
        r0, r1 = r1, resto
        x0, x1 = x1, x0 - q*x1
        y0, y1 = y1, y0 - q*y1
    return r0, x0, y0, passos


def chave_pequena():
    """Exemplo 1: p=5,q=11,e=3. Obter n,phi,d e identidade de Bezout."""
    g, x, y, passos = euclides(3, 40)
    return dict(n=55, phi=40, e=3, d=x % 40, mdc=g,
                bezout=(x, y), divisoes=passos)


def potencia(base, expoente, modulo):
    """Exemplo 2: quadrados sucessivos. Nao e implementacao de tempo constante."""
    if expoente < 0 or modulo < 2:
        raise ValueError("Expoente >= 0, modulo >= 2")
    resultado, passos = 1, []
    base %= modulo
    while expoente:
        passos.append((expoente, base, resultado))
        if expoente & 1:
            resultado = resultado*base % modulo
        base = base*base % modulo
        expoente //= 2
    return resultado, passos


def rsa_bruto(m, expoente, n):
    if not isinstance(m, int) or isinstance(m, bool) or not 0 <= m < n:
        raise ValueError("Representante inteiro deve estar em 0 <= m < n")
    return pow(m, expoente, n)


def ida_volta(m=7):
    """Exemplo 2: cifrar e decifrar com n=55,e=3,d=27."""
    c = rsa_bruto(m, 3, 55)
    recuperada, passos = potencia(c, 27, 55)
    return dict(m=m, c=c, recuperada=recuperada, passos=passos)


def nao_coprimo():
    """Exemplo 3: m=5 nao e coprimo com 55, mas volta corretamente."""
    return ida_volta(5)


def maleabilidade():
    """Exemplo 4: multiplicar c por 2^e altera m para 2*m mod n."""
    c = rsa_bruto(7, 3, 55)
    alterado = c*pow(2, 3, 55) % 55
    return dict(c=c, repetido=rsa_bruto(7, 3, 55), alterado=alterado,
                recuperado=rsa_bruto(alterado, 27, 55))


def primo_compartilhado():
    """Exemplo 5: fatorar 55 e 85 sem conhecer as chaves privadas."""
    p = math.gcd(55, 85)
    return dict(p=p, q1=55//p, q2=85//p, d1=pow(3, -1, 40),
                d2=pow(3, -1, 64))


def oaep():
    return padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None)


def pss():
    return padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)


def esquemas():
    """Exemplo 6: OAEP e PSS separados; limites e verificacoes negativas."""
    privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publica = privada.public_key()
    mensagem = b"pedido=7"
    c1 = publica.encrypt(mensagem, oaep())
    c2 = publica.encrypt(mensagem, oaep())
    limite = 2048//8 - 2*32 - 2
    fronteira = publica.encrypt(b"A"*limite, oaep())
    try:
        publica.encrypt(b"A"*(limite+1), oaep())
    except ValueError:
        excesso_rejeitado = True
    else:
        excesso_rejeitado = False
    # Chave distinta para assinatura: finalidades separadas.
    assinante = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    verificadora = assinante.public_key()
    assinatura = assinante.sign(mensagem, pss(), hashes.SHA256())
    verificadora.verify(assinatura, mensagem, pss(), hashes.SHA256())
    try:
        verificadora.verify(assinatura, b"pedido=8", pss(), hashes.SHA256())
    except InvalidSignature:
        alteracao_rejeitada = True
    else:
        alteracao_rejeitada = False
    try:
        publica.verify(assinatura, mensagem, pss(), hashes.SHA256())
    except InvalidSignature:
        chave_errada_rejeitada = True
    else:
        chave_errada_rejeitada = False
    return dict(limite=limite, cifra_bytes=len(c1),
                recuperou=privada.decrypt(c1, oaep()) == mensagem,
                cifras_distintas=c1 != c2,
                fronteira_recuperada=privada.decrypt(fronteira, oaep()) == b"A"*190,
                excesso_rejeitado=excesso_rejeitado,
                assinatura_valida=True, alteracao_rejeitada=alteracao_rejeitada,
                chave_errada_rejeitada=chave_errada_rejeitada)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exemplo", type=int, choices=range(1, 7))
    parser.add_argument("--mensagem", type=int, default=7)
    args = parser.parse_args()
    funcoes = [chave_pequena, lambda: ida_volta(args.mensagem), nao_coprimo,
               maleabilidade, primo_compartilhado, esquemas]
    for i in ([args.exemplo] if args.exemplo else range(1, 7)):
        print(f"Exemplo {i}: {funcoes[i-1]()}")


if __name__ == "__main__":
    main()
