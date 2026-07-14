# Análise Financeira — ClearBank

Projeto final de análise de transações financeiras com Python. O notebook processa um CSV contendo dados válidos e inválidos, gera métricas mensais, sinaliza valores suspeitos e exporta um relatório JSON.

## Arquivos da entrega

- `desafio-final.ipynb`: notebook autossuficiente, com código e saídas salvas.
- `grafico.png`: gráfico opcional de saldo mensal.
- `README.md`: instruções de execução.

## Como executar

1. Use Python 3.10 ou superior.
2. Crie manualmente um arquivo `transacoes.csv` no mesmo diretório do notebook, com as colunas `id,data,cliente_id,tipo,valor,descricao,categoria`.
3. Abra `desafio-final.ipynb` no Google Colab ou no Jupyter Notebook.

4. Execute todas as células em ordem.

Para gerar novamente o gráfico opcional em ambiente local, instale matplotlib:

   ```bash
   python -m pip install matplotlib
   ```

O notebook lê `transacoes.csv`, exibe o relatório formatado no output, gera `relatorio.json` durante a execução e salva `grafico.png` pela célula opcional.

## Regras da análise

- CSV obrigatório lido com `csv.DictReader`, sem pandas na solução principal.
- Linhas com ID, cliente, data, tipo ou valor inválidos são descartadas sem interromper a execução.
- Uma transação é suspeita quando seu valor é maior que `R$ 10.000,00`.
- O relatório mensal mostra quantidade, créditos, débitos, saldo, média, maior e menor valor.
