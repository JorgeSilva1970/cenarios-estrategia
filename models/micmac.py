import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean
from core.theme import MUTED, SERIES, quad_shapes

CLASS_COLORS = {"Motora": SERIES[0], "Ligação": SERIES[7], "Dependente": SERIES[1], "Autónoma": "#9a9993"}


def matrix(data: dict):
    v = clean(data["variaveis"], "Código")
    codes = [str(c).strip() for c in v["Código"]]
    m = data["matriz"].reindex(index=codes, columns=codes).apply(pd.to_numeric, errors="coerce").fillna(0)
    m = m.clip(0, 3)
    for c in codes:
        m.loc[c, c] = 0
    return v, codes, m.values.astype(float)


def micmac(M: np.ndarray, kmax: int = 10):
    """Eleva a matriz a potências até a ordenação de motricidade e dependência estabilizar."""
    inf_d, dep_d = M.sum(1), M.sum(0)
    P, k, prev, stable = M.copy(), 1, None, 0
    while k < kmax:
        P = P @ M
        k += 1
        if P.sum() == 0:
            break
        P = P / P.max()  # normalização numérica (não altera a ordenação)
        rank = (tuple(np.argsort(-P.sum(1), kind="stable")), tuple(np.argsort(-P.sum(0), kind="stable")))
        stable = stable + 1 if rank == prev else 0
        prev = rank
        if stable >= 1:
            break
    inf_i, dep_i = P.sum(1), P.sum(0)
    if inf_i.sum() > 0:  # reescala para a mesma soma da matriz direta (comparabilidade)
        s = M.sum() / inf_i.sum()
        inf_i, dep_i = inf_i * s, dep_i * s
    return inf_d, dep_d, inf_i, dep_i, k


def classify(inf, dep):
    mi, md = inf.mean(), dep.mean()
    out = []
    for a, b in zip(inf, dep):
        if a > mi and b <= md:
            out.append("Motora")
        elif a > mi and b > md:
            out.append("Ligação")
        elif a <= mi and b > md:
            out.append("Dependente")
        else:
            out.append("Autónoma")
    return out


def _plane(codes, names, inf, dep, cls, title):
    fig = go.Figure()
    for c in CLASS_COLORS:
        idx = [i for i, k in enumerate(cls) if k == c]
        if not idx:
            continue
        fig.add_scatter(x=dep[idx], y=inf[idx], mode="markers+text", name=c,
                        text=[codes[i] for i in idx], textposition="top center",
                        customdata=[names[i] for i in idx],
                        hovertemplate="<b>%{text}</b> %{customdata}<br>Dependência %{x:.1f}<br>Motricidade %{y:.1f}<extra></extra>",
                        marker=dict(size=14, color=CLASS_COLORS[c], line=dict(width=2, color="white")))
    xr = [-0.08 * max(dep.max(), 1), max(dep.max(), 1) * 1.15]
    yr = [-0.08 * max(inf.max(), 1), max(inf.max(), 1) * 1.15]
    quad_shapes(fig, dep.mean(), inf.mean(), xr, yr,
                {"TL": "Motoras", "TR": "Ligação", "BR": "Dependentes", "BL": "Autónomas"})
    fig.update_layout(title=title, xaxis_title="Dependência", yaxis_title="Motricidade (influência)", height=500)
    return fig


