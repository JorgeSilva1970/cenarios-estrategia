"""Páginas: PESTEL, Porter, MICMAC."""
import pandas as pd
import streamlit as st

from core import state, ui
from models import micmac, pestel, porter

CC = st.column_config


def page_pestel():
    def inputs():
        st.markdown("Pontue cada fator de **1 (baixo)** a **5 (alto)** em impacto e incerteza. Adicione linhas no fim da tabela.")
        ui.editor("pestel", "fatores", {
            "Dimensão": CC.SelectboxColumn(options=pestel.DIMS, required=True, width="small"),
            "Fator": CC.TextColumn(width="large"),
            "Impacto": CC.NumberColumn(min_value=1, max_value=5, step=1, width="small"),
            "Incerteza": CC.NumberColumn(min_value=1, max_value=5, step=1, width="small"),
            "Horizonte": CC.SelectboxColumn(options=["Curto", "Médio", "Longo"], width="small"),
            "Tendência": CC.SelectboxColumn(options=["↑", "↓", "="], width="small"),
        })
        st.slider("Limiar de 'alto' (impacto e incerteza)", 2.5, 4.5, 3.5, 0.5, key="pestel_thr",
                  help="Fatores com pontuação ≥ limiar são considerados altos.")

    ui.standard_tabs("pestel", inputs,
                     lambda: pestel.analyze(state.current("pestel"), st.session_state.get("pestel_thr", 3.5)))


def page_porter():
    def inputs():
        st.markdown("Para cada força, liste os fatores e pontue a **intensidade da ameaça** de 1 (baixa) a 5 (alta).")
        ui.editor("porter", "fatores", {
            "Força": CC.SelectboxColumn(options=porter.FORCES, required=True, width="medium"),
            "Fator": CC.TextColumn(width="large"),
            "Intensidade": CC.NumberColumn(min_value=1, max_value=5, step=1, width="small"),
        })
    ui.standard_tabs("porter", inputs, lambda: porter.analyze(state.current("porter")))


def page_micmac():
    def inputs():
        st.markdown("**1. Variáveis do sistema** — use códigos curtos e únicos (ex.: REG, INF).")
        v = ui.editor("micmac", "variaveis", {"Código": CC.TextColumn(width="small", required=True),
                                              "Variável": CC.TextColumn(width="medium"),
                                              "Descrição": CC.TextColumn(width="large")})
        codes = [str(c).strip() for c in v["Código"].dropna() if str(c).strip() not in ("", "None")]
        codes = list(dict.fromkeys(codes))

        def reshape(prev):
            m = prev.copy()
            m.index, m.columns = m.index.astype(str), m.columns.astype(str)
            return m.reindex(index=codes, columns=codes).fillna(0).astype(int)

        st.markdown("**2. Matriz de influências diretas** — a linha influencia a coluna: "
                    "0 = nenhuma · 1 = fraca · 2 = média · 3 = forte. A diagonal é ignorada.")
        ui.editor("micmac", "matriz", {c: CC.NumberColumn(min_value=0, max_value=3, step=1, width="small") for c in codes},
                  num_rows="fixed", reshape=reshape, hide_index=False)

    ui.standard_tabs("micmac", inputs, lambda: micmac.analyze(state.current("micmac")))
