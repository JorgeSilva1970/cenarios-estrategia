"""Caso exemplo 1 — Seguradora: gestão de sinistros automóvel em Portugal, horizonte 2030."""
import pandas as pd

TITLE = "Seguradora — Gestão de Sinistros Automóvel 2030"
CONTEXT = ("Seguradora portuguesa do ramo automóvel que pretende redesenhar a gestão de sinistros até 2030, "
           "num contexto de inflação dos custos de reparação, adoção de IA e veículos com condução assistida.")


def build():
    pestel = pd.DataFrame([
        ["Político", "Supervisão da ASF sobre prazos e qualidade de regularização de sinistros", 4, 2, "Curto", "↑"],
        ["Político", "Políticas de incentivo ao veículo elétrico", 3, 3, "Médio", "↑"],
        ["Económico", "Inflação dos custos de reparação e peças", 5, 3, "Curto", "↑"],
        ["Económico", "Taxas de juro e rendimento das reservas técnicas", 4, 4, "Médio", "="],
        ["Social", "Expectativa de serviço digital e imediato pelo cliente", 4, 2, "Curto", "↑"],
        ["Social", "Envelhecimento da população condutora", 3, 2, "Longo", "↑"],
        ["Tecnológico", "IA na peritagem, triagem e deteção de fraude", 5, 4, "Médio", "↑"],
        ["Tecnológico", "Veículos com condução assistida/autónoma (ADAS)", 5, 5, "Longo", "↑"],
        ["Tecnológico", "Telemática e seguros baseados na utilização (UBI)", 4, 4, "Médio", "↑"],
        ["Ecológico", "Fenómenos climáticos extremos (granizo, inundações)", 4, 4, "Médio", "↑"],
        ["Ecológico", "Reparação sustentável e peças recicladas", 2, 3, "Médio", "↑"],
        ["Legal", "AI Act europeu e RGPD em decisões automatizadas", 4, 3, "Curto", "↑"],
        ["Legal", "Revisão da Diretiva do Seguro Automóvel (UE 2021/2118)", 3, 2, "Curto", "="],
        ["Legal", "Litigância e custos de danos corporais", 3, 3, "Médio", "↑"],
    ], columns=["Dimensão", "Fator", "Impacto", "Incerteza", "Horizonte", "Tendência"])

    porter = pd.DataFrame([
        ["Rivalidade entre concorrentes", "Número e equilíbrio dos concorrentes", 4],
        ["Rivalidade entre concorrentes", "Guerra de preços no ramo automóvel", 5],
        ["Rivalidade entre concorrentes", "Crescimento reduzido do mercado", 4],
        ["Ameaça de novos entrantes", "Insurtechs digitais", 3],
        ["Ameaça de novos entrantes", "Requisitos de capital (Solvência II)", 2],
        ["Ameaça de novos entrantes", "Baixa lealdade à marca", 3],
        ["Ameaça de substitutos", "Mobilidade partilhada com seguro incluído", 3],
        ["Ameaça de substitutos", "Seguro embutido pelo fabricante (OEM)", 4],
        ["Poder negocial dos fornecedores", "Oficinas e redes de reparação", 3],
        ["Poder negocial dos fornecedores", "Fabricantes de peças originais", 4],
        ["Poder negocial dos fornecedores", "Resseguradoras", 3],
        ["Poder negocial dos clientes", "Comparadores de preço online", 5],
        ["Poder negocial dos clientes", "Custos de mudança baixos", 4],
        ["Poder negocial dos clientes", "Mediadores e corretores", 3],
    ], columns=["Força", "Fator", "Intensidade"])

    codes = ["REG", "INF", "IA", "TEL", "ADAS", "CLI", "CLIM", "CUS", "COMP", "RENT"]
    var = pd.DataFrame([
        ["REG", "Regulação (ASF, AI Act)", "Enquadramento regulatório da atividade e das decisões automatizadas"],
        ["INF", "Inflação de reparação", "Evolução do custo de peças e mão-de-obra"],
        ["IA", "IA na gestão de sinistros", "Grau de automação da triagem, peritagem e antifraude"],
        ["TEL", "Telemática / UBI", "Penetração de dados de condução e produtos por utilização"],
        ["ADAS", "Veículos ADAS/autónomos", "Peso do parque com condução assistida"],
        ["CLI", "Expectativa digital do cliente", "Exigência de serviço imediato e self-service"],
        ["CLIM", "Clima extremo", "Frequência de eventos catastróficos"],
        ["CUS", "Custo médio de sinistros", "Custo médio por sinistro participado"],
        ["COMP", "Competências digitais", "Competências digitais e analíticas das equipas"],
        ["RENT", "Rentabilidade técnica", "Rácio combinado do ramo automóvel"],
    ], columns=["Código", "Variável", "Descrição"])
    M = [
        [0, 0, 2, 2, 0, 0, 0, 2, 1, 2],
        [0, 0, 1, 0, 0, 0, 0, 3, 0, 3],
        [0, 0, 0, 2, 0, 2, 0, 3, 2, 2],
        [0, 0, 2, 0, 0, 2, 0, 2, 0, 2],
        [2, 2, 2, 3, 0, 0, 0, 3, 0, 2],
        [0, 0, 3, 2, 0, 0, 0, 0, 2, 2],
        [0, 1, 0, 0, 0, 0, 0, 3, 0, 2],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 3],
        [0, 0, 3, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 1, 0, 0, 0, 0, 2, 0],
    ]
    mat = pd.DataFrame(M, index=codes, columns=codes)

    eixos = pd.DataFrame([
        ["X", "Ritmo de adoção de IA e veículos ADAS", "Lento", "Acelerado"],
        ["Y", "Enquadramento regulatório das decisões automatizadas", "Restritivo", "Facilitador"],
    ], columns=["Eixo", "Incerteza", "Polo −", "Polo +"])
    cen = pd.DataFrame([
        ["Q1", "Sinistro Autónomo", "Carros reportam o acidente sozinhos; IA decide e paga a maioria dos sinistros em minutos; "
         "fabricantes e seguradoras partilham dados.", "Quota de veículos com eCall/ADAS > 40%; guias da ASF sobre IA; parcerias OEM", 25],
        ["Q2", "Digital Gradual", "Regulação permite automação mas o parque automóvel envelhece; a digitalização faz-se pela app "
         "e pela peritagem remota.", "Idade média do parque > 14 anos; adesão à app > 60%", 35],
        ["Q3", "Status Quo Pesado", "Pouca tecnologia e regras restritivas; a concorrência faz-se pelo preço e pela rede de oficinas.",
         "Rácio combinado > 100%; estagnação de vendas de VE", 20],
        ["Q4", "IA sob Vigilância", "A tecnologia avança depressa mas cada decisão automatizada exige explicação e revisão humana; "
         "custos de compliance elevados.", "Coimas por decisões automatizadas; exigência de revisão humana obrigatória", 20],
    ], columns=["Quadrante", "Nome", "Narrativa", "Sinais de alerta", "Probabilidade (%)"])
    estr = pd.DataFrame([
        ["Triagem automática de sinistros com IA", 2, 1, 0, -1],
        ["Rede própria de oficinas convencionadas", 0, 1, 2, 1],
        ["Produto UBI telemático", 2, 1, -1, 1],
        ["Parcerias com fabricantes (seguro embutido)", 2, -1, -2, 1],
        ["Requalificação dos gestores de sinistros", 1, 2, 1, 2],
    ], columns=["Estratégia", "Q1", "Q2", "Q3", "Q4"])
    cen.insert(3, "Implicações e ações", [
        "Integrar dados de fabricantes e telemática; decisão automática para a maioria dos sinistros; requalificar gestores para casos complexos.",
        "Investir na app e na peritagem remota; manter capacidade humana para um parque automóvel antigo.",
        "Competir em custo: rede convencionada, combate à fraude e eficiência operacional.",
        "Governança de IA forte: explicabilidade, revisão humana e auditoria; o custo de compliance entra no preço.",
    ])
    posicao = pd.DataFrame([
        ["Hoje", 2026, -0.3, -0.2, "Automação ainda pontual e regras do AI Act em adaptação"],
        ["Horizonte", 2030, 0.4, -0.15, "ADAS a crescer depressa, mas com supervisão apertada das decisões automatizadas"],
    ], columns=["Momento", "Ano", "X (−1 a +1)", "Y (−1 a +1)", "Justificação"])
    casos = pd.DataFrame([
        ["Económico", "Inflação dos custos de reparação", "Subida de 3–4% ao ano", "Estabiliza com peças recicladas", "Subida acima de 8% ao ano"],
        ["Tecnológico", "IA na gestão de sinistros", "Triagem automática em 30% dos casos", "Automação em 70% dos casos", "Projetos-piloto travados"],
        ["Legal", "AI Act e RGPD", "Requisitos claros e cumpríveis", "Guias setoriais da ASF facilitam", "Revisão humana obrigatória em todos os casos"],
        ["Ecológico", "Clima extremo", "Um evento grave por ano", "Anos amenos", "Vários eventos catastróficos por ano"],
    ], columns=["Dimensão", "Fator", "Business as usual", "Melhor caso", "Pior caso"])

    par = pd.DataFrame([
        ["Canal de participação", s] for s in ["Telefone/balcão", "App/self-service", "Automático (telemática/eCall)"]] + [
        ["Peritagem", s] for s in ["Presencial", "Remota por vídeo/foto", "IA automática"]] + [
        ["Regulação de decisões automatizadas", s] for s in ["Restritiva", "Moderada", "Facilitadora"]] + [
        ["Rede de reparação", s] for s in ["Aberta (cliente escolhe)", "Convencionada", "Própria da seguradora"]] + [
        ["Modelo de produto", s] for s in ["Tradicional anual", "UBI (pay-how-you-drive)", "Embutido no veículo (OEM)"]],
        columns=["Parâmetro", "Estado"])
    inc = pd.DataFrame([
        ["Peritagem: IA automática", "Regulação de decisões automatizadas: Restritiva", "Empírica"],
        ["Canal de participação: Automático (telemática/eCall)", "Modelo de produto: Tradicional anual", "Empírica"],
        ["Canal de participação: Telefone/balcão", "Peritagem: IA automática", "Lógica"],
        ["Modelo de produto: Embutido no veículo (OEM)", "Rede de reparação: Aberta (cliente escolhe)", "Empírica"],
        ["Canal de participação: Telefone/balcão", "Modelo de produto: Embutido no veículo (OEM)", "Lógica"],
    ], columns=["Estado A", "Estado B", "Tipo"])
    mc = pd.DataFrame([
        ["Continuidade", "Telefone/balcão", "Presencial", "Restritiva", "Aberta (cliente escolhe)", "Tradicional anual"],
        ["Salto Digital", "App/self-service", "Remota por vídeo/foto", "Moderada", "Convencionada", "UBI (pay-how-you-drive)"],
        ["Ecossistema Automático", "Automático (telemática/eCall)", "IA automática", "Facilitadora", "Própria da seguradora",
         "Embutido no veículo (OEM)"],
    ], columns=["Cenário", "Canal de participação", "Peritagem", "Regulação de decisões automatizadas", "Rede de reparação",
                "Modelo de produto"])

    swot = pd.DataFrame([
        ["Força", "Base de clientes alargada e marca reconhecida", 0.15, 4],
        ["Força", "Equipa experiente em gestão de sinistros", 0.12, 4],
        ["Força", "Solidez financeira (Solvência II)", 0.12, 3],
        ["Força", "Rede de mediadores de proximidade", 0.10, 3],
        ["Fraqueza", "Sistemas legados fragmentados", 0.16, 1],
        ["Fraqueza", "Tempo médio de regularização elevado", 0.15, 2],
        ["Fraqueza", "Baixa maturidade analítica", 0.10, 2],
        ["Fraqueza", "Custos operacionais acima da média", 0.10, 1],
        ["Oportunidade", "IA para triagem e deteção de fraude", 0.15, 3],
        ["Oportunidade", "Procura de produtos UBI", 0.10, 2],
        ["Oportunidade", "Parcerias com fabricantes (OEM)", 0.10, 2],
        ["Oportunidade", "Digitalização dos clientes", 0.15, 3],
        ["Ameaça", "Inflação dos custos de reparação", 0.15, 2],
        ["Ameaça", "Insurtechs e comparadores de preço", 0.15, 2],
        ["Ameaça", "Eventos climáticos extremos", 0.10, 2],
        ["Ameaça", "Exigência regulatória (AI Act/RGPD)", 0.10, 3],
    ], columns=["Tipo", "Fator", "Peso", "Classificação"])
    tows = pd.DataFrame([
        ["SO", "Participação 100% digital com triagem por IA, apoiada na base de clientes e na marca", "S1, O1, O4", 1],
        ["WO", "Substituir sistemas legados por uma plataforma cloud de sinistros", "W1, W2, O1", 1],
        ["ST", "Usar a solidez financeira para negociar uma rede convencionada com preços fixos", "S3, T1", 2],
        ["WT", "Programa de eficiência e antifraude para reduzir custos e exposição ao preço", "W4, T2", 2],
        ["SO", "Lançar produto UBI através da rede de mediadores", "S4, O2", 3],
    ], columns=["Quadrante", "Estratégia", "Fatores ligados", "Prioridade"])

    stk = pd.DataFrame([
        ["Comissão Executiva", 5, 5, 5, 4, 1],
        ["ASF (regulador)", 5, 3, 5, 3, 0],
        ["Clientes tomadores", 3, 5, 4, 4, 0],
        ["Mediadores de seguros", 3, 4, 4, 3, -1],
        ["Oficinas convencionadas", 2, 4, 3, 3, 1],
        ["Gestores de sinistros", 2, 5, 4, 4, -1],
        ["Comissão de trabalhadores", 3, 3, 3, 2, -1],
        ["Fornecedor de IA", 2, 4, 2, 3, 2],
        ["Fabricantes automóveis (OEM)", 4, 2, 3, 1, 1],
        ["Associação de defesa do consumidor", 3, 3, 4, 2, 0],
    ], columns=["Stakeholder", "Poder", "Interesse", "Legitimidade", "Urgência", "Atitude"])

    roles = ["Diretor de Sinistros", "Gestor de Projeto", "Data Science", "TI / Arquitetura", "Compliance / DPO",
             "Gestores de Sinistros", "Fornecedor IA"]
    raci = pd.DataFrame([
        ["Iniciação", "Business case e aprovação do orçamento", "A", "R", "C", "C", "C", "I", ""],
        ["Iniciação", "Avaliação de impacto (DPIA / AI Act)", "I", "C", "C", "C", "AR", "", "S"],
        ["Desenho", "Requisitos e regras de triagem", "A", "C", "R", "C", "C", "C", "C"],
        ["Desenho", "Arquitetura e integração com o sistema core", "I", "C", "C", "AR", "I", "", "R"],
        ["Construção", "Treino e validação do modelo", "", "I", "A", "S", "I", "C", "R"],
        ["Construção", "Testes de aceitação (UAT)", "I", "A", "S", "S", "", "R", ""],
        ["Implementação", "Formação dos gestores de sinistros", "I", "AR", "S", "", "", "I", "S"],
        ["Implementação", "Comunicação a mediadores e clientes", "C", "R", "", "", "C", "I", ""],
        ["Implementação", "Go-live e monitorização", "A", "R", "R", "R", "I", "I", "S"],
        ["Operação", "Monitorização de enviesamento e drift", "I", "", "R", "S", "A", "", "S"],
    ], columns=["Fase", "Tarefa"] + roles)
    raci[roles] = raci[roles].replace("", "—")
    aut = pd.DataFrame([
        ["Pagamento de indemnização até 2 500 € (triagem IA)", "Sinistros", "Sistema IA", "Gestor de Sinistros", "Gestor de Sinistros", "Coordenador"],
        ["Pagamento entre 2 500 € e 25 000 €", "Sinistros", "Gestor de Sinistros", "Coordenador", "Diretor de Sinistros", "—"],
        ["Pagamento acima de 25 000 €", "Sinistros", "Coordenador", "Diretor de Sinistros", "Comissão Executiva", "Atuariado / Resseguro"],
        ["Recusa de sinistro por suspeita de fraude", "Sinistros", "Unidade Antifraude", "Jurídico", "Diretor de Sinistros", "Compliance"],
        ["Alteração das regras do modelo de IA", "Tecnologia", "Data Science", "Compliance / DPO", "Diretor de Sinistros", "Auditoria Interna"],
        ["Contratação de fornecedor > 100 000 €", "Compras", "Gestor de Projeto", "Compras", "Gestor de Projeto", "Comissão Executiva"],
    ], columns=["Decisão", "Categoria", "Propõe", "Valida", "Aprova", "Informado"])

    # ---------- Plano estratégico / Balanced Scorecard (guia de E. Shehab; Kaplan & Norton) ----------
    T_SO = "Participação 100% digital com triagem por IA, apoiada na base de clientes e na marca"
    T_WO = "Substituir sistemas legados por uma plataforma cloud de sinistros"
    T_ST = "Usar a solidez financeira para negociar uma rede convencionada com preços fixos"
    T_WT = "Programa de eficiência e antifraude para reduzir custos e exposição ao preço"
    identidade = pd.DataFrame([
        ["Valor", "Integridade", "Decidimos cada sinistro com transparência e justiça"],
        ["Valor", "Proximidade", "Estamos presentes quando o cliente mais precisa"],
        ["Valor", "Inovação responsável", "Usamos tecnologia com supervisão humana"],
        ["Visão", "Em 2030, ser a seguradora automóvel de referência em Portugal na resolução rápida e justa de sinistros, "
                  "com 80% dos casos simples resolvidos em 48 horas.", "Horizonte de 4 anos, alinhado com os cenários"],
        ["Missão", "Proteger a mobilidade dos nossos clientes, regularizando sinistros de forma rápida, justa e transparente, "
                   "com uma rede de parceiros de confiança.", "O que fazemos hoje e para quem"],
    ], columns=["Elemento", "Declaração", "Descrição"])
    objetivos = pd.DataFrame([
        ["F1", "Financeira", "Melhorar a rentabilidade técnica do ramo automóvel", "Rácio combinado", "%", "↓", 104, 97, 101, 2028,
         "Programa de eficiência e antifraude", "Diretor de Sinistros", T_WT, True, True, True],
        ["F2", "Financeira", "Reduzir o custo médio por sinistro", "Custo médio por sinistro", "€", "↓", 2400, 2150, 2330, 2027,
         "Rede convencionada com preços fixos", "Diretor de Sinistros", T_ST, True, True, True],
        ["C1", "Clientes", "Resolver depressa os sinistros simples", "% sinistros simples resolvidos em 48 h", "%", "↑", 25, 80, 58, 2028,
         "Triagem por IA e participação digital", "Gestor de Projeto", T_SO, True, True, True],
        ["C2", "Clientes", "Aumentar a satisfação no momento do sinistro", "NPS pós-sinistro", "pontos", "↑", 12, 35, 24, 2028,
         "Comunicação proativa ao cliente", "Gestores de Sinistros", T_SO, True, True, True],
        ["P1", "Processos internos", "Automatizar a triagem de sinistros", "% sinistros triados por IA", "%", "↑", 0, 60, 33, 2027,
         "Implementação da triagem com IA (ver RAM)", "Data Science", T_SO, True, True, True],
        ["P2", "Processos internos", "Detetar mais fraude", "Taxa de fraude detetada", "%", "↑", 3, 6, 6.2, 2027,
         "Modelo antifraude", "Data Science", T_WT, True, True, True],
        ["P3", "Processos internos", "Modernizar os sistemas de sinistros", "", "", "↑", None, None, None, None,
         "Plataforma cloud de sinistros", "TI / Arquitetura", T_WO, False, True, True],
        ["A1", "Aprendizagem e crescimento", "Requalificar os gestores de sinistros", "% gestores certificados em análise de dados", "%",
         "↑", 5, 70, 45, 2027, "Academia de sinistros", "Gestor de Projeto", "Scenario Planning (estratégia robusta)", True, True, True],
        ["A2", "Aprendizagem e crescimento", "Garantir a governação da IA", "% modelos com auditoria trimestral", "%", "↑", 0, 100, 50,
         2027, "Comité de ética e IA", "Compliance / DPO", "", True, True, True],
    ], columns=["Código", "Perspetiva", "Objetivo", "Indicador (KPI)", "Unidade", "Sentido", "Base", "Meta", "Atual", "Prazo", "Iniciativa", "Responsável", "Origem", "Específico", "Atingível", "Relevante"])
    ligacoes = pd.DataFrame([["A1", "P1"], ["A1", "C2"], ["A2", "P1"], ["P3", "P1"], ["P1", "C1"], ["P1", "F2"], ["P2", "F2"],
                             ["C1", "C2"], ["C2", "F1"], ["F2", "F1"]], columns=["De", "Para"])

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
