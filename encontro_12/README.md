# Encontro 12: Diffie–Hellman e ElGamal

Sete exemplos resolvidos com enunciado, etapas e interpretação. Este diretório
não contém gabarito da lista nem solução da atividade de programação.
Tudo roda localmente, sem serviços de rede. O grupo (23,11,2) é inseguro.
O exemplo X25519/HKDF/AES-GCM não autentica participantes e não é protocolo.

## Executar e variar entradas

Python 3.10 ou superior. Testado com Python 3.11 e cryptography 41.0.5.
A partir da raiz do repositório (ou do ZIP extraído):

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r encontro_12/requirements.txt
python encontro_12/exemplos.py
python encontro_12/exemplos.py --exemplo 2 --a 2 --b 5
python encontro_12/exemplos.py --exemplo 4 --mensagem 9 --k 5
python -m unittest discover -s encontro_12 -p 'test_*.py' -v
```

Há 15 testes; um deles enumera 100 acordos, outro 1.100 combinações de
mensagens, privadas e expoentes de cifração. Isso testa este modelo pequeno,
não prova segurança. Para uma entrada inválida, o programa deve terminar com
`ValueError`, não reduzir silenciosamente a entrada.

## Antes do código

- `pow(b,e,p)` calcula potência modular; `pow(s,-1,p)`, inverso. `%` é resto.
- `secrets.token_bytes(n)` gera bytes por uma fonte apropriada à criptografia.
  O sal de 16 bytes pertence à derivação; o nonce de 12 bytes, à cifração.
- `X25519PrivateKey.generate()` gera a privada, `public_key()` obtém a pública
  e `exchange()` calcula o material compartilhado. Não autentica a identidade.
- `serialization`, `public_bytes` e os formatos `Raw` exportam a pública como
  bytes; `from_public_bytes` lê uma pública nesse formato.
- `HKDF(...).derive()` produz a chave. `hashes.SHA256()` configura o resumo;
  `length` define bytes de saída, `salt` é o sal e `info` é o contexto.
  Cada derivação usa uma instância nova.
- `AESGCM.encrypt()` devolve cifra com etiqueta; `decrypt()` verifica e abre.
  `InvalidTag` sinaliza falha de autenticação e não deve ser ignorada.
- `len(...).to_bytes(4,'big')` codifica um tamanho com o byte mais significativo
  primeiro; `join` concatena campos. `serializar` usa tamanho antes de cada
  campo, evitando ambiguidade entre `ab,c` e `a,bc`.
- `argparse` lê opções; `unittest` organiza testes e asserções. `type(x) is int`
  exclui booleanos: Python trata `True` como subclasse de inteiro, mas o contrato
  didático não o aceita como chave. Nenhuma função manual é de tempo constante.

## 1. Ordem e logaritmo discreto — `elementos`

**Enunciado:** liste as potências de 2 módulo 23 até voltar a 1 e encontre o
expoente de 16 no intervalo 0..10.

1. Partindo de 1, multiplique por 2 e reduza cada resultado.
2. A sequência é 1,2,4,8,16,9,18,13,3,6,12,1.
3. A primeira volta ocorre no expoente 11; 16 aparece no expoente 4.

Ordem é 11, módulo é 23. A tabela resolve o logaritmo porque o grupo é pequeno.
Variação: procure os expoentes dos alvos 3 e 12; depois tente 5, fora do grupo.

## 2. Acordo — `acordo`

**Enunciado:** com a=4,b=3, calcule públicas e os dois segredos.

1. A=2⁴=16; B=2³=8.
2. Alice: 8² mod23=18; 18² mod23=2.
3. Bob: 16² mod23=3; 3×16 mod23=2.
4. Ambos calculam 2¹² mod23=2. Somente A e B são enviados.

Variação: `--a 2 --b 5`, depois `--a 0`. A última entrada deve ser rejeitada.

## 3. Intermediário — `intermediario`

**Enunciado:** Mallory envia U=4 (privada2) a Alice e V=9 (privada5) a Bob.

1. Alice calcula 4⁴ mod23=3; Mallory calcula 16² mod23=3.
2. Bob calcula 9³ mod23=16; Mallory calcula 8⁵ mod23=16.
3. Os pares de pontas compartilham 3 e 16. As falsas públicas passam na validação.

É uma simulação local de substituição, sem alvos externos. Públicos válidos
não identificam Bob; procurar apenas segredos diferentes também não autentica.

## 4. ElGamal — `elgamal`, `cifrar`, `decifrar`

**Enunciado:** com x=3,y=8,m=6,k=4, cifre e recupere; compare k=5.

1. c1=16; máscara s=8⁴ mod23=2; c2=6×2=12.
2. Bob calcula 16³ mod23=2. O inverso é12: 2×12=24≡1.
3. 12×12 mod23=6: recuperou a mensagem.
4. Com k=5, c1=9,s=16,c2=4; inverso de16 é13 e 4×13 mod23=6.

Variação: `--mensagem 1 --k 10`; depois mensagem0 ou5, ambas rejeitadas.
O expoente `k` explícito é para reproduzir contas, não para uso real.

## 5. Reuso e maleabilidade — `falhas`

**Enunciado:** cifre6 e9 com k=4; use a mensagem conhecida6 para recuperar9.
Depois multiplique por4 o segundo componente da primeira cifra.

1. Ambas usam c1=16 e s=2; segundos componentes12 e18.
2. 12⁻¹ mod23=2; razão18×2 mod23=13.
3. 6×13 mod23=9, sem usar a privada.
4. Alterando12 para4×12 mod23=2, a abertura de(16,2) produz1.
5. 1=4×6 mod23. A alteração mantém elementos válidos, sem erro de formato.

A mensagem1 é válida no grupo; uma pública1 é rejeitada por outro contrato.

## 6. Validação — `validacao`, `validar_publica`

**Enunciado:** classifique1,5,8,22 e examine o efeito de aceitar1 ou22.

1. 1 força segredo1; é excluído.
2. 5 passa na faixa2..21, mas 5¹¹ mod23=22, e não pertence ao subgrupo.
3. 8 passa na faixa e no teste de pertencimento.
4. 22 tem ordem2 e alterna resultados22,1 conforme a paridade do expoente.

A validação vale apenas para o grupo fixo conhecido; não gera nem certifica
parâmetros arbitrários e não se aplica como fórmula a X25519.

## 7. Biblioteca — `biblioteca`

**Enunciado:** estabeleça material X25519, derive chaves e proteja uma mensagem;
rejeite adulteração, dados associados diferentes e uma pública nula.

1. `exchange` produz32 bytes iguais dos dois lados, sem imprimí-los.
2. Versão, nomes e públicas são codificados com comprimentos. Um sal público
   e um rótulo de direção entram na HKDF; as chaves têm32 bytes.
3. A direção inversa usa rótulo diferente. Contexto não autentica nomes.
4. Um nonce de12 bytes é usado em uma única cifração sob a chave nova.
   `nota=8.5` possui8 bytes; a saída tem24, incluindo etiqueta de16.
5. Alterar cifra ou AAD provoca `InvalidTag`. A pública nula provoca `ValueError`.

Variação: mude só o contexto do receptor e preveja rejeição. Reabrir um
registro válido não testa proteção contra repetição: não há estado desse
tipo aqui. Não estenda o exemplo a um canal real. Remover uma variável Python
não garante apagar segredos da memória.

## Glossário

- DH: Diffie–Hellman, acordo de material secreto.
- DLP: Discrete Logarithm Problem, recuperar expoente.
- CDH: Computational Diffie–Hellman, calcular segredo de duas públicas.
- DDH: Decisional Diffie–Hellman, distinguir esse segredo de um valor aleatório.
- Grupo, ordem, gerador: estrutura de operação; tamanho do ciclo; elemento que
  percorre o grupo por suas potências. Inverso modular desfaz multiplicação.
- ElGamal: cifra de chave pública com máscara multiplicativa e expoente aleatório.
- KDF: Key Derivation Function. HKDF: HMAC-based Extract-and-Expand Key
  Derivation Function. HMAC: Hash-based Message Authentication Code; MAC é
  Message Authentication Code. SHA256: Secure Hash Algorithm de256 bits.
- AES-GCM: Advanced Encryption Standard com Galois/Counter Mode.
- AEAD: Authenticated Encryption with Associated Data. AAD: Additional
  Authenticated Data, dados visíveis mas autenticados. Tag: etiqueta.
- Nonce: valor que não se repete sob a mesma chave no AES-GCM. Salt: sal da
  derivação; não precisa ser secreto nem tem o mesmo contrato de nonce.
- Transcript: registro da negociação. Replay: reapresentação de registro válido.
- Sigilo futuro: proteção de sessões passadas após roubo de chave de longo prazo,
  sob condições de autenticação, geração e descarte efetivo dos efêmeros.
- X25519: acordo sobre Curve25519. Hazmat significa hazardous materials,
  nome da área de primitivas de baixo nível da biblioteca cryptography.
- Python: linguagem. pip: instalador de pacotes. venv: ambiente isolado.
  README: instruções; repositório: coleção versionada; GitHub: hospedagem de código.

Referências: [Boneh–Shoup](https://crypto.stanford.edu/~dabo/cryptobook/),
[RFC2785](https://www.rfc-editor.org/rfc/rfc2785),
[RFC5869](https://www.rfc-editor.org/rfc/rfc5869),
[RFC7748](https://www.rfc-editor.org/rfc/rfc7748) e
[documentação X25519](https://cryptography.io/en/stable/hazmat/primitives/asymmetric/x25519/).
