"""Páginas: Scenario Planning (2×2) e Scenario Development (morfológica)."""
import pandas as pd
import streamlit as st

from core import state, ui
from models import micmac, morph, pestel, scenarios

CC = st.column_config


def page_scenarios():
    def inputs():
        st.info("Processo em 4 passos (SME Strategy): **1** forças motrizes → **2** incertezas críticas → "
                "**3** cenários plausíveis → **4** implicações e trajetória. Trabalhe-o em workshop com a equipa.")

        # ---------- Passo 1 ----------
        st.markdown("### Passo 1 · Forças motrizes (PESTEL)")
        pe = pestel.analyze(state.current("pestel"), st.session_state.get("pestel_thr", 3.5))
        if pe.tables:
            t = pe.tables[0][1]
            st.caption(f"{len(t)} forças motrizes identificadas na PESTEL do caso, ordenadas por impacto × incerteza. "
                       "Inclua forças positivas e negativas.")
            st.dataframe(t[["Dimensão", "Fator", "Impacto", "Incerteza", "Classe"]].head(8), hide_index=True)
        pages = st.session_state.get("_pages", {})
        if "pestel" in pages:
            st.page_link(pages["pestel"], label="Editar as forças motrizes na PESTEL →", icon="🌍")

        # ---------- Passo 2 ----------
        st.markdown("### Passo 2 · Incertezas críticas (eixos)")
        with st.container(border=True):
            st.markdown("**💡 Candidatos a eixos** — vindos das outras análises do caso")
            c1, c2 = st.columns(2)
            with c1:
                st.caption("Incertezas críticas (PESTEL)")
                cu = pestel.critical_uncertainties(state.current("pestel"), st.session_state.get("pestel_thr", 3.5))
                if cu.empty:
                    st.write("—")
                else:
                    st.dataframe(cu, hide_index=True)
            with c2:
                st.caption("Variáveis motoras e de ligação (MICMAC, indireto)")
                r = micmac.analyze(state.current("micmac"))
                if r.tables:
                    t = r.tables[0][1]
                    t = t[t["Classe (indireta)"].isin(["Motora", "Ligação"])][["Código", "Variável", "Classe (indireta)"]]
                    st.dataframe(t, hide_index=True)
            st.caption("Escolha **apenas duas**, de grande impacto, prováveis dentro do horizonte e **bem diferentes entre si**; "
                       "defina os dois extremos de cada uma. Pode repetir o exercício com outro par.")
        ui.editor("cenarios", "eixos", {"Eixo": CC.TextColumn(disabled=True, width="small"),
                                        "Incerteza": CC.TextColumn(width="large"),
                                        "Polo −": CC.TextColumn(help="Extremo negativo/baixo do eixo"),
                                        "Polo +": CC.TextColumn(help="Extremo positivo/alto do eixo")}, num_rows="fixed")

        # ---------- Passo 3 ----------
        st.markdown("### Passo 3 · Cenários plausíveis")
        st.caption("Q1 = (X+, Y+) · Q2 = (X−, Y+) · Q3 = (X−, Y−) · Q4 = (X+, Y−). Escreva cada narrativa **no presente**, "
                   "como se a equipa já estivesse nesse futuro, cobrindo as seis dimensões PESTEL.")
        cen = ui.editor("cenarios", "cenarios", {
            "Quadrante": CC.TextColumn(disabled=True, width="small"),
            "Nome": CC.TextColumn(width="medium"),
            "Narrativa": CC.TextColumn(width="large"),
            "Implicações e ações": CC.TextColumn(width="large", help="O que este futuro significa para a organização e o que fazer"),
            "Sinais de alerta": CC.TextColumn(width="large", help="Indicadores precoces que mostram que este futuro está a chegar"),
            "Probabilidade (%)": CC.NumberColumn(min_value=0, max_value=100, step=5, width="small"),
        }, num_rows="fixed")
        tot = pd.to_numeric(cen["Probabilidade (%)"], errors="coerce").sum()
        if abs(tot - 100) > 0.5:
            st.caption(f"ℹ️ As probabilidades somam {tot:.0f}% — serão normalizadas para o valor esperado.")
        with st.expander("Alternativa: business as usual / melhor caso / pior caso por fator PESTEL"):
            st.caption("Abordagem complementar: para um ano-alvo, descreva para cada fator a evolução tendencial, a mais favorável "
                       "e a mais desfavorável.")
            ui.editor("cenarios", "casos", {
                "Dimensão": CC.SelectboxColumn(options=pestel.DIMS, width="small"),
                "Fator": CC.TextColumn(width="medium"),
                "Business as usual": CC.TextColumn(width="medium"),
                "Melhor caso": CC.TextColumn(width="medium"),
                "Pior caso": CC.TextColumn(width="medium")})

        # ---------- Passo 4 ----------
        st.markdown("### Passo 4 · Implicações e trajetória")
        st.caption("Exercício de posicionamento: a equipa vota **onde está hoje** (−1 a +1 em cada eixo) e **para onde vai** "
                   "até ao horizonte. A seta aparece na matriz de cenários.")
        ui.editor("cenarios", "posicao", {
            "Momento": CC.TextColumn(width="small"),
            "Ano": CC.NumberColumn(min_value=2000, max_value=2100, step=1, format="%d", width="small"),
            "X (−1 a +1)": CC.NumberColumn(min_value=-1.0, max_value=1.0, step=0.05, format="%.2f", width="small"),
            "Y (−1 a +1)": CC.NumberColumn(min_value=-1.0, max_value=1.0, step=0.05, format="%.2f", width="small"),
            "Justificação": CC.TextColumn(width="large")})
        nm = scenarios.names(state.current("cenarios"))
        st.markdown("**Wind tunneling** — desempenho de cada estratégia em cada cenário (−2 falha grave … +2 muito bem)")
        ui.editor("cenarios", "estrategias", {
            "Estratégia": CC.TextColumn(width="large"),
            **{q: CC.NumberColumn(label=f"{q} · {nm[q]}", min_value=-2, max_value=2, step=1) for q in scenarios.QUADS}})
        st.caption("Os resultados devem alimentar a visão, a missão, os objetivos e o plano de ação — ver SWOT/TOWS e "
                   "Plano Estratégico e BSC.")

    ui.standard_tabs("cenarios", inputs, lambda: scenarios.analyze(state.current("cenarios")))


