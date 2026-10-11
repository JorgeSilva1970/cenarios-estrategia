"""Caso exemplo 2 — EdTech: plataforma de aprendizagem digital para o Ensino Básico, horizonte 2035."""
import pandas as pd

TITLE = "EdTech — Aprendizagem Digital no Ensino Básico 2035"
CONTEXT = ("Empresa portuguesa de recursos educativos digitais para o 1.º e 2.º ciclos que avalia o lançamento de um "
           "tutor com IA, num contexto de fim de fundos PRR, regulação europeia de IA e debate sobre tempo de ecrã.")


def build():
    pestel = pd.DataFrame([
        ["Político", "Prioridade política à transição digital na educação", 4, 3, "Médio", "↑"],
        ["Político", "Autonomia e flexibilidade curricular das escolas", 3, 3, "Médio", "="],
        ["Económico", "Fim do financiamento PRR para equipamentos e conteúdos", 4, 4, "Curto", "↓"],
        ["Económico", "Custos de manutenção e renovação de equipamentos", 3, 2, "Médio", "↑"],
        ["Social", "Desigualdade de acesso digital das famílias", 4, 3, "Médio", "="],
        ["Social", "Escassez e envelhecimento do corpo docente", 5, 2, "Longo", "↑"],
        ["Social", "Preocupação com tempo de ecrã e bem-estar das crianças", 4, 4, "Médio", "↑"],
        ["Tecnológico", "IA generativa em contexto de aprendizagem", 5, 5, "Curto", "↑"],
        ["Tecnológico", "Plataformas de gestão da aprendizagem e manuais digitais", 4, 3, "Curto", "↑"],
        ["Tecnológico", "Conectividade e infraestrutura de rede nas escolas", 4, 2, "Curto", "↑"],
        ["Ecológico", "Pegada ambiental dos equipamentos (resíduos eletrónicos)", 2, 2, "Longo", "↑"],
        ["Legal", "Proteção de dados de menores (RGPD)", 4, 2, "Curto", "↑"],
        ["Legal", "Regras sobre uso de telemóveis e ecrãs nas escolas", 3, 4, "Curto", "↑"],
        ["Legal", "AI Act — IA na educação classificada de risco elevado", 4, 3, "Médio", "↑"],
    ], columns=["Dimensão", "Fator", "Impacto", "Incerteza", "Horizonte", "Tendência"])

    porter = pd.DataFrame([
        ["Rivalidade entre concorrentes", "Editoras tradicionais com plataformas próprias", 5],
        ["Rivalidade entre concorrentes", "Plataformas globais gratuitas", 4],
        ["Rivalidade entre concorrentes", "Diferenciação de conteúdos", 3],
        ["Ameaça de novos entrantes", "Startups com IA generativa", 5],
        ["Ameaça de novos entrantes", "Baixo custo de produção de conteúdos com IA", 4],
        ["Ameaça de novos entrantes", "Certificação e adoção pelo Ministério", 2],
        ["Ameaça de substitutos", "Assistentes de IA de uso geral", 4],
        ["Ameaça de substitutos", "Recursos educativos abertos (REA)", 3],
        ["Ameaça de substitutos", "Explicações presenciais", 2],
        ["Poder negocial dos fornecedores", "Fornecedores de modelos de IA (APIs)", 4],
        ["Poder negocial dos fornecedores", "Fornecedores de cloud", 3],
        ["Poder negocial dos fornecedores", "Autores e ilustradores", 2],
        ["Poder negocial dos clientes", "Compras públicas centralizadas", 5],
        ["Poder negocial dos clientes", "Famílias sensíveis ao preço", 3],
        ["Poder negocial dos clientes", "Professores como prescritores", 4],
    ], columns=["Força", "Fator", "Intensidade"])

    codes = ["POL", "FIN", "DOC", "IAG", "INF", "FAM", "BEM", "ADO", "APR", "DAD"]
    var = pd.DataFrame([
        ["POL", "Política educativa digital", "Orientações e programas nacionais"],
        ["FIN", "Financiamento", "Fundos públicos (PRR, OE, municípios) para o digital"],
        ["DOC", "Competências digitais docentes", "Formação e confiança dos professores"],
        ["IAG", "IA generativa", "Maturidade e custo das ferramentas de IA"],
        ["INF", "Infraestrutura e conectividade", "Equipamentos e rede nas escolas"],
        ["FAM", "Acesso digital das famílias", "Equipamentos e internet em casa"],
        ["BEM", "Preocupação com bem-estar", "Pressão social sobre ecrãs e IA"],
        ["ADO", "Adoção da plataforma", "Utilização efetiva por escolas e alunos"],
        ["APR", "Resultados de aprendizagem", "Desempenho dos alunos"],
        ["DAD", "Regulação de dados e IA", "RGPD e AI Act aplicados a menores"],
    ], columns=["Código", "Variável", "Descrição"])
    M = [
        [0, 3, 2, 0, 2, 0, 0, 3, 0, 2],
        [0, 0, 2, 0, 3, 2, 0, 3, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 3, 3, 0],
        [2, 1, 2, 0, 1, 0, 2, 3, 2, 3],
        [0, 0, 1, 0, 0, 0, 0, 3, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 2, 0],
        [2, 0, 1, 1, 0, 0, 0, 2, 1, 1],
        [0, 1, 1, 0, 1, 0, 0, 0, 2, 0],
        [1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    ]
    mat = pd.DataFrame(M, index=codes, columns=codes)

    eixos = pd.DataFrame([
        ["X", "Integração da IA na sala de aula", "Restrita", "Generalizada"],
        ["Y", "Investimento público em educação digital", "Escasso", "Robusto"],
    ], columns=["Eixo", "Incerteza", "Polo −", "Polo +"])
    cen = pd.DataFrame([
        ["Q1", "Tutor para Todos", "O Estado financia tutores de IA certificados para todos os alunos; o professor torna-se "
         "curador e analista da aprendizagem.", "Concurso público nacional para tutores IA; orientações da DGE sobre IA", 25],
        ["Q2", "Digital Humanista", "Investimento forte em equipamentos e formação, mas a IA é usada apenas pelo professor; "
         "valoriza-se o contacto humano.", "Restrições legais ao uso de IA por menores; programas de formação docente", 30],
        ["Q3", "Regresso ao Papel", "Sem fundos e com desconfiança social, as escolas regressam ao manual em papel; "
         "o digital fica para casa.", "Fim do PRR sem substituto; campanhas contra ecrãs", 20],
        ["Q4", "IA a Duas Velocidades", "A IA generaliza-se mas é paga pelas famílias; cresce a desigualdade entre alunos.",
         "Subida de subscrições privadas; estudos sobre fosso digital", 25],
    ], columns=["Quadrante", "Nome", "Narrativa", "Sinais de alerta", "Probabilidade (%)"])
    estr = pd.DataFrame([
        ["Tutor IA adaptativo premium", 2, -1, -2, 2],
        ["Conteúdos alinhados com as Aprendizagens Essenciais + modo offline", 1, 2, 1, 1],
        ["Formação certificada de professores", 2, 2, 0, 1],
        ["Modelo freemium para famílias", 0, 0, 1, 2],
        ["Parcerias com municípios", 1, 2, 1, -1],
    ], columns=["Estratégia", "Q1", "Q2", "Q3", "Q4"])
    cen.insert(3, "Implicações e ações", [
        "Certificar o tutor IA para concursos públicos; ferramentas de análise da aprendizagem para os professores.",
        "Conteúdos e ferramentas para o professor; formação certificada; a IA fica nas mãos do docente.",
        "Modo offline e versões impressas; vender diretamente a famílias e municípios.",
        "Modelo freemium e preços sociais; parcerias com municípios para reduzir o fosso digital.",
    ])
    posicao = pd.DataFrame([
        ["Hoje", 2026, -0.4, 0.3, "Fundos PRR ainda ativos e uso de IA pelos alunos muito limitado"],
        ["Horizonte", 2035, 0.3, -0.3, "Fim do PRR e IA generalizada fora da escola"],
    ], columns=["Momento", "Ano", "X (−1 a +1)", "Y (−1 a +1)", "Justificação"])
    casos = pd.DataFrame([
        ["Económico", "Financiamento público do digital", "Orçamento de Estado cobre manutenção", "Novo programa europeu substitui o PRR", "Corte sem substituto"],
        ["Tecnológico", "IA generativa na aprendizagem", "Uso supervisionado em projetos", "Tutores certificados nas escolas", "Proibição para menores de 16 anos"],
        ["Social", "Preocupação com ecrãs", "Limites por ciclo de ensino", "Uso equilibrado e orientado", "Regresso ao papel no 1.º ciclo"],
        ["Legal", "AI Act — risco elevado", "Conformidade com custo moderado", "Normas harmonizadas simplificam", "Certificação cara e demorada"],
    ], columns=["Dimensão", "Fator", "Business as usual", "Melhor caso", "Pior caso"])

    par = pd.DataFrame([
        ["Uso de IA pelos alunos", s] for s in ["Proibido", "Supervisionado pelo professor", "Autónomo"]] + [
        ["Equipamento", s] for s in ["Partilhado na escola", "1 aluno : 1 dispositivo", "BYOD (traz o teu)"]] + [
        ["Financiamento", s] for s in ["Estado central", "Municípios", "Famílias"]] + [
        ["Papel do professor", s] for s in ["Transmissor", "Mediador / curador", "Analista de dados de aprendizagem"]] + [
        ["Manuais", s] for s in ["Papel", "Híbrido", "Totalmente digital"]],
        columns=["Parâmetro", "Estado"])
    inc = pd.DataFrame([
        ["Uso de IA pelos alunos: Autónomo", "Papel do professor: Transmissor", "Lógica"],
        ["Manuais: Totalmente digital", "Equipamento: Partilhado na escola", "Empírica"],
        ["Uso de IA pelos alunos: Proibido", "Papel do professor: Analista de dados de aprendizagem", "Empírica"],
        ["Uso de IA pelos alunos: Autónomo", "Manuais: Papel", "Empírica"],
        ["Financiamento: Famílias", "Equipamento: Partilhado na escola", "Lógica"],
    ], columns=["Estado A", "Estado B", "Tipo"])
    mc = pd.DataFrame([
        ["Escola Tradicional", "Proibido", "Partilhado na escola", "Estado central", "Transmissor", "Papel"],
        ["Híbrido Equilibrado", "Supervisionado pelo professor", "1 aluno : 1 dispositivo", "Municípios", "Mediador / curador", "Híbrido"],
        ["Aprendizagem Aumentada", "Autónomo", "BYOD (traz o teu)", "Famílias", "Analista de dados de aprendizagem", "Totalmente digital"],
    ], columns=["Cenário", "Uso de IA pelos alunos", "Equipamento", "Financiamento", "Papel do professor", "Manuais"])

    swot = pd.DataFrame([
        ["Força", "Conteúdos alinhados com o currículo nacional", 0.14, 4],
        ["Força", "Equipa mista de pedagogos e engenheiros", 0.12, 4],
        ["Força", "Tecnologia própria de personalização", 0.12, 3],
        ["Força", "Marca reconhecida pelos professores", 0.10, 3],
        ["Fraqueza", "Dependência de um fornecedor de IA externo", 0.14, 1],
        ["Fraqueza", "Pequena escala comercial", 0.14, 2],
        ["Fraqueza", "Receita sazonal concentrada no início do ano letivo", 0.12, 2],
        ["Fraqueza", "Pouca presença fora da Grande Lisboa", 0.12, 1],
        ["Oportunidade", "Prioridade política à transição digital", 0.12, 3],
        ["Oportunidade", "IA generativa permite tutoria personalizada", 0.15, 3],
        ["Oportunidade", "Mercado lusófono (PALOP e Brasil)", 0.10, 2],
        ["Oportunidade", "Municípios com competências na educação", 0.13, 2],
        ["Ameaça", "Fim do financiamento PRR", 0.15, 2],
        ["Ameaça", "Restrições ao tempo de ecrã e à IA para crianças", 0.12, 2],
        ["Ameaça", "Plataformas globais gratuitas", 0.13, 1],
        ["Ameaça", "AI Act — requisitos de risco elevado", 0.10, 3],
    ], columns=["Tipo", "Fator", "Peso", "Classificação"])
    tows = pd.DataFrame([
        ["SO", "Tutor IA alinhado com as Aprendizagens Essenciais para programas públicos de digitalização", "S1, S3, O1, O2", 1],
        ["WO", "Reduzir a dependência com um modelo de IA aberto alojado na UE", "W1, O2", 2],
        ["ST", "Posicionamento como 'IA responsável e certificada' perante o AI Act e as famílias", "S2, T2, T4", 1],
        ["WT", "Parcerias com municípios fora de Lisboa para diversificar receita após o PRR", "W2, W4, T1", 1],
        ["SO", "Expansão para o mercado lusófono com conteúdos adaptados", "S1, O3", 3],
    ], columns=["Quadrante", "Estratégia", "Fatores ligados", "Prioridade"])

    stk = pd.DataFrame([
        ["Ministério da Educação", 5, 3, 5, 3, 0],
        ["Diretores de agrupamento", 4, 4, 4, 3, 1],
        ["Professores", 3, 5, 5, 4, -1],
        ["Pais e encarregados de educação", 3, 5, 5, 4, -1],
        ["Alunos", 1, 4, 4, 3, 1],
        ["Municípios", 4, 3, 4, 2, 1],
        ["Fornecedor de modelos de IA", 3, 3, 2, 2, 1],
        ["Editoras concorrentes", 3, 4, 2, 3, -2],
        ["CNPD (proteção de dados)", 4, 2, 5, 2, 0],
        ["Investidores", 4, 5, 4, 5, 2],
    ], columns=["Stakeholder", "Poder", "Interesse", "Legitimidade", "Urgência", "Atitude"])

    roles = ["CEO", "Product Manager", "Equipa Pedagógica", "Engenharia", "Jurídico / DPO", "Customer Success", "Escolas Piloto"]
    raci = pd.DataFrame([
        ["Planeamento", "Definição do âmbito do piloto", "A", "R", "C", "C", "I", "I", "C"],
        ["Planeamento", "Acordos de proteção de dados com as escolas", "I", "C", "", "", "AR", "", "C"],
        ["Desenvolvimento", "Conteúdos e prompts pedagógicos", "", "A", "R", "C", "", "", ""],
        ["Desenvolvimento", "Desenvolvimento e integração da plataforma", "", "A", "C", "R", "", "", ""],
        ["Desenvolvimento", "Avaliação de conformidade com o AI Act", "A", "C", "C", "C", "R", "", ""],
        ["Piloto", "Formação de professores", "", "A", "R", "", "", "R", "I"],
        ["Piloto", "Recolha de feedback e métricas", "", "A", "C", "I", "", "R", "C"],
        ["Avaliação", "Relatório de impacto na aprendizagem", "I", "A", "R", "S", "", "S", "I"],
        ["Avaliação", "Decisão de escalar para nível nacional", "A", "A", "C", "C", "C", "C", "I"],
    ], columns=["Fase", "Tarefa"] + roles)
    raci[roles] = raci[roles].replace("", "—")
    aut = pd.DataFrame([
        ["Desconto comercial até 10%", "Comercial", "Customer Success", "—", "Product Manager", "Financeiro"],
        ["Desconto > 10% ou contrato público", "Comercial", "Customer Success", "Jurídico / DPO", "CEO", "Financeiro"],
        ["Publicação de nova versão do modelo de IA", "Produto", "Engenharia", "Equipa Pedagógica", "Product Manager", "Jurídico / DPO"],
        ["Tratamento de dados de alunos para novos fins", "Dados", "Product Manager", "Jurídico / DPO", "CEO", "Escolas Piloto"],
        ["Despesa operacional até 5 000 €", "Financeiro", "Engenharia", "—", "Engenharia", "Financeiro"],
        ["Contratação de pessoal", "Pessoas", "Product Manager", "Financeiro", "CEO", "Equipa"],
    ], columns=["Decisão", "Categoria", "Propõe", "Valida", "Aprova", "Informado"])

    # ---------- Plano estratégico / Balanced Scorecard (guia de E. Shehab; Kaplan & Norton) ----------
    T_SO = "Tutor IA alinhado com as Aprendizagens Essenciais para programas públicos de digitalização"
    T_WO = "Reduzir a dependência com um modelo de IA aberto alojado na UE"
    T_ST = "Posicionamento como 'IA responsável e certificada' perante o AI Act e as famílias"
    T_WT = "Parcerias com municípios fora de Lisboa para diversificar receita após o PRR"
    identidade = pd.DataFrame([
        ["Valor", "Aprendizagem primeiro", "Cada funcionalidade tem de melhorar a aprendizagem"],
        ["Valor", "Equidade", "Nenhum aluno fica para trás por falta de meios"],
        ["Valor", "IA responsável", "Transparência, privacidade e o professor no centro"],
        ["Visão", "Em 2035, ser a plataforma de aprendizagem de referência no Ensino Básico em língua portuguesa, usada por "
                  "1 em cada 3 alunos.", "Horizonte de 9 anos, alinhado com os cenários"],
        ["Missão", "Ajudar cada aluno do 1.º e 2.º ciclos a aprender melhor, com conteúdos alinhados com o currículo e um tutor "
                   "digital responsável, ao serviço dos professores.", "O que fazemos hoje e para quem"],
    ], columns=["Elemento", "Declaração", "Descrição"])
    objetivos = pd.DataFrame([
        ["F1", "Financeira", "Diversificar a receita", "% receita fora do PRR e de compras centrais", "%", "↑", 20, 60, 42, 2028,
         "Parcerias com municípios", "CEO", T_WT, True, True, True],
        ["F2", "Financeira", "Atingir o break-even", "Margem EBITDA", "%", "↑", -15, 10, -6, 2028,
         "Modelo freemium para famílias", "CEO", "Scenario Planning (estratégia condicional)", True, True, True],
        ["C1", "Clientes", "Alargar a base de escolas", "Nº de agrupamentos clientes", "nº", "↑", 40, 250, 155, 2030,
         "Tutor IA alinhado com as Aprendizagens Essenciais", "Customer Success", T_SO, True, True, True],
        ["C2", "Clientes", "Conquistar a confiança das famílias", "% pais que confiam no uso de IA", "%", "↑", 35, 70, 41, 2028,
         "Selo 'IA responsável e certificada'", "Product Manager", T_ST, True, True, True],
        ["P1", "Processos internos", "Cumprir o AI Act", "% requisitos de risco elevado cumpridos", "%", "↑", 30, 100, 100, 2027,
         "Avaliação de conformidade (ver RAM)", "Jurídico / DPO", T_ST, True, True, True],
        ["P2", "Processos internos", "Reduzir a dependência do fornecedor de IA", "% pedidos servidos por modelo próprio", "%", "↑",
         0, 50, 0, 2029, "Modelo aberto alojado na UE", "Engenharia", T_WO, True, True, True],
        ["A1", "Aprendizagem e crescimento", "Capacitar professores", "Nº professores formados", "nº", "↑", 200, 3000, 1700, 2028,
         "Formação certificada de professores", "Equipa Pedagógica", "Scenario Planning (estratégia robusta)", True, True, True],
        ["A2", "Aprendizagem e crescimento", "Melhorar a cultura de inovação", "", "", "↑", None, None, None, None,
         "", "", "", False, False, True],
    ], columns=["Código", "Perspetiva", "Objetivo", "Indicador (KPI)", "Unidade", "Sentido", "Base", "Meta", "Atual", "Prazo", "Iniciativa", "Responsável", "Origem", "Específico", "Atingível", "Relevante"])
    ligacoes = pd.DataFrame([["A1", "C1"], ["A1", "C2"], ["A2", "P2"], ["P1", "C2"], ["P2", "F2"], ["C2", "C1"], ["C1", "F1"],
                             ["C1", "F2"]], columns=["De", "Para"])

    return {
        "pestel": {"fatores": pestel},
        "porter": {"fatores": porter},
        "micmac": {"variaveis": var, "matriz": mat},
        "cenarios": {"eixos": eixos, "cenarios": cen, "estrategias": estr, "posicao": posicao, "casos": casos},
        "morfologica": {"parametros": par, "incompatibilidades": inc, "cenarios": mc},
        "swot": {"fatores": swot, "estrategias": tows},
        "bsc": {"identidade": identidade, "objetivos": objetivos, "ligacoes": ligacoes},
        "stakeholders": {"stakeholders": stk},
        "ram": {"raci": raci, "autoridade": aut},
    }
