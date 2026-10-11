"""Páginas: SWOT/TOWS, Stakeholders, RAM."""
import html

import pandas as pd
import streamlit as st

from core import state, ui
from core.result import clean
from models import ram, stakeholders, swot

CC = st.column_config


def page_swot():
    def inputs():
        st.markdown("Pesos: os fatores **internos** (forças + fraquezas) somam 1 e os **externos** (oportunidades + ameaças) "
                    "somam 1. Classificação: 1 = fraqueza grave/resposta fraca … 4 = força maior/resposta excelente.")
        f = ui.editor("swot", "fatores", {
            "Tipo": CC.SelectboxColumn(options=list(swot.TYPES), required=True, width="small"),
            "Fator": CC.TextColumn(width="large"),
            "Peso": CC.NumberColumn(min_value=0.0, max_value=1.0, step=0.01, format="%.2f", width="small"),
            "Classificação": CC.NumberColumn(min_value=1, max_value=4, step=1, width="small")})
        w = pd.to_numeric(f["Peso"], errors="coerce").fillna(0)
        wi = w[f["Tipo"].isin(["Força", "Fraqueza"])].sum()
        we = w[f["Tipo"].isin(["Oportunidade", "Ameaça"])].sum()
        c1, c2 = st.columns(2)
        c1.metric("Soma pesos internos", f"{wi:.2f}", delta=None if abs(wi - 1) < 0.01 else f"{wi - 1:+.2f}", delta_color="off")
        c2.metric("Soma pesos externos", f"{we:.2f}", delta=None if abs(we - 1) < 0.01 else f"{we - 1:+.2f}", delta_color="off")
        st.markdown("**Matriz TOWS — estratégias = plano de ação** (prioridade 1 = mais alta)")
        st.caption("Estas estratégias são o plano de ação que resulta da SWOT. No **Plano Estratégico e BSC** cada uma é "
                   "traduzida em objetivos SMART com indicador, meta, iniciativa e responsável.")
        ui.editor("swot", "estrategias", {
            "Quadrante": CC.SelectboxColumn(options=list(swot.QUADS), required=True, width="small",
                                            help="; ".join(f"{k}: {v}" for k, v in swot.QUADS.items())),
            "Estratégia": CC.TextColumn(width="large"),
            "Fatores ligados": CC.TextColumn(width="small"),
            "Prioridade": CC.NumberColumn(min_value=1, max_value=5, step=1, width="small")})

    def grid(_res):
        d = state.current("swot")
        f = clean(d["fatores"], "Fator")
        s = clean(d["estrategias"], "Estratégia")

        def box(title, items, color):
            li = "".join(f"<li>{html.escape(str(i))}</li>" for i in items) or "<li>—</li>"
            return (f"<div style='border-top:4px solid {color};background:#fcfcfb;border-radius:8px;padding:10px 14px;"
                    f"height:100%'><b>{title}</b><ul style='margin:6px 0 0 -10px;font-size:14px'>{li}</ul></div>")
        st.markdown("#### Quadro SWOT")
        c = st.columns(2)
        c[0].markdown(box("💪 Forças (S)", f[f.Tipo == "Força"].Fator, swot.TCOL["Força"]), unsafe_allow_html=True)
        c[1].markdown(box("⚠️ Fraquezas (W)", f[f.Tipo == "Fraqueza"].Fator, swot.TCOL["Fraqueza"]), unsafe_allow_html=True)
        c = st.columns(2)
        c[0].markdown(box("🚀 Oportunidades (O)", f[f.Tipo == "Oportunidade"].Fator, swot.TCOL["Oportunidade"]), unsafe_allow_html=True)
        c[1].markdown(box("🌩️ Ameaças (T)", f[f.Tipo == "Ameaça"].Fator, swot.TCOL["Ameaça"]), unsafe_allow_html=True)
        st.markdown("#### Matriz TOWS (Weihrich, 1982)")
        c = st.columns(2)
        for i, q in enumerate(["SO", "WO", "ST", "WT"]):
            items = s[s.Quadrante == q].Estratégia if not s.empty else []
            c[i % 2].markdown(box(f"{q} — {swot.QUADS[q]}", items, "#2a78d6"), unsafe_allow_html=True)

    ui.standard_tabs("swot", inputs, lambda: swot.analyze(state.current("swot")), extra=("🧱 Quadro SWOT/TOWS", grid))