def page_morph():
    def inputs():
        st.markdown("**1. Parâmetros e estados** (uma linha por estado). Recomenda-se 4–7 parâmetros com 2–5 estados cada.")
        ui.editor("morfologica", "parametros", {"Parâmetro": CC.TextColumn(width="medium", required=True),
                                                "Estado": CC.TextColumn(width="large", required=True)})
        P = morph.params(state.current("morfologica"))
        labs = morph.labels(P)
        st.markdown("**2. Avaliação de consistência cruzada (CCA)** — pares de estados que **não podem coexistir**.")
        ui.editor("morfologica", "incompatibilidades", {
            "Estado A": CC.SelectboxColumn(options=labs, width="large"),
            "Estado B": CC.SelectboxColumn(options=labs, width="large"),
            "Tipo": CC.SelectboxColumn(options=["Lógica", "Empírica", "Normativa"], width="small",
                                       help="Ritchey: avalie primeiro lógica e empírica; a normativa só depois")})

        keys = list(P)

        def reshape(prev):
            m = prev.copy()
            if "Cenário" not in m:
                m.insert(0, "Cenário", "")
            return m.reindex(columns=["Cenário"] + keys)

        st.markdown("**3. Cenários desenvolvidos** — escolha um estado por parâmetro para cada cenário.")
        ui.editor("morfologica", "cenarios", {"Cenário": CC.TextColumn(width="medium"),
                                              **{k: CC.SelectboxColumn(options=P[k]) for k in keys}}, reshape=reshape)

    def explore(_res):
        st.markdown("Fixe um ou mais estados (**drivers**) e veja o que continua possível nos restantes parâmetros "
                    "— o *laboratório de cenários* de Ritchey.")
        d = state.current("morfologica")
        P = morph.params(d)
        bad = morph.incompat(d, P)
        cols = st.columns(min(len(P), 3) or 1)
        fixed = {}
        for i, (k, v) in enumerate(P.items()):
            with cols[i % len(cols)]:
                sel = st.selectbox(k, ["— livre —"] + v, key=f"drv.{k}.{st.session_state.ver}")
                if sel != "— livre —":
                    fixed[k] = sel
        n, poss = morph.options_after(P, bad, fixed)
        st.metric("Configurações consistentes com os drivers", n)
        rows = []
        for k, v in P.items():
            for s in v:
                rows.append({"Parâmetro": k, "Estado": s,
                             "Situação": "🔒 fixado" if fixed.get(k) == s else ("✅ possível" if s in poss[k] else "⛔ excluído")})
        st.dataframe(pd.DataFrame(rows), hide_index=True)

    ui.standard_tabs("morfologica", inputs, lambda: morph.analyze(state.current("morfologica")),
                     extra=("🔎 Explorar drivers", explore))
