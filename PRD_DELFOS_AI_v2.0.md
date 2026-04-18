# PRD — DELFOS AI v2.0

**Motor de Simulación Estratégica y Decision Engine**
Versión: 2.0 | Fecha: Abril 2026 | Autor: Ivanof / Intelinetworks
Estado: Pipeline funcional, frontend demo construido, en ruta a integración full-stack

---

## 0. SOBRE ESTE DOCUMENTO

Este PRD es el documento maestro de Delfos AI. Consolida:
- La visión arquitectónica del PRD v1.0 (capas de decisión, modelo económico)
- La realidad técnica del DELFOS_SETUP_TECNICO.md (pipeline híbrido, infra VPS)
- El frontend demo ya construido (React, 7 secciones, branding Delfos)
- El plan de ejecución con prompts específicos para Cursor

**Este documento se trabaja en Cursor. Cada sección incluye el prompt exacto y el agente que lo ejecuta.**

---

## 1. QUÉ ES DELFOS AI

Delfos AI es una plataforma de simulación estratégica que transforma inputs de negocio (business plans, modelos financieros, documentos estratégicos) en **reportes de decisión cuantificados y accionables**.

No es un chatbot que opina. No es un dashboard que describe el pasado. Es un **stress-tester de decisiones**: alimentas el contexto, defines una pregunta estratégica, y el sistema simula cómo reaccionarían los actores de tu ecosistema — mostrándote dinámicas que no habías considerado, riesgos que no habías visto, y supuestos que no habías cuestionado.

### Diferenciador técnico

Delfos combina tres capacidades que ninguna herramienta individual ofrece:

1. **GraphRAG** — No trata documentos como texto plano. Construye un grafo de conocimiento con entidades, relaciones, y causalidad. Los agentes razonan sobre estructura, no sobre palabras.
2. **Simulación multi-agente con memoria persistente** — Los agentes tienen personalidad, memoria entre rondas (vía Zep/Neo4j), y comportamiento emergente. No son prompts estáticos; evolucionan.
3. **Arquitectura híbrida local/API** — Modelo local (Qwen3.5) para volumen + API externa (DeepSeek) para calidad crítica. Costo por simulación: $0.50-$2.00.

### Créditos y base técnica

El motor de simulación de Delfos AI está basado en **MiroFish** (github.com/666ghj/MiroFish), un framework open-source de simulación multi-agente potenciado por OASIS de CAMEL-AI. Delfos extiende MiroFish con: frontend personalizado, pipeline híbrido local/API, formato de reporte estructurado de 7 secciones, modelo económico, y orientación a consultoría estratégica de negocios.

MiroFish fue creado por Guo Hangjiang y cuenta con soporte de Shanda Group. Delfos AI reconoce y mantiene esta atribución.

---

## 2. PROBLEMA QUE RESOLVEMOS

Las decisiones estratégicas de negocio se toman con:
- Información fragmentada y dispersa
- Cero simulación previa — se decide y se espera lo mejor
- Sin validación de escenarios — no hay "qué pasa si"
- Análisis estático que envejece al momento de recibirlo

### Por qué las alternativas no sirven

| Alternativa | Limitación |
|---|---|
| Excel / modelos financieros | Lineales, no capturan dinámicas de mercado ni comportamiento de actores |
| BI / Dashboards | Descriptivos — te dicen qué pasó, no qué puede pasar |
| LLMs directos (ChatGPT, Claude) | Responden preguntas individuales, no simulan sistemas con múltiples actores interactuando |
| Consultores tradicionales | Caros ($50K+), lentos (semanas), y su output es un PDF estático |
| MiroFish vanilla | Diseñado para predicción de opinión pública (Twitter/Reddit). No tiene formato de reporte de negocios, ni modelo económico, ni dashboard ejecutivo |

### Posicionamiento

Delfos no predice el futuro. Delfos **te muestra los futuros posibles y te dice qué decisión optimiza tus resultados bajo incertidumbre.**

