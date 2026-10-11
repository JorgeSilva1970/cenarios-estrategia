"""Páginas gerais: Início, Dashboard/Relatório integrado e Referências."""
import pandas as pd
import streamlit as st

from core import report, state, ui
from core.refs import METHODS, ORDER
from models import bsc, micmac, morph, pestel, porter, ram, scenarios, stakeholders, swot

VIDEOS = [
    ("https://youtu.be/jyCiINmicy4", "What is Scenario Planning & How to Use it in Your Strategic Plan", "SME Strategy",
     "Forças motrizes → duas incertezas críticas → matriz 2×2 → implicações; armadilhas a evitar (mais de duas incertezas, "
     "escolher um só cenário, foco no curto prazo). Incorporado no Scenario Planning (4 passos e avisos automáticos)."),
    ("https://youtu.be/ezUbcR9IzC0", "What is the scenario planning process in a strategic plan? // How to do scenario development",
     "SME Strategy", "PESTLE para as forças motrizes, narrativas no presente para cada quadrante, horizonte de 1–3 anos para PME e a "
     "alternativa business as usual / melhor / pior caso. Incorporado no Scenario Planning (passo 3 e tabela de casos)."),
    ("https://youtu.be/8HZQvykaoW8", "Strategic Planning: A Step-by-Step Guide That Works", "Edward Shehab",
     "Valores → visão → missão → SWOT e plano de ação → objetivos SMART → Balanced Scorecard (objetivos, indicadores, metas, "
     "iniciativas) → KPI → Mapa Estratégico. Incorporado no novo módulo Plano Estratégico e BSC."),
]


def run_all(keys=ORDER):
    s = st.session_state
    f = {
        "pestel": lambda: pestel.analyze(state.current("pestel"), s.get("pestel_thr", 3.5)),
        "porter": lambda: porter.analyze(state.current("porter")),
        "micmac": lambda: micmac.analyze(state.current("micmac")),
        "cenarios": lambda: scenarios.analyze(state.current("cenarios")),
        "morfologica": lambda: morph.analyze(state.current("morfologica")),
        "swot": lambda: swot.analyze(state.current("swot")),
        "stakeholders": lambda: stakeholders.analyze(state.current("stakeholders"), s.get("stk_thr", 3.0), s.get("stk_sal", 4.0)),
        "bsc": lambda: bsc.analyze(state.current("bsc"), {"tows": state.current("swot")["estrategias"],
                                                          "roles": ram.roles(state.current("ram")["raci"])}),
        "ram": lambda: ram.analyze(state.current("ram")),
    }
    return [(k, f[k]()) for k in keys]


FLOW = """digraph {
rankdir=LR; bgcolor="transparent"; node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=11 color="#c9c8c2" fillcolor="#fcfcfb"];
edge [color="#8a8984"];
subgraph cluster1 {label="1 · Diagnóstico" fontname="Helvetica" fontsize=10 color="#e6e5e1"; P [label="PESTEL"]; F [label="5 Forças"];}
M [label="MICMAC\\n(variáveis-chave)" fillcolor="#e9f1fc"];
subgraph cluster3 {label="3 · Cenários" fontname="Helvetica" fontsize=10 color="#e6e5e1"; C [label="Scenario Planning\\n2×2 + wind tunneling" fillcolor="#e9f1fc"]; D [label="Scenario Development\\nmorfológica + CCA" fillcolor="#e9f1fc"];}
subgraph cluster4 {label="4 · Estratégia" fontname="Helvetica" fontsize=10 color="#e6e5e1"; S [label="SWOT → TOWS\\nplano de ação"]; B [label="Plano estratégico\\nvalores · visão · missão\\nSMART · BSC · mapa" fillcolor="#e9f1fc"];}
subgraph cluster5 {label="5 · Implementação" fontname="Helvetica" fontsize=10 color="#e6e5e1"; K [label="Stakeholders"]; R [label="RAM\\nRACI + Autoridade"];}
P -> M; F -> M; P -> C [label=" incertezas\\n críticas" fontsize=9 fontcolor="#52514e"]; M -> C [label=" motoras" fontsize=9 fontcolor="#52514e"]; M -> D; C -> S [label=" robustez" fontsize=9 fontcolor="#52514e"]; D -> S; F -> S; S -> B; B -> K; B -> R [label=" responsáveis" fontsize=9 fontcolor="#52514e"]; K -> R;
}"""


def page_home():
    s = st.session_state
    st.title("🧭 Estúdio de Cenários & Estratégia")
    st.markdown("Plataforma de **prospetiva e planeamento estratégico**: do diagnóstico do meio envolvente à construção de "
                "cenários e à atribuição de responsabilidades para a implementação. Cada modelo tem **legenda** "
                "(o que analisa, autor, ano, fonte), **análise**, **dashboard**, **conclusões automáticas** e **relatório**.")
    st.info(f"**Caso ativo:** {s.case}\n\n{s.context}\n\nMude de caso na barra lateral.")
    st.subheader("Percurso metodológico recomendado")
    st.graphviz_chart(FLOW)
    st.subheader("Modelos disponíveis")
    pages = s.get("_pages", {})
    cols = st.columns(2)
    for i, k in enumerate(ORDER):
        m = METHODS[k]
        with cols[i % 2].container(border=True):
            st.markdown(f"### {m['icone']} {m['nome']}")
            st.caption(f"{m['fase']} · {m['autor']} ({m['ano']})")
            st.markdown(m["objetivo"])
            if k in pages:
                st.page_link(pages[k], label="Abrir modelo →")
    st.subheader("Como usar")
    st.markdown("""
1. **Escolha um caso** na barra lateral (dois casos exemplo completos ou um caso em branco).
2. Em cada modelo, edite as tabelas no separador **📝 Dados** (ou importe um Excel com o modelo descarregado).
3. Veja os gráficos em **📊 Análise e dashboard** e as **✅ Conclusões** geradas automaticamente.
4. Descarregue o **📄 Relatório** de cada modelo, ou o **relatório integrado** com todos os modelos.
""")


