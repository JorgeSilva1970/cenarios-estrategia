import pandas as pd

from cases import ensino, seguradora

TITLE_BLANK = "Novo caso (modelo em branco)"


def blank():
    codes = ["V1", "V2", "V3"]
    roles = ["Patrocinador", "Gestor de Projeto", "Equipa"]
    return {
        "pestel": {"fatores": pd.DataFrame([["Político", "", 3, 3, "Médio", "="]],
                                           columns=["Dimensão", "Fator", "Impacto", "Incerteza", "Horizonte", "Tendência"])},
        "porter": {"fatores": pd.DataFrame([["Rivalidade entre concorrentes", "", 3]], columns=["Força", "Fator", "Intensidade"])},
        "micmac": {"variaveis": pd.DataFrame([[c, f"Variável {c}", ""] for c in codes], columns=["Código", "Variável", "Descrição"]),
                   "matriz": pd.DataFrame(0, index=codes, columns=codes)},
        "cenarios": {
            "eixos": pd.DataFrame([["X", "Incerteza crítica 1", "Baixo", "Alto"], ["Y", "Incerteza crítica 2", "Baixo", "Alto"]],
                                  columns=["Eixo", "Incerteza", "Polo −", "Polo +"]),
            "cenarios": pd.DataFrame([[q, f"Cenário {q}", "", "", "", 25] for q in ["Q1", "Q2", "Q3", "Q4"]],
                                     columns=["Quadrante", "Nome", "Narrativa", "Implicações e ações", "Sinais de alerta",
                                              "Probabilidade (%)"]),
            "estrategias": pd.DataFrame([["Estratégia 1", 0, 0, 0, 0]], columns=["Estratégia", "Q1", "Q2", "Q3", "Q4"]),
            "posicao": pd.DataFrame([["Hoje", 2026, 0.0, 0.0, ""], ["Horizonte", 2029, 0.0, 0.0, ""]],
                                    columns=["Momento", "Ano", "X (−1 a +1)", "Y (−1 a +1)", "Justificação"]),
            "casos": pd.DataFrame([["Económico", "", "", "", ""]],
                                  columns=["Dimensão", "Fator", "Business as usual", "Melhor caso", "Pior caso"])},
        "morfologica": {
            "parametros": pd.DataFrame([["Parâmetro A", "Estado A1"], ["Parâmetro A", "Estado A2"],
                                        ["Parâmetro B", "Estado B1"], ["Parâmetro B", "Estado B2"]], columns=["Parâmetro", "Estado"]),
            "incompatibilidades": pd.DataFrame(columns=["Estado A", "Estado B", "Tipo"]),
            "cenarios": pd.DataFrame([["Cenário 1", "Estado A1", "Estado B1"]], columns=["Cenário", "Parâmetro A", "Parâmetro B"])},
        "swot": {"fatores": pd.DataFrame([["Força", "", 0.5, 3], ["Fraqueza", "", 0.5, 2],
                                          ["Oportunidade", "", 0.5, 3], ["Ameaça", "", 0.5, 2]],
                                         columns=["Tipo", "Fator", "Peso", "Classificação"]),
                 "estrategias": pd.DataFrame(columns=["Quadrante", "Estratégia", "Fatores ligados", "Prioridade"])},
        "bsc": {"identidade": pd.DataFrame([["Valor", "", ""], ["Visão", "", ""], ["Missão", "", ""]],
                                           columns=["Elemento", "Declaração", "Descrição"]),
                "objetivos": pd.DataFrame([["F1", "Financeira", "", "", "", "↑", None, None, None, None, "", "", "", False, False, False]],
                                          columns=["Código", "Perspetiva", "Objetivo", "Indicador (KPI)", "Unidade", "Sentido",
                                                   "Base", "Meta", "Atual", "Prazo", "Iniciativa", "Responsável", "Origem",
                                                   "Específico", "Atingível", "Relevante"]),
                "ligacoes": pd.DataFrame(columns=["De", "Para"])},
        "stakeholders": {"stakeholders": pd.DataFrame([["", 3, 3, 3, 3, 0]],
                                                      columns=["Stakeholder", "Poder", "Interesse", "Legitimidade", "Urgência", "Atitude"])},
        "ram": {"raci": pd.DataFrame([["Fase 1", "Tarefa 1", "A", "R", "I"]], columns=["Fase", "Tarefa"] + roles),
                "autoridade": pd.DataFrame(columns=["Decisão", "Categoria", "Propõe", "Valida", "Aprova", "Informado"])},
    }


CASES = {
    seguradora.TITLE: (seguradora.build, seguradora.CONTEXT),
    ensino.TITLE: (ensino.build, ensino.CONTEXT),
    TITLE_BLANK: (blank, "Caso em branco: preencha as tabelas ou carregue um ficheiro Excel com o modelo."),
}
