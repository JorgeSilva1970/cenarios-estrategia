import plotly.graph_objects as go

from core.result import Result, clean, num
from core.theme import SERIES, STATUS

FORCES = ["Rivalidade entre concorrentes", "Ameaça de novos entrantes", "Ameaça de substitutos",
          "Poder negocial dos fornecedores", "Poder negocial dos clientes"]
COLS = ["Força", "Fator", "Intensidade"]


def level(v):
    return "Alta" if v >= 3.5 else ("Moderada" if v > 2 else "Baixa")


def analyze(data: dict) -> Result:
    r = Result()
    df = clean(data["fatores"], "Fator")
    if df.empty:
        r.warnings.append("Sem fatores.")
        return r
    df = num(df, ["Intensidade"], 1, 5)
    g = df.groupby("Força")["Intensidade"].mean().reindex([f for f in FORCES if f in set(df["Força"])])
    overall = g.mean()
    attract = 6 - overall
    r.kpis = [("Intensidade competitiva média", f"{overall:.2f} / 5", None),
              ("Atratividade do setor", f"{attract:.2f} / 5", "6 − intensidade média"),
              ("Força dominante", g.idxmax().split(" ")[-1].capitalize(), g.idxmax()),
              ("Forças altas (≥3,5)", int((g >= 3.5).sum()), None)]

    theta = list(g.index) + [g.index[0]]
    fig = go.Figure(go.Scatterpolar(r=list(g.values) + [g.values[0]], theta=theta, fill="toself",
                                    line=dict(color=SERIES[0], width=2), fillcolor="rgba(42,120,214,0.18)",
                                    name="Intensidade"))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 5], tickvals=[1, 2, 3, 4, 5])),
                      title="Perfil das cinco forças", height=440, showlegend=False)
    r.figs.append(("Radar: quanto mais afastado do centro, maior a pressão sobre a rentabilidade.", fig))

    d = df.sort_values(["Força", "Intensidade"])
    colors = [STATUS["critical"] if v >= 3.5 else (STATUS["warning"] if v > 2 else STATUS["good"]) for v in d.Intensidade]
    fig2 = go.Figure(go.Bar(y=d.Fator, x=d.Intensidade, orientation="h", marker_color=colors,
                            customdata=d["Força"], hovertemplate="%{y}<br>%{customdata}<br>Intensidade %{x}<extra></extra>",
                            text=[level(v) for v in d.Intensidade], textposition="outside"))
    fig2.update_layout(title="Intensidade por fator (verde baixa · amarelo moderada · vermelho alta)",
                       xaxis_range=[0, 5.8], height=max(360, 26 * len(d)), yaxis=dict(automargin=True))
    r.figs.append(("Fatores que explicam cada força.", fig2))

    t = g.reset_index()
    t.columns = ["Força", "Intensidade média"]
    t["Nível"] = t["Intensidade média"].map(level)
    t["Intensidade média"] = t["Intensidade média"].round(2)
    r.tables.append(("Síntese por força", t))

    r.conclusions.append(f"A intensidade competitiva global é **{level(overall).lower()}** ({overall:.2f}/5); "
                         f"a atratividade estrutural do setor é {attract:.2f}/5.")
    hi = g[g >= 3.5]
    if len(hi):
        r.conclusions.append("Forças de pressão **alta** a neutralizar: " + "; ".join(f"{k} ({v:.1f})" for k, v in hi.items()) + ".")
    lo = g[g <= 2]
    if len(lo):
        r.conclusions.append("Forças **baixas** (fontes de margem a proteger): " + "; ".join(lo.index) + ".")
    top = df.sort_values("Intensidade", ascending=False).head(3)
    r.conclusions.append("Fatores mais críticos: " + "; ".join(top.Fator) + ".")
    return r
