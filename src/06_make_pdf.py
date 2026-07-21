"""Convert writeup/paper.md into a working-paper style PDF with embedded,
numbered figures. Run: python src/06_make_pdf.py"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Image as RLImage, HRFlowable)

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "writeup" / "paper.md"
FIGS = ROOT / "figures"
OUT = ROOT / "writeup" / "paper.pdf"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

pdfmetrics.registerFont(TTFont("PaperSerif", FONT_DIR / "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("PaperSerif-Bold", FONT_DIR / "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("PaperSerif-Italic", FONT_DIR / "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("PaperMono", FONT_DIR / "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily(
    "PaperSerif", normal="PaperSerif", bold="PaperSerif-Bold",
    italic="PaperSerif-Italic", boldItalic="PaperSerif-Bold",
)

# Figure placement: insert after the paragraph that first cites each figure
FIGURES = {
    "Figure 1": ("fig1_representation.png",
                 "Figure 1: AI usage share vs employment share by SOC major group."),
    "Figure 2": ("fig2_frontline_tasks.png",
                 "Figure 2: Top frontline (sales/admin/service) tasks by usage share."),
    "Figure 3": ("fig3_wage_gradient.png",
                 "Figure 3: Occupation-level usage share vs median wage."),
    "Figure 4": ("fig4_temporal.png",
                 "Figure 4: Representation index, Feb 2025 vs Aug 2025."),
    "Figure 5": ("fig5_automation_share.png",
                 "Figure 5: Automation-style share of conversations by group."),
    "Figure 6": ("fig6_exposure_2026.png",
                 "Figure 6: Observed AI exposure by occupation, Feb 2026."),
}


def md_inline(text: str) -> str:
    for source, replacement in {
        "\u2014": "--", "\u2013": "-", "\u2011": "-", "\u2192": " to ",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00d7": "x",
    }.items():
        text = text.replace(source, replacement)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<font face='PaperMono' size='8.5'>\1</font>", text)
    return text


def build() -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle("Body", parent=styles["Normal"], fontName="PaperSerif",
                          fontSize=10, leading=13.0, alignment=TA_JUSTIFY,
                          spaceAfter=7, allowWidows=0, allowOrphans=0)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="PaperSerif-Bold",
                        fontSize=13,
                        spaceBefore=14, spaceAfter=7, keepWithNext=1)
    title_st = ParagraphStyle("T", parent=styles["Title"], fontName="PaperSerif-Bold",
                              fontSize=16,
                              leading=20, spaceAfter=4)
    meta = ParagraphStyle("M", parent=styles["Normal"], fontName="PaperSerif",
                          fontSize=9.5,
                          alignment=TA_CENTER, spaceAfter=3)
    cap = ParagraphStyle("Cap", parent=styles["Normal"], fontName="PaperSerif-Italic",
                         fontSize=8.5,
                         alignment=TA_CENTER, spaceBefore=2, spaceAfter=10,
                         textColor="#444444")
    ref = ParagraphStyle("Ref", parent=body, fontSize=9, leading=11.5,
                         leftIndent=14, firstLineIndent=-14, spaceAfter=4,
                         alignment=TA_LEFT)

    lines = MD.read_text().splitlines()
    story, placed = [], set()
    in_refs = False

    for i, raw in enumerate(lines):
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("# "):  # main title
            story.append(Paragraph(md_inline(line[2:]), title_st))
            continue
        if line.startswith("## "):
            head = line[3:]
            in_refs = head.lower().startswith("references")
            story.append(Paragraph(md_inline(head), h1))
            continue
        if ((i < 6 and line.startswith("**") and "working paper" in line.lower())
                or line.startswith("Code and data:")):
            story.append(Paragraph(md_inline(line), meta))
            if line.startswith("Code"):
                story.append(HRFlowable(width="100%", thickness=0.6,
                                        spaceBefore=6, spaceAfter=10))
            continue
        if line.startswith("|"):  # markdown table -> monospace row
            story.append(Paragraph(
                f"<font face='PaperMono' size='8'>{md_inline(line)}</font>", body))
            continue
        story.append(Paragraph(md_inline(line), ref if in_refs else body))

        # place figures right after the paragraph that first mentions them
        for tag, (fname, caption) in FIGURES.items():
            if tag in line and tag not in placed and (FIGS / fname).exists():
                placed.add(tag)
                img = RLImage(str(FIGS / fname))
                scale = min(6.0 * inch / img.imageWidth, 3.6 * inch / img.imageHeight)
                img.drawWidth, img.drawHeight = (img.imageWidth * scale,
                                                 img.imageHeight * scale)
                story.append(Spacer(1, 6))
                story.append(img)
                story.append(Paragraph(caption, cap))

    doc = SimpleDocTemplate(str(OUT), pagesize=letter,
                            leftMargin=1 * inch, rightMargin=1 * inch,
                            topMargin=0.9 * inch, bottomMargin=0.9 * inch,
                            title="The Frontline Exposure Gap",
                            author="Sriramkrishnan Nandhakumar")
    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("PaperSerif", 8)
        canvas.setFillColor("#555555")
        canvas.drawCentredString(letter[0] / 2, 0.45 * inch, str(doc_obj.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF written: {OUT}")


if __name__ == "__main__":
    build()
