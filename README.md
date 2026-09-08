# Exemplos resolvidos — Introdução à Criptografia

Repositório público de apoio aos encontros 5 e 6 da disciplina **Introdução à
Criptografia**. Os programas reproduzem os cálculos e exemplos do material,
permitem variar entradas e vêm acompanhados de testes automatizados.

> Os códigos são didáticos. Não use a rede de Feistel, o estimador ou qualquer
> outro exemplo deste repositório para proteger dados reais.

## Requisitos

- Python 3.10 ou mais recente;
- nenhum pacote externo: os exemplos usam somente a biblioteca padrão;
- um terminal para executar os comandos.

## Baixar

```bash
git clone https://github.com/acandreani/criptografia-exemplos-resolvidos.git
cd criptografia-exemplos-resolvidos
```

Também é possível selecionar **Code → Download ZIP** na página do GitHub.

## Encontro 5 — rede de Feistel

Em `encontro_05/exemplos_resolvidos/` há uma implementação de referência,
quatro exemplos passo a passo, um programa para experimentar blocos e
subchaves diferentes e testes.

```bash
python encontro_05/exemplos_resolvidos/exemplos_passo_a_passo.py
python encontro_05/exemplos_resolvidos/experimentar.py \
  --bloco 0x1234 \
  --subchaves 3 17 91 201 \
  --bit-invertido 0 \
  --mostrar-rodadas
python -m unittest discover -s encontro_05/exemplos_resolvidos -p "test_*.py" -v
```

Para praticar antes de consultar a solução, complete os `TODO` em
`encontro_05/codigo_inicial/` e execute:

```bash
python -m unittest discover -s encontro_05/codigo_inicial -p "test_*.py" -v
```

## Encontro 6 — DES, 3DES e estimativas de segurança

Em `encontro_06/exemplos_resolvidos/` estão os cálculos resolvidos do texto:

- busca exaustiva para 56, 112 e 128 bits;
- pior caso e caso médio;
- efeito de máquinas paralelas;
- probabilidade de colisão pelo paradoxo do aniversário;
- conversão de blocos de 64 bits em volume e tempo;
- estimativa didática do encontro no meio.

Execute a sequência reproduzida no material:

```bash
python encontro_06/exemplos_resolvidos/exemplos_passo_a_passo.py
python -m unittest discover -s encontro_06/exemplos_resolvidos -p "test_*.py" -v
```

Para variar a taxa de testes, o número de máquinas e a quantidade de blocos:

```bash
python encontro_06/exemplos_resolvidos/experimentar.py \
  --taxa 1e12 --maquinas 1000 --blocos 4294967296
python encontro_06/exemplos_resolvidos/experimentar.py \
  --bits-bloco 128 --blocos 4294967296
```

O parâmetro `112` do cenário 3DES é uma **estimativa de força clássica**,
não uma afirmação de que as três chaves formam literalmente uma chave de 112
bits. O modelo também não representa custo de memória, energia, comunicação,
ataques analíticos ou limites normativos de uso.

## Como estudar com os arquivos

1. Leia o exemplo resolvido e anote a fórmula antes de executar.
2. Execute o programa sem modificá-lo e compare a saída com o PDF.
3. Altere uma entrada por vez e faça uma previsão do resultado.
4. Leia os testes como especificação executável do comportamento esperado.
5. Modifique o programa para incluir um caso de erro e escreva o que mudou.

## Vocabulário

- **Python** — linguagem usada nos exemplos;
- **Git** — sistema de controle de versões;
- **GitHub** — serviço que hospeda o repositório;
- **clone** — cópia local do repositório;
- **cifra de brinquedo** — construção pequena para aprendizagem, sem segurança
  operacional;
- **busca exaustiva** — teste sistemático de todas as chaves candidatas;
- **força de segurança** — ordem aproximada do trabalho de um ataque genérico;
- **paradoxo do aniversário** — efeito que torna provável uma colisão após cerca
  de `2^(n/2)` amostras em um espaço de `2^n` valores;
- **encontro no meio** (*meet-in-the-middle*) — ataque que calcula estados a
  partir das duas extremidades de uma composição e procura correspondências;
- **assert** — comando do Python que interrompe o programa quando uma condição
  esperada é falsa.

## Fontes técnicas para o Encontro 6

- [NIST — FIPS 46-3 e retirada do DES](https://csrc.nist.gov/pubs/fips/46-3/final);
- [NIST — retirada da recomendação do TDEA](https://www.nist.gov/news-events/news/2023/06/nist-withdraw-special-publication-800-67-revision-2);
- [EFF — recuperação de uma chave DES em 56 horas](https://w2.eff.org/Privacy/Crypto/Crypto_misc/DESCracker/HTML/19980716_eff_des_faq.html).

