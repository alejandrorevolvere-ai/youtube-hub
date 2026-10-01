# -*- coding: utf-8 -*-
"""Genera 30-prompts-senal-abierta.pdf y contenido.md.

Uso: python build_pdf.py
"""
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from contenido_a import SECTIONS_A
from contenido_b import RECETAS, SECTIONS_B

HERE = Path(__file__).resolve().parent
PDF_OUT = HERE / "30-prompts-senal-abierta.pdf"
MD_OUT = HERE / "contenido.md"

SECTIONS = SECTIONS_A + SECTIONS_B
TOTAL = sum(len(s["prompts"]) for s in SECTIONS)

INK = "#0F172A"
ACCENT = "#D97706"
AMBER = "#F59E0B"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_pdf():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate,
                                    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

    ink = colors.HexColor(INK)
    accent = colors.HexColor(ACCENT)
    muted = colors.HexColor("#64748B")
    box = colors.HexColor("#F1F5F9")

    def cover(canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(ink)
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setFillColor(accent)
        canvas.rect(0, h - 0.55 * cm, w, 0.18 * cm, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.setFillColor(colors.HexColor(AMBER))
        canvas.drawString(2.2 * cm, h - 3.2 * cm, "SENAL ABIERTA")
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawRightString(w - 2.2 * cm, h - 3.2 * cm, "senalabierta.pages.dev")
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 32)
        canvas.drawString(2.2 * cm, h - 7.2 * cm, f"{TOTAL} prompts de IA")
        canvas.setFillColor(colors.HexColor(AMBER))
        canvas.drawString(2.2 * cm, h - 8.6 * cm, "para trabajar el doble")
        canvas.setFillColor(colors.white)
        canvas.drawString(2.2 * cm, h - 10.0 * cm, "en la mitad de tiempo")
        canvas.setFont("Helvetica", 12)
        canvas.setFillColor(colors.HexColor("#CBD5E1"))
        canvas.drawString(2.2 * cm, h - 12.4 * cm,
                          "Los prompts exactos de los tips del canal, listos para copiar y pegar.")
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.HexColor("#64748B"))
        y = 5.6 * cm
        for line in [
            "Productividad · Carrera · Copy · Imagenes",
            "Presentaciones · Codigo · Recetas bonus",
            "",
            "Edicion 1 · Octubre 2026",
            "Uso personal: copialos, mezclalos, adaptalos. No revendas el pack.",
        ]:
            canvas.drawString(2.2 * cm, y, line)
            y -= 0.55 * cm
        canvas.restoreState()

    def later(canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setStrokeColor(colors.HexColor("#E2E8F0"))
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, h - 1.5 * cm, w - 2 * cm, h - 1.5 * cm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(2 * cm, h - 1.25 * cm, "SENAL ABIERTA")
        canvas.drawRightString(w - 2 * cm, h - 1.25 * cm, "senalabierta.pages.dev")
        canvas.line(2 * cm, 1.5 * cm, w - 2 * cm, 1.5 * cm)
        canvas.drawString(2 * cm, 1.05 * cm, f"{TOTAL} prompts de IA")
        canvas.drawRightString(w - 2 * cm, 1.05 * cm, f"Pagina {doc.page - 1}")
        canvas.restoreState()

    doc = BaseDocTemplate(str(PDF_OUT), pagesize=A4,
                          leftMargin=2 * cm, rightMargin=2 * cm,
                          topMargin=2.2 * cm, bottomMargin=2 * cm,
                          title=f"{TOTAL} prompts de IA - Senal Abierta",
                          author="Senal Abierta", subject="Pack de prompts")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="body", frames=[frame], onPage=later),
    ])

    ss = getSampleStyleSheet()
    h_sec = ParagraphStyle("h_sec", parent=ss["Heading1"], fontName="Helvetica-Bold",
                           fontSize=17, textColor=ink, spaceBefore=14, spaceAfter=4, leading=21)
    p_intro = ParagraphStyle("p_intro", parent=ss["Normal"], fontSize=9.5,
                             textColor=muted, spaceAfter=10, leading=13)
    p_title = ParagraphStyle("p_title", parent=ss["Heading3"], fontName="Helvetica-Bold",
                             fontSize=11.5, textColor=ink, spaceBefore=8, spaceAfter=2, leading=14)
    p_meta = ParagraphStyle("p_meta", parent=ss["Normal"], fontSize=8.5,
                            textColor=muted, spaceAfter=3, leading=11)
    p_when = ParagraphStyle("p_when", parent=ss["Normal"], fontSize=9.5,
                            textColor=colors.HexColor("#334155"), spaceAfter=4, leading=12)
    p_prompt = ParagraphStyle("p_prompt", parent=ss["Normal"], fontName="Courier",
                              fontSize=8.6, textColor=ink, leading=12.4,
                              spaceBefore=4, spaceAfter=4)
    p_small = ParagraphStyle("p_small", parent=ss["Normal"], fontSize=8.8,
                             textColor=colors.HexColor("#475569"), leading=11.5, spaceAfter=2)
    p_h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold",
                          fontSize=15, textColor=ink, spaceBefore=6, spaceAfter=6)
    p_toc = ParagraphStyle("p_toc", parent=ss["Normal"], fontSize=10, leading=17, textColor=ink)

    story = [NextPageTemplate("body"), PageBreak()]

    story.append(Paragraph("Contenido", p_h2))
    story.append(Spacer(1, 4))
    n = 1
    for s in SECTIONS:
        rng = f"{n}-{n + len(s['prompts']) - 1}"
        story.append(Paragraph(
            f"<b>{rng}.</b> {esc(s['title'])} <font color='#64748B'>({len(s['prompts'])} prompts)</font>",
            p_toc))
        n += len(s["prompts"])
    story.append(Paragraph("<b>Bonus.</b> 3 recetas de video sin prompt", p_toc))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Como usar este pack:</b> cada prompt tiene variables entre corchetes "
        "([METAS], [TEMA]...). Sustitúyelas por tu caso real. Cuanto más específico seas, "
        "mejor el resultado. Si la respuesta no te convence, añade una linea de correccion "
        "('mas corto', 'sin hype', 'mas datos') en lugar de empezar de cero.",
        p_when))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Todos estos prompts salieron de los tips diarios del canal. "
        "Cada ficha enlaza a su video original en senalabierta.pages.dev.",
        p_meta))

    for s in SECTIONS:
        story.append(PageBreak())
        story.append(Paragraph(esc(s["title"]), h_sec))
        story.append(Paragraph(esc(s["intro"]), p_intro))
        for p in s["prompts"]:
            block = [Paragraph(esc(p["title"]), p_title)]
            meta = f"Herramienta: <b>{esc(p['tool'])}</b>"
            if p.get("source"):
                if p.get("url"):
                    meta += f" · Origen: <a href='{p['url']}' color='{ACCENT}'>{esc(p['source'])}</a>"
                else:
                    meta += f" · Origen: {esc(p['source'])}"
            block.append(Paragraph(meta, p_meta))
            block.append(Paragraph(f"<b>Cuando:</b> {esc(p['when'])}", p_when))
            prompt_tbl = Table(
                [[Paragraph(esc(p["text"]).replace("\n", "<br/>"), p_prompt)]],
                colWidths=[doc.width])
            prompt_tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), box),
                ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            block.append(prompt_tbl)
            block.append(Spacer(1, 3))
            block.append(Paragraph(f"<b>Variables:</b> {esc(p['vars'])}", p_small))
            if p.get("truco"):
                block.append(Paragraph(f"<b>Truco:</b> {esc(p['truco'])}", p_small))
            block.append(Spacer(1, 8))
            story.append(KeepTogether(block))

    story.append(PageBreak())
    story.append(Paragraph("Bonus: 3 recetas de video (sin prompt que copiar)", h_sec))
    story.append(Paragraph(
        "Tres tips del canal que son flujos en la app, no texto: se explican en 60 segundos.",
        p_intro))
    for r in RECETAS:
        story.append(KeepTogether([
            Paragraph(esc(r["title"]), p_title),
            Paragraph(f"Origen: <a href='{r['url']}' color='{ACCENT}'>{esc(r['source'])}</a>", p_meta),
            Paragraph(esc(r["steps"]), p_when),
            Spacer(1, 8),
        ]))

    story.append(Spacer(1, 16))
    cierre = Table([[Paragraph(
        "<b>¿Te ahorro tiempo este pack?</b><br/>"
        "Invitame a un cafe: ko-fi.com/alejandrorevolvere · "
        "Newsletter semanal: buttondown.com/revolvere · "
        "Todos los tips: senalabierta.pages.dev<br/>"
        f"<font size=7.5 color='#64748B'>Cada prompt corresponde a un tip publicado en el canal. "
        f"Edicion 1 · Octubre 2026 · {TOTAL} prompts.</font>",
        ParagraphStyle("cierre", parent=ss["Normal"], fontSize=9.5, leading=14,
                       textColor=ink, alignment=1))]],
        colWidths=[doc.width])
    cierre.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7ED")),
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(cierre)

    doc.build(story)
    print(f"PDF: {PDF_OUT}")


