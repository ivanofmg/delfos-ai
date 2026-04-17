# DELFOS AI  Project Context

## What is this?
Fork of MiroFish (github.com/666ghj/MiroFish) being transformed into Delfos AI,
a strategic simulation platform for business consulting.
We keep MiroFish's backend (GraphRAG, OASIS, Zep memory) and extend it with:
hybrid LLM pipeline (Qwen3.5 local + DeepSeek API), PDF export with branding,
Devil's Advocate analysis, and eventually a custom React frontend.

## Current state
- MiroFish Vue frontend + Flask backend is LIVE at delfos.intelinetworks.com
- Backend: Flask app in /backend/app/ (blueprints: graph.py, simulation.py, report.py)
- Frontend: Vue 3 + Vite in /frontend/src/
- Core logic: /core/ (agents, graph, simulation  these are bridges to /backend/app/)
- Real code lives in /backend/app/  /core/ files just import from there
- LLM client: /backend/app/utils/llm_client.py (OpenAI-compatible, works with any provider)
- Report generation: /core/agents/report_agent.py (ReACT mode, Zep tools, markdown output)
- Reports stored in: /backend/uploads/reports/{report_id}/

## Architecture
- VPS: Contabo Cloud 50 (16 vCPU, 64GB RAM)
- LLM local: Ollama with Qwen3.5-35B-A3B (localhost:11434)
- LLM API: DeepSeek V3.2 (api.deepseek.com) for critical steps
- Memory: Zep Cloud
- Reverse proxy: Caddy
- Config: .env file at project root (LLM_API_KEY, ZEP_API_KEY, etc.)

## Rules
- Do NOT modify core/agents/report_agent.py unless explicitly asked
- Do NOT break existing MiroFish functionality
- New Delfos features go in new files (e.g., pdf_generator.py, devils_advocate.py)
- No MiroFish branding in user-facing UI  only in code comments and README
- All user-facing text must support Spanish (primary) and English
