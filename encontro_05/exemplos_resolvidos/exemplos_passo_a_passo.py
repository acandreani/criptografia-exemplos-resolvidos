"""Reproduz os quatro exemplos resolvidos do texto do aluno."""

from feistel import (
    cifrar,
    decifrar,
    distancia_hamming,
    funcao_rodada,
    trilha_cifragem,
)


def binario(valor: int, bits: int) -> str:
    return f"{valor:0{bits}b}"


def titulo(numero: int, texto: str) -> None:
    print(f"\n{'=' * 72}\nExemplo {numero} - {texto}\n{'=' * 72}")


def exemplo_1() -> None:
    titulo(1, "por que a cifra precisa ser uma permutação")
    print("ENUNCIADO: Para 00->10, 01->00, 10->11 e 11->01, verifique se")
    print("cada saída permite recuperar uma única entrada. Justifique.")
    print("\nRESOLUÇÃO:")
    tabela = {0b00: 0b10, 0b01: 0b00, 0b10: 0b11, 0b11: 0b01}
    for entrada, saida in tabela.items():
        print(f"  {binario(entrada, 2)} -> {binario(saida, 2)}")
    saidas = list(tabela.values())
    print(f"Saídas distintas: {len(set(saidas))} de {len(saidas)}")
    print("Conclusão: cada saída identifica uma única entrada.")


def exemplo_2() -> None:
    titulo(2, "uma rodada Feistel e sua inversão")
    print("ENUNCIADO: Dados L=1010, R=0110 e F(R,K)=1100, calcule L' e R'.")
    print("Depois recupere L e R sem inverter F. Todos os valores são binários.")
    print("\nRESOLUÇÃO:")
    esquerda, direita, valor_f = 0b1010, 0b0110, 0b1100
    esquerda_saida = direita
    direita_saida = esquerda ^ valor_f
    print(f"L' = R = {binario(esquerda_saida, 4)}")
    print(
        "R' = L XOR F(R,K) = "
        f"{binario(esquerda, 4)} XOR {binario(valor_f, 4)} "
        f"= {binario(direita_saida, 4)}"
    )
    direita_recuperada = esquerda_saida
    esquerda_recuperada = direita_saida ^ valor_f
    print(f"R recuperado = L' = {binario(direita_recuperada, 4)}")
    print(
        "L recuperado = R' XOR F(R,K) = "
        f"{binario(direita_saida, 4)} XOR {binario(valor_f, 4)} "
        f"= {binario(esquerda_recuperada, 4)}"
    )
    assert (esquerda_recuperada, direita_recuperada) == (esquerda, direita)


def exemplo_3() -> None:
    titulo(3, "duas rodadas e ordem inversa das subchaves")
    print("ENUNCIADO: Cifre 00100101 em duas rodadas, com metades de 4 bits,")
    print("subchaves 0011 e 0010, e F(R,K)=(R+K) mod 16. Depois decifre.")
    print("\nRESOLUÇÃO:")
    bloco, subchaves, bits_metade = 0b00100101, [0b0011, 0b0010], 4
    print(f"Bloco inicial: {binario(bloco, 8)}")
    for etapa in trilha_cifragem(bloco, subchaves, bits_metade):
        print(
            f"Rodada {etapa['rodada']}: "
            f"F={binario(etapa['valor_f'], 4)}, "
            f"L={binario(etapa['esquerda_saida'], 4)}, "
            f"R={binario(etapa['direita_saida'], 4)}"
        )
    bloco_cifrado = cifrar(bloco, subchaves, bits_metade)
    assert bloco_cifrado == 0b10101001
    recuperado = decifrar(bloco_cifrado, subchaves, bits_metade)
    print(f"Bloco cifrado: {binario(bloco_cifrado, 8)}")
    print(f"Subchaves na volta: {list(reversed(subchaves))}")
    print(f"Bloco recuperado: {binario(recuperado, 8)}")
    assert recuperado == bloco


def exemplo_4() -> None:
    titulo(4, "medir o efeito avalanche")
    print("ENUNCIADO: As entradas 10110010 e 10110011 produziram as saídas")
    print("01101101 e 11000110. Conte os bits diferentes e sua porcentagem.")
    print("Esse único caso demonstra segurança? As saídas são dados do enunciado.")
    print("\nRESOLUÇÃO:")
    entrada, entrada_alterada = 0b10110010, 0b10110011
    saida, saida_alterada = 0b01101101, 0b11000110
    print(
        f"Entradas: {binario(entrada, 8)} e {binario(entrada_alterada, 8)}; "
        f"distância = {distancia_hamming(entrada, entrada_alterada)} bit"
    )
    xor_saidas = saida ^ saida_alterada
    diferentes = distancia_hamming(saida, saida_alterada)
    print(f"Saídas:   {binario(saida, 8)} e {binario(saida_alterada, 8)}")
    print(f"XOR:      {binario(xor_saidas, 8)}")
    print(f"Mudaram {diferentes} de 8 bits = {100 * diferentes / 8:.1f}%")
    print("Um caso ilustra avalanche, mas não prova segurança.")


def main() -> None:
    exemplo_1()
    exemplo_2()
    exemplo_3()
    exemplo_4()


if __name__ == "__main__":
    main()