def page_stakeholders():
    def inputs():
        st.markdown("Escalas 1–5 para **Poder**, **Interesse**, **Legitimidade** e **Urgência**; "
                    "**Atitude** de −2 (opositor ativo) a +2 (apoiante ativo).")
        n15 = dict(min_value=1, max_value=5, step=1, width="small")
        ui.editor("stakeholders", "stakeholders", {
            "Stakeholder": CC.TextColumn(width="large"),
            "Poder": CC.NumberColumn(**n15), "Interesse": CC.NumberColumn(**n15),
            "Legitimidade": CC.NumberColumn(**n15), "Urgência": CC.NumberColumn(**n15),
            "Atitude": CC.NumberColumn(min_value=-2, max_value=2, step=1, width="small")})
        c1, c2 = st.columns(2)
        c1.slider("Limiar de poder/interesse 'alto' (Mendelow)", 2.0, 4.0, 3.0, 0.5, key="stk_thr")
        c2.slider("Limiar para atributo de saliência presente", 3.0, 5.0, 4.0, 0.5, key="stk_sal")

    ui.standard_tabs("stakeholders", inputs, lambda: stakeholders.analyze(
        state.current("stakeholders"), st.session_state.get("stk_thr", 3.0), st.session_state.get("stk_sal", 4.0)))


def page_ram():
    def inputs():
        st.markdown("**Legenda RACI/RASCI:** " + " · ".join(f"**{k}** = {v}" for k, v in ram.LEGEND.items()))
        cur = state.current("ram")["raci"]
        default = "\n".join(ram.roles(cur))
        txt = st.text_area("Papéis (um por linha) — alterar aqui acrescenta/remove colunas da matriz", default,
                           key=f"roles.{st.session_state.ver}", height=190)
        roles = list(dict.fromkeys(r.strip() for r in txt.splitlines() if r.strip()))

        def reshape(prev):
            out = prev.reindex(columns=["Fase", "Tarefa"] + roles)
            out[roles] = out[roles].fillna("—").replace("", "—")
            return out

        st.markdown("**1. Matriz de responsabilidades (RACI)**")
        ui.editor("ram", "raci", {"Fase": CC.TextColumn(width="small"), "Tarefa": CC.TextColumn(width="large"),
                                  **{r: CC.SelectboxColumn(options=ram.CODES) for r in roles}},
                  reshape=reshape)
        st.markdown("**2. Matriz de autoridade (delegação de competências)** — quem propõe, valida e aprova cada decisão.")
        ui.editor("ram", "autoridade", {"Decisão": CC.TextColumn(width="large"), "Categoria": CC.TextColumn(width="small")})
        st.caption("Regras verificadas automaticamente: um único A por tarefa, pelo menos um R, nº de consultados, "
                   "sobrecarga de papéis, aprovador definido e segregação de funções (quem propõe ≠ quem aprova).")

    ui.standard_tabs("ram", inputs, lambda: ram.analyze(state.current("ram")))


def _bsc_context():
    from models import ram as ram_model
    return {"tows": state.current("swot")["estrategias"], "roles": ram_model.roles(state.current("ram")["raci"])}


