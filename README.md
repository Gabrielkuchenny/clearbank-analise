# ClearBank — Análise Financeira com Python

Desafio final do módulo de Python para análise de dados. O notebook lê o histórico de transações exportado pela equipe de operações da ClearBank (`transacoes.csv`), descarta os registros com problema, calcula métricas financeiras por mês, sinaliza transações suspeitas e gera um relatório no terminal e em JSON.

## O que o notebook faz

- **Leitura** do CSV com o módulo nativo `csv` (`csv.DictReader`), tratando arquivo inexistente.
- **Validação e limpeza**: descarta, sem interromper o programa, linhas com `id` vazio, não numérico ou duplicado, `cliente_id` vazio, data fora do formato AAAA-MM-DD, `tipo` diferente de `credito`/`debito` e `valor` não numérico ou menor/igual a zero.
- **Datas** com `datetime`: conversão com `strptime`, extração do mês (AAAA-MM) e cálculo dos dias entre a transação mais antiga e a mais recente.
- **Métricas mensais**: quantidade, total de crédito, total de débito, saldo, média, maior e menor valor.
- **Transações suspeitas**: valores acima de `LIMITE_SUSPEITO = 10000.00`.
- **Relatório** formatado no terminal (padrão brasileiro, `R$ 1.234,56`) e exportado para `relatorio.json`.
- **Opcional RO1**: `analise_pandas.py` refaz a leitura e o agrupamento com `pd.read_csv` e `groupby` e confere que os valores são iguais aos da solução nativa.
- **Opcional RO2**: `grafico.png` com o saldo mensal (crédito − débito) em barras, feito com matplotlib.

## Como executar

**Google Colab**
1. Abra o `desafio-final.ipynb` no Colab (*Arquivo → Fazer upload de notebook* ou *Abrir notebook → GitHub*).
2. Clique em *Ambiente de execução → Executar tudo*.

**Jupyter local** (Python 3.10 ou superior)
```bash
pip install notebook pandas matplotlib
jupyter notebook desafio-final.ipynb
```
Depois, *Run → Run All Cells*.

A primeira célula de código cria o `transacoes.csv` de teste. Para analisar outro arquivo, coloque-o na mesma pasta com esse nome e pule essa célula. As células devem ser executadas em ordem; a **Célula de Execução Principal** (seção 8) roda a análise completa de uma vez.

## Saídas

| Arquivo | Conteúdo |
|---|---|
| saída da seção 8 | resumo da limpeza, período analisado, relatório mensal e transações suspeitas |
| `relatorio.json` | data de geração, totais de válidas/inválidas, período, resumo mensal e lista de suspeitas |
| `grafico.png` | saldo mensal em barras (azul positivo, vermelho negativo) |

## Dados de teste

O `transacoes.csv` tem 30 registros: 20 válidos entre janeiro e abril de 2026 e 10 inválidos, cobrindo cada regra de validação (incluindo um registro duplicado). Três transações passam de R$ 10.000,00 e uma tem exatamente R$ 10.000,00, para testar a borda do limite.

## Estrutura

```
clearbank-analise/
├── desafio-final.ipynb   # notebook com o código e as saídas salvas
├── transacoes.csv        # dados de entrada de teste
├── analise_pandas.py     # versão com pandas (opcional RO1)
├── relatorio.json        # relatório gerado pelo notebook
├── grafico.png           # gráfico do saldo mensal (opcional RO2)
└── README.md
```
