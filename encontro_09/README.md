# Encontro 9 — cifração autenticada, contexto e nonces

Seis exemplos resolvidos do texto do aluno, com **enunciado → etapas →
interpretação**. Aqui não há gabaritos da lista, atividades incompletas ou
material do professor.

1. Registro `nota=8.5`: mensagem de 8 bytes, AAD de 7 bytes, nonce de 12,
   etiqueta de 16; registro completo de 43 bytes.
2. `(ab,c)` e `(a,bc)`: ambiguidade e solução com comprimentos explícitos.
3. Prefixo 7 e contador 9: composição de 96 bits e próximo valor.
4. Colisões: `q=2^32,n=96` e `q=2^16,n=32`, com hipóteses do modelo.
5. Adivinhação: `2^20` tentativas e etiquetas ideais de 32/128 bits.
6. AES-GCM: cifração, alterações isoladas, contexto errado e repetição.

## Antes de executar: bibliotecas e métodos

Python 3.10 ou posterior. Os exemplos 1–5 só usam a biblioteca padrão.
`modelo.py` é nosso módulo local de formatos e contas; não implementa uma cifra.

- `int.to_bytes(n,"big")` escreve um inteiro em n bytes, mais significativo
  primeiro; `int.from_bytes` faz a conversão inversa. `bytes.fromhex` lê
  hexadecimal; `.hex(" ")` mostra os bytes separados por espaços.
- `len` conta elementos; `+` concatena bytes; `dados[inicio:fim]` seleciona
  uma parte, excluindo a posição final. Índices começam em zero; `-1` é o último.
- `math.expm1(x)` calcula `exp(x)-1` com precisão para valores pequenos;
  `-expm1(-lambda)` avalia a aproximação `1-exp(-lambda)` sem subtrair valores
  muito próximos de 1. `lambda=q(q-1)/(2*2^n)` conta pares esperados em colisão.
- `argparse.ArgumentParser` define opções do terminal; `parse_args` lê valores;
  `parser.error` apresenta entradas inválidas.
- `unittest` executa testes; `assertEqual`, `assertAlmostEqual`, `assertRaises`
  e `assertRaisesRegex` verificam igualdade, aproximação e exceções esperadas.
- `try/except/else` distingue falha esperada de aceitação; `raise ValueError`
  rejeita entradas; `assert` confere resultados didáticos (não execute com `-O`,
  que desativa essas verificações).

No exemplo 6, `cryptography` é externo:

- `AESGCM.generate_key(bit_length=128)` cria uma chave nova;
  `AESGCM(chave)` cria o objeto de cifração autenticada.
- `encrypt(nonce,mensagem,aad)` retorna C seguido da etiqueta T (16 bytes).
  `decrypt(nonce,pacote,aad)` retorna texto autenticado ou lança `InvalidTag`.
- `bytearray` cria uma cópia modificável; `^=1` inverte um bit;
  `bytes` volta à sequência imutável. Cada teste altera um único campo.
- `set()` cria um conjunto; `in` consulta pertinência; `add` registra a
  sequência aceita. O conjunto pertence a uma única chave/sessão.
- `.decode("ascii")` converte bytes autenticados em texto ASCII.

## Executar na raiz do repositório

```bash
python encontro_09/exemplos_resolvidos/exemplos_passo_a_passo.py
python -m unittest discover -s encontro_09/exemplos_resolvidos -p 'test_modelo.py' -v
python encontro_09/exemplos_resolvidos/experimentar.py --mensagem 23 --contador 255
python encontro_09/exemplos_resolvidos/experimentar.py --amostras 65536 --bits-nonce 32 --bits-tag 32
```

Argumentos numéricos são decimais. Teste também `--contador 18446744073709551616`
para observar a rejeição do estouro de 64 bits. Os campos da serialização do
exemplo 2 admitem no máximo 255 bytes cada; o decodificador rejeita truncamento
e bytes excedentes. Comprimentos se referem a bytes, não a caracteres Unicode.

