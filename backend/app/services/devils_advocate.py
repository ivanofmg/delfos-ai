"""
Delfos AI — Devil's Advocate Service
Challenges assumptions in simulation results using DeepSeek API.
Runs after report generation to add critical analysis.
"""

from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger('delfos.devils_advocate')

DEVILS_ADVOCATE_SYSTEM = """Eres un analista estratégico escéptico y riguroso. Tu trabajo es identificar 
los supuestos más frágiles en un análisis de simulación y cuestionar cada uno con datos y lógica. 
No seas complaciente. Sé directo y específico.

Para cada supuesto que identifiques, proporciona:
1. Cuál es el supuesto
2. Por qué podría fallar
3. Qué evidencia lo validaría o invalidaría
4. Qué pasa con el negocio si falla

Responde en el mismo idioma del input (español o inglés).
Formatea tu respuesta en Markdown con secciones claras."""


def run_devils_advocate(
    simulation_requirement: str,
    report_markdown: str,
    max_tokens: int = 4096
) -> str:
    """
    Run Devil's Advocate analysis on a completed report.
    Uses DeepSeek API if configured, otherwise falls back to default LLM.
    
    Args:
        simulation_requirement: The original simulation question/requirement
        report_markdown: The generated report in markdown format
        
    Returns:
        Devil's Advocate analysis as markdown text
    """
    client = LLMClient.create_deepseek_client()
    
    # Truncar el reporte si es muy largo para no exceder contexto
    report_text = report_markdown[:12000] if len(report_markdown) > 12000 else report_markdown
    
    messages = [
        {"role": "system", "content": DEVILS_ADVOCATE_SYSTEM},
        {"role": "user", "content": f"""Requisito de simulación: {simulation_requirement}

Reporte generado por la simulación:
{report_text}

Identifica los 5 supuestos más críticos y frágiles en este análisis.
Para cada uno, explica por qué podría fallar y cuáles serían las consecuencias.
Sé específico y cita detalles del reporte."""}
    ]
    
    try:
        response = client.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        logger.info(f"Devil's Advocate analysis completed ({len(response)} chars)")
        return response
    except Exception as e:
        logger.error(f"Devil's Advocate analysis failed: {e}")
        return f"Análisis Devil's Advocate no disponible: {str(e)}"