def page_bsc():
    from models import bsc, ram as ram_model

    def inputs():
        st.info("Guia passo a passo (E. Shehab): **1** valores → **2** visão → **3** missão → **4** SWOT e plano de ação → "
                "**5** objetivos SMART no Balanced Scorecard, com indicadores, metas, iniciativas e responsáveis → "
                "**6** Mapa Estratégico.")

        st.markdown("### Passos 1–3 · Valores, visão e missão")
        st.caption("**Valores**: o que é mais importante para a organização (se não forem claros, faça um brainstorming com a "
                   "equipa). **Visão**: onde se vê a organização daqui a 2, 5 ou mais anos — seja realista. "
                   "**Missão**: o que a organização faz hoje, e para quem — olhe para onde realmente está.")
        ui.editor("bsc", "identidade", {
            "Elemento": CC.SelectboxColumn(options=["Valor", "Visão", "Missão"], required=True, width="small"),
            "Declaração": CC.TextColumn(width="large"),
            "Descrição": CC.TextColumn(width="medium")})

        st.markdown("### Passo 4 · SWOT e plano de ação")
        tw = clean(state.current("swot")["estrategias"], "Estratégia")
        if tw.empty:
            st.write("Ainda não há estratégias TOWS.")
        else:
            st.caption("Estratégias TOWS do caso: cada uma deve dar origem a pelo menos um objetivo do scorecard (coluna *Origem*).")
            st.dataframe(tw, hide_index=True)
        pages = st.session_state.get("_pages", {})
        if "swot" in pages:
            st.page_link(pages["swot"], label="Editar a SWOT/TOWS →", icon="🎯")

        st.markdown("### Passo 5 · Objetivos SMART no Balanced Scorecard")
        q = st.columns(4)
        for c, p in zip(q, bsc.PERSP):
            c.markdown(f"<div style='border-top:4px solid {bsc.PCOL[p]};padding:6px 4px;font-size:13px'><b>{p}</b><br>"
                       f"<i>{bsc.PQ[p]}</i></div>", unsafe_allow_html=True)
        cur = state.current("bsc")["objetivos"]
        roles = ram_model.roles(state.current("ram")["raci"])
        owners = list(dict.fromkeys(roles + [str(x) for x in cur["Responsável"].dropna() if str(x).strip()]))
        origins = list(dict.fromkeys(list(tw["Estratégia"]) if not tw.empty else [])) + [
            "Scenario Planning (estratégia robusta)", "Scenario Planning (estratégia condicional)", "Outra"]
        origins = list(dict.fromkeys(origins + [str(x) for x in cur["Origem"].dropna() if str(x).strip()]))
        ui.editor("bsc", "objetivos", {
            "Código": CC.TextColumn(width="small", help="Ex.: F1, C2, P1, A1"),
            "Perspetiva": CC.SelectboxColumn(options=bsc.PERSP, required=True),
            "Objetivo": CC.TextColumn(width="medium"),
            "Indicador (KPI)": CC.TextColumn(width="medium", help="O que se pode medir para provar que o objetivo foi atingido"),
            "Unidade": CC.TextColumn(width="small"),
            "Sentido": CC.SelectboxColumn(options=["↑", "↓"], width="small", help="↑ maior é melhor · ↓ menor é melhor"),
            "Base": CC.NumberColumn(width="small"), "Meta": CC.NumberColumn(width="small"), "Atual": CC.NumberColumn(width="small"),
            "Prazo": CC.NumberColumn(min_value=2000, max_value=2100, step=1, format="%d", width="small"),
            "Iniciativa": CC.TextColumn(width="medium", help="Ação que garante que a meta do KPI é cumprida"),
            "Responsável": CC.SelectboxColumn(options=owners, help="Quem apoia e suporta o objetivo (papéis da RAM)"),
            "Origem": CC.SelectboxColumn(options=origins, width="medium", help="Estratégia TOWS ou cenário que originou o objetivo"),
            "Específico": CC.CheckboxColumn(width="small"), "Atingível": CC.CheckboxColumn(width="small"),
            "Relevante": CC.CheckboxColumn(width="small")})
        st.caption("SMART: *Mensurável* (tem KPI e meta) e *Temporal* (tem prazo) são verificados automaticamente; "
                   "*Específico*, *Atingível* e *Relevante* são confirmados pela equipa.")

        st.markdown("### Passo 6 · Mapa Estratégico (relações causa-efeito)")
        codes = [str(c).strip() for c in state.current("bsc")["objetivos"]["Código"].dropna() if str(c).strip()]
        st.caption("Cada linha liga um objetivo a outro que ele ajuda a alcançar — normalmente de baixo para cima: "
                   "aprendizagem → processos → clientes → financeira.")
        ui.editor("bsc", "ligacoes", {"De": CC.SelectboxColumn(options=codes), "Para": CC.SelectboxColumn(options=codes)})

    ui.standard_tabs("bsc", inputs, lambda: bsc.analyze(state.current("bsc"), _bsc_context()))
