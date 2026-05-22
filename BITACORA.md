# DELFOS AI — Bitácora Maestra

> Bitácora unificada del proyecto Delfos AI (fork de MiroFish). Las sesiones se ordenan de la más reciente a la más antigua. Para agregar una sesión nueva, insertar un bloque `## SESIÓN [fecha]` al inicio (debajo de este encabezado), con Cursor directamente.

---
---

# SESIÓN — 22 Mayo 2026

**Tema:** Recuperación de producción + cacería de bugs del pipeline de simulación (404 → 400 → arranque del motor) + fact-check del primer reporte + hardening de seguridad planificado.
**Resultado principal:** 🟢 **PIPELINE COMPLETO FUNCIONANDO END-TO-END EN PRODUCCIÓN POR PRIMERA VEZ.** El motor de simulación multi-agente OASIS corre las rondas, los agentes interactúan, y se generó un reporte real (`report_16b3440cc84e`).

## RESUMEN EJECUTIVO

Se entró con producción "viva pero no validada": el sitio cargaba pero el pipeline de simulación nunca había corrido completo. Tras rotar las API keys, se ejecutaron smoke tests que revelaron y resolvieron una cadena de **cinco bugs** que bloqueaban la simulación, todos de "plomería" (rutas, entorno Python, estado), **ninguno del motor de IA en sí**. Al cierre, una simulación real (elección Colombia 2026, 8 agentes) corrió completa y generó su informe. Se hizo fact-check del reporte contra la realidad.

**Conclusión de producto:** el núcleo (GraphRAG + agentes + OASIS + Zep + OpenAI) es sólido. La deuda técnica está en la capa de integración frontend↔backend heredada de MiroFish, no en el cerebro. El valor de Delfos NO está en la simulación (se sesga al consenso) sino en el Devil's Advocate que la cuestiona.

## LO QUE SE LOGRÓ

### 1. 🟢 Bug del DEBUG mode en producción — RESUELTO
- **Síntoma:** backend con `Debug mode: on` en producción pese a `DEBUG=false` en `.env`.
- **Causa raíz:** `config.py` leía `FLASK_DEBUG` (no `DEBUG`), con default `'True'`.
- **Fix config:** `DEBUG=false` → `FLASK_DEBUG=false` en `.env` (VPS + local).
- **Fix código (permanente):** default `'True'` → `'False'` en `config.py`. Commit `8b8c15f`.

### 2. 🟢 Bug del 404 en `/profiles/realtime` y `/config/realtime` — RESUELTO (desbloqueó pasos 2,3,4)
- **Síntoma:** smoke test moría en paso 3→4 con "0 perfiles, Error 404". El motor generaba todo pero el frontend no lo releía.
- **Causa raíz:** discrepancia de UN `../`. Endpoint en `config.py`: `OASIS_SIMULATION_DATA_DIR = '../uploads/simulations'` → `/app/backend/uploads/simulations` (VACÍO). Motor guarda en `'../../uploads/simulations'` → `/app/uploads/simulations` (LLENO).
- **Fix:** `'../uploads/simulations'` → `'../../uploads/simulations'` en `config.py` L49. Commit `d1af6f2`.
- **Fix persistencia:** el mount `./backend/uploads:/app/backend/uploads` no cubría `/app/uploads` (donde el motor escribe) → simulaciones se perdían al recrear. Se agregó `./uploads:/app/uploads` en `docker-compose.yml`.

### 3. 🟢 docker-compose.yml roto — RESUELTO
- **Síntoma:** YAML inválido con `services:` anidado + servicio fantasma `delfos-api` (heredado de abril).
- **Fix:** eliminado el bloque inválido, solo queda `mirofish` (con los dos mounts) + red `ai-stack_default external`. Commit `423ba3e`.

