"""Permite variar as hipóteses numéricas dos exemplos do Encontro 6."""

from __future__ import annotations

import argparse

from calculos import cenarios, probabilidade_colisao, tempo_transmissao, volume_bytes


def numero(texto: str) -> float:
    try:
        return float(texto)
    except ValueError as erro:
        raise argparse.ArgumentTypeError(f"número inválido: {texto}") from erro


def inteiro(texto: str) -> int:
    try:
        return int(texto, 0)
    except ValueError as erro:
        raise argparse.ArgumentTypeError(f"inteiro inválido: {texto}") from erro


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Experimenta os cálculos de segurança do Encontro 6."
    )
    parser.add_argument("--taxa", type=numero, default=1e12,
                        help="testes por segundo (padrão: 1e12)")
    parser.add_argument("--maquinas", type=inteiro, default=1,
                        help="quantidade de máquinas (padrão: 1)")
    parser.add_argument("--blocos", type=inteiro, default=2**32,
                        help="quantidade de blocos para o aniversário")
    parser.add_argument("--bits-bloco", type=inteiro, default=64,
                        help="largura de cada bloco (padrão: 64)")
    return parser


def main() -> None:
    args = criar_parser().parse_args()
    print(f"Hipóteses: taxa={args.taxa:.3e} testes/s; máquinas={args.maquinas}")
    print("\nCenário                         bits    tempo médio")
    print("-" * 64)
    for cenario in cenarios(args.taxa, args.maquinas):
        print(
            f"{cenario['nome']:<31} {cenario['bits_seguranca']:>4}    "
            f"{cenario['segundos']:.3e} s"
        )

    prob = probabilidade_colisao(args.blocos, args.bits_bloco)
    volume = volume_bytes(args.blocos, args.bits_bloco)
    transmissao = tempo_transmissao(args.blocos, 1e9, args.bits_bloco)
    print(f"\n{args.blocos} blocos de {args.bits_bloco} bits:")
    print(f"  probabilidade de colisão ≈ {100 * prob:.3f}%")
    print(f"  volume = {volume} bytes")
    print(f"  transmissão a 10^9 bits/s = {transmissao:.3f} s")


if __name__ == "__main__":
    main()

