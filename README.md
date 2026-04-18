# δ Delfos AI

**Motor de Simulación Estratégica y Decision Engine**
**Strategic Simulation & Decision Engine**

---

## ES — Español

### ¿Qué es Delfos AI?

Delfos AI es una plataforma de simulación estratégica que transforma inputs de negocio — business plans, modelos financieros, documentos estratégicos — en **reportes de decisión cuantificados y accionables**.

No es un chatbot que opina. No es un dashboard que describe el pasado. Es un **stress-tester de decisiones**: alimentas el contexto de tu negocio, defines una pregunta estratégica, y el sistema simula cómo reaccionarían los actores de tu ecosistema — mostrándote dinámicas que no habías considerado, riesgos que no habías visto, y supuestos que no habías cuestionado.

### ¿Cómo funciona?

Delfos ejecuta un pipeline de 6 pasos:

| Paso | Descripción | Motor |
|------|-------------|-------|
| 1. Ingesta | Extracción de entidades y relaciones del documento | LLM Local |
| 2. GraphRAG | Construcción del grafo de conocimiento | LLM Local |
| 3. Agentes | Generación de perfiles de agentes simulados | LLM Local |
| 4. Simulación | Ejecución multi-agente con comportamiento emergente | LLM Local |
| 5. Devil's Advocate | Cuestionamiento escéptico de supuestos | DeepSeek API |
| 6. Síntesis | Generación del Prediction Report final | DeepSeek API |

### Diferenciador técnico

- **GraphRAG** — No trata documentos como texto plano. Construye un grafo de conocimiento con entidades, relaciones y causalidad.
- **Simulación multi-agente con memoria persistente** — Los agentes tienen personalidad, memoria entre rondas, y comportamiento emergente. No son prompts estáticos; evolucionan.
- **Arquitectura híbrida** — Modelo local para volumen + API externa para calidad crítica. Costo por simulación: $0.50–$2.00.
- **Devil's Advocate** — Análisis escéptico automatizado que cuestiona los 5 supuestos más frágiles de cada simulación.
- **PDF con branding** — Reportes descargables con diseño profesional, listos para presentar a stakeholders.

### Output: Prediction Report

Cada simulación produce un reporte PDF con branding Delfos AI que incluye:
- Análisis de simulación multi-agente
- Tendencias emergentes y riesgos identificados
- Análisis Crítico (Devil's Advocate) con supuestos cuestionados
- Evidencia de validación e invalidación para cada supuesto

### Stack técnico

| Componente | Tecnología |
|------------|-----------|
| Backend | Python 3.11, Flask |
| Frontend | Vue 3, Vite |
| Simulación | OASIS (CAMEL-AI) |
| Grafo de conocimiento | GraphRAG + Zep Cloud |
| LLM Local | Ollama (Qwen3.5-35B-A3B) |
| LLM API | DeepSeek V3.2 |
| PDF Export | fpdf2 |
| Infra | Docker, Caddy, Contabo VPS |

### Créditos

Delfos AI está construido sobre [MiroFish](https://github.com/666ghj/MiroFish) por Guo Hangjiang, con mejoras sustanciales en:
- Pipeline híbrido local/API con arquitectura de 6 pasos
- Servicio Devil's Advocate para análisis crítico automatizado
- Generación de reportes PDF con branding profesional
- Integración multi-LLM (Ollama + DeepSeek)
- Orientación a consultoría estratégica de negocios (vs. predicción de opinión pública)

Motor de simulación potenciado por [OASIS](https://github.com/camel-ai/oasis) de CAMEL-AI.

---

## EN — English

### What is Delfos AI?

Delfos AI is a strategic simulation platform that transforms business inputs — business plans, financial models, strategic documents — into **quantified, actionable decision reports**.

It's not a chatbot that gives opinions. It's not a dashboard that describes the past. It's a **decision stress-tester**: you feed it your business context, define a strategic question, and the system simulates how the actors in your ecosystem would react — revealing dynamics you hadn't considered, risks you hadn't seen, and assumptions you hadn't questioned.

### How does it work?

Delfos runs a 6-step pipeline:

| Step | Description | Engine |
|------|------------|--------|
| 1. Ingestion | Entity and relationship extraction from documents | Local LLM |
| 2. GraphRAG | Knowledge graph construction | Local LLM |
| 3. Agents | Simulated agent profile generation | Local LLM |
| 4. Simulation | Multi-agent execution with emergent behavior | Local LLM |
| 5. Devil's Advocate | Skeptical assumption challenging | DeepSeek API |
| 6. Synthesis | Final Prediction Report generation | DeepSeek API |

### Technical differentiators

- **GraphRAG** — Documents aren't treated as flat text. A knowledge graph with entities, relationships, and causality is built.
- **Multi-agent simulation with persistent memory** — Agents have personality, cross-round memory, and emergent behavior. They're not static prompts; they evolve.
- **Hybrid architecture** — Local model for volume + external API for critical quality. Cost per simulation: $0.50–$2.00.
- **Devil's Advocate** — Automated skeptical analysis that challenges the 5 most fragile assumptions of each simulation.
- **Branded PDF export** — Downloadable reports with professional design, ready to present to stakeholders.

### Output: Prediction Report

Each simulation produces a branded Delfos AI PDF report including:
- Multi-agent simulation analysis
- Emerging trends and identified risks
- Critical Analysis (Devil's Advocate) with challenged assumptions
- Validation and invalidation evidence for each assumption

### Tech stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11, Flask |
| Frontend | Vue 3, Vite |
| Simulation | OASIS (CAMEL-AI) |
| Knowledge graph | GraphRAG + Zep Cloud |
| Local LLM | Ollama (Qwen3.5-35B-A3B) |
| API LLM | DeepSeek V3.2 |
| PDF Export | fpdf2 |
| Infra | Docker, Caddy, Contabo VPS |

### Credits

Delfos AI is built on [MiroFish](https://github.com/666ghj/MiroFish) by Guo Hangjiang, with substantial improvements including:
- Hybrid local/API pipeline with 6-step architecture
- Devil's Advocate service for automated critical analysis
- Professional branded PDF report generation
- Multi-LLM integration (Ollama + DeepSeek)
- Business strategy consulting orientation (vs. public opinion prediction)

Simulation engine powered by [OASIS](https://github.com/camel-ai/oasis) from CAMEL-AI.

---

**δ Delfos AI** — *Strategic Simulation Engine*
Developed by [Intelinetworks](https://intelinetworks.com)
