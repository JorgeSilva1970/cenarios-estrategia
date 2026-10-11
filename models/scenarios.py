import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean, num
from core.theme import DIV, MUTED, SERIES, STATUS

QUADS = ["Q1", "Q2", "Q3", "Q4"]
QPOS = {"Q1": ("+", "+"), "Q2": ("−", "+"), "Q3": ("−", "−"), "Q4": ("+", "−")}  # (X, Y)
QXY = {"Q1": (1, 1), "Q2": (-1, 1), "Q3": (-1, -1), "Q4": (1, -1)}


def names(data):
    c = data["cenarios"].set_index("Quadrante")
    return {q: (str(c.loc[q, "Nome"]) if q in c.index and str(c.loc[q, "Nome"]).strip() not in ("", "nan", "None") else q)
            for q in QUADS}


def quadrant_of(x, y):
    x, y = float(x), float(y)
    if x >= 0 and y >= 0:
        return "Q1"
    if x < 0 and y >= 0:
        return "Q2"
    if x < 0:
        return "Q3"
    return "Q4"


def positions(data):
    """Posição atual e esperada no horizonte (exercício de posicionamento — SME Strategy)."""
    p = data.get("posicao")
    if p is None or p.empty:
        return None
    p = num(clean(p, "Momento"), ["X (−1 a +1)", "Y (−1 a +1)"], -1, 1)
    return p if len(p) else None


def robustness(data):
    s = clean(data["estrategias"], "Estratégia")
    if s.empty:
        return s
    s = num(s, QUADS, -2, 2)
    c = data["cenarios"].set_index("Quadrante")
    p = pd.to_numeric(c.reindex(QUADS)["Probabilidade (%)"], errors="coerce").fillna(25).values
    p = p / p.sum() if p.sum() > 0 else np.full(4, 0.25)
    v = s[QUADS].values
    s["Média"] = v.mean(1).round(2)
    s["Mínimo"] = v.min(1)
    s["Máximo"] = v.max(1)
    s["Valor esperado"] = (v @ p).round(2)
    s["Arrependimento máx."] = (v.max(0) - v).max(1)  # regret minimax (Savage)

    def cls(r):
        if r["Mínimo"] >= 0 and r["Média"] >= 1:
            return "Robusta (no-regret)"
        if r["Mínimo"] >= -1 and r["Média"] > 0:
            return "Condicional (hedge)"
        return "Aposta arriscada"
    s["Classificação"] = s.apply(cls, axis=1)
    return s