### 4. 🟢 Bug del 400 "ya está en ejecución" (estado zombie) — RESUELTO
- **Síntoma:** `POST /api/simulation/start` → 400 "ya está en ejecución" aunque nunca corrió.
- **Causa raíz:** el primer arranque falló a ~81ms (ver bug #5), dejando `run_state.json` con `runner_status: "starting"` y `process_pid: null` (zombie). El chequeo en `simulation_runner.py:334` trata `STARTING` como "corriendo" sin validar si el proceso existe. El `force:true` no rescata porque el chequeo va antes de la limpieza.
- **Fix inmediato:** borrar el `run_state.json` zombie.
- **Mejora futura:** detectar zombies (starting + pid null + stale = limpiar y arrancar).

### 5. 🟢 Bug del arranque del motor (DOS bugs en cadena) — EL BUG CLAVE
El subproceso moría en ms sin log. Ejecución manual del script reveló DOS problemas:
- **5a. Python equivocado:** el runner usaba `sys.executable`, que bajo `uv run` apunta a `/usr/local/bin/python` (sistema, SIN deps) en vez del venv `/app/backend/.venv/bin/python` (con deps). Fallaba con `ModuleNotFoundError: dotenv`, luego `camel`, etc. Prueba: ejecutar con el python del venv → arrancó y publicó posts.
- **5b. SCRIPTS_DIR mal:** `'../../scripts'` → `/app/scripts` (vacío). El script está en `/app/backend/scripts/`. No se había visto porque el zombie cortaba el flujo antes.
- **Fix combinado (commit `1936311`) en `core/simulation/simulation_runner.py`:**
  - SCRIPTS_DIR: `'../../scripts'` → `'../../backend/scripts'`
  - Nueva constante `VENV_PYTHON` (portable Win/Linux vía `sys.platform`): `os.path.join(dirname, '../../backend/.venv', 'Scripts/python.exe' if win32 else 'bin/python')`
  - En el `cmd`: `sys.executable` → `cls.VENV_PYTHON if os.path.exists(cls.VENV_PYTHON) else sys.executable`
  - `RUN_STATE_DIR` se dejó intacto (`'../../uploads/simulations'` ya correcto).

### 6. 🟢 Smoke test final — PIPELINE COMPLETO + REPORTE GENERADO
- Motor arrancó con `PID: 158` (ya no null). `[Plaza] R69/40`, `[Community] R66/40`, `TOTAL EVENTS: 161`. Agentes publicando/comentando/likeando.
- ReportAgent generó `report_16b3440cc84e` (3 secciones + Devil's Advocate). **Pipeline validado 100% end-to-end por primera vez.**

### 7. 🟡 Bug NUEVO — `interview_agents` import roto (NO bloqueante, PENDIENTE)
- **Síntoma:** `ERROR: interview_agents falló: No module named 'core.graph.simulation_runner'`.
- **Causa:** import con ruta equivocada — `core.graph.simulation_runner` debe ser `core.simulation.simulation_runner`.
- **Impacto:** no bloqueó el reporte (usó `quick_search` como fallback) pero el informe salió más pobre (sin las entrevistas a agentes).
- **Síntoma asociado:** `WARNING: Sección "Tendencias y Riesgos" alcanzó máximo de iteraciones; generación forzada` — NO es independiente: la sección intentó usar `interview_agents`, falló, no se completó bien, agotó iteraciones. **Hipótesis: arreglar el import elimina ERROR + WARNING de una.** NO subir `max_iterations` como parche aislado.
- **Fix futuro (fácil):** corregir `core.graph` → `core.simulation` en las herramientas del ReportAgent.

## FACT-CHECK DEL REPORTE (contra encuestas reales mayo 2026)
- 🟢 **Datos del seed:** correctos (Cepeda 37.6%, Abelardo 32.9%, Paloma 16.7%, Fajardo 5.9%, rechazo Cepeda 46.5% — de AtlasIntel/Semana). El motor no inventó números.
- 🔴 **Conclusión "alianzas/colaboración":** DESVIADA. La realidad es alta polarización, no convergencia. **Sesgo de manada confirmado** (agentes LLM tienden al consenso cortés).
- 🔴 **Omitió segunda vuelta** (lo decisivo: Cepeda lidera 1ª pero pierde balotaje vs Abelardo/Paloma). Culpa del prompt light.
- 🟢🟢 **Devil's Advocate (DeepSeek): EXCELENTE.** Desmontó las conclusiones del propio reporte con precisión (rechazo alto ≠ catalizador de consenso; likes ≠ alianzas; polarización moviliza en ambos sentidos). Coincide con la realidad.

## HALLAZGOS DE PRODUCTO (estrategia comercial)
1. 🔴 Delfos NO sirve para predicción numérica — se sesga al consenso (confirmado).
2. 🟢 Delfos SÍ sirve para escenarios + estrés crítico. El valor está en el Devil's Advocate sobre la simulación, no en la simulación misma. Esa tensión ES el producto.
3. 🟡 El prompt/seed es determinante (light → análisis light).
4. 🟡 El motor solo simula lo que está en el seed. Faltaron candidatos reales (Claudia López, Roy Barreras, Miguel Uribe Londoño, Santiago Botero) porque el seed solo tenía 4.
5. 🔴 Riesgo comercial: si un cliente lee el reporte sin el Devil's Advocate, se lleva conclusión errada. Vender Delfos como herramienta de pensamiento/contraste, NO bola de cristal.

## LECCIONES APRENDIDAS (DEPLOY)
- **L1. `--force-recreate` NO reconstruye la imagen.** Dockerfile usa `COPY . .` → código horneado. Deploy correcto: `git pull` → `docker compose build mirofish` → `up -d --force-recreate`.
- **L2. NUNCA editar archivos en el VPS directamente.** Desincroniza git → cada pull choca (pasó 3 veces hoy con docker-compose.yml). Todo: local → commit → push → VPS solo `git pull`. Si el VPS tiene cambios locales: `cp backup` + `git checkout` + `git pull`.
- **L3. "Dubious ownership":** `git config --global --add safe.directory /apps/delfos-ai` (para usuario y root con sudo).
- **L4. `sys.executable` ≠ python del venv bajo `uv run`.** Usar ruta explícita del venv para subprocesos que necesitan deps del proyecto.
- **L5. Contar bien los `../` en rutas relativas.** `uploads` está en `/app/uploads`, pero `scripts` en `/app/backend/scripts`. No asumir mismo nivel.
- **L6. Subproceso que muere sin log:** ejecutarlo a mano en primer plano (`docker exec mirofish <python> <script> <args>`) revela el traceback real.
- **L7. Errores HTTP:** el motivo del 400/404 está en la respuesta (DevTools→Network→Response o HAR), no siempre en los logs del backend.
- **L8. `docker logs -f` se bloquea al copiar/pegar.** Usar `docker logs --tail N` (sin `-f`) para copiar, o segunda sesión SSH.

## ESTADO DE PRODUCCIÓN AL CIERRE
| Componente | Estado |
|---|---|
| Sitio (Caddy) | 🟢 Vivo |
| API keys (OpenAI, DeepSeek, Zep) | 🟢 Rotadas y verificadas |
| DEBUG mode | 🟢 Off |
| Pipeline completo (grafo→agentes→config→activación→simulación→reporte) | 🟢 Funciona end-to-end |
| Persistencia de simulaciones (mount) | 🟢 Arreglado |
| `interview_agents` (enriquecimiento del reporte) | 🟡 Roto (no bloqueante) |
| Commits VPS = GitHub = local | 🟢 Sincronizados (`1936311`) |

**Commits clave:** `8b8c15f` (DEBUG), `d1af6f2` (path uploads + mount), `423ba3e` (compose limpio), `1936311` (SCRIPTS_DIR + VENV_PYTHON).

## PENDIENTES Y FASES FUTURAS

### A. Seguridad — Autenticación
- **Inmediato (~30 min):** Basic Auth en **Caddy** (no en la app). Credenciales manuales del dueño (sin email/reset). Evita que bots/curiosos drenen la API. No toca código de Delfos.
- **Fase 2-3:** Auth real con usuarios, login, sesiones.
- **Fase 3-4 (estratégico): BYOK** — usuario ingresa su propia key de OpenAI/DeepSeek. Traslada costo de cómputo al usuario, elimina riesgo de drenaje, alinea modelo de negocio (vender motor+análisis, no cómputo). `config.py` ya es OpenAI-compatible. Cuidado: manejo seguro de keys de terceros (nunca plaintext).

### B. Seguridad — Hardening antes de exposición pública
- **XSS (riesgo ALTO):** Delfos renderiza contenido LLM en Vue. Auditar `v-html` → DOMPurify. **Prioridad #1.**
- **SQLi (riesgo BAJO):** no usa SQL. Excepción: si se agrega PostgreSQL (persistencia) → queries parametrizadas.
- **Prompt injection:** separar instrucciones de sistema vs contenido de usuario.
- **Path traversal:** validar formato de `simulation_id`.
- **File upload:** validar tipo/tamaño.
- **Rate limiting:** ausente, agregar.
- **Headers (CSP, etc.) + CORS:** vía Caddy; CORS no debe ser `*`.
- **Pentest interno:** correr Kali contra staging (une el máster de cibersec con Delfos).

### C. Deuda técnica / mejoras
- **Fix `interview_agents`** (`core.graph` → `core.simulation`) — resuelve también el warning de iteraciones.
- **Persistencia/caché (compute-level):** tabla PostgreSQL `simulations` (id, input_hash sha256, report_json JSONB, status, created_at) + `get_cached_report`/`save_report` + flag `force_rerun`. Evita re-quemar API en consultas repetidas.
- **SECRET_KEY:** default público `'mirofish-secret-key'` en `config.py`. Definir uno propio en `.env`.
- **Rebranding frontend Vue:** sigue MiroFish (header, barra "EnPíxeles Lab / Manuel Peña", logo betta, "Motor: MiroFish-V1.0", prompt ejemplo chino). Resolver narrativa de atribución a terceros antes de mostrar a prospectos.
- **Resolver duplicación `core/` vs `backend/app/services/`** (raíz de la confusión de rutas).
- **Unificar `.env`** (local en `backend/.env`, VPS en raíz).
- **Dueño consistente del repo en VPS** (root vs ivanof).
- **Arquitectura LLM:** producción corre TODO en OpenAI gpt-4o (no el híbrido Qwen-local + DeepSeek del PRD). Costo real > estimado optimista. Plan: migrar a qwen3-coder local.

## PLAN PRÓXIMA SESIÓN
**Objetivo:** correr Delfos con input SERIO (vs test light) atacando los dos problemas detectados.
- **Frente 1 — Seeds ricos:** material real de prensa (🟢 El Tiempo, Semana, Infobae, La Silla Vacía, fichas de encuestadoras), X/Twitter (🟡 narrativa, sesgo activista), Reddit (🟡 segmento joven-urbano). Múltiples seeds. Seed estructurado: datos duros + mapa COMPLETO de actores + narrativas etiquetadas por fuente + pregunta de stress-test.
- **Frente 2 — Anti-manada:** instrucción adversarial (agentes confrontan, no buscan consenso), perfiles más combativos, explorar parámetros del motor ("cámara de eco", "tendencia emocional"). Límite honesto: el sesgo es parcialmente estructural de los LLMs; reducir, no eliminar → el Devil's Advocate sigue siendo la red de seguridad.
- **Propuesta:** "seed adversarial" (material diverso + instrucciones de confrontación + mapa completo) + más rondas.

---
---

# SESIÓN — 17-18 Abril 2026

**Tema:** PRD v2.0 + PDF Export + DeepSeek Devil's Advocate + Deploy completo (rebuild de imagen).

## LO QUE SE LOGRÓ

### 1. PRD v2.0 creado (`PRD_DELFOS_AI_v2.0.md`)
- Visión de producto, arquitectura real, clientes target, modelo de negocio.
- Formato de reporte de 7 secciones con JSON schema. Roadmap de 5 fases con prompts para Cursor. `CLAUDE.md` creado y commiteado.

### 2. PDF Export con branding Delfos AI — EN PRODUCCIÓN
- `backend/app/utils/pdf_generator.py`, usa fpdf2 (pure Python).
- Cover navy #0a0e17, δ dorado, "DELFOS AI", metadata, "CONFIDENTIAL". Headers navy, blockquotes borde dorado. Back page con timestamp.
- Endpoints: `GET /api/report/<id>/download?format=pdf` y `/api/report/<id>/pdf`.
- Fix: blockquotes con markdown complejo → fallback a texto plano.

### 3. DeepSeek API como LLM secundario — EN PRODUCCIÓN
- `DEEPSEEK_API_KEY/BASE_URL/MODEL` en `.env`. Factory `LLMClient.create_deepseek_client()`. Formato OpenAI-compatible.

### 4. Devil's Advocate Service — EN PRODUCCIÓN
- `backend/app/services/devils_advocate.py`. Endpoint `POST /api/report/<id>/devils-advocate`.
- Cuestiona los 5 supuestos más frágiles. **Auto-run** después de generar cada reporte; appende sección "Análisis Crítico (Devil's Advocate)" antes de guardar.

### 5. Reporte completo generado y verificado
- `delfos_ecohomes_complete.pdf` (10 págs): simulación (3 secciones) + Devil's Advocate (5 supuestos) + branding. `report_2391e5048de1`.

### 6. Container reconstruido + docker-compose.yml corregido + README rebrandeado
- Imagen nueva `delfos-ai-mirofish:latest`. Eliminado el bloque `services:`/`delfos-api` erróneo (volvió a aparecer en mayo, ver esa sesión). fpdf2/markdown vía `uv lock && uv sync`. README bilingüe ES/EN con δ Delfos AI + créditos a MiroFish/OASIS.

### 7. Seguridad VPS
- Login SSH root deshabilitado. Acceso: `ivanof` → `sudo su`. SSH puerto 2224. Fail2ban activo.

## INFRAESTRUCTURA (abril)
- **VPS Contabo Cloud 50:** 16 vCPU, 64GB RAM, 300GB NVMe, Ubuntu 24.
- **Containers:** `mirofish` (Flask :5001 + Vue :3000), `caddy` (:80/:443), `open-webui` (:3001), `n8n` (:5678), `n8n-postgres` (:5432).
- **Deploy (establecido en abril):** `git push` (Windows) → VPS: `git pull` → `docker compose build mirofish` → stop/rm → `up -d` → `uv lock && uv sync` si hay deps nuevas.
- **`.env` NO está en git** — crear manual en cada ambiente. Variables: `LLM_API_KEY/BASE_URL/MODEL_NAME` (OpenAI gpt-4o), `ZEP_API_KEY`, `VITE_API_BASE_URL`, `DEEPSEEK_*`, `DEBUG`.

## PENDIENTES QUE QUEDARON DE ABRIL (estado en mayo)
- ✅ docker-compose.yml roto → resuelto definitivamente en mayo (commit `423ba3e`).
- ✅ Deps/fixes que se perdían en restart → entendido en mayo (L1: `--force-recreate` no rebuildeа; falta `build`).
- ✅ Reportes perdidos al recrear → resuelto en mayo (mount `./uploads:/app/uploads`).
- ⏳ Restructurar reporte a 7 secciones Delfos (post-processor o modificar prompts del ReportAgent) — PENDIENTE.
- ⏳ Rebranding frontend Vue — PENDIENTE.
- ⏳ Botones PDF download + Devil's Advocate en frontend — PENDIENTE.
- ⏳ Página 2 del PDF vacía (cosmético) — PENDIENTE.

## NOTAS DE ARQUITECTURA (referencia abril)
- ReportAgent core (`core/agents/report_agent.py`, ~2578 líneas, modo ReACT) genera secciones narrativas libres. Plan: NO modificar el core; usar post-processor o ajustar `PLAN_SYSTEM_PROMPT`/`SECTION_SYSTEM_PROMPT_TEMPLATE`.
- LLM principal pasó de gpt-4o-mini (inicio abril) a gpt-4o (final abril).
- Commits abril: `91fc96f` (PDF), `ab904ab` (deps), `976b2bc` (DeepSeek+DevilsAdvocate), `82e9d1c` (README), `6bdd546` (auto-run DA), `19b51c3` (uv.lock).

---
---

## INFRAESTRUCTURA ACTUAL (referencia rápida, mayo 2026)

- **VPS:** Contabo Cloud 50, host `vmi2939288`, 16 vCPU / 64GB / 300GB NVMe, Ubuntu 24. SSH puerto 2224, `ivanof` + `sudo su`, root login off, fail2ban.
- **Repo VPS:** `/apps/delfos-ai` (owned by root). **Repo local:** `C:\dev\delfos-ai\delfos-ai` (carpeta anidada). **GitHub:** `github.com/ivanofmg/delfos-ai` (privado).
- **Dominio:** delfos.intelinetworks.com vía Caddy.
- **Container:** `mirofish` (`npm run dev` = concurrently backend Flask :5001 + frontend Vue :3000). Imagen `delfos-ai-mirofish:latest`. Red `ai-stack_default` (external).
- **Python del backend:** venv de uv en `/app/backend/.venv/bin/python` (NO `/usr/local/bin/python`).
- **Datos de simulación:** `/app/uploads/simulations/<sim_id>/` (montado a `./uploads` del host).
- **LLM:** OpenAI gpt-4o (principal), DeepSeek (Devil's Advocate). Memoria: Zep Cloud.
- **Deploy correcto:** `git pull` → `docker compose build mirofish` → `docker compose up -d --force-recreate mirofish`. NUNCA editar en el VPS directamente.

---

*Bitácora maestra. Última actualización: 22 de mayo de 2026. Para nuevas sesiones, anexar bloque `# SESIÓN [fecha]` al inicio con Cursor.*
