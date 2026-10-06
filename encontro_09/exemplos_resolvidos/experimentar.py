"""Varia as entradas dos exemplos resolvidos, sem cifrar dados."""
import argparse
from modelo import tamanhos, nonce, colisao, etiqueta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mensagem', type=int, default=8, help='comprimento em bytes')
    parser.add_argument('--aad', type=int, default=7, help='comprimento em bytes')
    parser.add_argument('--prefixo', type=int, default=7)
    parser.add_argument('--contador', type=int, default=9)
    parser.add_argument('--amostras', type=int, default=2**32)
    parser.add_argument('--bits-nonce', type=int, default=96)
    parser.add_argument('--tentativas', type=int, default=2**20)
    parser.add_argument('--bits-tag', type=int, default=128)
    args = parser.parse_args()
    try:
        print('C, C||T, registro (bytes):', tamanhos(args.mensagem, args.aad))
        print('Nonce determinístico de 96 bits:', nonce(args.prefixo, args.contador).hex(' '))
        print('Modelo de sorteio: lambda, P aproximada:', colisao(args.amostras, args.bits_nonce))
        print('Modelo ideal de adivinhação: limite:', etiqueta(args.tentativas, args.bits_tag))
    except ValueError as erro:
        parser.error(str(erro))
    print('Cenários independentes: bits-nonce não altera o formato determinístico de 96 bits.')
    print('bits-tag altera só a conta ideal; a contagem de bytes usa a etiqueta AESGCM de 16 bytes.')


if __name__ == '__main__':
    main()
