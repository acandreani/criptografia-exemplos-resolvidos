"""Varia entradas das resoluções; todos os argumentos numéricos são hexadecimais."""
import argparse
from modos import ecb, cbc_etapas, cbc, dec_cbc, ctr_etapas, ctr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocos", nargs="*", default=[6,6,6], type=lambda x: int(x,16))
    parser.add_argument("--chave", default=3, type=lambda x: int(x,16))
    parser.add_argument("--iv", default=5, type=lambda x: int(x,16))
    parser.add_argument("--nonce", default=2, type=lambda x: int(x,16))
    parser.add_argument("--inicio", default=0, type=lambda x: int(x,16))
    a = parser.parse_args()
    try:
        resultado = ctr(a.blocos, a.nonce, a.inicio, a.chave)
        print("ECB:", [f"{x:X}" for x in ecb(a.blocos, a.chave)])
        print("CBC (M, anterior, XOR, C):")
        for linha in cbc_etapas(a.blocos,a.iv,a.chave):
            print([f"{x:X}" for x in linha])
        print("CTR (contador, T, fluxo, C):")
        for linha in ctr_etapas(a.blocos,a.nonce,a.inicio,a.chave):
            print([f"{x:X}" for x in linha])
        assert dec_cbc(cbc(a.blocos,a.iv,a.chave),a.iv,a.chave) == a.blocos
        assert ctr(resultado,a.nonce,a.inicio,a.chave) == a.blocos
        print("As duas recuperações conferem.")
    except ValueError as erro:
        parser.error(str(erro))


if __name__ == "__main__":
    main()
