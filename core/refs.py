"""Legendas metodológicas: descrição, objetivo, autor, ano, obra e site de cada modelo."""

METHODS = {
    "pestel": {
        "nome": "Análise PESTEL",
        "icone": "🌍",
        "fase": "1 · Diagnóstico externo",
        "objetivo": "Identificar e classificar os fatores do macroambiente (Político, Económico, "
                    "Social, Tecnológico, Ecológico e Legal) que podem afetar a organização no horizonte em estudo.",
        "descricao": "Cada fator é avaliado em **Impacto** (1–5) e **Incerteza** (1–5). Cruzando as duas "
                     "dimensões (matriz Impacto × Incerteza de Schwartz) obtêm-se as **tendências pesadas** "
                     "(alto impacto, baixa incerteza — entram em todos os cenários) e as **incertezas críticas** "
                     "(alto impacto, alta incerteza — candidatas a eixos dos cenários).",
        "autor": "Francis J. Aguilar (origem ETPS); matriz Impacto × Incerteza: Peter Schwartz",
        "ano": "1967 / 1991",
        "obra": "Aguilar, F. J. (1967). *Scanning the Business Environment*. Macmillan. · "
                "Schwartz, P. (1991). *The Art of the Long View*. Doubleday.",
        "site": "https://en.wikipedia.org/wiki/PEST_analysis",
        "leitura": "Quanto mais acima e à direita, mais o fator deve ser vigiado. Os fatores do quadrante "
                   "superior direito alimentam diretamente o módulo de Cenários.",
    },
    "porter": {
        "nome": "Cinco Forças de Porter",
        "icone": "⚔️",
        "fase": "1 · Diagnóstico setorial",
        "objetivo": "Avaliar a intensidade competitiva e a atratividade estrutural do setor.",
        "descricao": "Cada força (rivalidade, novos entrantes, substitutos, poder dos fornecedores, poder dos "
                     "clientes) é decomposta em fatores pontuados de 1 (ameaça baixa) a 5 (ameaça alta). "
                     "A média por força indica a pressão sobre a rentabilidade; a atratividade do setor é o inverso.",
        "autor": "Michael E. Porter",
        "ano": "1979 / 2008",
        "obra": "Porter, M. E. (1979). How Competitive Forces Shape Strategy. *Harvard Business Review*, 57(2), 137–145. · "
                "Porter, M. E. (2008). The Five Competitive Forces That Shape Strategy. *HBR*, 86(1), 78–93.",
        "site": "https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy",
        "leitura": "Forças com média ≥ 3,5 são pressões altas que a estratégia deve neutralizar; "
                   "forças ≤ 2 são fontes potenciais de rentabilidade.",
    },
    "micmac": {
        "nome": "Análise Estrutural MICMAC",
        "icone": "🕸️",
        "fase": "2 · Variáveis-chave",
        "objetivo": "Identificar as variáveis-chave de um sistema através das relações de influência "
                    "diretas e indiretas entre elas.",
        "descricao": "Preenche-se uma matriz de influências diretas (0 = nenhuma, 1 = fraca, 2 = média, 3 = forte; "
                     "linha influencia coluna). A **motricidade** é a soma da linha; a **dependência** a soma da coluna. "
                     "O método MICMAC (*Matrice d'Impacts Croisés — Multiplication Appliquée à un Classement*) eleva a "
                     "matriz a potências sucessivas para revelar influências indiretas, até a hierarquia estabilizar.",
        "autor": "Michel Godet (com J.-C. Duperrin)",
        "ano": "1973 / 1994",
        "obra": "Godet, M. (1994). *From Anticipation to Action: A Handbook of Strategic Prospective*. UNESCO Publishing. · "
                "Godet, M. & Durance, P. (2011). *Strategic Foresight for Corporate and Regional Development*. Dunod/UNESCO.",
        "site": "http://en.laprospective.fr",
        "leitura": "**Motoras** (alta motricidade, baixa dependência) condicionam o sistema — são as alavancas. "
                   "**Ligação/relé** (altas em ambas) são instáveis e amplificam efeitos. **Dependentes** são resultados "
                   "a monitorizar. **Autónomas** têm pouca relação com o sistema.",
    },
    "cenarios": {
        "nome": "Scenario Planning (Matriz 2×2 + Wind Tunneling)",
        "icone": "🧭",
        "fase": "3 · Cenários",
        "objetivo": "Construir quatro futuros plausíveis e contrastados a partir de duas incertezas críticas "
                    "e testar a robustez das estratégias em cada um deles.",
        "descricao": "Segue o processo em 4 passos: (1) forças motrizes via PESTEL; (2) duas incertezas críticas "
                     "independentes como eixos; (3) quatro cenários com nome, narrativa no presente, implicações e "
                     "**sinais de alerta**; (4) implicações e **trajetória** (onde estamos hoje e para onde vamos). As opções estratégicas são depois "
                     "pontuadas de −2 a +2 em cada cenário (*wind tunneling*) para distinguir estratégias **robustas** "
                     "(funcionam em todos) de **apostas** (só funcionam num futuro).",
        "autor": "Pierre Wack (Royal Dutch/Shell); Peter Schwartz; Kees van der Heijden; processo em 4 passos: SME Strategy",
        "ano": "1985 / 1991 / 1996 / 2020–2023",
        "obra": "Wack, P. (1985). Scenarios: Uncharted Waters Ahead. *HBR*, 63(5), 73–89. · "
                "Schwartz, P. (1991). *The Art of the Long View*. Doubleday. · "
                "van der Heijden, K. (1996). *Scenarios: The Art of Strategic Conversation*. Wiley. · "
                "Taylor, A. (2020). *How to do Scenario Development & Plan for Anything*. SME Strategy. · "
                "Heckl, J. (2021, atual. 2023). *The 4-Step Scenario Planning Process (with Examples)*. SME Strategy.",
        "site": "https://hbr.org/1985/09/scenarios-uncharted-waters-ahead · "
                "https://www.smestrategy.net/blog/the-4-step-scenario-planning-process-with-examples",
        "leitura": "Os cenários não são previsões: servem para preparar a organização. Uma estratégia robusta "
                   "(mínimo ≥ 0 e média ≥ 1) é *no-regret*; as restantes exigem sinais de alerta e planos de contingência.",
    },
    "morfologica": {
        "nome": "Scenario Development — Análise Morfológica (Zwicky Box + CCA)",
        "icone": "🧩",
        "fase": "3 · Desenvolvimento de cenários",
        "objetivo": "Gerar sistematicamente todas as combinações possíveis de hipóteses futuras e reduzi-las às "
                    "configurações internamente consistentes, a partir das quais se desenvolvem os cenários.",
        "descricao": "Cada **parâmetro** (dimensão do futuro) recebe 2–5 **estados** alternativos. O produto dos "
                     "estados é o espaço total de configurações. A **Avaliação de Consistência Cruzada (CCA)** marca "
                     "os pares de estados incompatíveis; todas as configurações que contenham um par incompatível são "
                     "eliminadas, restando o **espaço de soluções**. Fixando estados (*drivers*) explora-se o que continua possível.",
        "autor": "Fritz Zwicky; Tom Ritchey (Swedish Morphological Society); Michel Godet (MORPHOL)",
        "ano": "1969 / 2002 (rev. 2013)",
        "obra": "Zwicky, F. (1969). *Discovery, Invention, Research through the Morphological Approach*. Macmillan. · "
                "Ritchey, T. (2011). *Wicked Problems – Social Messes: Decision Support Modelling with Morphological Analysis*. Springer.",
        "site": "https://www.swemorph.com/ma.html",
        "leitura": "Uma forte redução do espaço indica um problema bem estruturado. Estados com frequência baixa "
                   "no espaço de soluções são restritivos; um cenário nomeado só é válido se for consistente.",
    },
    "swot": {
        "nome": "SWOT → TOWS (com matrizes IFE/EFE e IE)",
        "icone": "🎯",
        "fase": "4 · Opções estratégicas e plano de ação",
        "objetivo": "Cruzar o diagnóstico interno (forças/fraquezas) com o externo (oportunidades/ameaças) e "
                    "transformá-lo em opções estratégicas concretas.",
        "descricao": "Os fatores são ponderados (pesos somam 1 no interno e 1 no externo) e classificados de 1 a 4, "
                     "obtendo-se os totais **IFE** e **EFE** e a posição na **matriz Interna-Externa (IE)**. "
                     "A **matriz TOWS** gera estratégias SO (maxi-maxi), WO (mini-maxi), ST (maxi-mini) e WT (mini-mini).",
        "autor": "Heinz Weihrich (TOWS); Fred R. David (IFE/EFE/IE)",
        "ano": "1982 / 2017",
        "obra": "Weihrich, H. (1982). The TOWS Matrix — A Tool for Situational Analysis. *Long Range Planning*, 15(2), 54–66. · "
                "David, F. R. & David, F. R. (2017). *Strategic Management: Concepts and Cases* (16.ª ed.). Pearson.",
        "site": "https://doi.org/10.1016/0024-6301(82)90120-0",
        "leitura": "Totais ≥ 3,0 são fortes, 2,0–2,99 médios e < 2,0 fracos. Células I, II e IV da matriz IE → "
                   "crescer e construir; III, V e VII → manter; VI, VIII e IX → colher ou desinvestir.",
    },
    "stakeholders": {
        "nome": "Mapa de Stakeholders (Mendelow + Saliência)",
        "icone": "👥",
        "fase": "5 · Implementação",
        "objetivo": "Priorizar as partes interessadas e definir a estratégia de envolvimento de cada uma.",
        "descricao": "A **matriz Poder × Interesse** de Mendelow define quatro estratégias (gerir de perto, manter "
                     "satisfeito, manter informado, monitorizar). A **teoria da saliência** acrescenta Legitimidade e "
                     "Urgência e classifica cada stakeholder em sete tipos (definitivo, dominante, perigoso, …). "
                     "A **atitude** (−2 a +2) distingue apoiantes de opositores.",
        "autor": "Aubrey L. Mendelow; Ronald K. Mitchell, Bradley R. Agle & Donna J. Wood",
        "ano": "1991 / 1997",
        "obra": "Mendelow, A. (1991). Stakeholder Mapping. *Proc. 2nd Int. Conference on Information Systems*, Cambridge, MA. · "
                "Mitchell, R. K., Agle, B. R. & Wood, D. J. (1997). Toward a Theory of Stakeholder Identification and "
                "Salience. *Academy of Management Review*, 22(4), 853–886.",
        "site": "https://www.open.edu/openlearn/science-maths-technology/computing-ict/successful-it-systems/content-section-4.4",
        "leitura": "Stakeholders com muito poder e atitude negativa são o principal risco de implementação.",
    },
    "ram": {
        "nome": "RAM — Matriz de Responsabilidades (RACI) e de Autoridade",
        "icone": "🗂️",
        "fase": "5 · Implementação",
        "objetivo": "Definir quem faz o quê (responsabilidade) e quem decide o quê, até que limite (autoridade).",
        "descricao": "**RACI/RASCI**: para cada tarefa, R = Responsável (executa), A = Aprovador (presta contas, só um), "
                     "S = Suporte, C = Consultado, I = Informado; *AR* = aprova e executa. "
                     "**Matriz de Autoridade (Delegação de Competências)**: para cada decisão e limite, quem propõe, "
                     "valida e aprova — verificando a **segregação de funções**.",
        "autor": "Project Management Institute (RAM/RACI); COSO (controlo interno e segregação de funções)",
        "ano": "2017 / 2013",
        "obra": "PMI (2017). *A Guide to the Project Management Body of Knowledge (PMBOK® Guide)*, 6.ª ed., "
                "secção 9.1 (Responsibility Assignment Matrix). · COSO (2013). *Internal Control — Integrated Framework*.",
        "site": "https://www.pmi.org/pmbok-guide-standards · https://www.coso.org",
        "leitura": "Cada tarefa deve ter exatamente um A e pelo menos um R. Cada decisão deve ter um único aprovador, "
                   "diferente de quem propõe.",
    },
    "bsc": {
        "nome": "Plano Estratégico — Valores, Visão, Missão, Objetivos SMART, Balanced Scorecard e Mapa Estratégico",
        "icone": "🏁",
        "fase": "4 · Plano estratégico",
        "objetivo": "Transformar o diagnóstico e as opções estratégicas num plano mensurável: quem somos (valores), "
                    "onde queremos chegar (visão), o que fazemos (missão), que objetivos perseguimos, como os medimos e "
                    "que ações garantem as metas.",
        "descricao": "Segue o guia passo a passo de E. Shehab: (1) **valores**; (2) **visão** a 2, 5 ou mais anos, realista; "
                     "(3) **missão**; (4) **SWOT** e plano de ação (módulo SWOT/TOWS); (5) **objetivos SMART** organizados no "
                     "**Balanced Scorecard** — perspetivas financeira, clientes, processos internos e aprendizagem e crescimento — "
                     "cada um com **indicador (KPI), meta, iniciativa e responsável**. O **Mapa Estratégico** liga os objetivos "
                     "por relações causa-efeito, da aprendizagem até ao resultado financeiro.",
        "autor": "Robert S. Kaplan & David P. Norton (BSC e Mapa Estratégico); George T. Doran (SMART); guia em vídeo: Edward Shehab",
        "ano": "1992 / 2004 / 1981",
        "obra": "Kaplan, R. S. & Norton, D. P. (1992). The Balanced Scorecard — Measures That Drive Performance. *HBR*, 70(1), 71–79. · "
                "Kaplan, R. S. & Norton, D. P. (2004). *Strategy Maps: Converting Intangible Assets into Tangible Outcomes*. "
                "Harvard Business School Press. · Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals "
                "and objectives. *Management Review*, 70(11), 35–36. · Shehab, E. *Strategic Planning: A Step-by-Step Guide "
                "That Works* (vídeo, YouTube).",
        "site": "https://hbr.org/1992/01/the-balanced-scorecard-measures-that-drive-performance-2 · "
                "https://en.wikipedia.org/wiki/SMART_criteria · https://youtu.be/8HZQvykaoW8",
        "leitura": "Cumprimento = (atual − base) / (meta − base): ≥ 100% atingido, ≥ 50% em linha, < 50% em risco. "
                   "Atingir as metas dos KPI prova que o plano estratégico foi cumprido. No mapa, as setas vão de baixo para cima.",
    },
}

ORDER = ["pestel", "porter", "micmac", "cenarios", "morfologica", "swot", "bsc", "stakeholders", "ram"]
