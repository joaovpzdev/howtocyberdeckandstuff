import math
import os

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homelab_fase5_no_ia_desenho_tecnico.pdf")
S = 1 / 3

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))


c = canvas.Canvas(OUT, pagesize=landscape(A3))
c.setTitle("Homelab - fase 5: nó de IA")
c.setAuthor("João Victor Paixão Zolim")


def P(v):
    return v * mm


def rect(x, y, w, h, lw=0.5, dash=None, fill=None, r=0):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    if fill is not None:
        c.setFillGray(fill)
    if r:
        c.roundRect(P(x), P(y), P(w), P(h), P(r), stroke=1, fill=1 if fill is not None else 0)
    else:
        c.rect(P(x), P(y), P(w), P(h), stroke=1, fill=1 if fill is not None else 0)
    c.setFillGray(0)
    c.setDash()


def line(x1, y1, x2, y2, lw=0.35, dash=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    c.line(P(x1), P(y1), P(x2), P(y2))
    c.setDash()


def text(x, y, s, size=7, anchor="l", bold=False):
    c.setFont("DVB" if bold else "DV", size)
    fn = {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[anchor]
    fn(P(x), P(y), s)


def arrowhead(x, y, ang_deg, size=1.6):
    a = math.radians(ang_deg)
    p = c.beginPath()
    p.moveTo(P(x), P(y))
    for d in (155, -155):
        b = a + math.radians(d)
        p.lineTo(P(x + size * math.cos(b)), P(y + size * math.sin(b)))
    p.close()
    c.setLineWidth(0.2)
    c.drawPath(p, stroke=1, fill=1)


def arrow(x1, y1, x2, y2, lw=0.4, dash=None):
    line(x1, y1, x2, y2, lw, dash)
    arrowhead(x2, y2, math.degrees(math.atan2(y2 - y1, x2 - x1)))


def dim_h(x1, x2, y, label, ext_from=None):
    if ext_from is not None:
        off = 1 if y > ext_from else -1
        line(x1, ext_from, x1, y + off * 1.5, 0.2)
        line(x2, ext_from, x2, y + off * 1.5, 0.2)
    line(x1, y, x2, y, 0.25)
    arrowhead(x1, y, 180)
    arrowhead(x2, y, 0)
    text((x1 + x2) / 2, y + 1, label, 6.2, "c")


def dim_v(x, y1, y2, label, ext_from=None, side="l"):
    if ext_from is not None:
        off = 1 if x > ext_from else -1
        line(ext_from, y1, x + off * 1.5, y1, 0.2)
        line(ext_from, y2, x + off * 1.5, y2, 0.2)
    line(x, y1, x, y2, 0.25)
    arrowhead(x, y1, 270)
    arrowhead(x, y2, 90)
    c.saveState()
    c.translate(P(x - 1 if side == "l" else x + 3.2), P((y1 + y2) / 2))
    c.rotate(90)
    c.setFont("DV", 6.2)
    c.drawCentredString(0, 0, label)
    c.restoreState()


def balloon(x, y, n, r=2.3):
    c.setLineWidth(0.4)
    c.setFillGray(1)
    c.circle(P(x), P(y), P(r), stroke=1, fill=1)
    c.setFillGray(0)
    text(x, y - 0.9, str(n), 5.6, "c", bold=True)


def box(x, y, w, h, title, sub=None, fill=0.93, dash=None, ts=7, ss_=5.8):
    rect(x, y, w, h, 0.5, dash=dash, fill=fill)
    if sub:
        text(x + w / 2, y + h / 2 + 0.8, title, ts, "c", bold=True)
        text(x + w / 2, y + h / 2 - 3.4, sub, ss_, "c")
    else:
        text(x + w / 2, y + h / 2 - 1.2, title, ts, "c", bold=True)


def table(x, y, rows, cols, width, size=6.1, rh=5.0):
    for r, row in enumerate(rows):
        yy = y - 4 - r * rh
        if r == 0:
            rect(x, yy - 1.6, width, rh, 0.3, fill=0.88)
        else:
            line(x, yy - 1.6, x + width, yy - 1.6, 0.2)
        for k, val in enumerate(row):
            anchor = "r" if isinstance(cols[k], tuple) else "l"
            cx = cols[k][0] if anchor == "r" else cols[k]
            text(x + (cx - 1.5 if anchor == "r" else cx + 1.5), yy, str(val), size, anchor, bold=(r == 0))
    rect(x, y - 4 - (len(rows) - 1) * rh - 1.6, width, len(rows) * rh, 0.4)
    return y - 4 - (len(rows) - 1) * rh - 1.6


def frame_and_title(sheet, title2, scale):
    rect(10, 10, 400, 277, 0.8)
    rect(15, 15, 390, 267, 0.4)
    x0, y0, w, h = 255, 15, 150, 42
    rect(x0, y0, w, h, 0.6)
    for yy in (30, 20, 10):
        line(x0, y0 + yy, x0 + w, y0 + yy, 0.4)
    line(x0 + 75, y0, x0 + 75, y0 + 20, 0.4)
    line(x0 + 112, y0, x0 + 112, y0 + 20, 0.4)
    text(x0 + 2, y0 + 36, "HOMELAB TINY - FASE 5: NÓ DE IA", 8.6, bold=True)
    text(x0 + 2, y0 + 32, title2, 6.3)
    text(x0 + 2, y0 + 26, "Autor: João Victor Paixão Zolim", 6.3)
    text(x0 + 2, y0 + 22, "github.com/joaovpzdev", 6.3)
    for (xx, a, b) in ((2, "Data", "21/10/2026 - rev. A"), (77, "Escala", scale), (114, "Folha", f"{sheet}/2")):
        text(x0 + xx, y0 + 16, a, 5.3)
        text(x0 + xx, y0 + 12, b, 6.8)
    for (xx, a, b) in ((2, "Unidade", "mm"), (77, "Projeção", "1º diedro"), (114, "Formato", "A3")):
        text(x0 + xx, y0 + 6, a, 5.3)
        text(x0 + xx, y0 + 2, b, 6.8)




def circ(x, y, r, lw=0.3, fill=None, dash=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    if fill is not None:
        c.setFillGray(fill)
    c.circle(P(x), P(y), P(r), stroke=1, fill=1 if fill is not None else 0)
    c.setFillGray(0)
    c.setDash()


def hatch(x, y, w, h, step=1.6, lw=0.15):
    c.saveState()
    p = c.beginPath()
    p.rect(P(x), P(y), P(w), P(h))
    c.clipPath(p, stroke=0, fill=0)
    c.setLineWidth(lw)
    k = -h
    while k < w:
        c.line(P(x + k), P(y), P(x + k + h), P(y + h))
        k += step
    c.restoreState()


def notes(x, y, title, items, size=5.6, gap=4.4):
    text(x, y, title, 7.5, bold=True)
    for i, n in enumerate(items):
        text(x, y - 6 - i * gap, n, size)


# ---------------- parâmetros (mm) ----------------
RACK_W, RACK_D, RACK_H = 280, 260, 406
U = 44.45
FRAME_TB = (RACK_H - 8 * U) / 2
TINY = (179, 183, 34.5)
PES = 10
MOD = (160, 260, 210)          # módulo GPU em perfil 2020 (L x P x A)
GAP = 50                       # vão entre rack e módulo
SFX = (125, 100, 63.5)
GPU = (242, 125, 42)           # RTX 3060 12 GB dual-fan típica (C x A x espessura)
DOCK_H = 15

# ============================ FOLHA 1 ============================
frame_and_title(1, "Montagem: nó 5 no topo do rack e módulo GPU OCuLink", "1:3 / S/E")
S = 1 / 3

# ---- vista frontal ----
rx, ry = 34, 112
rw, rh = RACK_W * S, RACK_H * S
rect(rx, ry, rw, rh, 0.8)
rect(rx + 4, ry + FRAME_TB * S, rw - 8, 8 * U * S, 0.3, fill=0.97)
ocup = ["switch TL-SG108E", "nó 1 monitoramento", "nó 2 dados + rádio", "nó 3 lab",
        "nó 4 sensor 32 GB", "base de encaixe", "4 fontes 65 W", "régua -> nobreak"]
for i, lab in enumerate(ocup):
    top = ry + rh - FRAME_TB * S - i * U * S
    line(rx + 4, top - U * S, rx + rw - 4, top - U * S, 0.2)
    rect(rx + 8, top - U * S + 2.2, rw - 16, U * S - 4.4, 0.3, fill=0.82 if 1 <= i <= 4 else 0.9)
    text(rx + 10, top - U * S / 2 - 1, f"U{i + 1}", 4.6, bold=True)
    text(rx + 18, top - U * S / 2 - 1, lab, 4.4)
# nó 5 no topo
n5x = rx + (RACK_W - TINY[0]) / 2 * S
n5y = ry + rh + PES * S
for fx in (n5x + 3, n5x + TINY[0] * S - 6):
    rect(fx, ry + rh, 3, PES * S, 0.3, fill=0.5)
rect(n5x, n5y, TINY[0] * S, TINY[2] * S, 0.7, fill=0.7, r=0.8)
text(n5x + TINY[0] * S / 2, n5y + TINY[2] * S / 2 - 1.2, "NÓ 5 - M720q (IA)", 5.6, "c", bold=True)
balloon(n5x - 4, n5y + TINY[2] * S / 2, 1, r=1.9)
balloon(n5x + TINY[0] * S + 4, ry + rh + 1.6, 2, r=1.7)
# módulo GPU
mx = rx + rw + GAP * S
mw, mh = MOD[0] * S, MOD[2] * S
rect(mx, ry, mw, mh, 0.7)
for xx in (mx, mx + mw - 20 * S):
    rect(xx, ry, 20 * S, mh, 0.3, fill=0.75)
rect(mx, ry + mh - 20 * S, mw, 20 * S, 0.3, fill=0.75)
rect(mx, ry, mw, 20 * S, 0.3, fill=0.75)
psx = mx + (MOD[0] - SFX[0]) / 2 * S
rect(psx, ry + 20 * S, SFX[0] * S, SFX[2] * S, 0.5, fill=0.6)
text(psx + SFX[0] * S / 2, ry + 20 * S + SFX[2] * S / 2 - 1.2, "fonte SFX", 4.8, "c", bold=True)
dy = ry + (20 + SFX[2]) * S
rect(psx, dy, SFX[0] * S, DOCK_H * S, 0.4, fill=0.4)
gx = mx + (MOD[0] / 2 - GPU[2] / 2) * S
rect(gx, dy + DOCK_H * S, GPU[2] * S, GPU[1] * S, 0.6, fill=0.82)
c.saveState()
c.translate(P(gx + GPU[2] * S / 2 + 1), P(dy + DOCK_H * S + GPU[1] * S / 2))
c.rotate(90)
c.setFont("DVB", 4.8)
c.drawCentredString(0, 0, "RTX 3060 12 GB")
c.restoreState()
balloon(psx - 2.5, ry + 20 * S + SFX[2] * S / 2, 5, r=1.7)
balloon(psx - 2.5, dy + DOCK_H * S / 2, 4, r=1.7)
balloon(gx + GPU[2] * S + 4, dy + DOCK_H * S + GPU[1] * S - 4, 6, r=1.7)
balloon(mx + mw - 2, ry + mh + 3, 7, r=1.7)
# fluxo de ar
arrow(mx + mw + 12, dy + 30, mx + mw + 1, dy + 30, 0.5)
text(mx + mw + 2, dy + 32, "ar entra", 4.4)
arrow(gx + GPU[2] * S / 2, ry + mh - 2, gx + GPU[2] * S / 2, ry + mh + 9, 0.5)
text(gx + GPU[2] * S / 2 + 2, ry + mh + 6, "ar sai", 4.4)
# cabo OCuLink
c.setLineWidth(0.7)
c.setDash(2, 1.2)
p = c.beginPath()
p.moveTo(P(n5x + TINY[0] * S), P(n5y + 3))
p.curveTo(P(mx + 8), P(n5y + 6), P(mx - 6), P(dy + 20), P(psx + 6), P(dy + DOCK_H * S / 2 + 1))
c.drawPath(p, stroke=1, fill=0)
c.setDash()
balloon(mx - 6, n5y - 8, 3, r=1.7)
text(mx - 3, n5y - 3, "OCuLink 50 cm", 4.6)
# energia
line(psx + SFX[0] * S / 2, ry, psx + SFX[0] * S / 2, ry - 7, 0.4, dash=(1.5, 1))
text(psx + SFX[0] * S / 2 + 1, ry - 6.5, "tomada c/ DPS", 4.4)
# cotas
dim_v(rx - 6, ry, ry + rh, "406", ext_from=rx)
dim_v(rx - 6, ry + rh, n5y + TINY[2] * S, "~45", ext_from=n5x)
dim_h(rx, rx + rw, ry - 12, "280", ext_from=ry)
dim_h(rx + rw, mx, ry - 12, "50")
dim_h(mx, mx + mw, ry - 12, "160", ext_from=ry)
dim_v(mx + mw + 18, ry, ry + mh, "210", ext_from=mx + mw, side="r")
text(rx, ry - 21, "VISTA FRONTAL (1:3)", 7.4, bold=True)
text(rx, ry - 25.5, "rack 8U sem alteração; nó 5 sobre pés impressos no tampo", 5.2)

# ---- vista lateral do módulo (lado das ventoinhas) ----
lx, ly = 212, 182
lw_, lh = MOD[1] * S, MOD[2] * S
rect(lx, ly, lw_, lh, 0.7)
for xx in (lx, lx + lw_ - 20 * S):
    rect(xx, ly, 20 * S, lh, 0.3, fill=0.75)
rect(lx, ly, lw_, 20 * S, 0.3, fill=0.75)
rect(lx, ly + lh - 20 * S, lw_, 20 * S, 0.3, fill=0.75)
rect(lx + lw_ - (20 + SFX[1]) * S, ly + 20 * S, SFX[1] * S, SFX[2] * S, 0.5, fill=0.6)
text(lx + lw_ - (20 + SFX[1] / 2) * S, ly + 20 * S + SFX[2] * S / 2 - 1.2, "SFX", 4.8, "c", bold=True)
rect(lx + 20 * S, ly + (20 + SFX[2]) * S, (MOD[1] - 40) * S, DOCK_H * S, 0.4, fill=0.4)
text(lx + 24 * S, ly + 20 * S + SFX[2] * S - 3, "porta OCuLink", 4.2)
gy0 = ly + (20 + SFX[2] + DOCK_H) * S
gx0 = lx + (MOD[1] - GPU[0]) / 2 * S
rect(gx0, gy0, GPU[0] * S, GPU[1] * S, 0.6, fill=0.85)
for fx in (0.28, 0.72):
    circ(gx0 + GPU[0] * S * fx, gy0 + GPU[1] * S / 2, 14, 0.4, fill=0.95)
    circ(gx0 + GPU[0] * S * fx, gy0 + GPU[1] * S / 2, 4, 0.3, fill=0.7)
rect(gx0 + GPU[0] * S - 1.5, gy0 - 2, 1.5, GPU[1] * S + 6, 0.4, fill=0.3)
text(gx0 + GPU[0] * S + 1, gy0 + GPU[1] * S + 2.5, "suporte traseiro", 4.2)
dim_h(lx, lx + lw_, ly - 6, "260 (= profundidade do rack)", ext_from=ly)
dim_h(gx0, gx0 + GPU[0] * S, ly + lh + 5, "~242 (placa)", ext_from=gy0 + GPU[1] * S)
text(lx, ly - 13, "VISTA LATERAL DIREITA DO MÓDULO (1:3)", 7.4, bold=True)
text(lx, ly + lh + 12, "FRENTE <-", 4.8, bold=True)
text(lx + lw_, ly + lh + 12, "-> TRÁS", 4.8, "r", bold=True)

# ---- esquema interno do nó 5 ----
ex, ey = 212, 92
text(ex, ey + 68, "ESQUEMA DO NÓ 5 (sem escala)", 7.4, bold=True)
rect(ex, ey, 105, 62, 0.7, r=2)
box(ex + 4, ey + 44, 30, 13, "i5-8500T", "6 núcleos, VT-d", ts=6, ss_=4.8)
box(ex + 38, ey + 44, 30, 13, "RAM 2x16 GB", "DDR4 SODIMM", ts=6, ss_=4.8)
box(ex + 72, ey + 44, 29, 13, "Rede 1 GbE", "VLAN 20 (lab)", ts=6, ss_=4.8)
box(ex + 4, ey + 24, 44, 14, "Slot M.2 NVMe", "-> adaptador OCuLink", ts=6, ss_=4.8)
box(ex + 54, ey + 24, 47, 14, "SSD SATA 2,5\" 1 TB", "boot + modelos", ts=6, ss_=4.8)
box(ex + 4, ey + 5, 44, 13, "Abertura do slot PCIe", "saída do cabo", ts=5.6, ss_=4.8, dash=(1.5, 1), fill=1)
box(ex + 54, ey + 5, 47, 13, "Fonte 65 W", "igual aos nós 1-3", ts=6, ss_=4.8)
arrow(ex + 26, ey + 24, ex + 26, ey + 18, 0.5)
arrow(ex + 26, ey + 5, ex + 26, ey - 3, 0.5)
text(ex + 28, ey - 3, "cabo OCuLink ao módulo GPU", 4.4)
balloon(ex + 50.5, ey + 31, 8, r=1.6)
balloon(ex + 101 - 1.5, ey + 31 + 6, 9, r=1.6)

# ---- planta ----
px, py = 34, 24
pS = 1 / 6
rect(px, py, RACK_W * pS, RACK_D * pS, 0.7, fill=0.9)
text(px + RACK_W * pS / 2, py + RACK_D * pS / 2 - 1, "rack 8U", 5.4, "c", bold=True)
mpx = px + (RACK_W + GAP) * pS
rect(mpx, py, MOD[0] * pS, MOD[1] * pS, 0.7, fill=0.8)
text(mpx + MOD[0] * pS / 2, py + MOD[1] * pS / 2 - 1, "módulo GPU", 5.2, "c", bold=True)
line(px - 3, py + RACK_D * pS + 20 * pS, mpx + MOD[0] * pS + 30 * pS, py + RACK_D * pS + 20 * pS, 0.8)
text(px, py + RACK_D * pS + 20 * pS + 1.5, "parede (>= 100 mm livres atrás)", 4.6)
arrow(mpx + MOD[0] * pS + 14, py + 26, mpx + MOD[0] * pS + 1, py + 26, 0.5)
text(mpx + MOD[0] * pS + 2, py + 28, ">= 80 mm livres", 4.4)
text(px + 125, py + 2, "PLANTA (1:6) - frente para baixo", 7.4, bold=True)

# ---- itens ----
rows = [("N", "Item", "Medidas ~ (mm)")]
spec = [
    (1, "Lenovo M720q i5-8500T - nó 5", "179 x 183 x 34,5"),
    (2, "4 pés impressos + trava no tampo", "ASA"),
    (3, "Adaptador M.2 -> OCuLink + cabo", "50 cm"),
    (4, "Dock eGPU OCuLink (PCIe x16 aberto)", "~130 x 100"),
    (5, "Fonte SFX 600 W 80+ Gold", "125 x 100 x 63,5"),
    (6, "RTX 3060 12 GB (usada)", "~242 x 125 x 42"),
    (7, "Quadro em perfil de alumínio 2020", "160 x 260 x 210"),
    (8, "SSD SATA 2,5\" 1 TB", "100 x 70 x 7"),
    (9, "2 x 16 GB DDR4 SODIMM", "-"),
]
rows += [(str(a), b, d) for a, b, d in spec]
text(330, 222, "ITENS (balões)", 7.5, bold=True)
table(330, 220, rows, [0, 6, 52], 75, size=5.0, rh=4.4)

notes(330, 272, "NOTAS", [
    "1. Nó 5 igual aos outros: mesma",
    "   fonte, peças de reposição e cluster.",
    "2. O M.2 NVMe vira OCuLink (PCIe 3.0",
    "   x4); o boot vai para o SSD SATA.",
    "3. Para IA a banda x4 basta: o modelo",
    "   carrega uma vez e roda na placa.",
    "4. Ligue a GPU ANTES do nó 5.",
    "5. Módulo fora do nobreak (DPS).",
    "6. Medidas da placa variam por marca.",
], size=5.4, gap=4.1)
notes(330, 168, "ALTERNATIVA DENTRO DO NÓ", [
    "Placa low profile no riser PCIe do",
    "M720q (ex.: RTX A1000 8 GB, 50 W):",
    "sem módulo externo, mas só 8 GB e",
    "fonte de 135 W. Conferir antes.",
], size=5.4, gap=4.1)

c.showPage()

# ============================ FOLHA 2 ============================
frame_and_title(2, "Software, integrações, energia e materiais", "S/E")

text(25, 272, "SERVIÇOS E INTEGRAÇÕES (VLAN 20, ACESSO SÓ PELO TAILSCALE)", 8, bold=True)
rect(25, 205, 98, 60, 0.7, r=2)
text(74, 259, "NÓ 5 - Proxmox (cluster)", 7, "c", bold=True)
rect(29, 209, 90, 44, 0.4, fill=0.95, r=1.5)
text(74, 248, "LXC \"ia\" com a GPU (driver NVIDIA no host)", 5.4, "c")
for i, (t_, s_) in enumerate([("Ollama", "API de modelos :11434"), ("Open WebUI", "chat + documentos :3000"),
                              ("faster-whisper", "transcrição de áudio")]):
    box(33, 233 - i * 11.5, 82, 9.5, t_, s_, ts=5.8, ss_=4.6)
others = [(150, 250, "Nó 1: Wazuh, Grafana", "alertas e painéis"),
          (150, 232, "Nó 2: Node-RED, Kiwix, MQTT", "automação e biblioteca"),
          (150, 214, "Nó 4: Security Onion", "alertas de rede"),
          (205, 250, "Kit / cyberdeck", "via Tailscale"),
          (205, 232, "Gravações do SDR", "áudio de rádio, campo"),
          (205, 214, "Telegram/ntfy local", "avisos resumidos")]
for x, y, t_, s_ in others:
    box(x, y, 48, 12, t_, s_, ts=5.4, ss_=4.6)
for y in (256, 238, 220):
    arrow(150, y, 123, y if y != 256 else 245, 0.4)
text(126, 262, "eventos -> resumo", 4.6)

text(25, 196, "CASOS DE USO", 8, bold=True)
uso = [("Uso", "Fluxo", "Modelo (12 GB)"),
       ("Triagem de alertas", "Wazuh/SO -> Node-RED -> Ollama -> resumo no Grafana", "7-8B instruct"),
       ("Assistente do lab", "Open WebUI com os PDFs do repo, manuais, RFCs", "7-14B + embeddings"),
       ("Biblioteca offline", "Perguntas sobre o Kiwix e documentos locais (RAG)", "7-8B + embeddings"),
       ("Transcrição", "Áudio do SDR e de campo -> texto pesquisável", "Whisper small/medium"),
       ("Estudos", "Writeups do Bandit, Packet Tracer, revisão de código", "7-14B code"),
       ("Relatório SAR", "Log do Meshtastic -> rascunho do relatório", "7-8B instruct")]
table(25, 192, uso, [0, 30, (210,)], 210, size=5.4, rh=4.8)
text(25, 155, "Tudo local: nenhum alerta, log ou posição sai de casa (LGPD).", 5.6, bold=True)

text(262, 272, "ENERGIA E CUSTO (ESTIMADOS)", 8, bold=True)
en = [("Estado", "RTX 3060", "RTX 3090"),
      ("Ocioso (nó + GPU + fonte)", "~25-30 W", "~35-40 W"),
      ("Gerando texto", "~200 W", "~390 W"),
      ("Por mês, 24/7 + 2 h/dia de uso", "~R$ 30", "~R$ 45")]
table(262, 268, en, [0, (105,), (140,)], 140, size=5.6, rh=4.8)
for i, n in enumerate(["Tarifa considerada ~R$ 1,00/kWh (SP, com impostos).",
                       "O nobreak de 600-700 VA (~360 W) não aguenta a GPU:",
                       "módulo e nó 5 ficam na tomada com DPS. Opcional: nobreak",
                       "de 1.200 VA para colocar tudo protegido."]):
    text(262, 245 - i * 4.4, n, 5.4)

text(262, 222, "ESCOLHA DA PLACA (USADAS)", 8, bold=True)
gp = [("Placa", "VRAM", "Modelos (Q4)", "TDP"),
      ("RTX 3060 12 GB", "12 GB", "até ~14B", "170 W"),
      ("RTX 4060 Ti 16 GB", "16 GB", "até ~20B", "165 W"),
      ("RTX 3090 24 GB", "24 GB", "até ~32B", "350 W"),
      ("2 x MI50 (como no vídeo)", "2 x 32 GB", "70B+", "2 x 300 W")]
table(262, 218, gp, [0, 45, 75, (140,)], 140, size=5.6, rh=4.8)
for i, n in enumerate(["NVIDIA: CUDA funciona direto no Ollama, sem gambiarra.",
                       "MI50: barata por GB, mas sem suporte oficial no ROCm",
                       "atual e precisa de fonte e ventilação de servidor."]):
    text(262, 189 - i * 4.4, n, 5.4)

bom = [
    ("Lenovo M720q i5-8500T usado (nó 5)", 1000),
    ("2 x 16 GB DDR4 SODIMM", 450),
    ("SSD SATA 2,5\" 1 TB", 350),
    ("Adaptador M.2 NVMe -> OCuLink + cabo 50 cm", 150),
    ("Dock eGPU OCuLink", 450),
    ("Fonte SFX 600 W 80+ Gold", 600),
    ("RTX 3060 12 GB usada", 1400),
    ("Perfil 2020, cantoneiras, pés e trava impressos", 180),
    ("Régua com DPS para o módulo", 80),
]
opc = [("RTX 3090 24 GB no lugar da 3060 (diferença; fonte 850 W)", 3800),
       ("Nobreak 1.200 VA", 900)]
tot = sum(v for _, v in bom)


def brl(v):
    return f"{v:,.0f}".replace(",", ".")


rows = [("It.", "Descrição", "R$ (estim.)")]
rows += [(str(i + 1), d, f"~{brl(v)}") for i, (d, v) in enumerate(bom)]
rows += [("", "Total fase 5 (RTX 3060)", f"~{brl(tot)}")]
rows += [(str(len(bom) + i + 1), d + " (opcional)", f"~{brl(v)}") for i, (d, v) in enumerate(opc)]
text(25, 145, "LISTA DE MATERIAIS", 8, bold=True)
table(25, 141, rows, [0, 9, (210,)], 210, size=5.6, rh=4.7)

notes(262, 170, "ORDEM DE INSTALAÇÃO", [
    "1. Nó 5 no topo do rack; Proxmox e entrada no cluster.",
    "2. BIOS: VT-d ligado; SSD SATA como boot.",
    "3. Montar o módulo: quadro 2020, SFX, dock e GPU.",
    "4. Adaptador no M.2, cabo pela abertura do slot PCIe.",
    "5. Ligar GPU e depois o nó; conferir: lspci | grep NVIDIA.",
    "6. Driver NVIDIA no host; GPU no LXC \"ia\".",
    "7. Docker no LXC: Ollama, Open WebUI, faster-whisper.",
    "8. Node-RED: fluxo de triagem dos alertas do Wazuh.",
    "9. Teste de 1 h gerando texto: temperatura e consumo.",
    "",
    "Preços estimados, out/2026; usados variam muito.",
], size=5.5, gap=4.4)

c.showPage()
c.save()
print("ok", OUT, tot)