def build_md():
    lines = [f"# {TOTAL} prompts de IA — Señal Abierta (fuente editable)", "",
             "Regenerar el PDF: `python build_pdf.py`", ""]
    n = 1
    for s in SECTIONS:
        lines.append(f"## {s['title']}")
        lines.append(f"_{s['intro']}_")
        lines.append("")
        for p in s["prompts"]:
            src = f" — [{p['source']}]({p['url']})" if p.get("url") else f" — {p['source']}"
            lines.append(f"### {n}. {p['title']}")
            lines.append(f"- Herramienta: {p['tool']}{src}")
            lines.append(f"- Cuándo: {p['when']}")
            lines.append(f"- Variables: {p['vars']}")
            if p.get("truco"):
                lines.append(f"- Truco: {p['truco']}")
            lines.append("")
            lines.append("```")
            lines.append(p["text"])
            lines.append("```")
            lines.append("")
            n += 1
    lines.append("## Bonus: 3 recetas de vídeo")
    lines.append("")
    for r in RECETAS:
        lines.append(f"### {r['title']} — [{r['source']}]({r['url']})")
        lines.append("")
        lines.append(r["steps"])
        lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"MD: {MD_OUT}")


if __name__ == "__main__":
    assert TOTAL == 30, f"Se esperaban 30 prompts, hay {TOTAL}"
    build_pdf()
    build_md()
    print(f"OK: {TOTAL} prompts + {len(RECETAS)} recetas")
