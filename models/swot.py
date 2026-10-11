import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean, num
from core.theme import MUTED, SERIES

TYPES = {"Força": "S", "Fraqueza": "W", "Oportunidade": "O", "Ameaça": "T"}
TCOL = {"Força": SERIES[0], "Fraqueza": SERIES[1], "Oportunidade": SERIES[2], "Ameaça": SERIES[7]}
QUADS = {"SO": "Maxi-maxi: usar forças para aproveitar oportunidades",
         "WO": "Mini-maxi: superar fraquezas aproveitando oportunidades",
         "ST": "Maxi-mini: usar forças para reduzir ameaças",
         "WT": "Mini-mini: minimizar fraquezas e evitar ameaças"}


def _lvl(v):
    return "forte" if v >= 3 else ("média" if v >= 2.5 else "abaixo da média")


def ie_cell(ife, efe):
    col = 0 if ife >= 3 else (1 if ife >= 2 else 2)
    row = 0 if efe >= 3 else (1 if efe >= 2 else 2)
    cell = row * 3 + col + 1
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"][cell - 1]
    if cell in (1, 2, 4):
        rx = "Crescer e construir (penetração, desenvolvimento de mercado/produto, integração)"
    elif cell in (3, 5, 7):
        rx = "Manter e sustentar (penetração de mercado e desenvolvimento de produto)"
    else:
        rx = "Colher ou desinvestir"
    return roman, rx


def analyze(data: dict) -> Result:
    r = Result()
    f = clean(data["fatores"], "Fator")
    if f.empty:
        r.warnings.append("Sem fatores SWOT.")
        return r
    f = num(f, ["Peso", "Classificação"], 0, None)
    f["Classificação"] = f["Classificação"].clip(1, 4)
    f["Pontuação ponderada"] = (f["Peso"] * f["Classificação"]).round(3)
    internal = f[f["Tipo"].isin(["Força", "Fraqueza"])]
    external = f[f["Tipo"].isin(["Oportunidade", "Ameaça"])]
    wi, we = internal["Peso"].sum(), external["Peso"].sum()
    for lbl, w in (("internos", wi), ("externos", we)):
        if abs(w - 1) > 0.01:
            r.warnings.append(f"A soma dos pesos dos fatores {lbl} é {w:.2f} (deveria ser 1,00). Os totais foram normalizados.")
    ife = internal["Pontuação ponderada"].sum() / (wi or 1)
    efe = external["Pontuação ponderada"].sum() / (we or 1)
    roman, rx = ie_cell(ife, efe)
    r.kpis = [("Total IFE (interno)", f"{ife:.2f}", "1 = muito fraco · 2,5 = médio · 4 = muito forte"),
              ("Total EFE (externo)", f"{efe:.2f}", "Qualidade da resposta às oportunidades/ameaças"),
              ("Célula da matriz IE", roman, None),
              ("Prescrição", rx.split(" ")[0], rx)]

    d = f.sort_values(["Tipo", "Pontuação ponderada"])
    fig = go.Figure()
    for t in TYPES:
        s = d[d["Tipo"] == t]
        if len(s):
            fig.add_bar(y=s["Fator"], x=s["Pontuação ponderada"], orientation="h", name=t, marker_color=TCOL[t],
                        customdata=s[["Peso", "Classificação"]],
                        hovertemplate="%{y}<br>Peso %{customdata[0]:.2f} × Class. %{customdata[1]:.0f} = %{x:.2f}<extra></extra>")
    fig.update_layout(title="Pontuação ponderada por fator (peso × classificação)", height=max(380, 26 * len(d) + 120),
                      yaxis=dict(automargin=True))
    r.figs.append(("Os fatores mais longos são os que mais pesam no diagnóstico.", fig))

    ie = go.Figure()
    labels = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    fills = {1: "#cfe8d4", 2: "#cfe8d4", 4: "#cfe8d4", 3: "#fdf0cc", 5: "#fdf0cc", 7: "#fdf0cc", 6: "#f8d6d5", 8: "#f8d6d5", 9: "#f8d6d5"}
    for i in range(9):
        row, col = divmod(i, 3)
        x0, x1 = [4, 3, 2][col], [3, 2, 1][col]
        y0, y1 = [4, 3, 2][row], [3, 2, 1][row]
        ie.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=fills[i + 1], line=dict(color="white", width=3), layer="below")
        ie.add_annotation(x=(x0 + x1) / 2, y=(y0 + y1) / 2, text=labels[i], showarrow=False, font=dict(size=18, color=MUTED))
    ie.add_scatter(x=[ife], y=[efe], mode="markers+text", text=["Posição atual"], textposition="top center",
                   marker=dict(size=18, color=SERIES[0], line=dict(width=3, color="white")), showlegend=False,
                   hovertemplate="IFE %{x:.2f} · EFE %{y:.2f}<extra></extra>")
    ie.update_layout(title="Matriz Interna-Externa (IE)", height=460,
                     xaxis=dict(title="Total IFE (forte ← → fraco)", range=[4, 1], tickvals=[4, 3, 2, 1]),
                     yaxis=dict(title="Total EFE", range=[1, 4], tickvals=[1, 2, 3, 4]))
    r.figs.append(("Verde = crescer · amarelo = manter · vermelho = colher/desinvestir.", ie))

    r.tables.append(("Matriz IFE/EFE", f[["Tipo", "Fator", "Peso", "Classificação", "Pontuação ponderada"]]))
    st_ = clean(data["estrategias"], "Estratégia")
    if not st_.empty:
        st_ = st_.sort_values(["Quadrante", "Prioridade"])
        r.tables.append(("Matriz TOWS — estratégias", st_))
    best_s = f[f.Tipo == "Força"].nlargest(1, "Pontuação ponderada")
    worst_w = f[f.Tipo == "Fraqueza"].nlargest(1, "Peso")
    r.conclusions.append(f"Posição interna **{_lvl(ife)}** (IFE = {ife:.2f}) e resposta ao meio envolvente **{_lvl(efe)}** (EFE = {efe:.2f}).")
    r.conclusions.append(f"Célula **{roman}** da matriz IE → *{rx}*.")
    if len(best_s):
        r.conclusions.append(f"Força mais determinante: **{best_s.iloc[0]['Fator']}**.")
    if len(worst_w):
        r.conclusions.append(f"Fraqueza com maior peso: **{worst_w.iloc[0]['Fator']}** — prioridade das estratégias WO/WT.")
    if not st_.empty:
        top = st_[pd.to_numeric(st_["Prioridade"], errors="coerce") == 1]
        if len(top):
            r.conclusions.append("Estratégias TOWS de prioridade 1: " + "; ".join(f"[{q}] {s}" for q, s in zip(top.Quadrante, top.Estratégia)) + ".")
        miss = [q for q in QUADS if q not in set(st_.Quadrante)]
        if miss:
            r.warnings.append("Quadrantes TOWS sem estratégias: " + ", ".join(miss))
    return r
