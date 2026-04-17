"""Smoke test for pdf_generator — runs against minimal/empty/full Report objects."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
sys.path.insert(0, REPO_ROOT)

from core.agents.report_agent import (
    Report, ReportOutline, ReportSection, ReportStatus,
)
from backend.app.utils.pdf_generator import generate_pdf

OUT_DIR = os.path.join(HERE, ".pdf-smoke")
os.makedirs(OUT_DIR, exist_ok=True)


def save(report: Report, name: str) -> None:
    b = generate_pdf(report)
    path = os.path.join(OUT_DIR, name)
    with open(path, "wb") as f:
        f.write(b)
    assert b[:4] == b"%PDF", f"{name}: not a PDF (magic bytes wrong)"
    assert len(b) > 1000, f"{name}: PDF suspiciously small ({len(b)} bytes)"
    print(f"  OK  {name:32s}  {len(b):>7d} bytes  ->  {path}")


def test_full():
    sections = [
        ReportSection(
            title="Resumen Ejecutivo",
            content=(
                "Este reporte analiza el escenario de simulación estratégica.\n\n"
                "Los **hallazgos clave** incluyen tres vectores críticos de riesgo y "
                "cinco oportunidades de mitigación.\n\n"
                "### Contexto\n"
                "La simulación corrió 10 rondas con 200 agentes.\n\n"
                "> El sesgo de confirmación dominó las primeras 3 rondas.\n\n"
                "- Primer hallazgo con acento: opinión pública dividida.\n"
                "- Segundo hallazgo: polarización creciente.\n"
                "- Tercer hallazgo: dinámica no lineal.\n\n"
                "1. Acción inmediata\n"
                "2. Acción a mediano plazo\n"
                "3. Monitoreo continuo"
            ),
        ),
        ReportSection(
            title="Hallazgos Detallados",
            content="Sección con contenido mínimo para probar layout.",
        ),
        ReportSection(title="Sección Vacía", content=""),  # empty section
    ]
    outline = ReportOutline(
        title="Análisis Estratégico: Lanzamiento de Producto Q2 2026",
        summary=(
            "Evaluación de escenarios para el lanzamiento del producto X en el "
            "mercado latinoamericano, con foco en dinámicas de adopción temprana "
            "y riesgos reputacionales."
        ),
        sections=sections,
    )
    report = Report(
        report_id="report_test123456",
        simulation_id="sim_abc987",
        graph_id="mirofish_graph_xyz",
        simulation_requirement="Simular lanzamiento de producto en redes sociales",
        status=ReportStatus.COMPLETED,
        outline=outline,
        markdown_content=outline.to_markdown(),
        created_at="2026-04-17T12:34:56",
        completed_at="2026-04-17T12:40:10",
    )
    save(report, "full.pdf")


def test_empty_outline():
    report = Report(
        report_id="report_empty01",
        simulation_id="sim_empty",
        graph_id="g",
        simulation_requirement="test",
        status=ReportStatus.COMPLETED,
        outline=None,
        markdown_content="",
        created_at="2026-04-17T00:00:00",
        completed_at="",
    )
    save(report, "empty.pdf")


def test_outline_no_sections():
    outline = ReportOutline(title="Título Solo", summary="Resumen breve.", sections=[])
    report = Report(
        report_id="report_noSec",
        simulation_id="sim_x",
        graph_id="g",
        simulation_requirement="test",
        status=ReportStatus.COMPLETED,
        outline=outline,
        markdown_content="",
        created_at="2026-04-17T00:00:00",
        completed_at="",
    )
    save(report, "no_sections.pdf")


def test_markdown_only():
    report = Report(
        report_id="report_mdOnly",
        simulation_id="sim_y",
        graph_id="g",
        simulation_requirement="test",
        status=ReportStatus.COMPLETED,
        outline=None,
        markdown_content=(
            "# Reporte sin Outline\n\n"
            "> Resumen en blockquote.\n\n"
            "## Sección A\n\n"
            "Texto de la sección con **negritas** y *cursivas*.\n\n"
            "- item 1\n- item 2\n"
        ),
        created_at="2026-04-17T00:00:00",
        completed_at="",
    )
    save(report, "markdown_only.pdf")


if __name__ == "__main__":
    print("Running PDF smoke tests...")
    test_full()
    test_empty_outline()
    test_outline_no_sections()
    test_markdown_only()
    print("All smoke tests passed.")
