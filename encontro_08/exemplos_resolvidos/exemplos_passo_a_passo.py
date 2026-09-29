"""Enunciados e resoluções dos Exemplos 1 a 5 do material."""
from modos import e, d, ecb, cbc_etapas, cbc, dec_cbc, ctr_etapas, ctr, preencher, remover


def hexs(valores):
    return " ".join(f"{x:X}" for x in valores)


def main():
    print("Modelo inseguro de quatro bits. E(x)=(x+3)%16; D(y)=(y-3)%16.")
    print("Valores de blocos em hexadecimal. Não use para proteger dados.")
    m = [6, 6, 6]
    print("\n1 — ENUNCIADO: cifre [6,6,6] em ECB e recupere a entrada.")
    print("RESOLUÇÃO: cada 6 recebe soma 3 módulo 16.")
    print("Saída:", hexs(ecb(m)))
    print("Inversa:", hexs([d(c) for c in ecb(m)]))
    print("Interpretação: igualdade dos blocos continua visível.")

    print("\n2 — ENUNCIADO: cifre [6,6,6] em CBC com IV=5; depois decifre.")
    print("RESOLUÇÃO: primeiro XOR, depois E. M, anterior, XOR, C:")
    for linha in cbc_etapas(m, 5):
        print(hexs(linha))
    anterior = 5
    for c in cbc(m, 5):
        print(f"D({c:X})={d(c):X}; {d(c):X} XOR {anterior:X} = {d(c) ^ anterior:X}")
        anterior = c
    print("Recuperação:", hexs(dec_cbc(cbc(m, 5), 5)))
    print("As saídas distintas são deste exemplo, não uma garantia universal.")

    print("\n3 — ENUNCIADO: use CTR, nonce binário 10, contador de dois bits.")
    print("RESOLUÇÃO: concatene os campos; cifre T; combine o fluxo com M.")
    for contador, t, fluxo, c in ctr_etapas(m, 2):
        print(f"10|{contador:02b}={t:04b} ({t:X}); E(T)={fluxo:X}; 6 XOR {fluxo:X}={c:X}")
    print("Inversa por XOR com o mesmo fluxo:", hexs(ctr(ctr(m, 2), 2)))
    print("São quatro contadores possíveis. Um quinto bloco deve ser rejeitado.")

    print("\n4 — ENUNCIADO: P=41, Q=42 e fluxo reutilizado S=A6; depois altere um bit.")
    p, q, s = 0x41, 0x42, 0xA6
    c, outro = p ^ s, q ^ s
    print(f"C=41 XOR A6={c:02X}; C'=42 XOR A6={outro:02X}")
    print(f"C XOR C'={c ^ outro:02X}; Q=P XOR C XOR C'={p ^ c ^ outro:02X}")
    alterado = c ^ 1
    print(f"Alteração: C XOR 01={alterado:02X}; texto recuperado={alterado ^ s:02X}")
    print("Reuso revela relações. Maleabilidade existe também sem reuso.")

    print("\n5 — ENUNCIADO: preencha mensagens de 20 e 16 bytes com PKCS #7.")
    for n in (20, 16):
        entrada = b"A" * n
        saida = preencher(entrada)
        p = len(saida) - n
        print(f"L={n}; p=16-(L%16)={p}; acrescente {p} bytes {p:02X}; total={len(saida)}.")
        assert remover(saida) == entrada
    print("Zeros finais seriam ambíguos; preenchimento válido não autentica.")
    print("\nExemplo 6: execute exemplo_aes_gcm.py após instalar cryptography.")


if __name__ == "__main__":
    main()
