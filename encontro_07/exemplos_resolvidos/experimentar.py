"""Variação das entradas dos exemplos resolvidos; use --help."""
import argparse
from aes_operacoes import gf_mul, parcelas, produtos_coluna, mix_column, estado, shift_rows


def hexbyte(texto):
    valor = int(texto, 16)
    if not 0 <= valor <= 255:
        raise argparse.ArgumentTypeError("Use um byte hexadecimal entre 00 e FF")
    return valor


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--a", type=hexbyte, default=0x57)
    p.add_argument("--b", type=hexbyte, default=0x13)
    p.add_argument("--coluna", type=hexbyte, nargs=4, default=[0xD4, 0xBF, 0x5D, 0x30])
    p.add_argument("--bloco", default="000102030405060708090a0b0c0d0e0f", help="16 bytes em hexadecimal")
    args = p.parse_args()
    try:
        s = estado(bytes.fromhex(args.bloco))
    except ValueError as erro:
        p.error(str(erro))
    print("Enunciado: reproduza os exemplos com estas entradas alternativas.")
    print("Resolução — parcelas (índice do bit, valor, selecionada):")
    for i, valor, selecionada in parcelas(args.a, args.b):
        print(i, f"{valor:02X}", selecionada)
    print(f"Produto: {args.a:02X} * {args.b:02X} = {gf_mul(args.a, args.b):02X}")
    print("Produtos das quatro linhas de MixColumns:")
    for linha in produtos_coluna(args.coluna):
        print(" XOR ".join(f"{v:02X}" for v in linha))
    print("Coluna de saída:", " ".join(f"{v:02X}" for v in mix_column(args.coluna)))
    print("Estado antes e depois de ShiftRows:")
    for a, b in zip(s, shift_rows(s)):
        print(" ".join(f"{v:02X}" for v in a), " -> ", " ".join(f"{v:02X}" for v in b))


if __name__ == "__main__":
    main()
