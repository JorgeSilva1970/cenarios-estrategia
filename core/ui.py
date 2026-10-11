"""Componentes de interface partilhados por todos os modelos."""
import io

import pandas as pd
import streamlit as st

from core import report, state
from core.refs import METHODS

INDEXED = {("micmac", "matriz")}  # tabelas cujo índice faz parte dos dados


def header(key: str):
    m = METHODS[key]
    st.title(f"{m['icone']} {m['nome']}")
    st.caption(f"{m['fase']}  ·  Caso: **{st.session_state.case}**")


def legend(key: str, expanded: bool = True):
    m = METHODS[key]
    with st.expander("📖 Legenda — o que pretende analisar, autor, ano e fonte", expanded=expanded):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(f"**Objetivo.** {m['objetivo']}")
            st.markdown(f"**Descrição.** {m['descricao']}")
            st.markdown(f"**Como ler os resultados.** {m['leitura']}")
        with c2:
            st.markdown(f"**Autor(es):** {m['autor']}")
            st.markdown(f"**Ano:** {m['ano']}")
            st.markdown(f"**Referência:** {m['obra']}")
            st.markdown("**Site:** " + " · ".join(f"[{u.strip()}]({u.strip()})" for u in m["site"].split("·")))


def editor(module: str, key: str, column_config=None, num_rows="dynamic", reshape=None, height=None,
           hide_index=True, disabled=None):
    """data_editor com padrão base/corrente (evita duplicar edições) e reconfiguração opcional."""
    s = st.session_state
    base = s.data[module][key]
    if reshape is not None:
        prev = s.cur.get(module, {}).get(key, base)
        new = reshape(prev)
        if list(new.columns) != list(base.columns) or list(new.index) != list(base.index):
            state.replace(module, key, new)
            base = new
    k = f"ed.{module}.{key}.{s.ver}.{s.kver.get(f'{module}.{key}', 0)}"
    extra = {"height": height} if height else {}
    if disabled is not None:
        extra["disabled"] = disabled
    out = st.data_editor(base, key=k, column_config=column_config, num_rows=num_rows, hide_index=hide_index, **extra)
    s.cur.setdefault(module, {})[key] = out
    return out


def io_panel(module: str):
    """Exportar/importar todas as tabelas do módulo em Excel (uma folha por tabela)."""
    s = st.session_state
    with st.expander("📥 Importar / 📤 exportar dados (Excel)"):
        data = state.current(module)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as xw:
            for k, df in data.items():
                df.to_excel(xw, sheet_name=k[:31], index=(module, k) in INDEXED)
        st.download_button("Descarregar dados atuais / modelo (.xlsx)", buf.getvalue(), f"{module}.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key=f"dl.{module}")
        st.caption("Para usar dados próprios: descarregue o ficheiro, edite-o mantendo os nomes das folhas e colunas, e carregue-o.")
        f = st.file_uploader("Carregar ficheiro Excel com as mesmas folhas", type=["xlsx"], key=f"up.{module}.{s.ver}")
        if f is not None and s.get(f"up_done.{module}") != f.file_id:
            try:
                xl = pd.read_excel(f, sheet_name=None, index_col=None)
                n = 0
                for k in data:
                    if k in xl:
                        df = xl[k]
                        if (module, k) in INDEXED:
                            df = df.set_index(df.columns[0])
                            df.index = df.index.astype(str)
                            df.columns = df.columns.astype(str)
                        state.replace(module, k, df)
                        n += 1
                s[f"up_done.{module}"] = f.file_id
                st.success(f"{n} tabela(s) importada(s).")
                st.rerun()
            except Exception as e:  # noqa: BLE001
                st.error(f"Não foi possível ler o ficheiro: {e}")


def show(module: str, res, figs=True, tables=True, key_suffix=""):
    """Apresenta KPIs, avisos, gráficos e tabelas de um Result."""
    if res.kpis:
        cols = st.columns(len(res.kpis))
        for c, (lbl, val, hlp) in zip(cols, res.kpis):
            c.metric(lbl, val, help=hlp)
    for w in res.warnings:
        st.warning(w)
    if figs:
        for i, (cap, fig) in enumerate(res.figs):
            st.plotly_chart(fig, key=f"fig.{module}.{i}{key_suffix}", config={"displaylogo": False})
            st.caption(cap)
    if tables:
        for cap, df in res.tables:
            if df is not None and not df.empty:
                st.markdown(f"**{cap}**")
                st.dataframe(df, hide_index=True)


def conclusions(res):
    if not res.conclusions:
        st.info("Sem conclusões — complete os dados.")
    for c in res.conclusions:
        st.markdown(f"- {c}")


def report_button(module: str, res):
    html = report.build([(module, res)], st.session_state.case, st.session_state.context,
                        title=f"Relatório — {METHODS[module]['nome']}")
    st.download_button("📄 Descarregar relatório HTML deste modelo", html.encode("utf-8"),
                       f"relatorio_{module}.html", "text/html", key=f"rep.{module}", type="primary")
    st.caption("O relatório inclui a legenda, os gráficos interativos, as tabelas e as conclusões. "
               "Abra-o no browser e use Ctrl+P → Guardar como PDF.")


def standard_tabs(module: str, inputs_fn, analyze_fn, extra=None):
    """Esqueleto comum: Dados → Análise/Dashboard → [extra] → Conclusões → Relatório."""
    header(module)
    legend(module, expanded=False)
    names = ["📝 Dados", "📊 Análise e dashboard"] + ([extra[0]] if extra else []) + ["✅ Conclusões", "📄 Relatório"]
    tabs = st.tabs(names)
    t1, t2, t3, t4 = tabs[0], tabs[1], tabs[-2], tabs[-1]
    with t1:
        inputs_fn()
        io_panel(module)
    res = analyze_fn()
    with t2:
        show(module, res)
    if extra:
        with tabs[2]:
            extra[1](res)
    with t3:
        conclusions(res)
    with t4:
        report_button(module, res)
    return res
