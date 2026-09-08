# Encontro 6 — resoluções dos exemplos

As quatro resoluções do material estão em
[exemplos_passo_a_passo.py](exemplos_resolvidos/exemplos_passo_a_passo.py).
Cada função imprime o enunciado, as etapas da resolução e a interpretação.

Execute a partir da raiz do repositório com Python 3.10 ou mais recente:

```bash
python encontro_06/exemplos_resolvidos/exemplos_passo_a_passo.py
```

## Localizar e modificar um exemplo

| Função | Resolução | Resultado de referência |
| --- | --- | --- |
| `exemplo_1()` | Larguras da função de rodada e equações Feistel | 8 × 6 = 48 bits; 8 × 4 = 32 bits |
| `exemplo_2()` | Busca DES: tentativas → segundos → horas; comparação com 128 bits | Aproximadamente 20 h no pior caso, 10 h na média; razão 2⁷² |
| `exemplo_3()` | Blocos → bytes → bits → segundos → minutos | 34.359.738.368 bytes; aproximadamente 275 s ou 4,6 min |
| `exemplo_4()` | Cancelamento EDE e encontro no meio na dupla cifração | E_K(D_K(E_K(P))) = E_K(P); duas passagens de 2⁵⁶ cálculos |

No exemplo 2, altere `taxa` e observe os tempos. No exemplo 3, altere `blocos`
e observe o volume e o tempo. As mensagens numéricas acompanham esses valores;
o enunciado continua registrando os dados originais do material. No exemplo 4,
a resolução é algébrica e o programa calcula as ordens de trabalho, sem
enumerar o espaço de chaves. Mudar `bits_chave` permite explorar o custo do
modelo de dupla cifração; os trechos explicativos sobre DES continuam usando
seus parâmetros reais de 56 bits.

## Antes do código: bibliotecas, funções e métodos

- `calculos` é o arquivo local [calculos.py](exemplos_resolvidos/calculos.py).
  Não requer instalação. `tempo_medio` e `tempo_pior_caso` dividem tentativas
  pela taxa total; `em_anos` converte segundos em anos de 365,25 dias.
- `volume_bytes` multiplica blocos por bytes por bloco; `tempo_transmissao`
  divide o volume em bits pela taxa em bits por segundo.
- `math` é uma biblioteca padrão do Python. Seu método `expm1(x)` calcula
  `exp(x)-1` com boa precisão perto de zero. `exp` é a exponencial de base e.
  `probabilidade_colisao` usa esse recurso no complemento do exemplo 3.
- `argparse` é a biblioteca padrão que lê opções como `--taxa` e `--maquinas`
  em [experimentar.py](exemplos_resolvidos/experimentar.py). `add_argument`
  declara uma opção; `parse_args` lê as opções informadas.
- `**` calcula potências; `/` divide; `print` mostra o resultado.
  Uma *f-string* insere valores no texto: `:.3f` mostra três casas decimais
  e `:.3e` mostra notação científica.
- `unittest` executa verificações automáticas dos cálculos; `assertEqual`
  compara valores e `assertAlmostEqual` compara resultados aproximados.

## Variar entradas e conferir resultados

```bash
python encontro_06/exemplos_resolvidos/experimentar.py --taxa 1e12 --maquinas 1000
python encontro_06/exemplos_resolvidos/experimentar.py --bits-bloco 128 --blocos 4294967296
python -m unittest discover -s encontro_06/exemplos_resolvidos -p "test_*.py" -v
```

A busca usa M/2 como aproximação da média exata (M+1)/2, com candidatas
testadas sem repetição e posição uniforme da chave correta. A probabilidade
do aniversário supõe amostras independentes uniformes com reposição. Não é
probabilidade de quebra, nem colisão entre entradas distintas de uma cifra
de bloco com chave fixa. A estimativa de 112 bits para 3DES não transforma
seu conjunto de três chaves em uma chave literal de 112 bits.

## Siglas e termos usados nas resoluções

- **DES**: *Data Encryption Standard*, Padrão de Criptografia de Dados.
- **3DES**: *Triple DES*, aplicação tripla do DES.
- **AES**: *Advanced Encryption Standard*, Padrão de Criptografia Avançado;
  AES-128 usa uma chave de 128 bits.
- **EDE**: *Encrypt–Decrypt–Encrypt*, cifrar–decifrar–cifrar.
- **XOR**: *Exclusive OR*, OU exclusivo; resulta em 1 quando os bits diferem.
- **S-box**: *Substitution box*, caixa de substituição; no DES, converte seis
  bits em quatro por uma tabela não linear.
- **Subchave**: chave derivada da chave principal para uma rodada.
- **Feistel**: estrutura que atualiza as metades por L' = R e R' = L XOR F(R,K).
- **Encontro no meio** (*meet-in-the-middle*): cálculo de estados a partir
  das duas extremidades de uma composição, procurando correspondências.
- **P e C**: bloco claro e bloco cifrado; **E_K e D_K**: cifração e decifração
  sob a mesma chave K.
- **Bit e byte**: dígito binário e grupo de oito bits, respectivamente.
