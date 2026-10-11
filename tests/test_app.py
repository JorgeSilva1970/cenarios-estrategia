"""Testes: modelos (lógica) e páginas (renderização sem erros) para todos os casos."""
import sys
from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import CASES  # noqa: E402
from core import report  # noqa: E402
from models import bsc, micmac, morph, pestel, porter, ram, scenarios, stakeholders, swot  # noqa: E402

MODELS = {"pestel": pestel, "porter": porter, "micmac": micmac, "cenarios": scenarios, "morfologica": morph,
          "swot": swot, "bsc": bsc, "stakeholders": stakeholders, "ram": ram}


@pytest.mark.parametrize("case", list(CASES))
def test_models_run(case):
    data = CASES[case][0]()
    results = [(k, m.analyze(data[k])) for k, m in MODELS.items()]
    html = report.build(results, case, "ctx")
    assert html.count("<h2") >= 8


def test_micmac_direct_sums():
    M = np.array([[0, 3, 0], [0, 0, 2], [1, 0, 0]], float)
    inf, dep, *_ = micmac.micmac(M)
    assert list(inf) == [3, 2, 1] and list(dep) == [1, 3, 2]


def test_morph_cca():
    P = {"A": ["a1", "a2"], "B": ["b1", "b2"]}
    bad = {frozenset(("A: a1", "B: b1"))}
    _, sols = morph.solve(P, bad)
    assert len(sols) == 3 and ("a1", "b1") not in sols


def test_ram_rules():
    data = CASES[list(CASES)[0]][0]()["ram"]
    r = ram.analyze(data)
    probs = r.tables[0][1]
    assert (probs["Problema"].str.contains("Sem Aprovador")).any()
    assert (probs["Problema"].str.contains("Segregação")).any()


def test_ie_cells():
    assert swot.ie_cell(3.5, 3.5)[0] == "I"
    assert swot.ie_cell(2.5, 2.5)[0] == "V"
    assert swot.ie_cell(1.5, 1.5)[0] == "IX"


def _page_script(page):
    return f"""
import sys; sys.path.insert(0, {str(ROOT)!r})
import streamlit as st
import core.theme
from core import state
from views import general, models_a, models_b, models_c
state.init()
if st.session_state.case != CASE:
    state.load_case(CASE)
{page}()
"""


PAGES = ["general.page_home", "models_a.page_pestel", "models_a.page_porter", "models_a.page_micmac",
         "models_b.page_scenarios", "models_b.page_morph", "models_c.page_swot", "models_c.page_bsc", "models_c.page_stakeholders",
         "models_c.page_ram", "general.page_dashboard", "general.page_refs"]


@pytest.mark.parametrize("case", list(CASES))
@pytest.mark.parametrize("page", PAGES)
def test_pages_render(page, case):
    at = AppTest.from_string(f"CASE = {case!r}\n" + _page_script(page), default_timeout=60)
    at.run()
    assert not at.exception, at.exception


def test_ram_roles_reshape():
    at = AppTest.from_string("CASE = " + repr(list(CASES)[0]) + "\n" + _page_script("models_c.page_ram"), default_timeout=60)
    at.run()
    roles = at.text_area[0].value.splitlines()
    at.text_area[0].set_value("\n".join(roles[:3] + ["Novo Papel"])).run()
    assert not at.exception
    cols = list(at.session_state["data"]["ram"]["raci"].columns)
    assert cols == ["Fase", "Tarefa"] + roles[:3] + ["Novo Papel"]


def test_case_switch_and_report():
    at = AppTest.from_string("CASE = " + repr(list(CASES)[1]) + "\n" + _page_script("general.page_dashboard"), default_timeout=60)
    at.run()
    assert not at.exception
    assert at.session_state["case"] == list(CASES)[1]


def test_report_is_self_contained():
    """O relatório não depende de CDN: a biblioteca Plotly vai embutida (evita 'Plotly is not defined')."""
    data = CASES[list(CASES)[0]][0]()
    res = [(k, m.analyze(data[k])) for k, m in MODELS.items()]
    html = report.build(res, "c", "ctx", summary=report.executive_summary(res))
    assert "<script src=" not in html and "src=\"https://cdn.plot.ly" not in html  # nenhum script externo
    assert html.index("Plotly") < html.index('class="fig"')  # biblioteca definida antes dos gráficos
    assert "Sumário executivo" in html
