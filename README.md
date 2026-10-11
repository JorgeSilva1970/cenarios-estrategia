# 🧭 Estúdio de Cenários & Estratégia

Aplicação web em **Python + Streamlit** para prospetiva e planeamento estratégico: do diagnóstico do meio envolvente à
construção de cenários e à atribuição de responsabilidades. Cada modelo inclui **legenda** (o que analisa, autor, ano,
fonte), **edição de dados**, **análise e dashboard** (Plotly), **conclusões automáticas** e **relatório HTML** descarregável.

## Modelos incluídos

| Fase | Modelo | Autor(es) · Ano | Resultados |
|---|---|---|---|
| 1 · Diagnóstico | PESTEL + matriz Impacto × Incerteza | Aguilar (1967); Schwartz (1991) | Incertezas críticas, tendências pesadas |
| 1 · Diagnóstico | Cinco Forças | Porter (1979, 2008) | Intensidade por força, atratividade |
| 2 · Variáveis-chave | Análise estrutural MICMAC | Godet (1994); Duperrin & Godet (1973) | Planos direto/indireto, variáveis motoras, grafo |
| 3 · Cenários | **Scenario Planning** em 4 passos, matriz 2×2 + wind tunneling | Wack (1985); Schwartz (1991); van der Heijden (1996); SME Strategy (2020–2023) | Matriz de cenários com trajetória hoje → horizonte, implicações, sinais de alerta, casos BAU/melhor/pior, robustez, minimax-regret |
| 3 · Cenários | **Scenario Development** — análise morfológica + CCA | Zwicky (1969); Ritchey (2002/2011) | Espaço de soluções, caixa morfológica, validação de cenários, drivers |
| 4 · Estratégia | SWOT → TOWS + IFE/EFE/IE | Weihrich (1982); David & David (2017) | Matriz IE, prescrição, estratégias SO/WO/ST/WT |
| 4 · Estratégia | **Plano Estratégico**: valores, visão, missão, objetivos SMART, **Balanced Scorecard** e **Mapa Estratégico** | Kaplan & Norton (1992, 2004); Doran (1981); guia de E. Shehab | Cumprimento das metas (KPI), estado por objetivo, verificação SMART, equilíbrio das perspetivas, ligação às estratégias TOWS e aos papéis da RAM |
| 5 · Implementação | Stakeholders (Poder × Interesse + Saliência) | Mendelow (1991); Mitchell, Agle & Wood (1997) | Plano de envolvimento, opositores com poder |
| 5 · Implementação | **RAM** — RACI/RASCI + Matriz de Autoridade | PMI (2017); COSO (2013) | Validação de regras (1 A, ≥1 R, segregação de funções), carga por papel |
| Resultados | Dashboard e relatório integrado | — | Sumário executivo, relatório HTML único, Excel com todos os dados |

Os módulos estão encadeados: as incertezas críticas da PESTEL e as variáveis motoras do MICMAC aparecem como
**candidatos a eixos** no Scenario Planning.

## Vídeos orientadores e como foram incorporados

| Vídeo | Autor | Incorporado em |
|---|---|---|
| [What is Scenario Planning & How to Use it in Your Strategic Plan](https://youtu.be/jyCiINmicy4) | SME Strategy | Processo em 4 passos; avisos sobre armadilhas (planear para um só cenário, implicações em falta) |
| [What is the scenario planning process in a strategic plan? // How to do scenario development](https://youtu.be/ezUbcR9IzC0) | SME Strategy | PESTEL como forças motrizes; narrativas no presente; horizonte; tabela business as usual / melhor / pior caso; exercício de posicionamento (hoje → horizonte) |
| [Strategic Planning: A Step-by-Step Guide That Works](https://youtu.be/8HZQvykaoW8) | Edward Shehab | Novo módulo **Plano Estratégico e BSC**: valores → visão → missão → SWOT e plano de ação → objetivos SMART → Balanced Scorecard (objetivos, indicadores, metas, iniciativas) → KPI → Mapa Estratégico |

## Casos exemplo

1. **Seguradora — Gestão de Sinistros Automóvel 2030** (IA na peritagem, ADAS, regulação, inflação de reparação).
2. **EdTech — Aprendizagem Digital no Ensino Básico 2035** (tutor IA, fim do PRR, AI Act, bem-estar digital).
3. **Novo caso (modelo em branco)** para dados próprios.

Os exemplos incluem erros propositados na RAM (tarefa sem Aprovador, dois Aprovadores, segregação de funções violada)
para demonstrar a validação automática.

## Estrutura

```
cenarios-estrategia/
├── app.py                 # entrada: barra lateral, navegação
├── core/
│   ├── refs.py            # legendas: descrição, autor, ano, obra, site
│   ├── ui.py              # editores, legenda, import/export Excel, separadores comuns
│   ├── state.py           # caso ativo e dados editados
│   ├── report.py          # relatórios HTML
│   ├── result.py          # estrutura comum dos resultados
│   └── theme.py           # paleta e tema Plotly
├── models/                # lógica pura de cada modelo (testável sem interface)
├── views/                 # páginas Streamlit
├── cases/                 # casos exemplo
├── tests/                 # pytest (modelos + todas as páginas em todos os casos)
├── exemplos/              # relatórios integrados já gerados
├── requirements.txt
├── render.yaml            # deploy no Render (Blueprint)
└── .streamlit/config.toml
```

## 1. Executar localmente (VS Code)

```bash
git clone https://github.com/<o-seu-utilizador>/cenarios-estrategia.git
cd cenarios-estrategia
python -m venv .venv
# Windows: .venv\Scripts\activate    |    macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
streamlit run app.py
```

No VS Code também pode usar **Run and Debug → "Streamlit: app.py"** (já configurado em `.vscode/launch.json`).
Testes: `pytest -q`.

## 2. Publicar no GitHub

```bash
git init
git add .
git commit -m "Estúdio de Cenários & Estratégia"
git branch -M main
git remote add origin https://github.com/<o-seu-utilizador>/cenarios-estrategia.git
git push -u origin main
```

## 3. Deploy no Render

**Opção A — Blueprint (recomendado):** no Render, *New → Blueprint* → escolha o repositório. O `render.yaml` cria o serviço.

**Opção B — manual:** *New → Web Service* → repositório, e configure:

- Runtime: **Python 3**
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Variável de ambiente: `PYTHON_VERSION = 3.12.7`

No plano gratuito o serviço adormece após inatividade; o primeiro acesso pode demorar ~1 minuto.

## Como usar

1. Escolha o caso na barra lateral.
2. Em cada modelo, edite as tabelas em **📝 Dados** (ou descarregue o Excel modelo, preencha e volte a carregar).
3. Veja **📊 Análise e dashboard** e **✅ Conclusões**.
4. Descarregue o **📄 Relatório** do modelo ou, em **Dashboard e relatório**, o relatório integrado.
   Os relatórios são autónomos (a biblioteca Plotly vai embutida, ~5 MB): funcionam offline e em qualquer pré-visualizador. Para PDF: abrir o HTML no browser → Ctrl+P → Guardar como PDF.

## Acrescentar um novo modelo

1. Legenda em `core/refs.py` (`METHODS` e `ORDER`).
2. Função `analyze(data) -> Result` em `models/novo.py`.
3. Dados exemplo em cada ficheiro de `cases/`.
4. Página em `views/` usando `ui.standard_tabs(...)` e registo em `app.py` e em `views/general.run_all`.
