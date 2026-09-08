"""Enunciados e resoluções dos quatro exemplos do Encontro 6.

Antes de executar: ``calculos`` é o arquivo local calculos.py, não um pacote
a instalar. Suas funções implementam as fórmulas usadas abaixo. ``print``
mostra cada etapa; ``**`` calcula potências; ``/`` divide; f-strings inserem
valores no texto (:.3f = três casas decimais, :.3e = notação científica).
Edite os dados no início de cada exemplo para investigar outros valores.
O exemplo 4 desenvolve uma resolução algébrica e calcula custos; não executa
uma busca real no espaço de chaves DES.
"""

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
    print("ENUNCIADO: Uma metade de 32 bits é expandida para 48 bits e recebe")
    print("uma subchave de 48 bits por OU exclusivo. O resultado entra em oito")
    print("S-boxes de 6 bits de entrada e 4 de saída. Calcule as larguras antes")
    print("e depois das S-boxes e escreva a atualização das metades da rodada.")
    print("\nRESOLUÇÃO:")
    grupos, bits_por_grupo = 8, 6
    saida_sbox = 4
    print("1. A expansão repete posições: 32 -> 48 bits, sem criar informação.")
    print("2. O OU exclusivo combina dois valores de 48 bits e mantém 48 bits.")
    print(
        f"3. Entrada das caixas: {grupos} grupos × {bits_por_grupo} bits = "
        f"{grupos * bits_por_grupo} bits"
    )
    print(
        f"4. Saída das caixas: {grupos} caixas × {saida_sbox} bits = "
        f"{grupos * saida_sbox} bits"
    )
    print("5. A permutação reorganiza os 32 bits. F pode ser combinada com L_i.")
    print("6. L_(i+1) = R_i; R_(i+1) = L_i XOR F(R_i, K_(i+1)).")
    print("   i vai de 0 a 15; K_1 é a subchave aplicada ao estado inicial.")


def exemplo_2() -> None:
    titulo(2, "busca exaustiva: pior caso e caso médio")
    print("ENUNCIADO: Testando 10^12 chaves/s sem repetição, estime o pior caso")
    print("e a média para DES de 56 bits, em segundos e horas. Compare a média")
    print("com uma busca ideal de 128 bits, em segundos e anos. Calcule a razão.")
    print("Considere posição uniforme da chave e anos de 365,25 dias.")
    print("\nRESOLUÇÃO:")
    taxa = 10**12
    # A média exata é (M+1)/2; aproximamos por M/2 para estas estimativas.
    print("1. M = 2^56 candidatas. Média exata: (M+1)/2 ≈ 2^55 tentativas.")
    pior = tempo_pior_caso(56, taxa)
    medio = tempo_medio(56, taxa)
    print(f"2. Pior caso: 2^56 / {taxa:.3e} = {pior:.3f} s = {pior / 3600:.2f} h")
    print(f"3. Média: 2^55 / {taxa:.3e} ≈ {medio:.3f} s = {medio / 3600:.2f} h")
    print("   Dividimos segundos por 3600 para converter em horas.")
    ideal_128 = tempo_medio(128, taxa)
    print(
        f"4. Busca ideal de 128 bits: 2^127 / taxa ≈ {ideal_128:.3e} s = "
        f"{em_anos(ideal_128):.3e} anos"
    )
    print("   Para anos, dividimos segundos por 365,25 × 24 × 60 × 60.")
    print(f"5. Razão: 2^127 / 2^55 = 2^72 = {2**72:.3e}.")
    print("A média não é um prazo garantido; a taxa é uma hipótese didática.")


def exemplo_3() -> None:
    titulo(3, "transformar blocos em volume e tempo")
    print("ENUNCIADO: Converta 2^32 blocos de 64 bits em bytes e determine o")
    print("tempo de transmissão a 10^9 bits/s, em segundos e minutos. Considere")
    print("8 bits/byte e nenhuma sobrecarga. Esse volume é garantidamente seguro?")
    print("\nRESOLUÇÃO:")
    blocos = 2**32
    print("1. Um bloco tem 64 / 8 = 8 bytes.")
    bytes_totais = volume_bytes(blocos, 64)
    segundos = tempo_transmissao(blocos, 10**9, 64)
    print(f"2. Volume: {blocos} × 8 = {bytes_totais} bytes.")
    print(f"3. Em bits: {bytes_totais} × 8 = {bytes_totais * 8} bits.")
    print(f"4. Tempo: bits / 10^9 = {segundos:.3f} s = {segundos / 60:.2f} min.")
    print("5. Não: a conta não autoriza usar DES até esse volume. O limite depende")
    print("   do modo, do protocolo e das regras aplicáveis; pode ser bem menor.")
    prob = probabilidade_colisao(blocos, 64)
    print("\nComplemento: no modelo de amostras independentes e uniformes com")
    print("reposição, p ≈ 1-exp(-q(q-1)/(2×2^64)). Para q=2^32:")
    print(f"p ≈ {prob:.6f} = {100 * prob:.2f}%. Não é probabilidade de quebra.")
    print("Na permutação DES com chave fixa, entradas distintas não colidem.")


def exemplo_4() -> None:
    titulo(4, "composição e encontro no meio")
    print("ENUNCIADO: Para C=E_K3(D_K2(E_K1(P))), mostre o resultado com chaves")
    print("iguais. Na dupla cifração com duas chaves de 56 bits, compare testar")
    print("pares de chaves com procurar estados iguais a partir de P e C, supondo")
    print("memória suficiente. Por que somar bits de chave não prova segurança?")
    print("P é o bloco claro; C é o cifrado; D_K desfaz E_K sob a mesma chave.")
    print("\nRESOLUÇÃO:")
    print("1. Substitua K1, K2 e K3 por K: C = E_K(D_K(E_K(P))).")
    print("2. Cancele a dupla interna: D_K(E_K(P)) = P. Logo C = E_K(P).")
    print("   A composição reproduz uma única cifração DES nesse caso.")
    print("3. Na dupla cifração, C=E_K2(E_K1(P)); aplique D_K2 aos dois lados:")
    print("   D_K2(C) = E_K1(P). Esse é o estado que podemos procurar no meio.")
    bits_chave = 56
    escolhas = 2 ** bits_chave
    pares = escolhas ** 2
    calculos = 2 * escolhas
    print(f"4. Enumeração: 2^{bits_chave} × 2^{bits_chave} = {pares:.3e} pares.")
    print(f"5. Calcule E_K1(P) para {escolhas:.3e} chaves e armazene os estados.")
    print("   Guarde todas as chaves associadas a cada estado.")
    print(f"6. Calcule D_K2(C) para {escolhas:.3e} chaves e consulte a tabela.")
    print("   Verifique os pares candidatos usando outros blocos conhecidos.")
    print(f"7. São 2^56 + 2^56 = 2^57 = {calculos:.3e} cálculos de DES,")
    print("   além de memória, consultas e verificação; não 2^112 pares testados.")
    print("8. Esse ataque é para dupla cifração. O 3DES exige outra análise:")
    print("   168 bits de material de chave correspondem a cerca de 112 bits de")
    print("   força clássica estimada. A composição cria seus próprios ataques.")
    print("Para decifrar 3DES: P = D_K1(E_K2(D_K3(C))), invertendo as etapas.")


def main() -> None:
    exemplo_1()
    exemplo_2()
    exemplo_3()
    exemplo_4()


if __name__ == "__main__":
    main()
