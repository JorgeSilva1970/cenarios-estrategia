import plotly.graph_objects as go

from core.result import Result, clean, num
from core.theme import DIV, quad_shapes

STRAT = {"Gerir de perto": "Envolver ativamente, co-decidir, reuniões regulares",
         "Manter satisfeito": "Consultar nas decisões-chave, evitar surpresas",
         "Manter informado": "Comunicação regular, recolher contributos",
         "Monitorizar": "Acompanhar com esforço mínimo"}
SALIENCE = {(1, 0, 0): "Adormecido", (0, 1, 0): "Discricionário", (0, 0, 1): "Exigente",
            (1, 1, 0): "Dominante", (1, 0, 1): "Perigoso", (0, 1, 1): "Dependente",
            (1, 1, 1): "Definitivo", (0, 0, 0): "Sem atributos salientes"}


def quadrant(p, i, thr):
    if p >= thr and i >= thr:
        return "Gerir de perto"
    if p >= thr:
        return "Manter satisfeito"
    if i >= thr:
        return "Manter informado"
    return "Monitorizar"


def analyze(data: dict, thr: float = 3.0, sal_thr: float = 4.0) -> Result:
    r = Result()
    df = clean(data["stakeholders"], "Stakeholder")
    if df.empty:
        r.warnings.append("Sem stakeholders.")
        return r
    df = num(df, ["Poder", "Interesse", "Legitimidade", "Urgência"], 1, 5)
    df = num(df, ["Atitude"], -2, 2)
    df["Estratégia (Mendelow)"] = [quadrant(p, i, thr) for p, i in zip(df.Poder, df.Interesse)]
    df["Tipo (saliência)"] = [SALIENCE[(int(p >= sal_thr), int(l >= sal_thr), int(u >= sal_thr))]
                              for p, l, u in zip(df.Poder, df.Legitimidade, df.Urgência)]
    df["Prioridade"] = (df.Poder * df.Interesse * (1 + 0.25 * df.Atitude.abs())).round(1)

    risk = df[(df.Poder >= thr) & (df.Atitude < 0)]
    r.kpis = [("Stakeholders", len(df), None),
              ("A gerir de perto", int((df["Estratégia (Mendelow)"] == "Gerir de perto").sum()), None),
              ("Apoiantes / Opositores", f"{int((df.Atitude > 0).sum())} / {int((df.Atitude < 0).sum())}", None),
              ("Opositores com poder", len(risk), "Principal risco de implementação")]

    # desvio determinístico para stakeholders com a mesma posição (evita sobreposição de rótulos)
    seen, dx, dy = {}, [], []
    for p_, i_ in zip(df.Poder, df.Interesse):
        n = seen.get((p_, i_), 0)
        seen[(p_, i_)] = n + 1
        off = [(0, 0), (0.22, -0.22), (-0.22, -0.22), (0.22, 0.22), (-0.22, 0.22)][n % 5]
        dx.append(off[0])
        dy.append(off[1])
    fig = go.Figure(go.Scatter(
        x=df.Interesse + dx, y=df.Poder + dy, mode="markers+text", text=df.Stakeholder, textposition="top center",
        marker=dict(size=14 + 6 * df.Legitimidade, color=df.Atitude, colorscale=DIV, cmin=-2, cmax=2,
                    line=dict(width=2, color="white"), colorbar=dict(title="Atitude", tickvals=[-2, -1, 0, 1, 2])),
        customdata=df[["Tipo (saliência)", "Estratégia (Mendelow)", "Atitude"]],
        hovertemplate="<b>%{text}</b><br>Poder %{y} · Interesse %{x}<br>%{customdata[1]}<br>Saliência: %{customdata[0]}"
                      "<br>Atitude %{customdata[2]:+d}<extra></extra>"))
    quad_shapes(fig, thr - 0.5 if thr == int(thr) else thr, thr - 0.5 if thr == int(thr) else thr, [0.4, 5.6], [0.4, 5.6],
                {"TR": "Gerir de perto", "TL": "Manter satisfeito", "BR": "Manter informado", "BL": "Monitorizar"})
    fig.update_layout(title="Matriz Poder × Interesse (cor = atitude · tamanho = legitimidade)", height=560,
                      xaxis_title="Interesse", yaxis_title="Poder")
    r.figs.append(("Vermelho = opositor · azul = apoiante · cinzento = neutro.", fig))

    c = df["Tipo (saliência)"].value_counts()
    bar = go.Figure(go.Bar(x=c.index, y=c.values, marker_color="#2a78d6", text=c.values, textposition="outside"))
    bar.update_layout(title="Tipologia de saliência (Mitchell, Agle & Wood)", height=340, yaxis_title="Nº de stakeholders")
    r.figs.append(("Definitivos = poder + legitimidade + urgência: prioridade máxima.", bar))

    out = df.sort_values("Prioridade", ascending=False)
    out["Ação de envolvimento"] = out["Estratégia (Mendelow)"].map(STRAT)
    r.tables.append(("Plano de envolvimento (ordenado por prioridade)",
                     out[["Stakeholder", "Poder", "Interesse", "Legitimidade", "Urgência", "Atitude",
                          "Estratégia (Mendelow)", "Tipo (saliência)", "Prioridade", "Ação de envolvimento"]]))

    key = df[df["Estratégia (Mendelow)"] == "Gerir de perto"]
    r.conclusions.append(f"**{len(key)} stakeholders a gerir de perto**: " + ", ".join(key.Stakeholder) + ".")
    if len(risk):
        r.conclusions.append("⚠️ **Opositores com poder** (risco crítico): " + ", ".join(risk.Stakeholder)
                             + " — preparar plano de negociação/mitigação específico.")
    allies = df[(df.Atitude > 0) & (df.Poder >= thr)]
    if len(allies):
        r.conclusions.append("Aliados com poder a mobilizar como patrocinadores: " + ", ".join(allies.Stakeholder) + ".")
    latent = df[(df.Interesse >= 4) & (df.Poder < thr) & (df.Atitude < 0)]
    if len(latent):
        r.conclusions.append("Opositores com alto interesse e pouco poder podem coligar-se: " + ", ".join(latent.Stakeholder)
                             + " — manter informados e ouvir preocupações.")
    d = df[df["Tipo (saliência)"] == "Definitivo"]
    if len(d):
        r.conclusions.append("Stakeholders **definitivos** (saliência máxima): " + ", ".join(d.Stakeholder) + ".")
    return r
