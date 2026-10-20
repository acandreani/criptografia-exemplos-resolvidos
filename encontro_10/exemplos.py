"""Seis exemplos resolvidos. Laboratorio local, NAO protocolo de producao."""
import argparse
import secrets
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def pares(n):
    """Exemplo 1: n pessoas, uma chave distinta para cada par nao ordenado."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("Use um inteiro n >= 2")
    return n * (n - 1) // 2


def potencia(base, expoente, modulo):
    """Exemplo 2: quadrados sucessivos; nao adequado a segredos reais."""
    if expoente < 0 or modulo < 2:
        raise ValueError("Expoente nao negativo e modulo >= 2")
    acumulado = 1
    base %= modulo
    passos = []
    while expoente:
        passos.append((expoente, base, acumulado))
        if expoente & 1:
            acumulado = acumulado * base % modulo
        base = base * base % modulo
        expoente //= 2
    return acumulado % modulo, passos


def acordo_brinquedo(a=6, b=15):
    """Exemplo 3: p=23, g=5 sao inseguros. Nao usar com dados reais."""
    p, g = 23, 5
    A, B = pow(g, a, p), pow(g, b, p)
    return A, B, pow(B, a, p), pow(A, b, p)


def ataque_brinquedo():
    """Exemplo 4: mostrar os DOIS segredos conhecidos por Mallory."""
    p, a, b, m = 23, 6, 15, 13
    A, B, _, _ = acordo_brinquedo(a, b)
    M = pow(5, m, p)
    return M, pow(M, a, p), pow(A, m, p), pow(M, b, p), pow(B, m, p)


def limite_oaep(bits=2048, hash_bytes=32):
    """Exemplo 5: k - 2*hLen - 2; entrada e saida em bytes."""
    if bits <= 0 or bits % 8 or hash_bytes <= 0:
        raise ValueError("Use bits positivos multiplos de 8 e hash positivo")
    limite = bits // 8 - 2 * hash_bytes - 2
    if limite < 0:
        raise ValueError("Modulo pequeno demais para esta parametrizacao")
    return limite


def publica(privada):
    return privada.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def derivar(segredo, sal, contexto):
    # Nova instancia por derivacao; contexto nao autentica identidades.
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=sal, info=contexto).derive(segredo)


def acordo_real():
    """Exemplo 6A: acordo funcional, SEM autenticacao da negociacao."""
    a, b = X25519PrivateKey.generate(), X25519PrivateKey.generate()
    sa, sb = a.exchange(b.public_key()), b.exchange(a.public_key())
    sal = secrets.token_bytes(16)
    contexto = b"curso-v1|Alice->Bob|exemplo6"
    ka, kb = derivar(sa, sal, contexto), derivar(sb, sal, contexto)
    # Uma unica cifracao com esta chave nova: nao estender para um canal.
    nonce, aad, mensagem = bytes(12), b"registro-v1", b"nota=8.5"
    pacote = AESGCM(ka).encrypt(nonce, mensagem, aad)
    recuperada = AESGCM(kb).decrypt(nonce, pacote, aad)
    adulterado = bytes([pacote[0] ^ 1]) + pacote[1:]
    try:
        AESGCM(kb).decrypt(nonce, adulterado, aad)
    except InvalidTag:
        rejeitou = True
    else:
        rejeitou = False
    return {
        "publicas_32": len(publica(a)) == len(publica(b)) == 32,
        "segredos_32_iguais": len(sa) == len(sb) == 32 and sa == sb,
        "chaves_iguais": ka == kb,
        "contexto_separa": ka != derivar(sa, sal, contexto + b"-outro"),
        "abertura_correta": recuperada == mensagem,
        "adulteracao_rejeitada": rejeitou,
        "pacote_bytes": len(pacote),
    }


def intermediario():
    """Exemplo 6B: simulacao local de duas conexoes, sem alvo externo."""
    a, b, m = (X25519PrivateKey.generate() for _ in range(3))
    sal = secrets.token_bytes(16)
    contexto = b"curso-v1|Alice->Bob|exemplo6"
    ka = derivar(a.exchange(m.public_key()), sal, contexto)
    kma = derivar(m.exchange(a.public_key()), sal, contexto)
    kb = derivar(b.exchange(m.public_key()), sal, contexto)
    kmb = derivar(m.exchange(b.public_key()), sal, contexto)
    # Uma cifracao por chave nova. Mallory termina as duas conexoes.
    nonce, aad = bytes(12), b"registro-v1"
    envio = AESGCM(ka).encrypt(nonce, b"nota=8.5", aad)
    try:
        AESGCM(kb).decrypt(nonce, envio, aad)
    except InvalidTag:
        bob_rejeita_envio = True
    else:
        bob_rejeita_envio = False
    leu = AESGCM(kma).decrypt(nonce, envio, aad)
    repasse = AESGCM(kmb).encrypt(nonce, leu, aad)
    recebeu = AESGCM(kb).decrypt(nonce, repasse, aad)
    return {"alice_mallory": ka == kma, "bob_mallory": kb == kmb,
            "conexoes_distintas": ka != kb,
            "bob_rejeita_envio_original": bob_rejeita_envio,
            "mallory_leu": leu == b"nota=8.5",
            "bob_recebeu": recebeu == b"nota=8.5"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exemplo", type=int, choices=range(1, 7))
    parser.add_argument("--pessoas", type=int, default=8)
    args = parser.parse_args()
    funcoes = {
        1: lambda: {"pares": pares(args.pessoas)},
        2: lambda: potencia(5, 6, 23),
        3: acordo_brinquedo,
        4: ataque_brinquedo,
        5: limite_oaep,
        6: lambda: (acordo_real(), intermediario()),
    }
    for i in ([args.exemplo] if args.exemplo else range(1, 7)):
        print(f"Exemplo {i}: {funcoes[i]()}")


if __name__ == "__main__":
    main()
