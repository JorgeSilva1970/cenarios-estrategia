import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean
from core.theme import SERIES

CODES = ["—", "R", "A", "AR", "S", "C", "I"]  # "—" = sem papel
LEGEND = {"R": "Responsável (executa)", "A": "Aprovador (presta contas)", "AR": "Aprova e executa",
          "S": "Suporte", "C": "Consultado", "I": "Informado"}
LCOL = {"R": SERIES[0], "A": SERIES[7], "S": SERIES[2], "C": SERIES[3], "I": "#b9b8b2"}
AUTH_COLS = ["Propõe", "Valida", "Aprova", "Informado"]


def roles(df):
    return [c for c in df.columns if c not in ("Fase", "Tarefa")]


def _norm(v):
    v = str(v).strip().upper()
    return "" if v in ("NAN", "NONE", "—", "-") else v


def _codes(v):
    v = _norm(v)
    return {"A", "R"} if v in ("AR", "A/R", "RA") else ({v} if v else set())


def analyze(data: dict, max_c: int = 3, overload: float = 0.4) -> Result:
    r = Result()
    m = clean(data["raci"], "Tarefa")
    a = clean(data["autoridade"], "Decisão")
    issues = []
    if not m.empty:
        R = roles(m)
        for _, t in m.iterrows():
            cs = {p: _codes(t[p]) for p in R}
            nA = sum("A" in c for c in cs.values())
            nR = sum("R" in c for c in cs.values())
            nC = sum("C" in c for c in cs.values())
            if nA == 0:
                issues.append((t["Tarefa"], "Sem Aprovador (A)", "Crítico"))
            elif nA > 1:
                issues.append((t["Tarefa"], f"{nA} Aprovadores — deve haver apenas um A", "Crítico"))
            if nR == 0:
                issues.append((t["Tarefa"], "Sem Responsável (R)", "Crítico"))
            if nC > max_c:
                issues.append((t["Tarefa"], f"{nC} consultados — risco de lentidão na decisão", "Atenção"))
            if nR > 3:
                issues.append((t["Tarefa"], f"{nR} responsáveis — responsabilidade diluída", "Atenção"))

        counts = pd.DataFrame({p: {k: sum(k in _codes(v) for v in m[p]) for k in LCOL} for p in R}).T
        counts["Carga (R+A)"] = counts["R"] + counts["A"]
        n = len(m)
        for p, row in counts.iterrows():
            if row["Carga (R+A)"] / n > overload and n >= 5:
                issues.append((p, f"Envolvido como R/A em {int(row['Carga (R+A)'])} de {n} tarefas — sobrecarga", "Atenção"))
            if row["R"] + row["A"] == 0:
                issues.append((p, "Papel sem qualquer R ou A — confirmar se é necessário", "Info"))

        # Heatmap categórico RACI
        order = {"": 0, "I": 1, "C": 2, "S": 3, "R": 4, "A": 5, "AR": 5}
        z = [[order.get(_norm(t[p]), 0) for p in R] for _, t in m.iterrows()]
        txt = [[_norm(t[p]) for p in R] for _, t in m.iterrows()]
        cs = [[0, "#ffffff"], [0.1999, "#ffffff"], [0.2, "#e4e3de"], [0.3999, "#e4e3de"], [0.4, "#fde7b0"], [0.5999, "#fde7b0"],
              [0.6, "#c8eedd"], [0.7999, "#c8eedd"], [0.8, "#bcd6f6"], [0.8999, "#bcd6f6"], [0.9, "#f6c6c5"], [1, "#f6c6c5"]]
        ylab = [f"{f} · {t}" if str(f) not in ("nan", "None", "") else t for f, t in zip(m.get("Fase", [""] * n), m["Tarefa"])]
        heat = go.Figure(go.Heatmap(z=z, x=R, y=ylab, text=txt, texttemplate="<b>%{text}</b>", colorscale=cs, zmin=0, zmax=5,
                                    showscale=False, xgap=2, ygap=2, hovertemplate="%{y}<br>%{x}: %{text}<extra></extra>"))
        heat.update_layout(title="Matriz RACI (A/AR vermelho · R azul · S verde · C amarelo · I cinzento)",
                           height=max(380, 34 * n + 140), yaxis=dict(autorange="reversed", automargin=True), xaxis=dict(side="top", tickangle=-30, automargin=True))
        r.figs.append(("Matriz de responsabilidades por tarefa e papel.", heat))

        bar = go.Figure()
        for k in ["A", "R", "S", "C", "I"]:
            bar.add_bar(x=counts.index, y=counts[k], name=LEGEND[k], marker_color=LCOL[k])
        bar.update_layout(barmode="stack", title="Carga de responsabilidades por papel", height=400, yaxis_title="Nº de tarefas")
        r.figs.append(("Papéis com muitas atribuições R/A podem ser um ponto de estrangulamento.", bar))
        r.tables.append(("Contagem de atribuições por papel", counts.reset_index().rename(columns={"index": "Papel"})))

    # Matriz de autoridade / delegação de competências
    if not a.empty:
        for _, d in a.iterrows():
            ap = str(d.get("Aprova", "")).strip()
            pr = str(d.get("Propõe", "")).strip()
            va = str(d.get("Valida", "")).strip()
            if ap in ("", "nan", "None", "—"):
                issues.append((d["Decisão"], "Decisão sem aprovador definido", "Crítico"))
            elif ap == pr:
                issues.append((d["Decisão"], f"Segregação de funções violada: '{ap}' propõe e aprova", "Crítico"))
            elif ap == va:
                issues.append((d["Decisão"], f"'{ap}' valida e aprova — reforçar controlo independente", "Atenção"))
        cnt = a["Aprova"].astype(str).value_counts()
        fig = go.Figure(go.Bar(x=cnt.index, y=cnt.values, marker_color=SERIES[6], text=cnt.values, textposition="outside"))
        fig.update_layout(title="Concentração de autoridade: nº de decisões aprovadas por papel", height=340)
        r.figs.append(("Concentração excessiva num papel cria dependência e risco operacional.", fig))
        r.tables.append(("Matriz de autoridade (delegação de competências)", a))

    iss = pd.DataFrame(issues, columns=["Elemento", "Problema", "Gravidade"])
    if not iss.empty:
        iss["ord"] = iss["Gravidade"].map({"Crítico": 0, "Atenção": 1, "Info": 2})
        iss = iss.sort_values("ord").drop(columns="ord")
    r.tables.insert(0, ("Validação automática das regras RACI e de autoridade", iss))
    ncrit = int((iss["Gravidade"] == "Crítico").sum()) if not iss.empty else 0
    r.kpis = [("Tarefas", len(m), None), ("Papéis", len(roles(m)) if not m.empty else 0, None),
              ("Decisões delegadas", len(a), None), ("Problemas críticos", ncrit, "Sem A, vários A, sem R, segregação")]
    if ncrit == 0:
        r.conclusions.append("✅ Todas as tarefas têm exatamente um Aprovador e pelo menos um Responsável; não há violações de segregação.")
    else:
        r.conclusions.append(f"❌ Foram encontrados **{ncrit} problemas críticos** — corrigir antes de comunicar a matriz.")
        for _, i in iss[iss["Gravidade"] == "Crítico"].iterrows():
            r.conclusions.append(f"– *{i['Elemento']}*: {i['Problema']}.")
    if not m.empty:
        top = counts["Carga (R+A)"].idxmax()
        r.conclusions.append(f"O papel com maior carga é **{top}** ({int(counts.loc[top, 'Carga (R+A)'])} atribuições R/A).")
    if not a.empty:
        r.conclusions.append(f"A autoridade de aprovação está concentrada em **{cnt.index[0]}** ({cnt.iloc[0]} de {len(a)} decisões).")
    return r