def page_dashboard():
    s = st.session_state
    st.title("📈 Dashboard e relatório integrado")
    st.caption(f"Caso: **{s.case}**")
    sel = st.multiselect("Modelos a incluir", ORDER, default=ORDER, format_func=lambda k: f"{METHODS[k]['icone']} {METHODS[k]['nome']}")
    if not sel:
        st.stop()
    results = run_all(sel)
    summary = report.executive_summary(results)

    t1, t2, t3 = st.tabs(["📊 Dashboard", "🧾 Sumário executivo", "📄 Relatório integrado"])
    with t1:
        for k, r in results:
            with st.container(border=True):
                st.markdown(f"#### {METHODS[k]['icone']} {METHODS[k]['nome']}")
                if r.kpis:
                    cols = st.columns(len(r.kpis))
                    for c, (lbl, val, hlp) in zip(cols, r.kpis):
                        c.metric(lbl, val, help=hlp)
                if r.figs:
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.plotly_chart(r.figs[0][1], key=f"dash.{k}", config={"displaylogo": False})
                    with c2:
                        st.markdown("**Principais conclusões**")
                        for c in r.conclusions[:4]:
                            st.markdown(f"- {c}")
    with t2:
        st.markdown("Síntese das duas conclusões mais relevantes de cada modelo:")
        for x in summary:
            st.markdown(f"- {x}")
    with t3:
        html = report.build(results, s.case, s.context, summary=summary)
        st.download_button("📄 Descarregar relatório integrado (HTML)", html.encode("utf-8"), "relatorio_integrado.html",
                           "text/html", type="primary")
        st.caption(f"{len(results)} modelos · {sum(len(r.figs) for _, r in results)} gráficos interativos (funciona offline) · "
                   "abra no browser e use Ctrl+P → Guardar como PDF para obter um PDF.")
        xl = _excel_all()
        st.download_button("📊 Descarregar todos os dados do caso (Excel)", xl, "dados_caso.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def _excel_all():
    import io
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        for k in ORDER:
            for t, df in state.current(k).items():
                df.to_excel(xw, sheet_name=f"{k[:14]}_{t[:16]}", index=(k, t) in ui.INDEXED)
    return buf.getvalue()


def page_refs():
    st.title("📚 Referências e glossário")
    rows = [{"Modelo": f"{m['icone']} {m['nome']}", "Autor(es)": m["autor"], "Ano": m["ano"],
             "Referência": m["obra"].replace("*", ""), "Site": m["site"]} for m in (METHODS[k] for k in ORDER)]
    st.dataframe(pd.DataFrame(rows), hide_index=True,
                 column_config={"Referência": st.column_config.TextColumn(width="large")})
    st.subheader("Bibliografia complementar")
    st.markdown("""
- Savage, L. J. (1951). The Theory of Statistical Decision. *Journal of the American Statistical Association*, 46(253), 55–67 — critério minimax-regret usado no *wind tunneling*.
- Godet, M. & Roubelat, F. (1996). Creating the future: the use and misuse of scenarios. *Long Range Planning*, 29(2), 164–171.
- Ritchey, T. (2006). Problem structuring using computer-aided morphological analysis. *Journal of the Operational Research Society*, 57, 792–801.
- Bradfield, R., Wright, G., Burt, G., Cairns, G. & van der Heijden, K. (2005). The origins and evolution of scenario techniques in long range business planning. *Futures*, 37(8), 795–812.
""")
    st.subheader("Vídeos orientadores (indicados para o projeto)")
    for url, title, author, note in VIDEOS:
        with st.container(border=True):
            st.markdown(f"**{title}** — {author}")
            st.caption(note)
            st.video(url)
    st.subheader("Glossário")
    st.markdown("""
- **Tendência pesada** — evolução de alto impacto e previsível, presente em todos os cenários.
- **Incerteza crítica** — fator de alto impacto cuja evolução é imprevisível; base dos eixos de cenários.
- **Motricidade / dependência** — quanto uma variável influencia / é influenciada pelas restantes (MICMAC).
- **Configuração** — combinação de um estado por parâmetro na caixa morfológica.
- **CCA** — *Cross-Consistency Assessment*: avaliação par a par da compatibilidade entre estados.
- **Wind tunneling** — teste de estratégias contra vários cenários.
- **No-regret** — estratégia que não gera arrependimento em nenhum cenário.
- **Sinal de alerta (signpost)** — indicador precoce de que um cenário se está a concretizar.
- **Segregação de funções** — princípio de controlo interno: quem propõe/executa não aprova.
- **Visão / missão / valores** — onde queremos estar no futuro / o que fazemos hoje e para quem / o que é mais importante para nós.
- **Objetivo SMART** — específico, mensurável, atingível, relevante e com prazo (Doran, 1981).
- **Balanced Scorecard** — objetivos, indicadores, metas e iniciativas em quatro perspetivas: financeira, clientes, processos internos, aprendizagem e crescimento.
- **KPI** — indicador-chave de desempenho: o que se mede para provar que a meta foi atingida.
- **Mapa Estratégico** — diagrama das relações causa-efeito entre os objetivos do scorecard (Kaplan & Norton, 2004).
""")