---

## 3. CLIENTES TARGET (VALIDACIÓN MULTI-SECTOR)

| Cliente | Sector | Pregunta estratégica que Delfos responde |
|---|---|---|
| **Ecohomes Group** | Fintech / Home Improvement | ¿Es viable el modelo PACE en South Florida? ¿Qué pasa si cambia la regulación? |
| **Kyrios** | (Por confirmar) | Escenarios de crecimiento y riesgo operativo |
| **Audara** | (Por confirmar) | Validación de estrategia comercial y posicionamiento |
| **Seguros Mundial** | Seguros | Impacto de cambios en pricing, siniestralidad, o regulación |

Si Delfos produce insights accionables para 3 de 4 clientes → valida que el motor es genuinamente multi-sector.

---

## 4. ARQUITECTURA TÉCNICA

### 4.1 Infraestructura

```
┌─────────────────────────────────────────────────────────────┐
│                 VPS CONTABO — Cloud VPS 50                   │
│           16 vCPU · 64GB RAM · 300GB NVMe · CPU-only        │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Caddy    │  │ n8n      │  │ Ollama   │  │ PostgreSQL │  │
│  │ :443     │  │ :5678    │  │ :11434   │  │ :5432      │  │
│  │ Rev proxy│  │ Workflows│  │ LLM local│  │ Data       │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            DELFOS AI — Full Stack                     │   │
│  │                                                       │   │
│  │  Frontend: React/Vite  ◄── delfos.intelinetworks.com │   │
│  │  Backend:  FastAPI/Python                             │   │
│  │  Pipeline: 6-step hybrid (local + API)                │   │
│  │  Graph:    Neo4j/GraphRAG                             │   │
│  │  Memory:   Zep Cloud / Neo4j                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────────┐     │
│  │ Ollama Instance 1    │  │ Ollama Instance 2        │     │
│  │ qwen3.5:35b-a3b      │  │ qwen3-coder abliterated  │     │
│  │ (~26GB RAM)           │  │ (~18GB RAM)              │     │
│  │ Para: DELFOS          │  │ Para: LABS OFENSIVOS     │     │
│  └──────────────────────┘  └──────────────────────────┘     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  DeepSeek API       │
                   │  V3.2               │
                   │  $0.28/M in         │
                   │  $0.42/M out        │
                   └─────────────────────┘
```

**Dominio:** delfos.intelinetworks.com (Caddy reverse proxy)
**Costo mensual:** ~$38-42/mes (VPS $36.80 + API ~$1-5)
**GitHub:** delfos-ai repo

### 4.2 Pipeline de Simulación (6 pasos)

| Paso | Descripción | Motor | Modo | Costo |
|---|---|---|---|---|
| 1. Ingesta | Extracción de entidades y relaciones del documento | Qwen3.5 local | non-thinking | $0 |
| 2. GraphRAG | Construcción del grafo de conocimiento | Qwen3.5 local | non-thinking | $0 |
| 3. Agentes | Generación de perfiles de agentes simulados | Qwen3.5 local | non-thinking | $0 |
| 4. Simulación | Ejecución multi-agente con interacciones emergentes | Qwen3.5 local | thinking | $0 |
| 5. Devil's Advocate | Cuestionamiento de supuestos (análisis escéptico) | DeepSeek API | — | ~$0.002 |
| 6. Síntesis | Generación del Prediction Report final | DeepSeek API | — | ~$0.002 |

**Costo total por simulación:** $0.50 - $2.00
**Precio de venta por simulación (consultoría):** $2,000 - $5,000
**ROI por simulación:** 1,000x - 10,000x

### 4.3 Modelos LLM

