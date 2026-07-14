"""Extras opcionais: conferência da análise com pandas e gráfico mensal."""

import math
import os
import json
from datetime import date
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".matplotlib"))

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LIMITE_SUSPEITO = 10000.00


def gerar_relatorio_pandas(caminho: str | Path) -> dict:
    """Lê, valida e agrega o CSV com pandas, isoladamente da solução obrigatória."""
    dados = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    total_lido = len(dados)
    dados["id_limpo"] = pd.to_numeric(dados["id"].str.strip(), errors="coerce")
    dados["data_limpa"] = pd.to_datetime(dados["data"].str.strip(), format="%Y-%m-%d", errors="coerce")
    dados["valor_limpo"] = pd.to_numeric(dados["valor"].str.strip(), errors="coerce")
    dados["tipo_limpo"] = dados["tipo"].str.strip().str.lower()
    dados["cliente_limpo"] = dados["cliente_id"].str.strip()

    validas = dados.loc[
        dados["id_limpo"].notna()
        & dados["data_limpa"].notna()
        & dados["valor_limpo"].notna()
        & (dados["valor_limpo"] > 0)
        & dados["cliente_limpo"].ne("")
        & dados["tipo_limpo"].isin(["credito", "debito"])
    ].copy()
    validas["mes"] = validas["data_limpa"].dt.strftime("%Y-%m")

    resumo_mensal = {}
    for mes, grupo in validas.groupby("mes", sort=True):
        valores = grupo["valor_limpo"]
        creditos = grupo.loc[grupo["tipo_limpo"] == "credito", "valor_limpo"].sum()
        debitos = grupo.loc[grupo["tipo_limpo"] == "debito", "valor_limpo"].sum()
        resumo_mensal[mes] = {
            "quantidade": int(len(grupo)),
            "total_credito": float(creditos),
            "total_debito": float(debitos),
            "saldo": float(creditos - debitos),
            "media": float(valores.mean()),
            "maior_valor": float(valores.max()),
            "menor_valor": float(valores.min()),
        }

    inicio = validas["data_limpa"].min()
    fim = validas["data_limpa"].max()
    suspeitas = validas.loc[validas["valor_limpo"] > LIMITE_SUSPEITO]
    return {
        "gerado_em": date.today().isoformat(),
        "total_transacoes_validas": int(len(validas)),
        "total_transacoes_invalidas": int(total_lido - len(validas)),
        "periodo": {
            "inicio": inicio.strftime("%Y-%m-%d") if pd.notna(inicio) else None,
            "fim": fim.strftime("%Y-%m-%d") if pd.notna(fim) else None,
            "dias": int((fim - inicio).days) if pd.notna(inicio) and pd.notna(fim) else 0,
        },
        "resumo_mensal": resumo_mensal,
        "transacoes_suspeitas": [
            {
                "id": int(linha.id_limpo),
                "cliente_id": linha.cliente_limpo,
                "data": linha.data_limpa.strftime("%Y-%m-%d"),
                "valor": float(linha.valor_limpo),
            }
            for linha in suspeitas.itertuples()
        ],
    }


def comparar_relatorios(nativo: dict, pandas: dict) -> bool:
    """Compara os resultados obrigatórios, tolerando diferenças de ponto flutuante."""
    campos = ["total_transacoes_validas", "total_transacoes_invalidas", "periodo", "transacoes_suspeitas"]
    if any(nativo[campo] != pandas[campo] for campo in campos):
        return False
    if nativo["resumo_mensal"].keys() != pandas["resumo_mensal"].keys():
        return False
    for mes, metricas_nativas in nativo["resumo_mensal"].items():
        metricas_pandas = pandas["resumo_mensal"][mes]
        for campo, valor_nativo in metricas_nativas.items():
            if not math.isclose(valor_nativo, metricas_pandas[campo], rel_tol=1e-9, abs_tol=1e-9):
                return False
    return True


def gerar_grafico(relatorio: dict, caminho: str | Path = "grafico.png") -> None:
    """Salva um gráfico de barras com o saldo de cada mês."""
    meses = list(relatorio["resumo_mensal"])
    saldos = [relatorio["resumo_mensal"][mes]["saldo"] for mes in meses]
    figura, eixo = plt.subplots(figsize=(8, 4.5))
    eixo.bar(meses, saldos, color="#147d64", label="Saldo mensal")
    eixo.set_title("Saldo mensal da ClearBank")
    eixo.set_xlabel("Mês")
    eixo.set_ylabel("Saldo (R$)")
    eixo.legend()
    eixo.axhline(0, color="#333333", linewidth=0.8)
    figura.tight_layout()
    figura.savefig(caminho, dpi=150)
    plt.close(figura)


if __name__ == "__main__":
    relatorio_pandas = gerar_relatorio_pandas("transacoes.csv")
    with open("relatorio.json", encoding="utf-8") as arquivo:
        relatorio_nativo = json.load(arquivo)
    gerar_grafico(relatorio_pandas)
    if comparar_relatorios(relatorio_nativo, relatorio_pandas):
        print("Resultados do pandas conferem com a solução nativa.")
    else:
        print("Os resultados do pandas divergem da solução nativa.")
    print("Gráfico salvo em grafico.png.")
