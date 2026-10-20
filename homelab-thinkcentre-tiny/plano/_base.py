import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(BASE, "homelab_plano_observacao.pdf")

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", F + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

INK = colors.HexColor("#1F2A33")
ACC = colors.HexColor("#1F6F8B")   # azul homelab
MUTED = colors.HexColor("#5B6770")
LINE = colors.HexColor("#C9D1D6")
TINT = colors.HexColor("#F3F5F6")

ss = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.6, leading=14, textColor=INK, spaceAfter=6),
    "small": ParagraphStyle("small", fontName="DV", fontSize=8, leading=11, textColor=MUTED),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, textColor=INK, spaceBefore=4, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=ACC, spaceBefore=10, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.4, leading=11, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.4, leading=11, textColor=INK),
    "title": ParagraphStyle("title", fontName="DVB", fontSize=28, leading=33, textColor=INK),
    "subtitle": ParagraphStyle("subtitle", fontName="DV", fontSize=13, leading=18, textColor=MUTED),
    "callout": ParagraphStyle("callout", fontName="DV", fontSize=9.4, leading=13.5, textColor=INK),
    "caption": ParagraphStyle("caption", fontName="DVI", fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER),
}


def P(t, s="body"):
    return Paragraph(t, ss[s])


def bullets(items):
    return ListFlowable([ListItem(P(i), leftIndent=10, value="•") for i in items],
                        bulletType="bullet", start="•", leftIndent=12, bulletFontName="DV",
                        bulletColor=ACC, spaceAfter=6)


def numbered(items):
    return ListFlowable([ListItem(P(i), leftIndent=14) for i in items], bulletType="1",
                        leftIndent=16, bulletFontName="DVB", bulletColor=ACC, spaceAfter=6)


def table(rows, widths, header=True):
    data = [[Paragraph(str(c), ss["cellb" if (header and r == 0) else "cell"]) for c in row]
            for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), TINT))
    t.setStyle(TableStyle(st))
    return t


def callout(text):
    t = Table([[Paragraph(text, ss["callout"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINT),
                           ("LINEBEFORE", (0, 0), (0, -1), 2.5, ACC),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("DV", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, 12 * mm, "Homelab – plano de monitoramento e observação global  ·  rev. D  ·  out/2026")
        canvas.drawRightString(190 * mm, 12 * mm, f"{doc.page}")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    else:
        canvas.setFillColor(ACC)
        canvas.rect(0, 0, 8 * mm, A4[1], stroke=0, fill=1)
    canvas.restoreState()


