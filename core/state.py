"""Gestão de estado: caso ativo, dados-base (entrada dos editores) e dados correntes (editados)."""
import streamlit as st

from cases import CASES

DEFAULT = list(CASES)[0]


def init():
    if "data" not in st.session_state:
        load_case(DEFAULT)


def load_case(name: str):
    s = st.session_state
    build, ctx = CASES[name]
    s.case, s.context = name, ctx
    s.data = build()        # dados-base que alimentam os editores
    s.cur = {}              # últimos valores editados (por módulo/tabela)
    s.ver = s.get("ver", 0) + 1
    s.kver = {}             # versão por tabela (força recriação de um editor)


def current(module: str) -> dict:
    s = st.session_state
    base, cur = s.data[module], s.cur.get(module, {})
    return {k: cur.get(k, v) for k, v in base.items()}


def replace(module: str, key: str, df):
    s = st.session_state
    s.data[module][key] = df
    s.cur.setdefault(module, {}).pop(key, None)
    s.kver[f"{module}.{key}"] = s.kver.get(f"{module}.{key}", 0) + 1
