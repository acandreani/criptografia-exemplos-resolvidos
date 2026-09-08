"""Permite variar bloco, subchaves, tamanho das metades e bit invertido."""

import argparse

from feistel import cifrar, decifrar, medir_avalanche, trilha_cifragem


def inteiro(texto: str) -> int:
    """Aceita números decimais, 0x... hexadecimal e 0b... binário."""

    try:
        return int(texto, 0)
    except ValueError as erro:
        raise argparse.ArgumentTypeError(f"valor inválido: {texto}") from erro


def formatar(valor: int, total_bits: int) -> str:
    largura_hex = (total_bits + 3) // 4
    return f"0x{valor:0{largura_hex}X} = {valor:0{total_bits}b}"


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Experimenta uma rede de Feistel didática."
    )
    parser.add_argument("--bloco", type=inteiro, default=0x1234)
    parser.add_argument("--subchaves", type=inteiro, nargs="+", default=[3, 17, 91, 201])
    parser.add_argument("--bits-metade", type=int, default=8)
    parser.add_argument("--bit-invertido", type=int, default=0)
    parser.add_argument("--mostrar-rodadas", action="store_true")
    return parser


def main() -> None:
    args = criar_parser().parse_args()
    total_bits = 2 * args.bits_metade
    cifrado = cifrar(args.bloco, args.subchaves, args.bits_metade)
    recuperado = decifrar(cifrado, args.subchaves, args.bits_metade)

    print(f"Entrada:    {formatar(args.bloco, total_bits)}")
    print(f"Subchaves:  {args.subchaves}")
    print(f"Cifrado:    {formatar(cifrado, total_bits)}")
    print(f"Recuperado: {formatar(recuperado, total_bits)}")
    print(f"Ida e volta correta: {recuperado == args.bloco}")

    if args.mostrar_rodadas:
        print("\nRodadas:")
        for etapa in trilha_cifragem(args.bloco, args.subchaves, args.bits_metade):
            print(
                f"  {etapa['rodada']}: "
                f"L={etapa['esquerda_entrada']:0{args.bits_metade}b}, "
                f"R={etapa['direita_entrada']:0{args.bits_metade}b}, "
                f"K={etapa['subchave']:0{args.bits_metade}b}, "
                f"F={etapa['valor_f']:0{args.bits_metade}b} -> "
                f"L'={etapa['esquerda_saida']:0{args.bits_metade}b}, "
                f"R'={etapa['direita_saida']:0{args.bits_metade}b}"
            )

    avalanche = medir_avalanche(
        args.bloco, args.subchaves, args.bit_invertido, args.bits_metade
    )
    print(f"\nEntrada com bit {args.bit_invertido} invertido: ")
    print(f"  {formatar(int(avalanche['bloco_alterado']), total_bits)}")
    print("Saída correspondente:")
    print(f"  {formatar(int(avalanche['saida_alterada']), total_bits)}")
    print(
        f"Diferença entre saídas: {avalanche['bits_diferentes']} de "
        f"{total_bits} bits ({avalanche['percentual']:.1f}%)"
    )
    print("Aviso: esta função de rodada é fraca e o resultado não prova segurança.")


if __name__ == "__main__":
    main()

