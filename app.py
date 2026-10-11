"""Estúdio de Cenários & Estratégia — ponto de entrada Streamlit.

Executar localmente:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="Estúdio de Cenários & Estratégia", page_icon="🧭", layout="wide")

import core.theme  # noqa: E402,F401  (regista o tema Plotly)
from cases import CASES  # noqa: E402
from core import state  # noqa: E402
from core.refs import METHODS  # noqa: E402
from views import general, models_a, models_b, models_c  # noqa: E402

state.init()

# ---------- Barra lateral: escolha do caso ----------
with st.sidebar:
    st.markdown("### 🧭 Estúdio de Cenários")
    names = list(CASES)
    choice = st.selectbox("Caso em análise", names, index=names.index(st.session_state.case))
    if choice != st.session_state.case:
        state.load_case(choice)
        st.rerun()
    if st.button("↺ Repor dados do caso", help="Descarta as alterações e recarrega o caso exemplo"):
        state.load_case(st.session_state.case)
        st.rerun()
    st.caption(st.session_state.context)

# ---------- Navegação ----------
def P(fn, key, url, title):
    return st.Page(fn, title=title, icon=METHODS[key]["icone"], url_path=url)


pages = {
    "pestel": P(models_a.page_pestel, "pestel", "pestel", "PESTEL"),
    "porter": P(models_a.page_porter, "porter", "porter", "Cinco Forças de Porter"),
    "micmac": P(models_a.page_micmac, "micmac", "micmac", "MICMAC"),
    "cenarios": P(models_b.page_scenarios, "cenarios", "scenario-planning", "Scenario Planning (2×2)"),
    "morfologica": P(models_b.page_morph, "morfologica", "scenario-development", "Scenario Development"),
    "swot": P(models_c.page_swot, "swot", "swot-tows", "SWOT / TOWS"),
    "bsc": P(models_c.page_bsc, "bsc", "plano-estrategico", "Plano Estratégico e BSC"),
    "stakeholders": P(models_c.page_stakeholders, "stakeholders", "stakeholders", "Stakeholders"),
    "ram": P(models_c.page_ram, "ram", "ram-raci", "RAM — RACI e Autoridade"),
}
st.session_state["_pages"] = pages
home = st.Page(general.page_home, title="Início", icon="🏠", default=True)
nav = st.navigation({
    "": [home],
    "1 · Diagnóstico": [pages["pestel"], pages["porter"]],
    "2 · Variáveis-chave": [pages["micmac"]],
    "3 · Cenários": [pages["cenarios"], pages["morfologica"]],
    "4 · Estratégia": [pages["swot"], pages["bsc"]],
    "5 · Implementação": [pages["stakeholders"], pages["ram"]],
    "Resultados": [st.Page(general.page_dashboard, title="Dashboard e relatório", icon="📈", url_path="dashboard"),
                   st.Page(general.page_refs, title="Referências", icon="📚", url_path="referencias")],
})
nav.run()
