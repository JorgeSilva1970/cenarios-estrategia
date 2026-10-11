from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Result:
    """Saída normalizada de cada modelo: alimenta o ecrã, o dashboard e os relatórios."""
    kpis: list = field(default_factory=list)          # [(rótulo, valor, ajuda)]
    figs: list = field(default_factory=list)          # [(legenda, plotly.Figure)]
    tables: list = field(default_factory=list)        # [(legenda, DataFrame)]
    conclusions: list = field(default_factory=list)   # [str markdown]
    warnings: list = field(default_factory=list)      # [str]


def num(df: pd.DataFrame, cols, lo=None, hi=None):
    """Converte colunas para numérico, preenchendo vazios com 0 e limitando ao intervalo."""
    df = df.copy()
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        if lo is not None or hi is not None:
            df[c] = df[c].clip(lo, hi)
    return df


def clean(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Remove linhas sem texto na coluna-chave."""
    if df is None or df.empty or key not in df:
        return pd.DataFrame(columns=df.columns if df is not None else [])
    m = df[key].astype(str).str.strip().replace({"None": "", "nan": ""}) != ""
    return df[m].reset_index(drop=True)
