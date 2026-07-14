# Análise Financeira - ClearBank

Este é o projeto final do módulo de Python. O notebook lê um arquivo CSV de transações, ignora linhas com erro e mostra um resumo por mês.

## Arquivos

- `desafio-final.ipynb`: notebook principal.
- `analise_pandas.py`: versão opcional com pandas.
- `grafico.png`: gráfico de saldo mensal.

## Como executar

1. Crie o arquivo `transacoes.csv` na mesma pasta do notebook.
2. O CSV precisa ter as colunas: `id,data,cliente_id,tipo,valor,descricao,categoria`.
3. Abra `desafio-final.ipynb` no Google Colab ou no Jupyter Notebook.
4. Rode todas as células em ordem.

## O que é gerado pelo notebook

- Um relatório no próprio notebook.
- O arquivo `relatorio.json`.
- O arquivo `grafico.png`.

## Extras

Para rodar a comparação com pandas depois de executar o notebook:

```bash
pip install pandas matplotlib
python analise_pandas.py
```
