"""Plano estratégico: identidade (valores, visão, missão), objetivos SMART, Balanced Scorecard e Mapa Estratégico."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean
from core.theme import MUTED, SERIES, STATUS

PERSP = ["Financeira", "Clientes", "Processos internos", "Aprendizagem e crescimento"]
PQ = {"Financeira": "Para ter sucesso financeiro, como devemos ser vistos pelos acionistas?",
      "Clientes": "Para alcançar a visão, como devemos ser vistos pelos clientes?",
      "Processos internos": "Para satisfazer acionistas e clientes, em que processos temos de ser excelentes?",
      "Aprendizagem e crescimento": "Para alcançar a visão, como sustentamos a capacidade de mudar e melhorar?"}
PCOL = {"Financeira": SERIES[0], "Clientes": SERIES[1], "Processos internos": SERIES[2], "Aprendizagem e crescimento": SERIES[3]}
LEVEL = {p: i for i, p in enumerate(reversed(PERSP))}  # 0 = base (aprendizagem) … 3 = topo (financeira)
SCOL = {"Atingido": STATUS["good"], "Em linha": "#2a78d6", "Em risco": STATUS["critical"], "Sem dados": "#9a9993"}
COLS = ["Código", "Perspetiva", "Objetivo", "Indicador (KPI)", "Unidade", "Sentido", "Base", "Meta", "Atual", "Prazo",
        "Iniciativa", "Responsável", "Origem", "Específico", "Atingível", "Relevante"]


def _txt(v):
    s = str(v).strip()
    return "" if s in ("nan", "None", "NaT") else s


def progress(df):
    """Grau de cumprimento: (atual − base) / (meta − base). Funciona para 'maior é melhor' e 'menor é melhor'."""
    b, m, a = (pd.to_numeric(df[c], errors="coerce") for c in ("Base", "Meta", "Atual"))
    p = (a - b) / (m - b)
    p[(m - b) == 0] = np.nan
    return p.clip(-0.5, 1.5)


def status(p):
    if pd.isna(p):
        return "Sem dados"
    if p >= 1:
        return "Atingido"
    if p >= 0.5:
        return "Em linha"
    return "Em risco"


def smart(df):
    """Verificação SMART (Doran, 1981): M e T calculados; E, A e R declarados pela equipa."""
    out = pd.DataFrame({"Código": df["Código"], "Objetivo": df["Objetivo"]})
    out["Específico"] = df["Específico"].fillna(False).astype(bool)
    out["Mensurável"] = df["Indicador (KPI)"].map(_txt).ne("") & pd.to_numeric(df["Meta"], errors="coerce").notna()
    out["Atingível"] = df["Atingível"].fillna(False).astype(bool)
    out["Relevante"] = df["Relevante"].fillna(False).astype(bool)
    out["Temporal"] = pd.to_numeric(df["Prazo"], errors="coerce").notna()
    out["Score SMART"] = out[["Específico", "Mensurável", "Atingível", "Relevante", "Temporal"]].sum(axis=1)
    return out


def analyze(data: dict, context: dict | None = None) -> Result:
    """context (opcional): {'tows': DataFrame de estratégias TOWS, 'roles': lista de papéis da RAM}."""
    r = Result()
    context = context or {}
    ide = clean(data["identidade"], "Declaração")
    obj = clean(data["objetivos"], "Objetivo")
    lig = clean(data["ligacoes"], "De")

    vals = ide[ide["Elemento"] == "Valor"]
    vis = ide[ide["Elemento"] == "Visão"]
    mis = ide[ide["Elemento"] == "Missão"]
    if vis.empty:
        r.warnings.append("Falta a **visão**: onde vê a organização daqui a 2, 5 ou mais anos (seja realista).")
    if mis.empty:
        r.warnings.append("Falta a **missão**: o que a organização faz, hoje, e para quem.")
    if vals.empty:
        r.warnings.append("Faltam os **valores**: se não forem claros, faça um brainstorming com a equipa.")
    if obj.empty:
        r.warnings.append("Sem objetivos no Balanced Scorecard.")
        return r

    obj["Código"] = obj["Código"].map(_txt)
    obj["% cumprimento"] = progress(obj)
    obj["Estado"] = obj["% cumprimento"].map(status)
    sm = smart(obj)
    obj["Score SMART"] = sm["Score SMART"].values

    n_ok = int((obj["Estado"] == "Atingido").sum())
    n_risk = int((obj["Estado"] == "Em risco").sum())
    avg = obj["% cumprimento"].clip(0, 1).mean()
    r.kpis = [("Objetivos estratégicos", len(obj), None),
              ("Cumprimento médio", f"{avg:.0%}" if pd.notna(avg) else "–", "Média de (atual − base) / (meta − base), limitada a 100%"),
              ("Atingidos / em risco", f"{n_ok} / {n_risk}", None),
              ("Objetivos 100% SMART", f"{int((sm['Score SMART'] == 5).sum())} de {len(sm)}", "Específico, Mensurável, Atingível, Relevante, Temporal")]

    # ---------- Mapa estratégico ----------
    pos = {}
    fig = go.Figure()
    for p in PERSP:
        lv = LEVEL[p]
        fig.add_shape(type="rect", x0=0, x1=1, y0=lv, y1=lv + 1, fillcolor=PCOL[p], opacity=0.10, line=dict(color="white", width=3),
                      layer="below")
        fig.add_annotation(x=0.01, y=lv + 0.93, text=f"<b>{p}</b>", showarrow=False, xanchor="left", yanchor="top",
                           font=dict(size=12, color="#0b0b0b"))
        sub = obj[obj["Perspetiva"] == p]
        for i, (_, o) in enumerate(sub.iterrows()):
            x = 0.18 + (i + 0.5) * (0.80 / max(len(sub), 1))
            pos[o["Código"]] = (x, lv + 0.45)
    arrows_back = []
    for _, l in lig.iterrows():
        a, b = _txt(l["De"]), _txt(l["Para"])
        if a in pos and b in pos and a != b:
            (x0, y0), (x1, y1) = pos[a], pos[b]
            back = y1 < y0
            if back:
                arrows_back.append(f"{a} → {b}")
            if y1 > y0:
                tail, head = (x0, y0 + 0.17), (x1, y1 - 0.17)
            elif y1 < y0:
                tail, head = (x0, y0 - 0.17), (x1, y1 + 0.17)
            else:
                sgn = 1 if x1 > x0 else -1
                tail, head = (x0 + 0.12 * sgn, y0), (x1 - 0.12 * sgn, y1)
            fig.add_annotation(x=head[0], y=head[1], ax=tail[0], ay=tail[1], xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=1.6,
                               arrowcolor=STATUS["critical"] if back else "#6f6e69", opacity=0.9)
    for _, o in obj.iterrows():
        if o["Código"] not in pos:
            continue
        x, y = pos[o["Código"]]
        pct = o["% cumprimento"]
        lab = f"<b>{o['Código']}</b> {_short(o['Objetivo'])}<br><span style='font-size:10px'>{o['Estado']}" + \
              (f" · {pct:.0%}" if pd.notna(pct) else "") + "</span>"
        fig.add_annotation(x=x, y=y, text=lab, showarrow=False, bgcolor="white", bordercolor=SCOL[o["Estado"]], borderwidth=2.5,
                           borderpad=5, font=dict(size=11, color="#0b0b0b"))
    fig.add_scatter(x=[p[0] for p in pos.values()], y=[p[1] for p in pos.values()], mode="markers", marker=dict(size=1, opacity=0),
                    hoverinfo="skip", showlegend=False)
    for st_, c in SCOL.items():
        fig.add_scatter(x=[None], y=[None], mode="markers", marker=dict(size=12, color="white", line=dict(width=3, color=c),
                                                                        symbol="square"), name=st_)
    vtxt = _txt(vis.iloc[0]["Declaração"]) if len(vis) else "Visão por definir"
    fig.update_layout(title=dict(text=f"Mapa Estratégico<br><sup>Visão: {_short(vtxt, 150)}</sup>"), height=660,
                      xaxis=dict(visible=False, range=[0, 1]), yaxis=dict(visible=False, range=[0, 4]),
                      plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=-0.04))
    r.figs.append(("Mapa Estratégico (Kaplan & Norton): relações causa-efeito de baixo (aprendizagem) para cima (financeira). "
                   "Cor da moldura = estado do indicador; seta vermelha = ligação no sentido inverso.", fig))

    # ---------- Cumprimento das metas ----------
    d = obj.copy()
    d["ord"] = d["Perspetiva"].map({p: i for i, p in enumerate(PERSP)})
    d = d.sort_values(["ord", "Código"], ascending=[False, False])
    pct = d["% cumprimento"].fillna(0).clip(0, 1.2) * 100
    bar = go.Figure(go.Bar(
        y=[f"{c} · {_short(o, 40)}" for c, o in zip(d["Código"], d["Objetivo"])], x=pct, orientation="h",
        marker_color=[SCOL[s] for s in d["Estado"]],
        text=[f"{s} · {v:.0f}%" if s != "Sem dados" else "Sem dados" for s, v in zip(d["Estado"], pct)], textposition="outside",
        customdata=d[["Indicador (KPI)", "Base", "Meta", "Atual", "Unidade"]].astype(str).values,
        hovertemplate="%{y}<br>%{customdata[0]}<br>Base %{customdata[1]} → Meta %{customdata[2]} · Atual %{customdata[3]} "
                      "%{customdata[4]}<extra></extra>"))
    bar.add_vline(x=100, line_dash="dot", line_color=MUTED)
    bar.update_layout(title="Cumprimento das metas (KPI): (atual − base) / (meta − base)", xaxis=dict(range=[0, 145], ticksuffix="%"),
                      height=max(360, 34 * len(d) + 120), yaxis=dict(automargin=True))
    r.figs.append(("Verde = meta atingida · azul = em linha (≥ 50%) · vermelho = em risco · cinzento = sem dados.", bar))

    g = obj.groupby("Perspetiva").agg(N=("Objetivo", "count"),
                                      Cumprimento=("% cumprimento", lambda s: s.clip(0, 1).mean())).reindex(PERSP)
    bal = go.Figure(go.Bar(x=g.index, y=(g["Cumprimento"].fillna(0) * 100), marker_color=[PCOL[p] for p in g.index],
                           text=[f"{int(n) if pd.notna(n) else 0} obj. · {c:.0%}" if pd.notna(c) else f"{int(n) if pd.notna(n) else 0} obj."
                                 for n, c in zip(g["N"], g["Cumprimento"])], textposition="outside"))
    bal.update_layout(title="Equilíbrio do scorecard: cumprimento médio por perspetiva", yaxis=dict(range=[0, 115], ticksuffix="%"),
                      height=360)
    r.figs.append(("Um scorecard equilibrado tem objetivos nas quatro perspetivas.", bal))

    crit = ["Específico", "Mensurável", "Atingível", "Relevante", "Temporal"]
    z = sm[crit].astype(int).values
    heat = go.Figure(go.Heatmap(z=z, x=crit, y=[f"{c} · {_short(o, 32)}" for c, o in zip(sm["Código"], sm["Objetivo"])],
                                colorscale=[[0, "#f6c6c5"], [1, "#c8eedd"]], zmin=0, zmax=1, showscale=False, xgap=3, ygap=3,
                                text=np.where(z == 1, "✓", "✗"), texttemplate="%{text}",
                                hovertemplate="%{y}<br>%{x}: %{text}<extra></extra>"))
    heat.update_layout(title="Verificação SMART dos objetivos", height=max(320, 30 * len(sm) + 120),
                       yaxis=dict(autorange="reversed", automargin=True), xaxis=dict(side="top"))
    r.figs.append(("Mensurável = tem indicador e meta numérica; Temporal = tem prazo; os restantes são declarados pela equipa.", heat))

    # ---------- Tabelas ----------
    idt = ide[["Elemento", "Declaração"] + (["Descrição"] if "Descrição" in ide else [])]
    r.tables.append(("Identidade estratégica: valores, visão e missão", idt))
    t = obj[["Perspetiva", "Código", "Objetivo", "Indicador (KPI)", "Unidade", "Base", "Meta", "Atual", "% cumprimento", "Estado",
             "Prazo", "Iniciativa", "Responsável", "Origem"]].copy()
    t["% cumprimento"] = (t["% cumprimento"] * 100).round(0)
    r.tables.append(("Balanced Scorecard: objetivos, indicadores, metas e iniciativas", t))
    r.tables.append(("Verificação SMART", sm))

    # ---------- Conclusões ----------
    if len(vis) and len(mis):
        r.conclusions.append(f"**Visão:** {_txt(vis.iloc[0]['Declaração'])}  \n**Missão:** {_txt(mis.iloc[0]['Declaração'])}")
    if len(vals):
        r.conclusions.append("**Valores:** " + "; ".join(vals["Declaração"].map(_txt)) + ".")
    missing = [p for p in PERSP if p not in set(obj["Perspetiva"])]
    if missing:
        r.conclusions.append("⚠️ Scorecard desequilibrado — perspetivas sem objetivos: " + ", ".join(missing) + ".")
    else:
        r.conclusions.append("O scorecard cobre as **quatro perspetivas** (financeira, clientes, processos, aprendizagem).")
    if pd.notna(avg):
        r.conclusions.append(f"Cumprimento médio das metas: **{avg:.0%}** — {n_ok} atingida(s) e {n_risk} em risco.")
    risk = obj[obj["Estado"] == "Em risco"]
    if len(risk):
        r.conclusions.append("**Objetivos em risco** (reforçar as iniciativas): "
                             + "; ".join(f"{c} {o}" for c, o in zip(risk["Código"], risk["Objetivo"])) + ".")
    weak = sm[sm["Score SMART"] < 5]
    if len(weak):
        r.conclusions.append("Objetivos **não SMART** a reformular: " + "; ".join(
            f"{c} (falta: {', '.join(k for k in crit if not row[k])})" for c, (_, row) in zip(weak["Código"], weak.iterrows())) + ".")
    noinit = obj[obj["Iniciativa"].map(_txt).eq("")]
    noown = obj[obj["Responsável"].map(_txt).eq("")]
    if len(noinit):
        r.conclusions.append("Objetivos **sem iniciativa** (ação que garante a meta): " + ", ".join(noinit["Código"]) + ".")
    if len(noown):
        r.conclusions.append("Objetivos **sem responsável** (quem apoia e suporta o objetivo): " + ", ".join(noown["Código"]) + ".")
    roles = context.get("roles")
    if roles:
        ext = sorted({_txt(x) for x in obj["Responsável"]} - set(roles) - {""})
        if ext:
            r.conclusions.append("Responsáveis que não constam da RAM (acrescentar papel ou corrigir): " + ", ".join(ext) + ".")
    linked = set(lig["De"].map(_txt)) | set(lig["Para"].map(_txt))
    orphans = [c for c in obj["Código"] if c not in linked]
    if orphans and len(lig):
        r.conclusions.append("Objetivos **isolados** no mapa estratégico (sem relação causa-efeito): " + ", ".join(orphans) + ".")
    if arrows_back:
        r.warnings.append("Ligações no sentido inverso ao mapa estratégico (deviam ir da base para o topo): " + ", ".join(arrows_back))
    b_, m_ = pd.to_numeric(obj["Base"], errors="coerce"), pd.to_numeric(obj["Meta"], errors="coerce")
    incoh = obj[((obj["Sentido"] == "↑") & (m_ < b_)) | ((obj["Sentido"] == "↓") & (m_ > b_))]
    if len(incoh):
        r.warnings.append("Sentido do indicador incoerente com a meta (↑ exige meta > base; ↓ exige meta < base): "
                          + ", ".join(incoh["Código"]))
    tows = context.get("tows")
    if tows is not None and not tows.empty:
        tw = clean(tows, "Estratégia")
        pr1 = tw[pd.to_numeric(tw["Prioridade"], errors="coerce") == 1]["Estratégia"].map(_txt)
        used = set(obj["Origem"].map(_txt))
        miss = [s for s in pr1 if s not in used]
        if miss:
            r.conclusions.append("Estratégias TOWS de prioridade 1 **sem objetivo no scorecard**: " + "; ".join(miss) + ".")
        elif len(pr1):
            r.conclusions.append("Todas as estratégias TOWS de prioridade 1 estão traduzidas em objetivos do scorecard.")
    return r


def _short(t, n=34):
    t = _txt(t)
    return t if len(t) <= n else t[: n - 1] + "…"