| Modelo | Uso | RAM | Características |
|---|---|---|---|
| Qwen3.5-35B-A3B (Q4_K_M) | Pipeline Delfos (pasos 1-4) | ~26GB | 3B params activos de 35B totales, rápido en CPU, thinking + non-thinking, hasta 256K contexto |
| DeepSeek V3.2 (API) | Pasos críticos (5-6) | N/A | Alta calidad de razonamiento, cache 90% descuento, $0.28/M input |
| Qwen3-Coder abliterated | Labs ofensivos (separado) | ~18GB | No se usa para Delfos |

**REGLA:** No correr ambos modelos Ollama simultáneamente. Delfos usa solo Qwen3.5 + DeepSeek API.

---

## 5. SISTEMA DE CAPAS (DECISION ENGINE)

### Layer 1 — Input & Structuring

Recibe: business plan, modelo financiero, documentos estratégicos, contexto de mercado.
Produce: variables estructuradas, entidades, relaciones, pregunta estratégica definida.

### Layer 2 — Graph Engine (GraphRAG)

Construye un grafo de conocimiento:
- Nodos: entidades (clientes, revenue streams, costos, reguladores, competidores)
- Edges: relaciones (dependencias, causalidad, influencia)
- Comunidades: clusters de entidades relacionadas

### Layer 3 — Simulation Engine

Modelo core:
```
State → Action → Transition → Outcome
```
- **State:** condiciones actuales del sistema
- **Action:** variable de decisión (pricing, hiring, marketing spend)
- **Transition:** reglas de causalidad + comportamiento emergente de agentes
- **Outcome:** resultados medibles

Agentes con: personalidad (MBTI), memoria persistente, opiniones que evolucionan, comportamiento emergente.

### Layer 4 — Evaluation Engine

Calcula:
- ROI proyectado
- Cash flow timing
- Exposición a riesgo
- Outcomes ponderados por probabilidad
- Sensibilidad de variables críticas

### Layer 5 — Decision Engine

Produce:
- Acción recomendada con confidence score
- Escenarios rankeados por utilidad esperada
- Trade-offs explícitos
- Supuestos cuestionados con evidencia

---

## 6. FORMATO DE REPORTE — 7 SECCIONES

Cada simulación produce un **Prediction Report** con esta estructura exacta:

### Sección 1: Executive Summary
- Veredicto claro (PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED / INSUFFICIENT DATA)
- Confidence score (0-100%)
- 3 párrafos: contexto, hallazgos clave, recomendación

### Sección 2: Critical Variables
- Las 3-5 variables que más afectan el éxito del negocio
- Para cada una: valor asumido, rango realista, sensibilidad (alta/media/baja)
- Visualización: barras de sensibilidad

### Sección 3: Key Risks
- Máximo 5 riesgos prioritarios
- Para cada uno: descripción, probabilidad, impacto, mitigación sugerida
- Visualización: Risk Meter gauge (0-100)

### Sección 4: Structural Weaknesses
- Debilidades sistémicas del modelo de negocio
- Diferencia vs riesgos: los riesgos son eventos; las debilidades son condiciones permanentes

### Sección 5: Scenario Outcomes
- 3-5 escenarios simulados (best case, base case, worst case + variantes)
- Para cada uno: probabilidad, proyecciones a 12 y 24 meses, narrativa
- Visualización: barras de probabilidad

### Sección 6: Decision Impact
- Si procede: qué esperar en 6, 12, 24 meses
- Si no procede: alternativas a considerar
- Condiciones que cambiarían la recomendación

### Sección 7: Recommended Actions
- Acciones priorizadas (alta/media/baja prioridad)
- Para cada una: descripción, deadline, impacto esperado
- Acciones inmediatas (próximos 30 días) vs estratégicas (90+ días)

### Formato JSON del reporte

