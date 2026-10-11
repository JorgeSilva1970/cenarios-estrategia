from math import prod

import pandas as pd
import plotly.graph_objects as go

from core.result import Result, clean
from core.theme import MUTED, SEQ, SERIES

CAP = 200_000  # limite de configurações consistentes enumeradas


def params(data) -> dict:
    p = clean(data["parametros"], "Estado")
    out = {}
    for _, r in p.iterrows():
        k, s = str(r["Parâmetro"]).strip(), str(r["Estado"]).strip()
        if k and s and s not in out.setdefault(k, []):
            out[k].append(s)
    return {k: v for k, v in out.items() if v}


def labels(P):
    return [f"{k}: {s}" for k, v in P.items() for s in v]


def incompat(data, P) -> set:
    valid = set(labels(P))
    df = clean(data["incompatibilidades"], "Estado A")
    out = set()
    for _, r in df.iterrows():
        a, b = str(r["Estado A"]), str(r["Estado B"])
        if a in valid and b in valid and a != b:
            out.add(frozenset((a, b)))
    return out


def solve(P: dict, bad: set, fixed: dict | None = None, cap: int = CAP):
    """Enumeração com poda (backtracking): devolve configurações consistentes."""
    keys = list(P)
    fixed = fixed or {}
    res, chosen = [], []

    def rec(i):
        if len(res) >= cap:
            return
        if i == len(keys):
            res.append(tuple(chosen))
            return
        k = keys[i]
        for s in ([fixed[k]] if k in fixed else P[k]):
            lab = f"{k}: {s}"
            if any(frozenset((lab, f"{keys[j]}: {c}")) in bad for j, c in enumerate(chosen)):
                continue
            chosen.append(s)
            rec(i + 1)
            chosen.pop()
    rec(0)
    return keys, res


def check(config: dict, bad: set):
    labs = [f"{k}: {v}" for k, v in config.items()]
    return [(a, b) for i, a in enumerate(labs) for b in labs[i + 1:] if frozenset((a, b)) in bad]


