# Encontro 11: seis exemplos resolvidos de RSA

Somente resoluções dos exemplos do texto, não gabarito da lista ou do laboratório.
Os inteiros pequenos são inseguros. O exemplo de biblioteca é local e não
implementa protocolo, autenticação da identidade, serviço ou armazenamento.

## Executar

Python 3.10 ou superior. A partir da raiz do repositório:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r encontro_11/requirements.txt
python encontro_11/exemplos.py
python encontro_11/exemplos.py --exemplo 2 --mensagem 5
python -m unittest discover -s encontro_11 -p 'test_*.py' -v
```

## Antes do código

`math.gcd` calcula o máximo divisor comum; `divmod` retorna quociente e resto.
`pow(m,e,n)` calcula potência modular e `pow(e,-1,t)` o inverso, se existir.
`argparse` lê as opções; `unittest` organiza testes. A função `potencia` registra
estados `(expoente restante, base reduzida, acumulador)`; não é de tempo constante.

O pacote externo `cryptography` fornece `rsa.generate_private_key`, que gera
a privada, e `public_key()`, que obtém a pública. `padding.OAEP`, `padding.PSS`
e `padding.MGF1` configuram os esquemas; `hashes.SHA256()` escolhe o resumo.
`encrypt/decrypt` cifram/abrem com OAEP; `sign/verify` assinam/verificam com PSS.
`verify` retorna `None` no sucesso e lança `InvalidSignature` na falha.
`ValueError` sinaliza entrada inadequada. As exceções não autorizam aceitar dados.
Usamos um par para cifração e outro para assinatura. Nenhuma privada é impressa.

## 1. Chave pequena e inverso (`chave_pequena`)

**Enunciado:** com p=5, q=11, e=3, obtenha n, totiente e d por Euclides.

1. n=5×11=55; φ=4×10=40.
2. 40=13×3+1; 3=3×1+0, portanto MDC=1.
3. 1=40−13×3: coeficiente de 3 é −13.
4. d=−13 mod40=27; 3×27=81=2×40+1.

Pública: (55,3). Fatores, totiente e d são privados. A ordem das divisões
impressas inclui a divisão inicial de 3 por 40, que não muda o resultado.
Experimente `euclides(10,40)` e explique por que não fornece um inverso.

## 2. Ida e volta (`ida_volta`, `potencia`)

**Enunciado:** cifre 7 e decifre com n=55,e=3,d=27, mostrando as reduções.

1. 7³=343=6×55+13, logo c=13.
2. Potências 13¹,13²,13⁴,13⁸,13¹⁶ têm restos 13,4,16,36,31.
3. 27=16+8+2+1. Produtos sucessivos: 31×36 mod55=16;
   16×4 mod55=9; 9×13 mod55=7.

Variação: `--exemplo 2 --mensagem 54`; depois tente 55, que deve ser rejeitado.
Não há codificação de arquivos: a entrada é um inteiro entre 0 e 54.

## 3. Mensagem não coprima (`nao_coprimo`)

**Enunciado:** cifre/decifre 5 e explique a hipótese que falta para Euler.

1. MDC(5,55)=5; não se aplica Euler diretamente módulo55.
2. 5³ mod55=15.
3. Restos de 15²,15⁴,15⁸,15¹⁶: 5,25,20,15.
4. Combinar expoentes 16+8+2+1: 15×20 mod55=25;
   25×5 mod55=15; 15×15 mod55=5.

A prova geral trabalha separadamente módulo5 e módulo11, incluindo resto0,
e combina pelo teorema chinês dos restos. O teste exaustivo dos55 representantes
verifica esta chave didática, não prova segurança de RSA.

## 4. Maleabilidade (`maleabilidade`)

**Enunciado:** com c=13 e pública(55,3), use r=2 para modificar a cifra.

1. r³=8; c'=13×8 mod55=49.
2. A decifração resulta em 14, o dobro de7 módulo55.
3. A transformação c×r^e depende só da pública. A privada aparece apenas
   na conferência local, não na criação da cifra alterada.

Repetir a entrada original repete c=13. Não transporte esta transformação
para OAEP como se a validação e a codificação não existissem.

## 5. Primo repetido (`primo_compartilhado`)

**Enunciado:** obtenha fatores e privadas dos módulos55 e85, ambos com e=3.

1. Euclides: 85=55+30,55=30+25,30=25+5,25=5×5.
2. MDC=5; outros fatores11 e17. Totientes40 e64.
3. Inversos: d1=27 e d2=43, pois3×43=129=2×64+1.

MDC1 não prova que uma geração seja segura. Este experimento usa apenas
módulos sintéticos, sem coleta de chaves de terceiros.

## 6. OAEP e PSS (`esquemas`)

**Enunciado:** use RSA2048/SHA256 para cifrar duas vezes `pedido=7`, abrir,
testar a fronteira e, com outro par, assinar e rejeitar alteração/pública errada.

1. Capacidade: 2048/8−2×32−2=190bytes. Cifra:256bytes.
2. OAEP usa SHA256 no esquema e na MGF1, rótulo vazio. As cifras normalmente
   diferem. O teste abre a primeira; também abre190bytes e rejeita191.
3. PSS usa SHA256, MGF1/SHA256 e sal32bytes. Verifica a original, rejeita
   `pedido=8` e pública de outro par com `InvalidSignature`.

As propriedades booleanas impressas devem ser verdadeiras. A distinção das
duas cifras é probabilística, não uma impossibilidade matemática de colisão.
Variação: abra também a segunda cifra; mude um parâmetro por vez e preveja
rejeição antes de executar. Não implemente uma interface de rede de erros.

## Glossário

- RSA: Rivest–Shamir–Adleman; bruto é a transformação modular sem esquema seguro.
- OAEP: Optimal Asymmetric Encryption Padding, codificação probabilística de cifração.
- PSS: Probabilistic Signature Scheme, esquema probabilístico de assinatura.
- MGF1: Mask Generation Function1, geração de máscara.
- SHA256: Secure Hash Algorithm256, resumo de256bits (32bytes).
- MDC/gcd: máximo divisor comum/greatest common divisor.
- Totiente: quantidade de representantes coprimos com o módulo.
- Inverso modular: d que satisfaz e×d≡1 no módulo adotado.
- Maleabilidade: modificar a cifra com efeito relacionado na mensagem.
- Salt: sal, aleatoriedade de PSS; não é senha. Label: rótulo OAEP.
- API: Application Programming Interface, contrato de chamadas.
- Hazmat: hazardous materials, nome da área de primitivas de baixo nível.
- Teste negativo: verifica rejeição, não uma saída válida.
- Sigilo futuro: preservar sessões anteriores após vazamento de chaves de longo prazo;
  transporte de chaves com RSA estático não oferece essa propriedade.

Referências: [RFC8017](https://www.rfc-editor.org/rfc/rfc8017) e
[documentação da biblioteca](https://cryptography.io/en/stable/hazmat/primitives/asymmetric/rsa/).
