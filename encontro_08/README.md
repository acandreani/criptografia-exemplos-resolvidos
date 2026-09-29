# Encontro 8 — modos de operação

Seis exemplos **resolvidos**, correspondentes ao texto do aluno. Não há
atividades incompletas, material do professor ou gabaritos da lista.

1. ECB: [6,6,6] vira [9,9,9] e revela igualdade.
2. CBC: [6,6,6], IV=5, vira [6,3,8]; conferir a inversa.
3. CTR: nonce binário 10, contador 00,01,10; saída [D,A,B].
4. Reuso de fluxo: 41 e 42 com A6 dão E7 e E4; alteração E7→E6 muda 41→40.
5. PKCS #7: 20 bytes recebem doze 0C; 16 recebem dezesseis 10.
6. AES-GCM: proteger `nota=10.0` com AAD `turma=8` e rejeitar adulteração.

## Antes de executar: bibliotecas e métodos

Python 3.10 ou posterior. Os Exemplos 1–5 usam somente a biblioteca padrão.
`modos.py` é um módulo local que define E(x)=(x+3)%16 e sua inversa.
É reversível, mas **inseguro**; não é AES e não deve proteger dados reais.

- `%` calcula resto; `^` é XOR; `<<` desloca bits; `|` é OU bit a bit.
- `enumerate` fornece índice e elemento; `append` acrescenta à lista;
  `range`, `len` e `zip` percorrem índices, contam e associam elementos.
- `bytes([p])*p` repete o byte de preenchimento; `dados[-p:]` seleciona o final.
- `f"{x:X}"` formata hexadecimal; `int(texto,16)` interpreta nessa base.
- `argparse` lê opções do terminal; `parse_args` as interpreta.
- `unittest` executa testes; `assertEqual` compara resultados e `assertRaises`
  verifica falhas esperadas. `itertools.product` enumera pares para testar.
- `raise ValueError` rejeita valores inválidos; `try/except` trata exceções.

No Exemplo 6:

- `secrets` é da biblioteca padrão; `token_bytes(12)` gera 12 bytes aleatórios.
- `cryptography` é um pacote externo; `AESGCM.generate_key` gera a chave;
  `AESGCM(chave)` cria o objeto, `encrypt` cifra/anexa etiqueta e `decrypt`
  autentica/recupera ou gera `InvalidTag` (etiqueta inválida).
- `b"..."` representa bytes; `decode("ascii")` converte a mensagem autenticada
  em texto usando ASCII, código de caracteres americano.
- A etiqueta tem 16 bytes nessa interface: a mensagem de 9 bytes gera 25 bytes.
  Com o nonce de 12 bytes enviado à parte, são 37 bytes, sem AAD/cabeçalhos.

## Executar na raiz do repositório

```bash
python encontro_08/exemplos_resolvidos/exemplos_passo_a_passo.py
python -m unittest discover -s encontro_08/exemplos_resolvidos -p 'test_modos.py' -v
python encontro_08/exemplos_resolvidos/experimentar.py --blocos 4 4 --iv 1 --nonce 1
python encontro_08/exemplos_resolvidos/experimentar.py --blocos 6 6 --inicio 2 --nonce 2
```

Os argumentos numéricos são hexadecimais. Blocos, IV e chave variam de 0 a F;
nonce e início, de 0 a 3. O limite de quatro contadores é intencional para
ser observado; não é o formato de contador de AES. Teste a rejeição:

```bash
python encontro_08/exemplos_resolvidos/experimentar.py --blocos 6 6 6 6 6
```

Para o exemplo com biblioteca, crie um ambiente virtual (pasta isolada de
dependências). Em Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cryptography
python encontro_08/exemplos_resolvidos/exemplo_aes_gcm.py
python -m unittest discover -s encontro_08/exemplos_resolvidos -p 'test_aes_gcm.py' -v
```

No Windows, a ativação pelo PowerShell é `.venv\Scripts\Activate.ps1`.
Use a versão estável mantida da biblioteca disponível para seu ambiente.
Os bytes gerados variam entre execuções; as propriedades verificadas não.
O teste usa valores fixos isolados, apenas para reprodução. A demonstração
gera chave nova e cifra uma mensagem por execução. Não gere um sistema real
copiando a chave fixa do teste; é necessário gerenciar nonces, colisões,
limites, armazenamento de chaves e proteção contra repetição de mensagens.

## Como explorar

Antes de rodar, resolva uma linha à mão. Depois varie uma entrada por vez e
registre a recuperação. Os testes verificam todas as permutações de quatro
bits e todos os pares de blocos na recuperação CBC/CTR. O teste autenticado
confere texto, tamanho e rejeição de alterações em mensagem, etiqueta, nonce
e AAD. Isso não certifica um protocolo completo.

## Fontes

- [NIST SP 800-38A](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf): modos.
- [NIST SP 800-38D](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf): GCM.
- [RFC 5652, seção 6.3](https://www.rfc-editor.org/rfc/rfc5652#section-6.3): preenchimento.
- [AESGCM, documentação oficial](https://cryptography.io/en/latest/hazmat/primitives/aead/): interface.

## Glossário

- AES: Advanced Encryption Standard, Padrão de Criptografia Avançado.
- ECB: Electronic Codebook, livro de códigos eletrônico.
- CBC: Cipher Block Chaining, encadeamento de blocos de cifra.
- CTR: Counter, contador.
- IV: Initialization Vector, vetor de inicialização.
- GCM: Galois/Counter Mode, modo Galois/contador.
- AEAD: Authenticated Encryption with Associated Data, cifração autenticada com dados associados.
- AAD: Additional Authenticated Data, dados adicionais autenticados, mas não cifrados.
- XOR: exclusive OR, OU exclusivo; bits iguais dão zero, diferentes dão um.
- Nonce: valor usado uma só vez no escopo especificado pelo algoritmo.
- Fluxo de chave (keystream): sequência combinada com a mensagem por XOR.
- Etiqueta (tag): valor usado para verificar autenticidade.
- Maleabilidade: possibilidade de provocar alterações no texto recuperado.
- Padding: preenchimento; PKCS #7: Public-Key Cryptography Standards #7,
  nome do padrão associado à regra de preenchimento usada aqui.
- NIST: National Institute of Standards and Technology, Instituto Nacional de Padrões e Tecnologia dos EUA.
- SP: Special Publication, publicação especial; RFC: Request for Comments, série de documentos técnicos.
