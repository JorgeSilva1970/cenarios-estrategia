"""Geração de relatórios HTML autónomos (gráficos interativos, tabelas, legendas e conclusões)."""
import datetime as dt
import html
import re

from plotly.offline import get_plotlyjs

from core.refs import METHODS

CSS = """
:root{--ink:#0b0b0b;--muted:#52514e;--line:#e6e5e1;--accent:#2a78d6;--bg:#fcfcfb}
*{box-sizing:border-box}body{font-family:Inter,Segoe UI,Arial,sans-serif;color:var(--ink);background:#fff;margin:0;line-height:1.55}
.wrap{max-width:1100px;margin:0 auto;padding:32px 20px}
header{border-bottom:3px solid var(--accent);padding-bottom:14px;margin-bottom:24px}
h1{margin:0 0 6px;font-size:28px}h2{margin:40px 0 10px;font-size:22px;border-bottom:1px solid var(--line);padding-bottom:6px}
h3{font-size:16px;margin:22px 0 8px;color:var(--muted)}
.meta{color:var(--muted);font-size:14px}
.legend{background:var(--bg);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:14px 18px;font-size:14px}
.legend p{margin:4px 0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:14px 0}
.kpi{border:1px solid var(--line);border-radius:8px;padding:10px 14px}.kpi b{display:block;font-size:22px}.kpi span{color:var(--muted);font-size:12px}
.concl{background:#eef5fd;border-radius:8px;padding:12px 18px}.concl li{margin:4px 0}
.warn{background:#fff6e0;border-radius:8px;padding:8px 14px;font-size:13px}
table{border-collapse:collapse;width:100%;font-size:12.5px;margin:6px 0 14px}th,td{border:1px solid var(--line);padding:5px 7px;text-align:left;vertical-align:top}
th{background:var(--bg)}.fig{margin:8px 0 2px}.cap{color:var(--muted);font-size:12.5px;margin:0 0 14px}
nav ol{columns:2;font-size:14px}footer{margin-top:40px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:10px}
@media print{.wrap{padding:0}h2{page-break-before:always}}
"""


def md(t: str) -> str:
    t = html.escape(str(t))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t


def _legend(key):
    m = METHODS[key]
    sites = " · ".join(f'<a href="{u.strip()}">{u.strip()}</a>' for u in m["site"].split("·"))
    return (f'<div class="legend"><p><b>Objetivo:</b> {md(m["objetivo"])}</p><p><b>Descrição:</b> {md(m["descricao"])}</p>'
            f'<p><b>Autor(es):</b> {md(m["autor"])} &nbsp;·&nbsp; <b>Ano:</b> {m["ano"]}</p>'
            f'<p><b>Referência:</b> {md(m["obra"])}</p><p><b>Site:</b> {sites}</p>'
            f'<p><b>Como ler:</b> {md(m["leitura"])}</p></div>')


def section(key, res, state):
    m = METHODS[key]
    out = [f'<h2 id="{key}">{m["icone"]} {m["nome"]}</h2>', _legend(key)]
    if res.kpis:
        out.append('<div class="kpis">' + "".join(f'<div class="kpi"><span>{md(k)}</span><b>{md(v)}</b></div>'
                                                  for k, v, _ in res.kpis) + "</div>")
    for w in res.warnings:
        out.append(f'<p class="warn">⚠️ {md(w)}</p>')
    if res.conclusions:
        out.append("<h3>Conclusões</h3><div class='concl'><ul>" + "".join(f"<li>{md(c)}</li>" for c in res.conclusions) + "</ul></div>")
    out.append("<h3>Gráficos</h3>")
    for cap, fig in res.figs:
        state["js"] = True
        out.append('<div class="fig">' + fig.to_html(full_html=False, include_plotlyjs=False, config={"displaylogo": False})
                   + f'</div><p class="cap">{md(cap)}</p>')
    for cap, df in res.tables:
        if df is None or df.empty:
            continue
        d = df.head(60)
        out.append(f"<h3>{md(cap)}</h3>" + d.to_html(index=False, border=0, na_rep=""))
    return "\n".join(out)


def executive_summary(results, n=2):
    """Sumário executivo: as n conclusões mais relevantes de cada modelo, identificadas pelo nome do modelo."""
    return [f"[{METHODS[k]['nome'].split(' (')[0]}] {c}" for k, r in results for c in r.conclusions[:n]]


def build(results: list, case: str, context: str, title: str = "Relatório de Análise Estratégica e Cenários",
          summary: list | None = None) -> str:
    state = {"js": False}
    now = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    toc = "".join(f'<li><a href="#{k}">{METHODS[k]["nome"]}</a></li>' for k, _ in results)
    body = "\n".join(section(k, r, state) for k, r in results)
    # Biblioteca Plotly embutida uma única vez no <head>: o relatório funciona offline e em pré-visualizadores
    # que bloqueiam scripts externos (CDN).
    js = f'<script type="text/javascript">{get_plotlyjs()}</script>' if state["js"] else ""
    summ = ""
    if summary:
        summ = "<h2 id='sumario'>Sumário executivo</h2><div class='concl'><ul>" + "".join(f"<li>{md(s)}</li>" for s in summary) + "</ul></div>"
    return f"""<!doctype html><html lang="pt-PT"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style>
{js}</head>
<body><div class="wrap"><header><h1>{html.escape(title)}</h1>
<div class="meta"><b>Caso:</b> {html.escape(case)} · gerado em {now}</div><p>{md(context)}</p></header>
{"<nav><b>Índice</b><ol>" + toc + "</ol></nav>" if len(results) > 1 else ""}
{summ}{body}
<footer>Gerado pelo Estúdio de Cenários &amp; Estratégia (Python · Streamlit · Plotly). Para PDF: Ctrl+P → Guardar como PDF.</footer>
</div></body></html>"""