def analyze(data: dict) -> Result:
    r = Result()
    v, codes, M = matrix(data)
    if len(codes) < 3:
        r.warnings.append("São necessárias pelo menos 3 variáveis.")
        return r
    names = list(v["Variável"].astype(str))
    inf_d, dep_d, inf_i, dep_i, k = micmac(M)
    cls_d, cls_i = classify(inf_d, dep_d), classify(inf_i, dep_i)
    fill = (M > 0).sum() / (len(codes) ** 2 - len(codes))

    r.kpis = [("Variáveis", len(codes), None),
              ("Taxa de preenchimento", f"{fill:.0%}", "Matrizes muito densas (>50%) discriminam pior as variáveis"),
              ("Potência de estabilização", f"M^{k}", "Iterações até a ordenação estabilizar"),
              ("Variáveis motoras (indireto)", cls_i.count("Motora"), None)]

    r.figs.append(("Plano de influência/dependência **direto**.", _plane(codes, names, inf_d, dep_d, cls_d, "Plano direto")))
    r.figs.append(("Plano **indireto** (MICMAC): revela influências escondidas nas cadeias de efeitos.",
                   _plane(codes, names, inf_i, dep_i, cls_i, f"Plano indireto (M^{k})")))

    heat = go.Figure(go.Heatmap(z=M, x=codes, y=codes, colorscale=[[0, "#f4f3ef"], [1, "#184f95"]], zmin=0, zmax=3,
                                text=M.astype(int), texttemplate="%{text}",
                                hovertemplate="%{y} → %{x}: %{z}<extra></extra>", showscale=False))
    heat.update_layout(title="Matriz de influências diretas (linha influencia coluna)", height=460,
                       yaxis=dict(autorange="reversed"))
    r.figs.append(("Matriz de entrada.", heat))
    r.figs.append(("Rede das influências fortes (valor 3) e médias (valor 2).", _network(codes, names, M)))

    t = pd.DataFrame({"Código": codes, "Variável": names,
                      "Motricidade direta": inf_d.astype(int), "Dependência direta": dep_d.astype(int),
                      "Motricidade indireta": inf_i.round(1), "Dependência indireta": dep_i.round(1),
                      "Classe (direta)": cls_d, "Classe (indireta)": cls_i})
    t["Rank mot. direto"] = t["Motricidade direta"].rank(ascending=False, method="min").astype(int)
    t["Rank mot. indireto"] = t["Motricidade indireta"].rank(ascending=False, method="min").astype(int)
    t["Δ rank"] = t["Rank mot. direto"] - t["Rank mot. indireto"]
    r.tables.append(("Classificação das variáveis", t.sort_values("Motricidade indireta", ascending=False)))

    mot = t[t["Classe (indireta)"] == "Motora"].sort_values("Motricidade indireta", ascending=False)
    lig = t[t["Classe (indireta)"] == "Ligação"]
    dep = t[t["Classe (indireta)"] == "Dependente"]
    if len(mot):
        r.conclusions.append("**Variáveis motoras** (alavancas do sistema, a usar como eixos de cenários ou "
                             "objetivos de ação): " + ", ".join(f"{a} – {b}" for a, b in zip(mot["Código"], mot["Variável"])) + ".")
    if len(lig):
        r.conclusions.append("**Variáveis de ligação** (instáveis, qualquer ação repercute-se e volta): "
                             + ", ".join(lig["Variável"]) + ".")
    if len(dep):
        r.conclusions.append("**Variáveis dependentes** (resultados/indicadores a monitorizar): " + ", ".join(dep["Variável"]) + ".")
    moved = t[t["Δ rank"].abs() >= 2]
    if len(moved):
        r.conclusions.append("Mudanças relevantes entre classificação direta e indireta (influências escondidas): "
                             + "; ".join(f"{a} ({'+' if d > 0 else ''}{d})" for a, d in zip(moved["Variável"], moved["Δ rank"])) + ".")
    if fill > 0.5:
        r.warnings.append("Matriz muito preenchida (>50%) — tende a esbater diferenças; reserve 3 para influências fortes.")
    return r


def _network(codes, names, M):
    n = len(codes)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = np.cos(ang), np.sin(ang)
    fig = go.Figure()
    for i in range(n):
        for j in range(n):
            if M[i, j] >= 2:
                fig.add_annotation(x=x[j] * 0.92, y=y[j] * 0.92, ax=x[i], ay=y[i], xref="x", yref="y", axref="x", ayref="y",
                                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2.2 if M[i, j] == 3 else 1,
                                   arrowcolor=SERIES[0] if M[i, j] == 3 else "#b9b8b2", opacity=0.85)
    infl = M.sum(1)
    fig.add_scatter(x=x, y=y, mode="markers+text", text=codes, textposition="middle center",
                    customdata=names, hovertemplate="<b>%{text}</b> %{customdata}<extra></extra>",
                    marker=dict(size=20 + 30 * infl / max(infl.max(), 1), color="#ffffff",
                                line=dict(width=2, color=MUTED)), textfont=dict(size=11), showlegend=False)
    fig.update_layout(title="Grafo de influências (tamanho = motricidade)", height=520,
                      xaxis=dict(visible=False, range=[-1.3, 1.3]), yaxis=dict(visible=False, range=[-1.3, 1.3], scaleanchor="x"),
                      plot_bgcolor="rgba(0,0,0,0)")
    return fig