Para o exemplo 6, crie um ambiente virtual (dependências isoladas):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cryptography
python encontro_09/exemplos_resolvidos/exemplo_aead.py
python -m unittest discover -s encontro_09/exemplos_resolvidos -p 'test_*.py' -v
```

No PowerShell do Windows, ative com `.venv\Scripts\Activate.ps1`.
O texto cifrado muda entre execuções porque a chave é nova.

## Experimente e interprete

Antes de executar, calcule uma saída no papel. Mude um parâmetro por vez e
compare. `--bits-nonce` muda apenas o modelo de sorteio: não muda o nonce
determinístico de 96 bits. `--bits-tag` muda a conta ideal: não muda a etiqueta
de 16 bytes da interface AESGCM usada na contagem do registro.

No exemplo 6, altere `mensagem` por outros bytes. Para várias cifragens sob
a mesma chave, use nonces distintos. A sequência autenticada também precisa
ser nova para a política do receptor. Não altere só a sequência mantendo nonce.
Os testes mostram que uma falha não consome sequência e que o próximo registro
legítimo pode ser aceito. Uma etiqueta válida não prova quem é uma pessoa.

## Limites de segurança

A demonstração gera uma chave nova e cifra uma vez com nonce fixo; isso não
autoriza fixar o nonce quando a chave é persistida. A construção prefixo/contador
exige atribuição exclusiva por chave, reserva durável e prevenção de reinício.
Capacidade de `2^64` contadores não significa autorização para cifrar esse volume.

O receptor de laboratório mantém estado só em memória, sem limitação de crescimento,
persistência, concorrência, rotação de chaves ou transação com a ação final.
Sua política simplificada considera a operação permitida para o usuário esperado;
não implementa um sistema real de permissões. Não o use como protocolo de produção.

As probabilidades de colisão pressupõem sorteios uniformes independentes e usam
aproximação de aniversário. O limite de adivinhação pressupõe etiquetas ideais;
não é a fórmula completa de segurança do GCM nem uma cota operacional.

## Fontes

- [RFC 5116: interface AEAD](https://www.rfc-editor.org/rfc/rfc5116).
- [NIST SP 800-38D: GCM](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf).
- [Documentação oficial AESGCM](https://cryptography.io/en/latest/hazmat/primitives/aead/).

## Glossário

- AEAD: Authenticated Encryption with Associated Data, cifração autenticada com dados associados.
- AAD: Additional Authenticated Data, dados adicionais autenticados e não cifrados.
- AES: Advanced Encryption Standard, Padrão de Criptografia Avançado.
- GCM: Galois/Counter Mode, modo Galois/contador.
- Nonce: número usado uma vez, sem repetição por chave nos esquemas aqui estudados.
- Tag: etiqueta de autenticação; InvalidTag: exceção de etiqueta inválida.
- Replay: repetição de uma mensagem anteriormente válida.
- Serialização: representação de uma estrutura em bytes; codificação canônica:
  escolha de uma representação definida e consistente.
- Big-endian: ordem de bytes do mais significativo para o menos significativo.
- ASCII: American Standard Code for Information Interchange, código americano
  padrão para intercâmbio de informação; Unicode: padrão de caracteres que
  abrange múltiplos sistemas de escrita.
- XOR: exclusive OR, OU exclusivo; bits diferentes resultam em 1.
- Bit: unidade binária; byte: oito bits; hexadecimal: representação na base 16.
- Contexto: informações que vinculam um registro ao seu uso esperado.
- Autorização: decisão de permitir uma operação; autenticação de mensagem:
  verificação criptográfica, não comprovação de identidade humana.
- Colisão: repetição de um valor sorteado; amostras uniformes independentes:
  todos os valores têm a mesma chance e um sorteio não influencia os demais.
- NIST: National Institute of Standards and Technology, Instituto Nacional de
  Padrões e Tecnologia dos Estados Unidos; SP: Special Publication, publicação
  especial; RFC: Request for Comments, série de documentos técnicos.