def analyze(data: dict) -> Result:
    r = Result()
    ax = data["eixos"].set_index("Eixo")
    nm = names(data)
    cen = data["cenarios"].set_index("Quadrante").reindex(QUADS)
    X, Y = ax.loc["X"], ax.loc["Y"]

    # Matriz 2×2
    fig = go.Figure()
    for i, q in enumerate(QUADS):
        xs = [0, 1] if QXY[q][0] > 0 else [-1, 0]
        ys = [0, 1] if QXY[q][1] > 0 else [-1, 0]
        fig.add_shape(type="rect", x0=xs[0], x1=xs[1], y0=ys[0], y1=ys[1], line=dict(color="white", width=4),
                      fillcolor=SERIES[i], opacity=0.16, layer="below")
        prob = cen.loc[q, "Probabilidade (%)"]
        narr = str(cen.loc[q, "Narrativa"])
        fig.add_annotation(x=np.mean(xs), y=np.mean(ys) + 0.18, text=f"<b>{nm[q]}</b>", showarrow=False,
                           font=dict(size=16, color="#0b0b0b"))
        fig.add_annotation(x=np.mean(xs), y=np.mean(ys) - 0.12,
                           text=_wrap(narr, 42, 4) + (f"<br><i>Prob. subjetiva: {prob}%</i>" if pd.notna(prob) else ""),
                           showarrow=False, font=dict(size=11, color=MUTED))
    fig.add_annotation(x=1, y=0, text=f"{X['Polo +']} ▶", showarrow=False, xanchor="right", yanchor="bottom", font=dict(size=12))
    fig.add_annotation(x=-1, y=0, text=f"◀ {X['Polo −']}", showarrow=False, xanchor="left", yanchor="bottom", font=dict(size=12))
    fig.add_annotation(x=0, y=1, text=f"▲ {Y['Polo +']}", showarrow=False, yanchor="top", xanchor="left", font=dict(size=12))
    fig.add_annotation(x=0, y=-1, text=f"▼ {Y['Polo −']}", showarrow=False, yanchor="bottom", xanchor="left", font=dict(size=12))
    fig.add_hline(y=0, line_color=MUTED, line_width=2)
    fig.add_vline(x=0, line_color=MUTED, line_width=2)
    pos = positions(data)
    if pos is not None:
        xs, ys = list(pos["X (−1 a +1)"]), list(pos["Y (−1 a +1)"])
        lab = [f"{m} ({int(a)})" if pd.notna(pd.to_numeric(a, errors="coerce")) else str(m)
               for m, a in zip(pos["Momento"], pos.get("Ano", [""] * len(pos)))]
        for i in range(len(xs) - 1):
            fig.add_annotation(x=xs[i + 1], y=ys[i + 1], ax=xs[i], ay=ys[i], xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowsize=1.4, arrowwidth=3, arrowcolor="#0b0b0b", opacity=0.85)
        fig.add_scatter(x=xs, y=ys, mode="markers+text", text=lab, textposition="bottom center", showlegend=False,
                        marker=dict(size=16, color=["#ffffff"] + ["#0b0b0b"] * (len(xs) - 1), line=dict(width=3, color="#0b0b0b")),
                        textfont=dict(size=12, color="#0b0b0b"), hovertemplate="%{text}<br>X %{x:+.2f} · Y %{y:+.2f}<extra></extra>")
    fig.update_layout(title=f"Eixo X: {X['Incerteza']}  ·  Eixo Y: {Y['Incerteza']}", height=620,
                      xaxis=dict(visible=False, range=[-1.02, 1.02]), yaxis=dict(visible=False, range=[-1.02, 1.02]),
                      plot_bgcolor="rgba(0,0,0,0)")
    r.figs.append(("Matriz de cenários 2×2 (Schwartz / Shell). Círculo branco = onde estamos hoje; seta = trajetória "
                   "esperada até ao horizonte (exercício de posicionamento, SME Strategy).", fig))

    s = robustness(data)
    if not s.empty:
        z = s[QUADS].values
        heat = go.Figure(go.Heatmap(z=z, x=[nm[q] for q in QUADS], y=s["Estratégia"], colorscale=DIV, zmin=-2, zmax=2,
                                    text=z.astype(int), texttemplate="%{text:+d}",
                                    hovertemplate="%{y}<br>%{x}: %{z:+d}<extra></extra>",
                                    colorbar=dict(title="Desempenho", tickvals=[-2, -1, 0, 1, 2])))
        heat.update_layout(title="Wind tunneling: desempenho de cada estratégia em cada cenário",
                           height=max(320, 60 * len(s) + 140), yaxis=dict(autorange="reversed", automargin=True),
                           xaxis=dict(side="top", tickangle=0))
        r.figs.append(("Vermelho = a estratégia falha nesse futuro; azul = a estratégia prospera.", heat))

        col = {"Robusta (no-regret)": STATUS["good"], "Condicional (hedge)": STATUS["warning"], "Aposta arriscada": STATUS["critical"]}
        ss = s.sort_values("Média")
        bar = go.Figure(go.Bar(y=ss["Estratégia"], x=ss["Média"], orientation="h",
                               marker_color=[col[c] for c in ss["Classificação"]],
                               error_x=dict(type="data", symmetric=False, array=ss["Máximo"] - ss["Média"],
                                            arrayminus=ss["Média"] - ss["Mínimo"], color=MUTED),
                               text=ss["Classificação"], textposition="outside",
                               hovertemplate="%{y}<br>Média %{x:.2f}<extra></extra>"))
        bar.update_layout(title="Robustez: média e amplitude (mín.–máx.) entre cenários", xaxis_range=[-2.5, 4.2],
                          height=max(300, 55 * len(s) + 120), yaxis=dict(automargin=True))
        r.figs.append(("Barras = desempenho médio; traço = do pior ao melhor cenário.", bar))

        r.tables.append(("Matriz de robustez", s.rename(columns={q: nm[q] for q in QUADS})))
        rob = s[s["Classificação"].str.startswith("Robusta")]
        r.kpis = [("Cenários", 4, None), ("Estratégias testadas", len(s), None),
                  ("Estratégias robustas", len(rob), "Mínimo ≥ 0 e média ≥ 1"),
                  ("Melhor valor esperado", f'{s["Valor esperado"].max():+.2f}', s.loc[s["Valor esperado"].idxmax(), "Estratégia"])]
        if len(rob):
            r.conclusions.append("**Estratégias robustas (no-regret)** a implementar já: " + "; ".join(rob["Estratégia"]) + ".")
        else:
            r.conclusions.append("Nenhuma estratégia é robusta em todos os cenários — combine opções num portefólio.")
        bets = s[s["Classificação"] == "Aposta arriscada"]
        for _, b in bets.iterrows():
            good = [nm[q] for q in QUADS if b[q] > 0] or [nm[max(QUADS, key=lambda q: b[q])]]
            badq = [nm[q] for q in QUADS if b[q] < 0]
            r.conclusions.append(f"**{b['Estratégia']}** é uma aposta: compensa em *{', '.join(good)}*"
                                 + (f" mas falha em *{', '.join(badq)}*" if badq else "")
                                 + "; ativar apenas se os sinais de alerta desses cenários se confirmarem.")
        mm = s.loc[s["Arrependimento máx."].idxmin()]
        r.conclusions.append(f"Pelo critério minimax-regret (Savage), a opção mais prudente é **{mm['Estratégia']}** "
                             f"(arrependimento máximo {mm['Arrependimento máx.']:.0f}).")
        worst = min(QUADS, key=lambda q: s[q].mean())
        r.conclusions.append(f"O cenário mais desafiante para o portefólio atual é **{nm[worst]}** "
                             f"(desempenho médio {s[worst].mean():+.2f}) — prepare um plano de contingência.")

    cols = [c for c in ["Quadrante", "Nome", "Narrativa", "Implicações e ações", "Sinais de alerta", "Probabilidade (%)"]
            if c in cen.reset_index().columns]
    t = cen.reset_index()[cols]
    t.insert(1, "Posição (X,Y)", [f"X{QPOS[q][0]} / Y{QPOS[q][1]}" for q in QUADS])
    r.tables.insert(0, ("Narrativas, implicações e sinais de alerta", t))

    # Posicionamento e trajetória (passo 4 do processo SME Strategy)
    if pos is not None and len(pos) >= 1:
        q0 = quadrant_of(pos.iloc[0]["X (−1 a +1)"], pos.iloc[0]["Y (−1 a +1)"])
        msg = f"**Posição atual** ({pos.iloc[0]['Momento']}): mais próxima do cenário *{nm[q0]}*"
        if len(pos) >= 2:
            q1 = quadrant_of(pos.iloc[-1]["X (−1 a +1)"], pos.iloc[-1]["Y (−1 a +1)"])
            if q1 != q0:
                msg += (f"; a trajetória esperada aponta para *{nm[q1]}* no horizonte — prioridade aos sinais de alerta e às "
                        f"implicações desse cenário.")
            else:
                msg += f"; a trajetória esperada mantém-se em *{nm[q0]}* até ao horizonte."
        r.conclusions.insert(0, msg.rstrip(".") + ".")
        try:
            anos = pd.to_numeric(pos["Ano"], errors="coerce").dropna()
            if len(anos) >= 2:
                h = int(anos.iloc[-1] - anos.iloc[0])
                r.kpis.insert(0, ("Horizonte", f"{h} anos", "SME Strategy recomenda 1–3 anos para PME; setores de ciclo longo usam 5–10+"))
        except (KeyError, ValueError):
            pass

    # Armadilhas a evitar (SME Strategy)
    probs = pd.to_numeric(cen["Probabilidade (%)"], errors="coerce").fillna(0)
    if probs.sum() > 0 and probs.max() / probs.sum() > 0.5:
        r.warnings.append(f"Um cenário concentra {probs.max() / probs.sum():.0%} da probabilidade — evite construir a estratégia "
                          "à volta de um único futuro: o objetivo é uma estratégia que resista aos quatro.")
    if "Implicações e ações" in cen.columns:
        miss = [nm[q] for q in QUADS if str(cen.loc[q, "Implicações e ações"]).strip() in ("", "nan", "None")]
        if miss:
            r.warnings.append("Discuta as implicações de todos os cenários, incluindo os menos prováveis. Em falta: " + ", ".join(miss))

    # Casos por fator: business as usual / melhor / pior
    bc = data.get("casos")
    if bc is not None:
        bc = clean(bc, "Fator")
        if not bc.empty:
            r.tables.append(("Casos por fator PESTEL: business as usual · melhor caso · pior caso", bc))
    return r


def _wrap(t, n, maxlines):
    words, lines, cur = t.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        lines[-1] += "…"
    return "<br>".join(lines)
