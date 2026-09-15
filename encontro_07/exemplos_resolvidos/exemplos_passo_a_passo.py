"""As cinco resoluções do texto do aluno, com contas visíveis."""
from aes_operacoes import estado, shift_rows, xtime, parcelas, gf_mul, produtos_coluna, mix_column


def mostrar(linhas):
    for linha in linhas:
        print("  " + " ".join(f"{a:02X}" for a in linha))


def main():
    print("Todos os bytes abaixo estão em hexadecimal. Índices começam em zero.")
    print("\nEXEMPLO 1 — ENUNCIADO: monte o estado de 00 a 0F e aplique ShiftRows.")
    s = estado(list(range(16)))
    print("RESOLUÇÃO 1: preencha por colunas; s[r,c] = entrada[4*c+r].")
    mostrar(s)
    print("2: gire as linhas 0, 1, 2 e 3 para a esquerda por 0, 1, 2 e 3 posições.")
    mostrar(shift_rows(s))
    print("Interpretação: 05 vai de (1,1) a (1,0); valores não mudam.")

    print("\nEXEMPLO 2 — ENUNCIADO: combine 3A 7C 10 F0 com 0F 01 AA 55 por XOR.")
    for a, k in zip((0x3A, 0x7C, 0x10, 0xF0), (0x0F, 0x01, 0xAA, 0x55)):
        c = a ^ k
        print(f"{a:08b} XOR {k:08b} = {c:08b}; {a:02X} XOR {k:02X} = {c:02X}")
        print(f"  Desfazer: {c:02X} XOR {k:02X} = {c ^ k:02X}")
    print("Interpretação: a mesma máscara desfaz AddRoundKey isoladamente.")

    print("\nEXEMPLO 3 — ENUNCIADO: calcule xtime(57) e xtime(AE).")
    for a in (0x57, 0xAE):
        print(f"1: {a:02X} deslocado = {a << 1:03X}.")
        if a & 0x80:
            print(f"2: reduza: {a << 1:03X} XOR 11B = {xtime(a):02X}.")
        else:
            print(f"2: não surgiu nono bit; resultado {xtime(a):02X}.")
    print("Interpretação: truncar 15C para 5C não basta; falta XOR com 1B.")

    print("\nEXEMPLO 4 — ENUNCIADO: calcule 57 vezes 13 no corpo do AES.")
    print("1: 13 = 00010011; selecione os bits 0, 1 e 4.")
    acumulado = 0
    for i, p, selecionada in parcelas(0x57, 0x13):
        if i > 4:
            break
        print(f"2: potência {i}: {p:02X}; entra na soma? {selecionada}")
        if selecionada:
            anterior = acumulado
            acumulado ^= p
            print(f"   Acumulador: {anterior:02X} XOR {p:02X} = {acumulado:02X}")
    print(f"3: resultado {gf_mul(0x57, 0x13):02X}. Não é multiplicação inteira módulo 256.")

    print("\nEXEMPLO 5 — ENUNCIADO: aplique MixColumns à coluna D4 BF 5D 30.")
    coluna = [0xD4, 0xBF, 0x5D, 0x30]
    print("1: multiplique pelos coeficientes de cada linha da matriz fixa.")
    print("2: combine os quatro produtos por XOR:")
    for i, (produtos, saida) in enumerate(zip(produtos_coluna(coluna), mix_column(coluna))):
        acumulado = 0
        for p in produtos:
            acumulado ^= p
            print(f"  Linha {i}: parcela {p:02X}; acumulador {acumulado:02X}")
        print("  " + " XOR ".join(f"{p:02X}" for p in produtos) + f" = {saida:02X}")
    print("Interpretação: saída 04 66 81 E5; quatro bytes entram e quatro saem.")


if __name__ == "__main__":
    main()
