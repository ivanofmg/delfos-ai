<div align="center">

# δ Delfos AI

### Rehearse the decision before you make it.
### Ensaya la decisión antes de tomarla.

**Strategic Simulation Engine** · *Motor de Simulación Estratégica*

[![Status](https://img.shields.io/badge/status-pipeline%20funcional-B8923A)]()
[![Stack](https://img.shields.io/badge/stack-multi--agent%20%2B%20GraphRAG-0a0e17)]()
[![By](https://img.shields.io/badge/by-Intelinetworks-B8923A)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0-lightgrey)]()

*Built by [Intelinetworks](https://intelinetworks.com) · Powered by a multi-agent simulation engine*

</div>

---

> **EN** — Most strategic decisions are made once, with no rehearsal. Delfos builds a digital model of your business ecosystem, populates it with simulated actors, and runs the decision forward — so you see the risks, the second-order effects, and the assumptions you never questioned, *before* you commit real capital.
>
> **ES** — La mayoría de las decisiones estratégicas se toman una sola vez, sin ensayo. Delfos construye un modelo digital del ecosistema de tu negocio, lo puebla con actores simulados, y corre la decisión hacia adelante — para que veas los riesgos, los efectos de segundo orden y los supuestos que nunca cuestionaste, *antes* de comprometer capital real.

---

## 🇪🇸 Español

### El problema

Las decisiones estratégicas de alto impacto se toman con información fragmentada, sin ensayo previo y sin validación de escenarios. Se decide y se espera lo mejor. Las herramientas existentes no ayudan:

| Herramienta | Por qué no basta |
|---|---|
| **Excel / modelos financieros** | Lineales. No capturan cómo reaccionan los actores del mercado. |
| **BI / Dashboards** | Describen el pasado, no simulan el futuro. |
| **LLMs directos (ChatGPT, Claude)** | Responden preguntas sueltas; no simulan un sistema con múltiples actores interactuando. |
| **Consultoría tradicional** | Cara, lenta y entrega un PDF estático que envejece al recibirlo. |

### Qué es Delfos

Delfos AI **no es un chatbot que opina. No es un dashboard que describe el pasado.** Es un **stress-tester de decisiones**: le das el contexto de tu negocio, defines una pregunta estratégica, y el sistema simula cómo reaccionaría tu ecosistema — revelando dinámicas que no habías considerado, riesgos que no habías visto y supuestos que no habías cuestionado.

> Delfos no predice *el* futuro. Te muestra **los futuros posibles** y qué decisión optimiza tus resultados bajo incertidumbre.

### Cómo se ve el resultado

Cada simulación produce un **Prediction Report** descargable en PDF, con 7 secciones y branding profesional:

1. **Executive Summary** — Veredicto claro (PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED) + confidence score.
2. **Critical Variables** — Las 3-5 variables que más mueven el resultado, con su sensibilidad.
3. **Key Risks** — Riesgos priorizados con probabilidad, impacto y mitigación.
4. **Structural Weaknesses** — Debilidades permanentes del modelo de negocio (no eventos, condiciones).
5. **Scenario Outcomes** — Escenarios simulados (best / base / worst) con proyecciones y narrativa.
6. **Decision Impact** — Qué esperar a 6, 12 y 24 meses; qué condiciones cambiarían la recomendación.
7. **Recommended Actions** — Acciones priorizadas, inmediatas (30 días) vs. estratégicas (90+ días).

> 📄 **Ejemplo real:** ver [`delfos_ecohomes_complete.pdf`](./delfos_ecohomes_complete.pdf) — simulación del modelo de financiamiento PACE para expansión en el sur de Florida, con análisis de Devil's Advocate incluido.

### El diferenciador: Devil's Advocate

La parte que ninguna herramienta genérica ofrece. Tras cada simulación, un agente escéptico **cuestiona automáticamente los 5 supuestos más frágiles** del análisis, buscando evidencia que los valide o los invalide. Es lo que convierte un "output de IA" en algo por lo que un consultor cobraría: no te dice solo qué puede salir bien, te dice **dónde te estás engañando.**

### Cómo funciona

Pipeline híbrido de 6 pasos — modelo local para volumen, API externa para calidad crítica:

| # | Paso | Motor |
|---|---|---|
| 1 | **Ingesta** — extracción de entidades y relaciones del documento | LLM local |
| 2 | **GraphRAG** — construcción del grafo de conocimiento | LLM local |
| 3 | **Agentes** — generación de perfiles simulados con personalidad y memoria | LLM local |
| 4 | **Simulación** — ejecución multi-agente con comportamiento emergente | LLM local |
| 5 | **Devil's Advocate** — cuestionamiento escéptico de supuestos | API |
| 6 | **Síntesis** — generación del Prediction Report de 7 secciones | API |

A diferencia de un prompt suelto, los agentes **razonan sobre la estructura del grafo** (entidades, relaciones, causalidad), tienen **memoria persistente entre rondas** y exhiben **comportamiento emergente** — no son prompts estáticos, evolucionan.

### Qué hace bien — y qué no

La honestidad es parte del producto. Delfos es fuerte para unas cosas y débil para otras:

| ✅ Fortaleza | ⚠️ Límite |
|---|---|
| Pensamiento estratégico cualitativo: escenarios, riesgos, dinámicas de actores | No es un modelo de pronóstico numérico exacto (precios, cuotas de mercado precisas) |
| Ampliar el rango de futuros considerados | Los resultados varían entre corridas — se recomienda correr varias veces |
| Cuestionar supuestos y revelar puntos ciegos | La precisión predictiva no está benchmarkeada formalmente: es un complemento al juicio, no un reemplazo |

> Para pronóstico cuantitativo duro, se combina con modelos estadísticos dedicados. Delfos amplía el análisis; no pretende ser una bola de cristal.

### Modelo de negocio

**Fase actual — Consultoría aumentada.** No se vende el software; se vende el análisis que produce.

| Concepto | Valor |
|---|---|
| Precio por simulación (consultoría) | $2,000 – $5,000 |
| Costo por simulación (infra + API) | $0.50 – $2.00 |
| Costo operativo mensual fijo | ~$40 |
| Break-even | 1 simulación vendida |

---

## 🇬🇧 English

### The problem

High-stakes strategic decisions get made with fragmented information, no rehearsal, and no scenario validation. You decide and hope for the best. Existing tools don't help:

| Tool | Why it falls short |
|---|---|
| **Excel / financial models** | Linear. They don't capture how market actors react. |
| **BI / Dashboards** | Describe the past; they don't simulate the future. |
| **Direct LLMs (ChatGPT, Claude)** | Answer isolated questions; don't simulate a system of interacting actors. |
| **Traditional consulting** | Expensive, slow, and delivers a static PDF that ages on arrival. |

### What Delfos is

Delfos AI **is not a chatbot that gives opinions. It's not a dashboard that describes the past.** It's a **decision stress-tester**: you feed it your business context, define a strategic question, and the system simulates how your ecosystem would react — surfacing dynamics you hadn't considered, risks you hadn't seen, and assumptions you hadn't questioned.

> Delfos doesn't predict *the* future. It shows you **the possible futures** and which decision optimizes your outcomes under uncertainty.

### What the output looks like

Every simulation produces a downloadable, professionally branded **Prediction Report** with 7 sections:

1. **Executive Summary** — Clear verdict (PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED) + confidence score.
2. **Critical Variables** — The 3-5 variables that most drive the outcome, with sensitivity.
3. **Key Risks** — Prioritized risks with probability, impact, and mitigation.
4. **Structural Weaknesses** — Permanent weaknesses of the business model (conditions, not events).
5. **Scenario Outcomes** — Simulated scenarios (best / base / worst) with projections and narrative.
6. **Decision Impact** — What to expect at 6, 12, 24 months; what would change the recommendation.
7. **Recommended Actions** — Prioritized actions, immediate (30 days) vs. strategic (90+ days).

> 📄 **Live example:** see [`delfos_ecohomes_complete.pdf`](./delfos_ecohomes_complete.pdf) — a simulation of the PACE financing model for South Florida expansion, with Devil's Advocate analysis included.

### The differentiator: Devil's Advocate

The part no generic tool offers. After each simulation, a skeptical agent **automatically challenges the 5 most fragile assumptions** of the analysis, hunting for evidence that validates or invalidates them. It's what turns an "AI output" into something a consultant would charge for: it doesn't just tell you what could go right — it tells you **where you're fooling yourself.**

### How it works

Hybrid 6-step pipeline — local model for volume, external API for critical quality:

| # | Step | Engine |
|---|---|---|
| 1 | **Ingestion** — entity and relationship extraction | Local LLM |
| 2 | **GraphRAG** — knowledge graph construction | Local LLM |
| 3 | **Agents** — simulated profiles with personality and memory | Local LLM |
| 4 | **Simulation** — multi-agent execution with emergent behavior | Local LLM |
| 5 | **Devil's Advocate** — skeptical assumption challenging | API |
| 6 | **Synthesis** — 7-section Prediction Report generation | API |

Unlike a one-shot prompt, the agents **reason over graph structure** (entities, relationships, causality), carry **persistent memory across rounds**, and exhibit **emergent behavior** — they're not static prompts; they evolve.

### What it does well — and what it doesn't

Honesty is part of the product. Delfos is strong at some things and weak at others:

| ✅ Strength | ⚠️ Limit |
|---|---|
| Qualitative strategic thinking: scenarios, risks, actor dynamics | Not an exact numerical forecasting model (prices, precise market shares) |
| Widening the range of futures considered | Results vary between runs — running several times is recommended |
| Challenging assumptions and revealing blind spots | Predictive accuracy is not formally benchmarked: it's a complement to judgment, not a replacement |

> For hard quantitative forecasting, it pairs with dedicated statistical models. Delfos widens the analysis; it doesn't claim to be a crystal ball.

### Business model

**Current phase — Augmented consulting.** We don't sell the software; we sell the analysis it produces.

| Item | Value |
|---|---|
| Price per simulation (consulting) | $2,000 – $5,000 |
| Cost per simulation (infra + API) | $0.50 – $2.00 |
| Fixed monthly operating cost | ~$40 |
| Break-even | 1 simulation sold |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Frontend | React 18 + Vite, Tailwind CSS, i18n (EN/ES) |
| Simulation engine | OASIS (CAMEL-AI) multi-agent framework |
| Knowledge graph | GraphRAG + Zep (persistent memory) |
| Local LLM | Ollama (Qwen3.5-35B-A3B) |
| API LLM | DeepSeek V3.2 |
| PDF export | reportlab / fpdf2 |
| Infra | Docker, Caddy, Contabo VPS (64GB RAM) |

**Cost per simulation:** $0.50 – $2.00 · **Monthly infra:** ~$40

---

## 📦 Quick start

```bash
# Frontend (dev)
cd frontend && npm install && npm run dev

# Backend (dev)
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Full stack
docker-compose up
```

Configure your environment variables (`.env`) — see [`.env.example`](./.env.example). Required: `DEEPSEEK_API_KEY` and the Ollama endpoint (`localhost:11434` by default).

---

## 🙏 Credits

Delfos AI's simulation engine is built on **[MiroFish](https://github.com/666ghj/MiroFish)** by Guo Hangjiang, powered by **[OASIS](https://github.com/camel-ai/oasis)** from the CAMEL-AI research community.

Delfos extends the base engine with substantial additions: a hybrid local/API 6-step pipeline, an automated **Devil's Advocate** critical-analysis service, a structured 7-section report format with branded PDF export, multi-LLM integration, and a reorientation from public-opinion prediction toward **strategic business decision-making**.

---

<div align="center">

**δ Delfos AI** — *Strategic Simulation Engine*

Developed by **[Intelinetworks](https://intelinetworks.com)**

*Rehearse the future. Win the decision.*

</div>
