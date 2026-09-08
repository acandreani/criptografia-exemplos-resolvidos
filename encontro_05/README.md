# Encontro 5 — Cifras de bloco e redes de Feistel

Este diretório contém as implementações resolvidas usadas para acompanhar
os exemplos do Encontro 5. Execute os comandos abaixo a partir desta pasta.

```bash
python exemplos_resolvidos/exemplos_passo_a_passo.py
python exemplos_resolvidos/experimentar.py --bloco 0x1234 \
  --subchaves 3 17 91 201 --mostrar-rodadas
python -m unittest discover -s exemplos_resolvidos -p "test_*.py" -v
```

O código implementa uma rede de Feistel pequena, deliberadamente didática. A
função de rodada usa `F(R,K) = (R + K) mod 2^n`; isso facilita as contas, mas
não cria uma cifra segura. O experimento de avalanche observa diferenças entre
entradas próximas, sem transformar essa observação em prova de segurança.