```json
{
  "simulation_id": "SIM-2026-001",
  "client": "Ecohomes Group",
  "title": "PACE Financing Model — South Florida Expansion",
  "date": "2026-04-05",
  "rounds": 40,
  "risk_score": 72,
  "report": {
    "executive_summary": {
      "verdict": "PROCEED WITH CONDITIONS",
      "confidence": 78,
      "paragraphs": ["...", "...", "..."]
    },
    "critical_variables": [
      {
        "name": "Customer Acquisition Cost",
        "current_value": "$340",
        "realistic_range": "$280-$520",
        "sensitivity": "high",
        "impact": "Each $50 increase reduces margins by 8%"
      }
    ],
    "key_risks": [
      {
        "title": "Regulatory Risk",
        "description": "...",
        "probability": "medium",
        "impact": "high",
        "mitigation": "..."
      }
    ],
    "structural_weaknesses": ["..."],
    "scenario_outcomes": [
      {
        "name": "Base Case",
        "probability": 45,
        "projection_12m": "...",
        "projection_24m": "...",
        "narrative": "..."
      }
    ],
    "decision_impact": {
      "if_proceed": { "6m": "...", "12m": "...", "24m": "..." },
      "if_not_proceed": { "alternatives": ["..."] },
      "conditions_to_change": ["..."]
    },
    "recommended_actions": [
      {
        "action": "...",
        "priority": "high",
        "deadline": "30 days",
        "expected_impact": "..."
      }
    ]
  }
}
```

---

## 7. FRONTEND — BRANDING & UX

### Identidad visual

