"""ClearBank — versão alternativa da análise usando pandas (Requisito Opcional RO1).

Aplica as mesmas regras de validação da solução nativa, agrupa as transações
por mês com groupby e compara as métricas com o relatorio.json gerado pela
solução principal do notebook (os valores devem ser iguais).

Uso: rode o notebook primeiro (ele gera o relatorio.json) e depois
    python analise_pandas.py
"""
import json

import numpy as np
import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"
TIPOS_VALIDOS = ["credito", "debito"]
METRICAS = ["quantidade", "total_credito", "total_debito", "saldo",
            "media", "maior_valor", "menor_valor"]
TOLERANCIA = 0.005  # diferença máxima aceita (meio centavo)


def carregar_dados(caminho=ARQUIVO_CSV):
    """Lê o CSV com pd.read_csv mantendo tudo como texto (vazio continua vazio)."""
    df = pd.read_csv(caminho, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    return df.apply(lambda coluna: coluna.str.strip())


def limpar_dados(df):
    """Aplica as regras da solução nativa. Devolve (validas, quantidade_invalidas)."""
    datas = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    valores = pd.to_numeric(df["valor"], errors="coerce")
    tipos = df["tipo"].str.lower()
    linha_valida = (
        df["id"].str.fullmatch(r"\d+")
        & (df["cliente_id"] != "")
        & (datas.dt.strftime("%Y-%m-%d") == df["data"])   # formato exato AAAA-MM-DD
        & tipos.isin(TIPOS_VALIDOS)
        & np.isfinite(valores)
        & (valores > 0)
    )
    df = df.assign(id=pd.to_numeric(df["id"], errors="coerce"),
                   data=datas, tipo=tipos, valor=valores)
    validas = df[linha_valida]
    validas = validas[~validas["id"].duplicated(keep="first")]  # id repetido = inválido
    return validas, len(df) - len(validas)


def resumo_mensal_pandas(validas):
    """Agrupa por mês (AAAA-MM) com groupby e calcula as mesmas métricas da versão nativa."""
    df = validas.assign(
        mes=validas["data"].dt.strftime("%Y-%m"),
        credito=validas["valor"].where(validas["tipo"] == "credito", 0.0),
        debito=validas["valor"].where(validas["tipo"] == "debito", 0.0),
    )
    resumo = df.groupby("mes").agg(
        quantidade=("valor", "size"),
        total_credito=("credito", "sum"),
        total_debito=("debito", "sum"),
        media=("valor", "mean"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
    )
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
    return resumo[METRICAS].round(2)


def carregar_resumo_nativo(caminho=ARQUIVO_JSON):
    """Lê o relatorio.json da solução nativa e devolve (dados, resumo em DataFrame)."""
    with open(caminho, encoding="utf-8") as arquivo:
        nativo = json.load(arquivo)
    resumo = pd.DataFrame(nativo["resumo_mensal"]).T[METRICAS].astype(float)
    resumo.index.name = "mes"
    return nativo, resumo


def comparar_com_nativo(resumo_pd, validas, invalidas):
    """Compara contagens e métricas mês a mês. Devolve True se forem iguais."""
    try:
        nativo, resumo_nat = carregar_resumo_nativo()
    except FileNotFoundError:
        print(f"'{ARQUIVO_JSON}' não encontrado — execute a solução nativa antes.")
        return False
    print("\n===== COMPARAÇÃO COM A SOLUÇÃO NATIVA =====")
    print(f"Válidas:   pandas {len(validas):>3} | nativo {nativo['total_transacoes_validas']:>3}")
    print(f"Inválidas: pandas {invalidas:>3} | nativo {nativo['total_transacoes_invalidas']:>3}")
    mesmos_meses = list(resumo_pd.index) == list(resumo_nat.index)
    print(f"Meses: {', '.join(resumo_pd.index)} | iguais: {'sim' if mesmos_meses else 'NÃO'}")
    if not mesmos_meses:
        return False
    diferenca = (resumo_pd.astype(float) - resumo_nat).abs().to_numpy().max()
    print(f"Maior diferença entre as métricas: {diferenca:.4f}")
    return (len(validas) == nativo["total_transacoes_validas"]
            and invalidas == nativo["total_transacoes_invalidas"]
            and diferenca < TOLERANCIA)


def exibir_tabela(resumo):
    """Mostra o resumo mensal com valores no padrão brasileiro."""
    def moeda(valor):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    formatos = {coluna: moeda for coluna in METRICAS if coluna != "quantidade"}
    print("\n===== RESUMO MENSAL (pandas) =====")
    print(resumo.to_string(formatters=formatos))


def main():
    try:
        df = carregar_dados()
    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO_CSV}' não encontrado.")
        return
    validas, invalidas = limpar_dados(df)
    print("===== LIMPEZA (pandas) =====")
    print(f"Total de linhas lidas: {len(df)}")
    print(f"Linhas válidas: {len(validas)}")
    print(f"Linhas inválidas: {invalidas}")
    resumo = resumo_mensal_pandas(validas)
    exibir_tabela(resumo)
    if comparar_com_nativo(resumo, validas, invalidas):
        print("✔ Os resultados do pandas são iguais aos da solução nativa.")
    else:
        print("✘ Há diferenças entre pandas e a solução nativa — verifique as regras.")


if __name__ == "__main__":
    main()
