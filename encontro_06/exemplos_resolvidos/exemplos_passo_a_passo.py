"""Reproduz os quatro exemplos matemáticos resolvidos do Encontro 6."""

from __future__ import annotations

from calculos import (
    em_anos,
    probabilidade_colisao,
    tempo_medio,
    tempo_pior_caso,
    tempo_transmissao,
    volume_bytes,
)


def titulo(numero: int, texto: str) -> None:
    print(f"\n{'=' * 72}\nExemplo {numero} — {texto}\n{'=' * 72}")


def exemplo_1() -> None:
    titulo(1, "larguras da função de rodada DES")
    grupos, bits_por_grupo = 8, 6
    saida_sbox = 4
    print(
        f"Expansão: {grupos} grupos × {bits_por_grupo} bits = "
        f"{grupos * bits_por_grupo} bits"
    )
    print(
        f"S-boxes:   {grupos} caixas × {saida_sbox} bits = "
        f"{grupos * saida_sbox} bits"
    )
    print("Conclusão: F recebe e devolve uma metade de 32 bits.")


def exemplo_2() -> None:
    titulo(2, "busca exaustiva: pior caso e caso médio")
    taxa = 10**12
    pior = tempo_pior_caso(56, taxa)
    medio = tempo_medio(56, taxa)
    print(f"Pior caso:  2^56 / 10^12 = {pior:.3f} s = {pior / 3600:.2f} h")
    print(f"Caso médio: 2^55 / 10^12 = {medio:.3f} s = {medio / 3600:.2f} h")
    ideal_128 = tempo_medio(128, taxa)
    print(
        f"AES-128 idealizado: {ideal_128:.3e} s = "
        f"{em_anos(ideal_128):.3e} anos"
    )
    print(f"Razão entre 128 e 56 bits: 2^72 = {2**72:.3e}")


def exemplo_3() -> None:
    titulo(3, "blocos de 64 bits: probabilidade, volume e tempo")
    blocos = 2**32
    prob = probabilidade_colisao(blocos, 64)
    bytes_totais = volume_bytes(blocos, 64)
    segundos = tempo_transmissao(blocos, 10**9, 64)
    print(f"Probabilidade aproximada de colisão: {prob:.6f} = {100 * prob:.2f}%")
    print(f"Volume: 2^32 × 8 bytes = {bytes_totais:,} bytes")
    print(f"A 10^9 bits/s: {segundos:.3f} s = {segundos / 60:.2f} min")
    print("A conta é um alerta de volume; não é um limite exato da permutação DES.")


def exemplo_4() -> None:
    titulo(4, "composição e encontro no meio")
    print("3DES-EDE: C = E_K3(D_K2(E_K1(P)))")
    print("Se K1 = K2 = K3 = K, então E_K(D_K(E_K(P))) = E_K(P).")
    print("Material de três chaves: 168 bits; força clássica estimada: cerca de 112 bits.")
    print("Dupla cifração: encontro no meio troca 2^112 pares por cerca de 2^57 operações.")


def main() -> None:
    exemplo_1()
    exemplo_2()
    exemplo_3()
    exemplo_4()


if __name__ == "__main__":
    main()