- **Logo:** Delta griega (δ) — símbolo del cambio y la diferencia
- **Paleta:** Fondo oscuro (#0a0e17), dorado como acento (#d4af37 → glow), texto claro
- **Tipografía:** Playfair Display (headers), Nunito Sans (body), JetBrains Mono (datos/métricas)
- **Tono:** Premium, ejecutivo, data-driven. No es una app consumer — es una herramienta de consultoría

### Páginas principales

1. **Dashboard** — Historial de simulaciones, métricas globales, acceso rápido
2. **New Simulation** — Input de documentos + contexto + pregunta estratégica → animación del pipeline de 6 pasos
3. **Report Viewer** — Navegación lateral por las 7 secciones, visualizaciones inline, descarga PDF
4. **Settings** — Configuración de idioma (EN/ES), API keys, preferencias

### Stack frontend

- React 18 + Vite
- Tailwind CSS (utilidades) + CSS custom (branding)
- i18n: inglés + español
- PDF export: react-pdf o server-side generation
- No se usan: localStorage, sessionStorage (incompatible con artifacts)

### Rebranding: eliminar alusiones a terceros

La página en delfos.intelinetworks.com debe mostrar branding Delfos AI exclusivamente. Eliminar:
- Cualquier referencia visual o textual a MiroFish en la UI
- Logos o nombres de otros proyectos en headers/footers
- El texto "Powered by MiroFish" o similar en la interfaz

**Mantener** en el codebase y documentación técnica:
- Comentarios de atribución en el código: `// Based on MiroFish (github.com/666ghj/MiroFish)`
- README del repo con crédito completo a MiroFish y OASIS/CAMEL-AI
- Este PRD con la sección de créditos

---

## 8. MODELO ECONÓMICO (CORE — v1)

### 8.1 Objective Function

Cada simulación define una función objetivo:
```
Utility = f(Revenue, Cost, Risk, Time)
```
Configurada por el usuario o inferida del business plan.

### 8.2 Variables de decisión
- Marketing spend, pricing, hiring, channel selection, timing de lanzamiento

### 8.3 Variables externas
- Condiciones de mercado, tasas de conversión, costos variables, regulación

### 8.4 Unit Economics
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- Payback period
- Márgenes por producto/servicio

### 8.5 Scenario Modeling (v1 — Determinístico)
- Inputs fijos por escenario
- Outputs comparables
- Sensitivity analysis por variable

### 8.6 Probabilistic Layer (v2 — futuro)
- Monte Carlo simulation
- Distribuciones de probabilidad en variables clave
- Confidence intervals en proyecciones

---

## 9. MODELO DE NEGOCIO

### Fase actual: Consultoría aumentada

Delfos como herramienta interna de Intelinetworks. No se vende Delfos — se vende el análisis que Delfos produce.

| Concepto | Valor |
|---|---|
| Precio por simulación (consultoría) | $2,000 - $5,000 |
| Costo por simulación (infra + API) | $0.50 - $2.00 |
| Costo mensual fijo (VPS + API budget) | ~$40 |
| ROI del primer cliente | 50x - 130x |
| Break-even | 1 simulación vendida |

### Fase futura: SaaS self-serve

Cuando haya 10+ simulaciones exitosas y el flujo esté automatizado:
- El cliente sube documentos, configura, y obtiene reporte
- Pricing: $500/simulación (self-serve) o $2K+ (managed)
- Requiere: autenticación, multi-tenancy, billing, onboarding

---

## 10. ROADMAP DE EJECUCIÓN

### FASE 0 — Infraestructura base (COMPLETADO ✓)
- [x] VPS Cloud 50 contratado (64GB RAM)
- [x] Ollama instalado y configurado
- [x] Modelos descargados (Qwen3.5 + Coder)
- [x] Caddy reverse proxy configurado
- [x] MiroFish corriendo en delfos.intelinetworks.com
- [x] Primera simulación ejecutada (40 rondas, Ecohomes)
- [x] Frontend demo construido (React, 7 secciones, branding Delfos)
- [x] GitHub repo delfos-ai creado

### FASE 1 — Integración y rebranding (2-3 semanas)

**Objetivo:** Reemplazar frontend MiroFish con el frontend Delfos AI. Conectar pipeline híbrido. Eliminar branding terceros.

Entregables:
- Frontend React/Vite desplegado en delfos.intelinetworks.com
- Pipeline de 6 pasos conectado (Qwen3.5 local + DeepSeek API)
- Rebranding completo en la UI
- i18n funcional (EN/ES)

### FASE 2 — Reporte estructurado y PDF (1-2 semanas)

**Objetivo:** El pipeline produce reportes en formato JSON de 7 secciones. PDF descargable.

Entregables:
- ReportAgent customizado que output el formato de 7 secciones
- Transformation layer: output MiroFish → JSON Delfos
- PDF export funcional
- Dashboard con métricas reales

### FASE 3 — Validación multi-cliente (2-3 semanas)

**Objetivo:** Correr simulaciones reales con los 4 clientes. Evaluar calidad del output.

Entregables:
- Simulación Ecohomes (ya parcial) → completa
- Simulación Kyrios
- Simulación Audara
- Simulación Seguros Mundial
- Evaluación: ¿el output es vendible?

### FASE 4 — Modelo económico (3-4 semanas)

**Objetivo:** Agregar capas de evaluación cuantitativa al reporte.

Entregables:
- Módulo economic_model.py (unit economics, cash flow, ROI)
- Módulo evaluation_engine.py (scoring de escenarios)
- Integration con el pipeline
- Sensitivity analysis automático

### FASE 5 — Producción y ventas (ongoing)

**Objetivo:** Vender simulaciones como consultoría.

Entregables:
- Workflow de intake → simulación → reporte → entrega
- Template de propuesta comercial
- 3 simulaciones vendidas

---

## 11. PLAN DE EJECUCIÓN EN CURSOR

### Estructura del repo

```
/delfos-ai
├── CLAUDE.md                    # Contexto para Claude Code / Cursor
├── PRD_DELFOS_AI_v2.0.md        # Este documento
├── /frontend
│   ├── src/
│   │   ├── App.jsx              # Componente principal Delfos AI
│   │   ├── components/          # Header, Sidebar, ReportSection, etc.
│   │   ├── i18n/                # Traducciones EN/ES
│   │   ├── styles/              # Branding, themes
│   │   └── utils/               # API client, formatters
│   ├── vite.config.js
│   └── package.json
├── /backend
│   ├── main.py                  # FastAPI entry point
│   ├── delfos_llm_client.py     # Cliente unificado Ollama/DeepSeek
│   ├── delfos_pipeline.py       # Pipeline de 6 pasos
│   ├── /models
│   │   └── economic_model.py    # Modelo económico
│   ├── /agents
│   │   ├── report_agent.py      # ReportAgent customizado (7 secciones)
│   │   └── devils_advocate.py   # Agente escéptico
│   ├── /core
│   │   ├── simulation_engine.py
│   │   ├── evaluation_engine.py
│   │   └── decision_engine.py
│   ├── /data
│   │   └── scenarios/           # Datos de clientes
│   └── requirements.txt
├── /docs
│   ├── SETUP_TECNICO.md
│   └── API.md
└── docker-compose.yml           # Optional: containerización
```

### PROMPTS PARA CURSOR — Fase por fase

---

#### FASE 1: Scaffolding e integración

**Prompt 1.1 — Scaffolding** (Cursor Agent)
```
Read PRD_DELFOS_AI_v2.0.md and CLAUDE.md. Set up the project structure:
- React frontend with Vite in /frontend
- Python FastAPI backend in /backend
- Create package.json, requirements.txt, vite.config.js
- Follow the repo structure defined in Section 11 of the PRD

Do NOT install MiroFish's Vue frontend. We are replacing it entirely.
```

**Prompt 1.2 — Frontend injection** (Cursor Agent)
```
I have a complete React component for the Delfos AI demo app (delfos-ai-demo.jsx 
in the project root). Decompose it into proper React components:
- App.jsx (main layout + routing)
- components/Header.jsx (branding, nav, language toggle)
- components/Dashboard.jsx (simulation history, metrics)
- components/SimulationView.jsx (pipeline animation, 6 steps)
- components/ReportView.jsx (7-section viewer with sidebar nav)
- components/ReportSection.jsx (individual section renderer)

Configure Vite to serve it. Add i18n with react-i18next for EN/ES.
Use the branding defined in the PRD: dark bg (#0a0e17), gold accent (#d4af37),
Playfair Display for headers, JetBrains Mono for data, Nunito Sans for body.
```

**Prompt 1.3 — Backend API** (Cursor Agent)
```
Create the FastAPI backend based on delfos_pipeline.py and delfos_llm_client.py.
Expose these endpoints:
- POST /api/simulate (receives document + context + question, runs 6-step pipeline)
- GET /api/simulations (list all simulation runs)
- GET /api/simulations/{id} (get simulation details)
- GET /api/simulations/{id}/report (get the 7-section report JSON)
- POST /api/simulate/status (SSE endpoint for real-time pipeline progress)

Add CORS for the React frontend.
Pipeline connects to Ollama on localhost:11434 and DeepSeek API via env vars.
Store results in PostgreSQL (already running on the VPS).
```

**Prompt 1.4 — Rebranding** (Cursor Agent)
```
Scan all frontend files for any references to MiroFish, OASIS, CAMEL-AI, 
or any other third-party branding in the UI. Remove them from:
- Page titles, headers, footers
- Meta tags, favicon, manifest
- Any visible UI text

Keep attribution ONLY in:
- Code comments (// Based on MiroFish...)
- README.md credits section
- This PRD

Replace with Delfos AI branding: "δ Delfos AI" as the app title,
"Strategic Simulation Engine" as tagline.
```

**Prompt 1.5 — Caddy config** (Tú — en el VPS)
```bash
# En el VPS, actualizar Caddyfile para servir el nuevo frontend
# Caddy ya está configurado para delfos.intelinetworks.com
# Ajustar para proxy al frontend Vite (dev) o servir build estático (prod)
```

---

#### FASE 2: Reporte estructurado y PDF

**Prompt 2.1 — Custom ReportAgent** (Cursor Agent)
```
Create backend/agents/report_agent.py. This agent takes the raw simulation 
output from the pipeline (entities, agents, simulation results, devil's advocate 
critique) and produces a structured JSON report following the 7-section format 
defined in Section 6 of PRD_DELFOS_AI_v2.0.md.

The agent uses DeepSeek API (via delfos_llm_client.py llm.api()) with a 
carefully crafted system prompt that enforces the exact JSON schema.

Include validation: if the LLM output doesn't match the schema, retry once 
with error feedback.
```

**Prompt 2.2 — PDF generation** (Cursor Agent)
```
Add PDF export to the backend. When the frontend requests 
GET /api/simulations/{id}/report/pdf, generate a professional PDF 
with the Delfos AI branding:
- Cover page with δ logo, client name, date, simulation ID
- 7 sections with proper formatting
- Charts/visualizations rendered as images (risk meter, probability bars)
- Use reportlab or weasyprint (Python-native, no browser dependency)
- Dark theme that matches the web app aesthetic
```

**Prompt 2.3 — Dashboard con datos reales** (Cursor Agent)
```
Connect the Dashboard component to the real API endpoints. Replace demo data 
with live data from GET /api/simulations. Show:
- Total simulations run
- Average risk score across simulations  
- Latest simulation card with quick stats
- Simulation history list with status indicators
```

---

#### FASE 3: Validación multi-cliente

**Prompt 3.1 — Preparar datos Ecohomes** (Tú + Cursor Agent)
```
Create backend/data/scenarios/ecohomes.json with the Ecohomes Group business 
context: PACE financing model, South Florida market, home improvement focus.
Include: business plan summary, financial assumptions (CAC, LTV, conversion rates),
strategic question ("Is the PACE model viable in South Florida given regulatory 
and market risks?"), relevant documents.
```

**Prompt 3.2 — End-to-end test** (Cursor Agent)
```
Create a test script that runs the full Delfos pipeline end-to-end 
with the Ecohomes scenario:
1. Load ecohomes.json
2. Run the 6-step pipeline
3. Generate the 7-section report
4. Validate the JSON schema
5. Save to database
6. Verify the frontend can display it

Print timing for each step and total API cost.
```

**Prompts 3.3-3.5** — Repetir para Kyrios, Audara, Seguros Mundial (misma estructura).

---

#### FASE 4: Modelo económico

**Prompt 4.1 — Economic model module** (Cursor Agent)
```
Create backend/models/economic_model.py with classes:
- RevenueModel: projects revenue based on assumptions (units, price, growth rate)
- CostModel: fixed costs + variable costs + CAC
- UnitEconomics: CAC, LTV, payback period, margin
- CashFlowModel: monthly cash flow projection over 24 months
- SensitivityAnalyzer: varies one variable at a time, measures impact on output

All models should accept parameters as dicts and return structured results.
Include a run_economic_analysis(business_context, assumptions) function 
that the pipeline calls between steps 5 and 6.
```

**Prompt 4.2 — Evaluation engine** (Cursor Agent)
```
Create backend/core/evaluation_engine.py that:
- Takes simulation results + economic model output
- Scores each scenario on: ROI, risk exposure, time-to-value, capital efficiency
- Ranks scenarios by a configurable utility function
- Returns ranked list with trade-off explanations
- Feeds into the Decision Engine for final recommendation
```

---

## 12. CLAUDE.md PARA EL REPO

Copiar este contenido al archivo `CLAUDE.md` en la raíz del repo:

```markdown
# DELFOS AI — Project Context

## What is this?
Delfos AI is a strategic simulation platform that transforms business inputs into 
quantified decision reports. Built on MiroFish's simulation engine, extended with 
a custom React frontend, hybrid LLM pipeline, and structured 7-section report format.

## Stack
- **Frontend:** React 18 + Vite, Tailwind CSS, i18n (EN/ES)
- **Backend:** Python 3.11+, FastAPI, PostgreSQL
- **LLM Pipeline:** Ollama (Qwen3.5-35B-A3B local) + DeepSeek API (V3.2)
- **Simulation:** MiroFish/OASIS engine (GraphRAG + multi-agent + Zep memory)
- **Infra:** Contabo VPS 50 (64GB RAM), Caddy reverse proxy

## Key files
- `PRD_DELFOS_AI_v2.0.md` — Master product document
- `backend/delfos_llm_client.py` — Unified LLM client (local + API)
- `backend/delfos_pipeline.py` — 6-step simulation pipeline
- `backend/agents/report_agent.py` — 7-section report generator
- `frontend/src/App.jsx` — Main app component

## Architecture
Pipeline: Ingesta → GraphRAG → Agents → Simulation → Devil's Advocate → Synthesis
Steps 1-4: Qwen3.5 local (via Ollama, localhost:11434)
Steps 5-6: DeepSeek API (api.deepseek.com)

## Conventions
- All API responses follow the JSON schema in PRD Section 6
- Frontend branding: dark theme, gold accent, Playfair Display / JetBrains Mono
- No references to MiroFish or third parties in the UI — only in code comments and docs
- i18n: all user-facing text must support EN and ES
- Environment variables for all secrets (DEEPSEEK_API_KEY, etc.)

## Commands
- Frontend dev: `cd frontend && npm run dev`
- Backend dev: `cd backend && uvicorn main:app --reload`
- Full stack: `docker-compose up` (when containerized)
```

---

## 13. MÉTRICAS DE ÉXITO

### Producto
| Métrica | Target Fase 1-2 | Target Fase 3-4 |
|---|---|---|
| % de clientes que identifican un insight nuevo | > 60% | > 80% |
| % de outputs donde el cliente toma una acción | > 30% | > 50% |
| Tiempo para obtener primer reporte | < 2 horas | < 30 min |
| NPS post-simulación | > 7 | > 8 |

### Técnicas
| Métrica | Target |
|---|---|
| Pipeline runs sin error | > 90% |
| Tiempo end-to-end (6 pasos) | < 15 min |
| Coherencia del grafo (entidades correctas) | > 85% |
| Reporte pasa validación de schema | 100% |

### Negocio
| Métrica | Target |
|---|---|
| Simulaciones vendidas (primeros 3 meses) | 3-5 |
| Revenue (primeros 3 meses) | $6K-25K |
| Costo operativo mensual | < $50 |

---

## 14. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Output genérico que no aporta valor | Alta | Crítico | Fase 2 — Structured report + Devil's Advocate cuestiona supuestos |
| Sobreconfianza del usuario en predicciones | Media | Alto | Disclaimers + confidence scoring + lenguaje de rangos |
| No hay moat vs prompt chain bien hecho | Media | Alto | GraphRAG + multi-agente + memoria persistente + templates de sector |
| DeepSeek API inestable/timeout | Media | Medio | Together.ai como fallback ($1.25/M tokens) |
| Qwen3.5 demasiado lento en CPU | Baja | Medio | Reducir contexto a 8K, o mover todo a API temporalmente ($2-5/sim) |
| Solo funciona para un sector | Media | Alto | Validación con 4 clientes en Fase 3 |

---

## 15. SIGUIENTE PASO INMEDIATO

1. Copiar este PRD y el CLAUDE.md al repo delfos-ai
2. Abrir el repo en Cursor
3. Ejecutar Prompt 1.1 (scaffolding)
4. Ejecutar Prompt 1.2 (frontend injection)
5. Ejecutar Prompt 1.3 (backend API)
6. Ejecutar Prompt 1.4 (rebranding)
7. Deploy a delfos.intelinetworks.com
8. Test end-to-end con caso Ecohomes

**Estimación:** Fase 1 completa en 2-3 semanas de trabajo iterativo con Cursor.

---

**Este PRD es un documento vivo. Cada fase completada debe actualizar este documento con resultados reales.**

---

*Delfos AI — Strategic Simulation Engine*
*Built on MiroFish (github.com/666ghj/MiroFish) by Guo Hangjiang*
*Powered by OASIS/CAMEL-AI*
*Extended by Intelinetworks*
