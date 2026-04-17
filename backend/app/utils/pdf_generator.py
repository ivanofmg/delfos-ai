"""
Delfos AI — PDF Report Generator
Converts markdown reports to branded PDFs

Public API:
    generate_pdf(report: Report) -> bytes
        Generate a branded PDF from a Report object. Returns PDF bytes.

Design notes:
    - Uses fpdf2 (pure Python, no system dependencies — unlike weasyprint).
    - Auto-detects a Unicode-capable TTF font on the host system so the "δ"
      glyph and Spanish diacritics render correctly. Falls back to the
      built-in core Helvetica (Latin-1 only) and sanitizes the text if no
      Unicode font is available, so PDF generation always succeeds.
    - Renders from Report.outline (title + summary + sections) when
      available. Falls back to Report.markdown_content if the outline is
      missing. Empty sections are handled gracefully.
    - Does NOT modify any core dataclass or the report generation pipeline.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import List, Optional

from fpdf import FPDF

# The Report type lives in core/agents/report_agent.py. Backend startup adds
# the repo root to sys.path, so this import resolves in both dev and prod.
from ..services.report_agent import Report, ReportSection


# ─────────────────────────────────────────────────────────────────
# Brand palette
# ─────────────────────────────────────────────────────────────────

DELFOS_NAVY       = (10, 14, 23)       # #0a0e17 — cover/back background
DELFOS_GOLD       = (212, 175, 55)     # #d4af37 — accent
DELFOS_DARK_NAVY  = (26, 26, 46)       # #1a1a2e — section headings
DELFOS_BODY       = (38, 38, 50)       # body text on white
DELFOS_LIGHT      = (245, 245, 250)    # light text on dark bg
DELFOS_MUTED      = (120, 120, 130)    # secondary text
DELFOS_QUOTE      = (70, 70, 85)       # blockquote text


# ─────────────────────────────────────────────────────────────────
# Unicode font auto-detection
# ─────────────────────────────────────────────────────────────────
#
# fpdf2's core fonts (Helvetica/Times/Courier) only support Latin-1.
# To render the Greek δ and Spanish accented characters we need a TTF.
# We try common system fonts; if none are found we gracefully degrade.

_UNICODE_FONT_REGULAR_CANDIDATES = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\Arial.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

_UNICODE_FONT_BOLD_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]

_UNICODE_FONT_ITALIC_CANDIDATES = [
    r"C:\Windows\Fonts\ariali.ttf",
    r"C:\Windows\Fonts\segoeuii.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf",
    "/Library/Fonts/Arial Italic.ttf",
]


def _first_existing(paths: List[str]) -> Optional[str]:
    for p in paths:
        if p and os.path.exists(p):
            return p
    return None


# Replacement table used only when no Unicode font is available.
# Keeps non-ASCII text readable without crashing fpdf2 on Latin-1 encoding.
_ASCII_FALLBACK = {
    "δ": "d", "Δ": "D",
    "—": "-", "–": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "•": "*",
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u",
    "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N", "Ü": "U",
    "¿": "?", "¡": "!",
}


# ─────────────────────────────────────────────────────────────────
# PDF class
# ─────────────────────────────────────────────────────────────────

class DelfosPDF(FPDF):
    """Branded PDF document for Delfos AI reports."""

    def __init__(self, report_id: str = "", title: str = ""):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.report_id = report_id or ""
        self.doc_title = title or "Strategic Simulation Report"
        self._draw_chrome = False  # suppress header/footer on cover/back pages

        self.set_left_margin(18)
        self.set_right_margin(18)
        self.set_auto_page_break(auto=True, margin=22)

        self._setup_fonts()

    # ── Font setup ────────────────────────────────────────────

    def _setup_fonts(self) -> None:
        regular = _first_existing(_UNICODE_FONT_REGULAR_CANDIDATES)
        bold    = _first_existing(_UNICODE_FONT_BOLD_CANDIDATES)
        italic  = _first_existing(_UNICODE_FONT_ITALIC_CANDIDATES)

        self.unicode_ok = False
        self.font_family = "helvetica"

        if regular:
            try:
                self.add_font("Delfos", "", regular)
                self.add_font("Delfos", "B", bold or regular)
                self.add_font("Delfos", "I", italic or regular)
                self.add_font("Delfos", "BI", bold or regular)
                self.font_family = "Delfos"
                self.unicode_ok = True
            except Exception:
                # Font file unreadable / unsupported — fall back silently.
                self.font_family = "helvetica"
                self.unicode_ok = False

    # ── Text sanitization ─────────────────────────────────────

    def _txt(self, text: Optional[str]) -> str:
        """Sanitize text for the active font encoding."""
        if text is None:
            return ""
        if self.unicode_ok:
            return text
        out = text
        for k, v in _ASCII_FALLBACK.items():
            out = out.replace(k, v)
        try:
            return out.encode("latin-1", "replace").decode("latin-1")
        except Exception:
            return out

    # ── Chrome (header/footer on content pages only) ──────────

    def header(self):
        if not self._draw_chrome:
            return
        self.set_y(10)
        self.set_font(self.font_family, "B", 9)
        self.set_text_color(*DELFOS_DARK_NAVY)
        logo = self._txt("δ Delfos AI") if self.unicode_ok else "Delfos AI"
        self.cell(0, 6, logo, align="L")
        if self.report_id:
            self.set_font(self.font_family, "", 8)
            self.set_text_color(*DELFOS_MUTED)
            self.set_xy(-60, 10)
            self.cell(42, 6, self._txt(self.report_id), align="R")
        # Thin gold separator
        self.set_draw_color(*DELFOS_GOLD)
        self.set_line_width(0.3)
        self.line(18, 18, 192, 18)
        self.set_y(24)

    def footer(self):
        if not self._draw_chrome:
            return
        self.set_y(-14)
        self.set_font(self.font_family, "", 9)
        self.set_text_color(*DELFOS_MUTED)
        self.cell(0, 8, f"{self.page_no() - 1}", align="C")

    # ── Cover page ────────────────────────────────────────────

    def cover_page(self, report: Report) -> None:
        self._draw_chrome = False
        self.add_page()

        # Dark background
        self.set_fill_color(*DELFOS_NAVY)
        self.rect(0, 0, 210, 297, style="F")

        # Giant δ symbol (or DELFOS fallback)
        self.set_text_color(*DELFOS_GOLD)
        if self.unicode_ok:
            self.set_font(self.font_family, "B", 180)
            self.set_xy(0, 55)
            self.cell(210, 80, "δ", align="C")
        else:
            self.set_font(self.font_family, "B", 64)
            self.set_xy(0, 90)
            self.cell(210, 30, "DELFOS", align="C")

        # Brand name
        self.set_font(self.font_family, "B", 34)
        self.set_text_color(*DELFOS_GOLD)
        self.set_xy(0, 148)
        self.cell(210, 12, "DELFOS AI", align="C")

        # Subtitle
        self.set_font(self.font_family, "", 13)
        self.set_text_color(*DELFOS_LIGHT)
        self.set_xy(0, 165)
        self.cell(210, 8, self._txt("Strategic Simulation Report"), align="C")

        # Gold divider
        self.set_draw_color(*DELFOS_GOLD)
        self.set_line_width(0.6)
        self.line(75, 183, 135, 183)

        # Report title
        report_title = (
            report.outline.title if (report.outline and report.outline.title) else self.doc_title
        )
        self.set_font(self.font_family, "B", 18)
        self.set_text_color(*DELFOS_LIGHT)
        self.set_xy(20, 195)
        self.multi_cell(170, 9, self._txt(report_title), align="C")

        # Meta block
        self.set_font(self.font_family, "", 10)
        self.set_text_color(*DELFOS_MUTED)

        sim_id = report.simulation_id or "—"
        created = report.created_at[:10] if report.created_at else datetime.now().strftime("%Y-%m-%d")

        self.set_xy(20, 245)
        self.cell(170, 6, self._txt(f"Simulation ID:  {sim_id}"), align="C")
        self.set_xy(20, 252)
        self.cell(170, 6, self._txt(f"Date:  {created}"), align="C")
        if self.report_id:
            self.set_xy(20, 259)
            self.cell(170, 6, self._txt(f"Report:  {self.report_id}"), align="C")

        # CONFIDENTIAL watermark
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(*DELFOS_GOLD)
        self.set_xy(0, 278)
        self.cell(210, 6, self._txt("— CONFIDENTIAL —"), align="C")

    # ── Content ───────────────────────────────────────────────

    def content_pages(self, report: Report) -> None:
        self._draw_chrome = True
        self.add_page()

        # Document title (repeat of cover title, smaller)
        if report.outline and report.outline.title:
            self.set_font(self.font_family, "B", 20)
            self.set_text_color(*DELFOS_DARK_NAVY)
            self.multi_cell(0, 10, self._txt(report.outline.title))
            self.ln(2)

        # Executive summary in a gold-bordered blockquote
        if report.outline and report.outline.summary:
            self._render_summary_box(report.outline.summary)
            self.ln(4)

        # Render sections (preferred: structured outline)
        rendered_from_outline = False
        if report.outline and report.outline.sections:
            for section in report.outline.sections:
                self._render_section(section)
            rendered_from_outline = True

        # Fallback: render from raw markdown if no outline available
        if not rendered_from_outline and report.markdown_content:
            self._render_markdown(report.markdown_content)

        # Graceful note if report has no content at all
        if not rendered_from_outline and not report.markdown_content:
            self.set_font(self.font_family, "I", 11)
            self.set_text_color(*DELFOS_MUTED)
            self.multi_cell(0, 6, self._txt("(No hay contenido disponible para este reporte.)"))

    def _render_summary_box(self, summary: str) -> None:
        left_x = self.l_margin
        start_y = self.get_y()
        self.set_xy(left_x + 5, start_y + 1)
        self.set_font(self.font_family, "I", 11)
        self.set_text_color(*DELFOS_QUOTE)
        self.multi_cell(
            self.epw - 5,
            6,
            self._txt(summary.strip()),
        )
        end_y = self.get_y()
        # Gold left border
        self.set_draw_color(*DELFOS_GOLD)
        self.set_line_width(1.2)
        self.line(left_x, start_y, left_x, end_y + 1)

    def _render_section(self, section: ReportSection) -> None:
        title = (section.title or "").strip()
        content = (section.content or "").strip()

        if title:
            self.ln(4)
            self.set_font(self.font_family, "B", 16)
            self.set_text_color(*DELFOS_DARK_NAVY)
            self.multi_cell(0, 9, self._txt(title))
            # Subtle gold underline
            self.set_draw_color(*DELFOS_GOLD)
            self.set_line_width(0.4)
            y = self.get_y()
            self.line(self.l_margin, y, self.l_margin + 18, y)
            self.ln(3)

        if content:
            self._render_markdown(content)
        # else: nothing to render — empty sections are acceptable.

    # ── Minimal markdown renderer ─────────────────────────────

    def _render_markdown(self, md_text: str) -> None:
        """Render a subset of Markdown: headings (##/###), paragraphs,
        bullet/numbered lists, blockquotes, inline **bold**/*italic*,
        and fenced code blocks."""
        lines = md_text.splitlines()
        in_code = False
        paragraph: List[str] = []

        def flush_paragraph() -> None:
            if not paragraph:
                return
            text = " ".join(paragraph).strip()
            self.set_font(self.font_family, "", 11)
            self.set_text_color(*DELFOS_BODY)
            try:
                self.multi_cell(0, 6, self._txt(text), markdown=True)
            except Exception:
                self.multi_cell(0, 6, self._txt(text))
            self.ln(1.5)
            paragraph.clear()

        for raw in lines:
            line = raw.rstrip()
            stripped = line.lstrip()

            # Fenced code block toggle
            if stripped.startswith("```"):
                flush_paragraph()
                in_code = not in_code
                continue

            if in_code:
                self.set_font("courier", "", 9)
                self.set_text_color(*DELFOS_BODY)
                self.multi_cell(0, 5, self._txt(line))
                continue

            # Blank line → end paragraph
            if not stripped:
                flush_paragraph()
                continue

            # Headings
            if stripped.startswith("#### "):
                flush_paragraph()
                self.ln(2)
                self.set_font(self.font_family, "B", 11)
                self.set_text_color(*DELFOS_DARK_NAVY)
                self.multi_cell(0, 6, self._txt(stripped[5:]))
                self.ln(1)
                continue
            if stripped.startswith("### "):
                flush_paragraph()
                self.ln(2)
                self.set_font(self.font_family, "B", 12)
                self.set_text_color(*DELFOS_DARK_NAVY)
                self.multi_cell(0, 7, self._txt(stripped[4:]))
                self.ln(1)
                continue
            if stripped.startswith("## "):
                flush_paragraph()
                self.ln(3)
                self.set_font(self.font_family, "B", 14)
                self.set_text_color(*DELFOS_DARK_NAVY)
                self.multi_cell(0, 8, self._txt(stripped[3:]))
                self.ln(1)
                continue
            if stripped.startswith("# "):
                flush_paragraph()
                self.ln(3)
                self.set_font(self.font_family, "B", 16)
                self.set_text_color(*DELFOS_DARK_NAVY)
                self.multi_cell(0, 9, self._txt(stripped[2:]))
                self.ln(2)
                continue

            # Blockquote
            if stripped.startswith("> "):
                flush_paragraph()
                quote = stripped[2:]
                left_x = self.l_margin
                start_y = self.get_y()
                self.set_xy(left_x + 5, start_y + 0.5)
                self.set_font(self.font_family, "I", 11)
                self.set_text_color(*DELFOS_QUOTE)
                self.multi_cell(self.epw - 5, 6, self._txt(quote))
                end_y = self.get_y()
                self.set_draw_color(*DELFOS_GOLD)
                self.set_line_width(1.0)
                self.line(left_x, start_y, left_x, end_y + 0.5)
                self.ln(1)
                continue

            # Bullet list
            m_bullet = re.match(r"^[\-\*\+]\s+(.*)", stripped)
            if m_bullet:
                flush_paragraph()
                self._render_list_item(
                    bullet=("•" if self.unicode_ok else "-"),
                    text=m_bullet.group(1),
                )
                continue

            # Numbered list
            m_num = re.match(r"^(\d+)\.\s+(.*)", stripped)
            if m_num:
                flush_paragraph()
                self._render_list_item(
                    bullet=f"{m_num.group(1)}.",
                    text=m_num.group(2),
                )
                continue

            # Default: paragraph text
            paragraph.append(stripped)

        flush_paragraph()

    def _render_list_item(self, bullet: str, text: str) -> None:
        self.set_font(self.font_family, "", 11)
        self.set_text_color(*DELFOS_BODY)
        y = self.get_y()
        # Bullet column
        self.set_xy(self.l_margin + 2, y)
        self.cell(6, 6, self._txt(bullet))
        # Text column (wraps within remaining width)
        body_x = self.l_margin + 8
        self.set_xy(body_x, y)
        body_w = self.epw - 8
        try:
            self.multi_cell(body_w, 6, self._txt(text), markdown=True)
        except Exception:
            self.multi_cell(body_w, 6, self._txt(text))

    # ── Back page ─────────────────────────────────────────────

    def back_page(self) -> None:
        self._draw_chrome = False
        self.add_page()
        self.set_fill_color(*DELFOS_NAVY)
        self.rect(0, 0, 210, 297, style="F")

        # Small δ mark
        self.set_text_color(*DELFOS_GOLD)
        if self.unicode_ok:
            self.set_font(self.font_family, "B", 80)
            self.set_xy(0, 95)
            self.cell(210, 40, "δ", align="C")

        self.set_font(self.font_family, "B", 22)
        self.set_text_color(*DELFOS_GOLD)
        self.set_xy(0, 148)
        self.cell(210, 10, "Generated by Delfos AI", align="C")

        self.set_font(self.font_family, "", 12)
        self.set_text_color(*DELFOS_LIGHT)
        self.set_xy(0, 162)
        self.cell(210, 8, self._txt("Strategic Simulation Engine"), align="C")

        # Divider
        self.set_draw_color(*DELFOS_GOLD)
        self.set_line_width(0.4)
        self.line(80, 178, 130, 178)

        self.set_font(self.font_family, "", 11)
        self.set_text_color(*DELFOS_LIGHT)
        self.set_xy(0, 188)
        self.cell(210, 8, "delfos.intelinetworks.com", align="C")

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.set_font(self.font_family, "", 9)
        self.set_text_color(*DELFOS_MUTED)
        self.set_xy(0, 202)
        self.cell(210, 6, self._txt(f"Generated: {ts}"), align="C")


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def generate_pdf(report: Report) -> bytes:
    """Generate a branded PDF from a Report object. Returns PDF bytes.

    Handles reports with missing outline, empty sections, or no content.
    """
    title = ""
    if report.outline and report.outline.title:
        title = report.outline.title

    pdf = DelfosPDF(report_id=report.report_id or "", title=title)
    pdf.cover_page(report)
    pdf.content_pages(report)
    pdf.back_page()

    out = pdf.output(dest="S")
    # fpdf2 >=2.5 returns bytearray; older versions may return str.
    if isinstance(out, str):
        return out.encode("latin-1")
    return bytes(out)
