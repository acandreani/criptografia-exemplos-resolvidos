"""Enunciados, cálculos e interpretações dos exemplos 1–5 do caderno."""
from modelo import cabecalho, nonce, codificar, tamanhos, colisao, etiqueta


def main():
    print('EXEMPLO 1 — Enunciado: proteger nota=8.5; versão 1, usuário 17, sequência 9.')
    print('1. Mensagem ASCII:', b'nota=8.5', '=>', len(b'nota=8.5'), 'bytes.')
    print('2. AAD = 1 + 2 + 4 = 7 bytes:', cabecalho().hex(' '))
    c, ct, total = tamanhos(8)
    print(f'3. C={c}; C||T={ct}; A||N||C||T=7+12+8+16={total} bytes.')
    print('Interpretação: A é público; a chave de 16 bytes fica fora do registro.\n')

    print('EXEMPLO 2 — Enunciado: distinguir (ab,c) de (a,bc).')
    print('1. Concatenação simples:', (b'ab'+b'c').hex(' '), '=', (b'a'+b'bc').hex(' '))
    print('2. Comprimento antes de cada campo:', codificar(b'ab', b'c').hex(' '))
    print('3. Segunda divisão:', codificar(b'a', b'bc').hex(' '))
    print('Interpretação: comprimentos distinguem as estruturas; cada campo tem até 255 bytes.\n')

    print('EXEMPLO 3 — Enunciado: prefixo 7 em 32 bits e contador 9 em 64 bits.')
    print('1. Nonce atual:', nonce().hex(' '))
    print('2. Próximo nonce:', nonce(contador=10).hex(' '))
    print('3. Capacidade por prefixo:', 2**64, 'valores de contador.')
    print('Interpretação: reservar duravelmente antes de cifrar; capacidade não é cota segura.\n')

    print('EXEMPLO 4 — Enunciado: estimar colisão em sorteios uniformes independentes.')
    for q, n in [(2**32, 96), (2**16, 32)]:
        intensidade, p = colisao(q, n)
        print(f'1. q={q}, n={n}; lambda=q(q-1)/(2*2^n)={intensidade:.12g}')
        print(f'2. P aproximadamente 1-exp(-lambda)={p:.12g} ({100*p:.8g}%).')
    print('Interpretação: P aproximadamente lambda só quando lambda é pequeno.\n')

    print('EXEMPLO 5 — Enunciado: 2^20 tentativas, etiquetas ideais de 32 e 128 bits.')
    for t in (32, 128):
        print(f'1. t={t}; uma tentativa: 2^-t={2**(-t):.12g}.')
        print(f'2. Limite por soma: v/2^t=2^{20-t}={etiqueta(2**20,t):.12g}.')
    print('Interpretação: modelo ideal de adivinhação; não é a garantia completa de GCM.')


if __name__ == '__main__':
    main()