def analyze(data: dict, fixed: dict | None = None) -> Result:
    r = Result()
    P = params(data)
    if len(P) < 2:
        r.warnings.append("Defina pelo menos 2 parâmetros com estados.")
        return r
    bad = incompat(data, P)
    total = prod(len(v) for v in P.values())
    keys, sols = solve(P, bad, fixed)
    n = len(sols)
    r.kpis = [("Parâmetros", len(P), None),
              ("Configurações possíveis", f"{total:,}".replace(",", " "), "Produto do nº de estados (Zwicky box)"),
              ("Configurações consistentes", f"{n:,}".replace(",", " ") + (" +" if n >= CAP else ""),
               "Após a avaliação de consistência cruzada"),
              ("Redução do espaço", f"{1 - n / total:.0%}" if total else "–", None)]

    # Caixa morfológica: frequência de cada estado no espaço de soluções
    maxs = max(len(v) for v in P.values())
    freq = {k: {s: 0 for s in v} for k, v in P.items()}
    for c in sols:
        for k, s in zip(keys, c):
            freq[k][s] += 1
    z, txt, hov = [], [], []
    for i in range(maxs):
        row, trow, hrow = [], [], []
        for k in keys:
            if i < len(P[k]):
                s = P[k][i]
                f = freq[k][s] / n if n else 0
                row.append(f)
                trow.append(f"{s}<br>{f:.0%}")
                hrow.append(f"{k}<br>{s}<br>presente em {freq[k][s]} configurações ({f:.0%})")
            else:
                row.append(None)
                trow.append("")
                hrow.append("")
        z.append(row)
        txt.append(trow)
        hov.append(hrow)
    box = go.Figure(go.Heatmap(z=z, x=list(range(len(keys))), y=list(range(1, maxs + 1)), text=txt, texttemplate="%{text}",
                               textfont=dict(size=11), hovertext=hov, hovertemplate="%{hovertext}<extra></extra>",
                               colorscale=[[0, "#f4f3ef"]] + [[(i + 1) / len(SEQ[:5]), c] for i, c in enumerate(SEQ[:5])],
                               zmin=0, zmax=1, xgap=3, ygap=3, colorbar=dict(title="Frequência", tickformat=".0%", x=1.02)))

    # Cenários nomeados sobrepostos na caixa (um marcador por cenário em cada parâmetro)
    sc = clean(data["cenarios"], "Cenário")
    rows = []
    symbols = ["circle", "diamond", "square", "triangle-up", "star", "hexagon", "cross", "x"]
    ns = len(sc)
    for i, (_, s) in enumerate(sc.iterrows()):
        conf = {k: str(s.get(k, "")) for k in keys if str(s.get(k, "")) in P[k]}
        viol = check(conf, bad)
        off = (i - (ns - 1) / 2) * 0.12
        xs = [j + off for j, k in enumerate(keys) if k in conf]
        ys = [P[k].index(conf[k]) + 1 - 0.32 for k in keys if k in conf]
        box.add_scatter(x=xs, y=ys, mode="lines+markers", name=str(s["Cenário"]) + (" ⚠ inconsistente" if viol else ""),
                        line=dict(width=2, color=SERIES[i % 8], dash="dot" if viol else "solid"),
                        marker=dict(size=12, symbol=symbols[i % 8], color=SERIES[i % 8], line=dict(width=2, color="white")),
                        text=[conf[k] for k in keys if k in conf], hovertemplate="%{text}<extra>%{fullData.name}</extra>")
        rows.append({"Cenário": s["Cenário"], "Completo": len(conf) == len(keys),
                     "Consistente": "Sim" if not viol else "Não",
                     "Conflitos": "; ".join(f"{a} × {b}" for a, b in viol) or "—",
                     **{k: conf.get(k, "—") for k in keys}})
    box.update_layout(title="Caixa morfológica (% de configurações consistentes com cada estado) e cenários desenvolvidos",
                      height=170 + 110 * maxs, legend=dict(y=-0.08),
                      yaxis=dict(autorange="reversed", tickvals=list(range(1, maxs + 1)),
                                 ticktext=[f"Estado {i + 1}" for i in range(maxs)]),
                      xaxis=dict(side="top", tickvals=list(range(len(keys))), ticktext=keys))
    r.figs.append(("Cor = frequência do estado no espaço de soluções (0% = nunca consistente). "
                   "Marcadores = estados escolhidos para cada cenário; tracejado = cenário inconsistente.", box))
    if rows:
        r.tables.append(("Validação dos cenários desenvolvidos", pd.DataFrame(rows)))

    r.tables.append(("Pares incompatíveis (CCA)", pd.DataFrame([sorted(p) for p in bad], columns=["Estado A", "Estado B"])))
    if n:
        sample = pd.DataFrame(sols[:500], columns=keys)
        r.tables.append((f"Espaço de soluções (primeiras {min(n, 500)} de {n} configurações)", sample))

    r.conclusions.append(f"A avaliação de consistência cruzada eliminou {total - n} de {total} configurações "
                         f"({1 - n / total:.0%}), restando **{n} futuros internamente consistentes**.")
    zero = [f"{k}: {s}" for k in keys for s in P[k] if freq[k][s] == 0]
    if zero:
        r.conclusions.append("Estados **nunca consistentes** (rever definição ou incompatibilidades): " + "; ".join(zero) + ".")
    if not zero and n:
        r.conclusions.append("Todos os estados continuam possíveis em alguma configuração: a incerteza está nas "
                             "**combinações** e não em estados isolados.")
    restr = sorted(((freq[k][s] / n, f"{k}: {s}") for k in keys for s in P[k] if 0 < freq[k][s] / n < 0.25)) if n else []
    if restr:
        r.conclusions.append("Estados mais **restritivos** (presentes em <25% das configurações): "
                             + "; ".join(f"{l} ({f:.0%})" for f, l in restr[:4]) + ".")
    inc = [x["Cenário"] for x in rows if x["Consistente"] == "Não"]
    ok = [x["Cenário"] for x in rows if x["Consistente"] == "Sim"]
    if ok:
        r.conclusions.append("Cenários desenvolvidos **consistentes**: " + ", ".join(map(str, ok)) + ".")
    if inc:
        r.conclusions.append("⚠️ Cenários **inconsistentes** a corrigir: " + ", ".join(map(str, inc)) + ".")
    if n and len(ok) < 3:
        r.conclusions.append("Sugestão: escolha 3–4 configurações bem contrastadas do espaço de soluções como cenários finais.")
    return r


def options_after(P, bad, fixed):
    """Estados ainda possíveis por parâmetro dado um conjunto de drivers fixados (inferência de Ritchey)."""
    keys, sols = solve(P, bad, fixed)
    poss = {k: sorted({c[i] for c in sols}, key=P[k].index) for i, k in enumerate(keys)}
    return len(sols), poss
