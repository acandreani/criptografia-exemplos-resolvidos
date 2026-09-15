# Encontro 7 — operações internas do AES

Cinco exemplos resolvidos, na mesma ordem do texto do aluno. Cada execução
apresenta enunciado, contas intermediárias e interpretação. Não é uma
implementação completa de AES e não deve proteger dados reais.

## Antes do código: bibliotecas e recursos

Requer Python 3.10 ou posterior, sem instalação de pacotes.

- `aes_operacoes.py` é um módulo local, não uma biblioteca externa.
- `argparse` (biblioteca padrão) lê opções do terminal; `add_argument` define
  entradas e `parse_args` interpreta o comando.
- `unittest` (biblioteca padrão) executa testes; `assertEqual` compara valores
  e `assertRaises` verifica a rejeição de entradas inválidas.
- `0x57` é hexadecimal; `int(texto, 16)` converte texto nessa base;
  `bytes.fromhex` converte pares de dígitos em bytes.
- `^` é XOR (OU exclusivo), `&` é E bit a bit e `<<` desloca bits à esquerda.
- `range(8)` percorre oito posições; `enumerate` fornece índice e valor;
  `zip` associa elementos de sequências; `len` mede seu comprimento.
- `linha[r:] + linha[:r]` reúne duas fatias para fazer uma rotação circular.
- `f"{valor:02X}"` mostra dois dígitos hexadecimais, em maiúsculas.
- `ValueError` sinaliza uma entrada inválida; `raise` dispara esse erro.

## Executar a partir da raiz do repositório

```bash
python encontro_07/exemplos_resolvidos/exemplos_passo_a_passo.py
python -m unittest discover -s encontro_07/exemplos_resolvidos -p "test_*.py" -v
python encontro_07/exemplos_resolvidos/experimentar.py --a 57 --b 03 --coluna 01 00 00 00
python encontro_07/exemplos_resolvidos/experimentar.py --a AE --b 02 --bloco 00112233445566778899aabbccddeeff
```

As opções de bytes são sempre hexadecimais: `13` significa dezenove em decimal.
O primeiro comando experimental deve dar produto `F9` e coluna `02 01 01 03`.
O segundo deve dar produto `47`.

## Correspondência com o texto

| Exemplo | Enunciado resumido | Resultado |
|---|---|---|
| 1 | Organizar 00–0F e deslocar linhas | Linha 1: 05 09 0D 01 |
| 2 | XOR das colunas 3A 7C 10 F0 e 0F 01 AA 55 | 35 7D BA A5 |
| 3 | Multiplicar 57 e AE por 02 | AE e 47 |
| 4 | Multiplicar 57 por 13 no corpo do AES | FE |
| 5 | Misturar D4 BF 5D 30 | 04 66 81 E5 |

Altere uma entrada, preveja a saída e acompanhe as parcelas. Os testes comparam
todos os 65.536 pares de bytes com uma segunda implementação, baseada em
produto de polinômios e divisão longa. Isso verifica a aritmética didática;
não certifica segurança, resistência a canais laterais ou uma cifra completa.

## Fonte

[NIST, FIPS 197 (2023)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf),
seções 3–5 e apêndice B: convenção de estado, operações e vetor MixColumns.

## Glossário

- **AES** — Advanced Encryption Standard, Padrão de Criptografia Avançado.
- **NIST** — National Institute of Standards and Technology, Instituto Nacional
  de Padrões e Tecnologia dos Estados Unidos.
- **FIPS** — Federal Information Processing Standards, padrões federais de processamento de informação.
- **GF(2⁸)** — corpo de Galois com 256 elementos; aqui os bytes representam polinômios binários.
- **XOR** — exclusive OR, OU exclusivo; soma dos coeficientes módulo dois.
- **estado** — matriz de quatro linhas e quatro colunas de bytes.
- **ShiftRows** — deslocamento circular das linhas do estado.
- **MixColumns** — mistura reversível de cada coluna por uma matriz fixa.
- **AddRoundKey** — incorporação da subchave por XOR.
- **xtime** — multiplicação pelo polinômio x, representado por 02.
- **redução polinomial** — obtenção do resto por divisão pelo polinômio do AES.
- **byte** — oito bits; **bit** — valor binário zero ou um.
- **hexadecimal** — sistema de base 16; **módulo** de Python — arquivo importável.
- **canal lateral** — informação sobre segredos obtida de tempo, consumo ou outros efeitos da execução.
