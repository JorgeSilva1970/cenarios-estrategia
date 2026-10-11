import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.result import Result, clean, num
from core.theme import SERIES, quad_shapes

DIMS = ["Político", "Económico", "Social", "Tecnológico", "Ecológico", "Legal"]
COLS = ["Dimensão", "Fator", "Impacto", "Incerteza", "Horizonte", "Tendência"]


def classify(df, thr=3.5):
    def f(r):
        if r.Impacto >= thr and r.Incerteza >= thr:
            return "Incerteza crítica"
        if r.Impacto >= thr:
            return "Tendência pesada"
        if r.Incerteza >= thr:
            return "Incerteza secundária"
        return "Fator de contexto"
    df = df.copy()
    df["Classe"] = df.apply(f, axis=1) if len(df) else []
    df["Score"] = df["Impacto"] * df["Incerteza"]
    return df


def analyze(data: dict, thr: float = 3.5) -> Result:
    r = Result()
    df = clean(data["fatores"], "Fator")
    if df.empty:
        r.warnings.append("Sem fatores. Adicione linhas na tabela.")
        return r
    df = num(df, ["Impacto", "Incerteza"], 1, 5)
    df = classify(df, thr).sort_values("Score", ascending=False)

    crit = df[df.Classe == "Incerteza crítica"]
    heavy = df[df.Classe == "Tendência pesada"]
    r.kpis = [("Fatores analisados", len(df), None),
              ("Incertezas críticas", len(crit), "Alto impacto e alta incerteza → eixos de cenários"),
              ("Tendências pesadas", len(heavy), "Alto impacto, previsíveis → presentes em todos os cenários"),
              ("Impacto médio", f"{df.Impacto.mean():.2f}", None)]

    # Dispersão Impacto × Incerteza (jitter determinístico para evitar sobreposição)
    rng = np.random.default_rng(7)
    p = df.copy()
    p["x"] = p.Incerteza + rng.uniform(-0.18, 0.18, len(p))
    p["y"] = p.Impacto + rng.uniform(-0.18, 0.18, len(p))
    cmap = {d: SERIES[i] for i, d in enumerate(DIMS)}
    fig = px.scatter(p, x="x", y="y", color="Dimensão", hover_name="Fator", color_discrete_map=cmap,
                     hover_data={"x": False, "y": False, "Impacto": True, "Incerteza": True, "Classe": True},
                     category_orders={"Dimensão": DIMS})
    fig.update_traces(marker=dict(size=13, line=dict(width=2, color="white")))
    quad_shapes(fig, thr, thr, [0.5, 5.5], [0.5, 5.5],
                {"TR": "Incertezas críticas", "TL": "Tendências pesadas",
                 "BR": "Incertezas secundárias", "BL": "Contexto"})
    fig.update_layout(title="Matriz Impacto × Incerteza", xaxis_title="Incerteza", yaxis_title="Impacto", height=480)
    r.figs.append(("Posicionamento dos fatores PESTEL (passe o rato para ver o fator).", fig))

    g = df.groupby("Dimensão").agg(Impacto=("Impacto", "mean"), Incerteza=("Incerteza", "mean"),
                                   N=("Fator", "count")).reindex([d for d in DIMS if d in set(df["Dimensão"])])
    fig2 = go.Figure()
    fig2.add_bar(x=g.index, y=g.Impacto, name="Impacto médio", marker_color=SERIES[0])
    fig2.add_bar(x=g.index, y=g.Incerteza, name="Incerteza média", marker_color=SERIES[1])
    fig2.update_layout(title="Impacto e incerteza médios por dimensão", barmode="group", yaxis_range=[0, 5], height=380)
    r.figs.append(("Comparação entre dimensões.", fig2))

    r.tables.append(("Ranking de fatores (Score = Impacto × Incerteza)",
                     df[["Dimensão", "Fator", "Impacto", "Incerteza", "Score", "Classe", "Horizonte", "Tendência"]]))

    top_dim = g.Impacto.idxmax()
    r.conclusions.append(f"A dimensão **{top_dim}** concentra o maior impacto médio ({g.Impacto.max():.1f}/5).")
    if len(crit):
        r.conclusions.append("**Incertezas críticas** (candidatas a eixos de cenários): "
                             + "; ".join(crit.Fator.head(4)) + ".")
    else:
        r.conclusions.append("Não há incertezas críticas acima do limiar — reveja o limiar ou as pontuações.")
    if len(heavy):
        r.conclusions.append("**Tendências pesadas** a incorporar em todos os cenários: " + "; ".join(heavy.Fator.head(4)) + ".")
    short = df[(df.Horizonte.astype(str).str.startswith("Curto")) & (df.Impacto >= thr)]
    if len(short):
        r.conclusions.append(f"{len(short)} fator(es) de alto impacto atuam no **curto prazo** e pedem ação imediata: "
                             + "; ".join(short.Fator.head(3)) + ".")
    return r


def critical_uncertainties(data: dict, thr=3.5) -> pd.DataFrame:
    df = clean(data["fatores"], "Fator")
    if df.empty:
        return df
    df = classify(num(df, ["Impacto", "Incerteza"], 1, 5), thr)
    return df[df.Classe == "Incerteza crítica"].sort_values("Score", ascending=False)[["Dimensão", "Fator", "Impacto", "Incerteza"]]
