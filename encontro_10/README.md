# Encontro 10 — exemplos resolvidos de chave pública

Somente resoluções dos seis exemplos do caderno. Não contém gabarito da lista
nem a cola do professor. Laboratório local com dados fictícios, sem rede:
não é protocolo de produção e não autentica as chaves públicas recebidas.

## Executar

Com Python 3.10 ou superior, dentro desta pasta:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python exemplos.py
python -m unittest -v
python exemplos.py --exemplo 1 --pessoas 10
```

No Windows, ative com `.venv\Scripts\activate`. Não use `python -O`.

## Enunciados e resoluções

1. **Distribuição:** oito pessoas, uma chave simétrica exclusiva por par.
   Cada pessoa tem sete parceiros; 8×7 conta cada par duas vezes: 28 chaves.
   `pares` resolve e aceita variar o número de pessoas; dez pessoas dão 45.
   Comparar com oito pares assimétricos não inclui chaves de sessão nem elimina confiança.
2. **Potência:** calcular 5⁶ mod 23. 5²→2, 5⁴→4, 5⁶→4×2→8.
   `potencia` mostra estados (expoente restante, base reduzida, acumulador).
   Compare com `pow(base, expoente, modulo)` e varie entradas.
3. **Acordo:** p=23, g=5, a=6, b=15. A=8; B=19;
   19⁶ mod 23 = 8¹⁵ mod 23 = 2. `acordo_brinquedo` devolve A,B,SA,SB.
   Só A e B são enviados; os parâmetros são públicos. Números inseguros.
4. **Intermediário:** Mallory escolhe m=13 e substitui ambas as públicas
   por M=21. Alice calcula 18, igual ao 8¹³ de Mallory; Bob calcula 7,
   igual ao 19¹³ de Mallory. `ataque_brinquedo` retorna 21,18,18,7,7.
   Mallory conhece duas conexões; não precisa recuperar a ou b.
5. **Tamanho:** RSA-OAEP com módulo 2048 bits e SHA-256.
   k=256 bytes; hLen=32; limite=256−64−2=190 bytes.
   Uma chave de 32 bytes cabe, um vídeo de um milhão de bytes não.
   `limite_oaep` calcula a fórmula; não implementa RSA.
6. **Biblioteca:** gerar pares X25519, derivar chaves e proteger `nota=8.5`.
   `acordo_real` verifica públicas/segredos de 32 bytes, igualdade,
   contexto diferente, abertura e adulteração. O pacote tem 24 bytes:
   oito de mensagem cifrada e dezesseis de etiqueta.
   `intermediario` demonstra duas conexões e Mallory lendo e recifrando.
   O sucesso das operações não prova a identidade de Bob.

## Antes de ler o código

- `cryptography` é a biblioteca externa. X25519 é o acordo baseado em
  Curve25519. `generate` cria privada, `public_key` obtém pública,
  `exchange` calcula segredo e `public_bytes` exporta a pública.
- `serialization.Encoding.Raw` e `PublicFormat.Raw`: codificação bruta.
- KDF significa função de derivação de chaves; HKDF é uma KDF por extração
  e expansão baseada em HMAC (código de autenticação baseado em hash).
  `HKDF(...).derive` transforma o segredo com sal (`salt`), contexto
  (`info`) e comprimento (`length`). SHA-256 é um algoritmo de hash de 256 bits.
- AES-GCM combina AES (Advanced Encryption Standard) com Galois/Counter Mode.
  É AEAD: cifração autenticada com dados associados. `encrypt` produz
  cifrado e etiqueta; `decrypt` autentica e abre ou lança `InvalidTag`.
- `secrets.token_bytes` gera aleatoriedade; `secrets`, `argparse` (argumentos
  de linha de comando) e `unittest` (testes) vêm com Python.
- `bytes(12)` são doze bytes zero: aqui só existe uma cifração por chave
  recém-gerada. **Não reutilize esse nonce para cifrar outra mensagem com a
  mesma chave.** Nonce significa valor usado uma vez conforme a regra do esquema.
- `pow` calcula potência modular; `len` mede comprimento. `^ 1` inverte
  um bit para testar adulteração. O código retorna apenas verificações;
  segredos reais gerados não são impressos.

## Modificar com propósito

Varie `--pessoas`, bases e expoentes de brinquedo; altere `info` em um lado;
preveja o resultado antes de rodar. Separe sempre falha matemática/funcional,
falha de etiqueta e falha de autenticação da identidade.
O teste de concordância deve exigir **comprimento 32 e igualdade**:
duas cadeias vazias também são iguais.

Os testes não provam segurança. Faltam autenticação da negociação, estados,
gestão de nonces em múltiplas mensagens, prevenção de repetição e proteção
do ciclo de vida das chaves. Não reutilize os exemplos como canal de rede.

## Fontes

- [X25519 na biblioteca cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/)
- [HKDF: RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html)
- [RSA-OAEP: RFC 8017, seção 7.1](https://www.rfc-editor.org/rfc/rfc8017.html)
