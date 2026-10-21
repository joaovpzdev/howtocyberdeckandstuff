import math
import os

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homelab_rack_gpu_5_placas_desenho_tecnico.pdf")
S = 1 / 3

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))


c = canvas.Canvas(OUT, pagesize=landscape(A3))
c.setTitle("Homelab - rack de GPU em alumínio para 5 placas")
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
    text(x0 + 2, y0 + 36, "HOMELAB - RACK DE GPU 2020 + HOST EPYC", 8.6, bold=True)
    text(x0 + 2, y0 + 32, title2, 6.3)
    text(x0 + 2, y0 + 26, "Autor: João Victor Paixão Zolim", 6.3)
    text(x0 + 2, y0 + 22, "github.com/joaovpzdev", 6.3)
    for (xx, a, b) in ((2, "Data", "21/10/2026 - rev. B"), (77, "Escala", scale), (114, "Folha", f"{sheet}/2")):
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
W, D, H = 480, 440, 400        # quadro externo em perfil 2020
PR = 20
Z_MID = 200
Z_PLATE = 223
PITCH = 80
N = 5
X0 = (W - N * PITCH) / 2
GPU_T, GPU_T3 = 42, 61
GPU_L, GPU_H = 300, 125
RISER_H = 15
FAN = 120
# placa-mãe ROMED8-2T (ATX 305 x 244) deitada, borda traseira (I/O) no fundo
MB_W, MB_D = 305, 244
MB_X = (W - MB_W) / 2
MB_Y = D - PR - MB_D           # encostada atrás
MB_Z = PR + 10                 # sobre espaçadores na chapa de baixo
PSU = (200, 150, 86)           # ATX 1600 W deitada (L x P x A)
PSU_X, PSU_Y = W - PR - PSU[0], PR
COOL = (95, 120, 125)          # cooler SP3 com ventoinha 92 mm
COOL_X, COOL_Y = MB_X + 175, MB_Y + 70
SLOT_X = [MB_X + 20 + k * 20.32 for k in range(7)]   # 7 slots x16 (esquema)
SLOT_Y0, SLOT_L = D - PR - 95, 89

S = 1 / 4


def quadro(x, y, w, h):
    rect(x, y, w * S, h * S, 0.8)
    for xx in (0, w - PR):
        rect(x + xx * S, y, PR * S, h * S, 0.3, fill=0.7)
    for zz in (0, Z_MID, H - PR):
        rect(x + PR * S, y + zz * S, (w - 2 * PR) * S, PR * S, 0.3, fill=0.7)


# ============================ FOLHA 1 ============================
frame_and_title(1, "Quadro 2020 com host EPYC no nível de baixo: vistas", "1:4 / 1:5")

# ---- vista frontal ----
fx, fy = 32, 168
quadro(fx, fy, W, H)
rect(fx + PR * S, fy + (Z_MID + PR) * S, (W - 2 * PR) * S, 3 * S, 0.3, fill=0.3)
for i in range(N):
    cx = X0 + PITCH * (i + 0.5)
    rect(fx + (cx - 30) * S, fy + Z_PLATE * S, 60 * S, RISER_H * S, 0.3, fill=0.45)
    rect(fx + (cx - GPU_T / 2) * S, fy + (Z_PLATE + RISER_H) * S, GPU_T * S, GPU_H * S, 0.5, fill=0.82)
    rect(fx + (cx - GPU_T3 / 2) * S, fy + (Z_PLATE + RISER_H) * S, GPU_T3 * S, (GPU_H + 13) * S, 0.25, dash=(1, 0.8))
    text(fx + cx * S, fy + (Z_PLATE + RISER_H + GPU_H / 2) * S - 1, f"G{i + 1}", 5.6, "c", bold=True)
for k in range(3):
    circ(fx + (W / 2 + (k - 1) * 135) * S, fy + (Z_PLATE + 78) * S, FAN / 2 * S, 0.3, dash=(1.5, 1))
# nível de baixo (vista de frente)
rect(fx + MB_X * S, fy + MB_Z * S, MB_W * S, 3 * S, 0.3, fill=0.3)
rect(fx + COOL_X * S, fy + (MB_Z + 3) * S, COOL[0] * S, COOL[2] * S, 0.45, fill=0.75, dash=(1.5, 1))
text(fx + (COOL_X + COOL[0] / 2) * S, fy + (MB_Z + 3 + COOL[2]) * S + 1, "cooler", 4.2, "c")
rect(fx + PSU_X * S, fy + PR * S, PSU[0] * S, PSU[2] * S, 0.5, fill=0.62)
text(fx + (PSU_X + PSU[0] / 2) * S, fy + (PR + PSU[2] / 2) * S - 1, "ATX 1600 W", 4.4, "c", bold=True)
circ(fx + 100 * S, fy + 105 * S, 60 * S, 0.4)
circ(fx + 100 * S, fy + 105 * S, 15 * S, 0.3, fill=0.7)
circ(fx + 360 * S, fy + 150 * S, 40 * S, 0.4)
circ(fx + 360 * S, fy + 150 * S, 10 * S, 0.3, fill=0.7)
balloon(fx + 100 * S, fy + 175 * S, 8, r=1.5)
balloon(fx + PSU_X * S - 2, fy + 60 * S, 6, r=1.5)
balloon(fx + (X0 + PITCH * 0.5) * S, fy + (Z_PLATE + RISER_H + GPU_H) * S + 4, 4, r=1.6)
balloon(fx + (W - PR / 2) * S, fy + (H + 12) * S, 1, r=1.6)
dim_h(fx, fx + W * S, fy - 6, "480", ext_from=fy)
dim_v(fx - 6, fy, fy + H * S, "400", ext_from=fx)
dim_h(fx + X0 * S, fx + (X0 + PITCH) * S, fy + H * S + 5, "80", ext_from=fy + (Z_PLATE + RISER_H + GPU_H) * S)
dim_v(fx + W * S + 10, fy + Z_PLATE * S, fy + (H - PR) * S, "157 livre", ext_from=fx + W * S, side="r")
dim_v(fx + W * S + 10, fy + PR * S, fy + Z_MID * S, "180", ext_from=fx + W * S, side="r")
text(fx, fy - 15, "VISTA FRONTAL (1:4) - entradas de ar 120 e 80 mm no nível de baixo", 7, bold=True)

# ---- vista lateral ----
lx, ly = 182, 168
quadro(lx, ly, D, H)
rect(lx + PR * S, ly + (Z_MID + PR) * S, (D - 2 * PR) * S, 3 * S, 0.3, fill=0.3)
gy0 = D - PR - GPU_L
rect(lx + gy0 * S, ly + (Z_PLATE + RISER_H) * S, GPU_L * S, GPU_H * S, 0.5, fill=0.85)
for fxr in (0.3, 0.7):
    circ(lx + (gy0 + GPU_L * fxr) * S, ly + (Z_PLATE + RISER_H + GPU_H / 2) * S, 11, 0.3, fill=0.95)
rect(lx + (D - PR - 95) * S, ly + Z_PLATE * S, 85 * S, RISER_H * S, 0.3, fill=0.45)
rect(lx + (D - PR - 2) * S, ly + (Z_PLATE + RISER_H - 5) * S, 2 * S + 0.5, (GPU_H + 10) * S, 0.4, fill=0.2)
rect(lx + (D - PR) * S, ly + 340 * S, PR * S, PR * S, 0.4, fill=0.5)
rect(lx + PR * S, ly + (Z_PLATE + 18) * S, 25 * S, FAN * S, 0.4, fill=0.6)
balloon(lx + PR * S + 2, ly + (Z_PLATE + 18 + FAN) * S + 3, 5, r=1.6)
# baixo: placa, cooler, fonte, riser
rect(lx + MB_Y * S, ly + MB_Z * S, MB_D * S, 3 * S, 0.4, fill=0.3)
rect(lx + COOL_Y * S, ly + (MB_Z + 3) * S, COOL[1] * S, COOL[2] * S, 0.45, fill=0.75)
text(lx + (COOL_Y + COOL[1] / 2) * S, ly + (MB_Z + 60) * S, "cooler", 4.4, "c")
rect(lx + PSU_Y * S, ly + PR * S, PSU[1] * S, PSU[2] * S, 0.45, fill=0.62)
text(lx + (PSU_Y + PSU[1] / 2) * S, ly + (PR + 43) * S - 1, "fonte", 4.4, "c")
rect(lx + (SLOT_Y0) * S, ly + (MB_Z + 3) * S, SLOT_L * S, 11 * S, 0.3, fill=0.2)
c.setLineWidth(0.6)
c.setDash(2, 1)
p = c.beginPath()
p.moveTo(P(lx + (SLOT_Y0 + 20) * S), P(ly + (MB_Z + 14) * S))
p.curveTo(P(lx + (SLOT_Y0 - 30) * S), P(ly + 120 * S), P(lx + (SLOT_Y0 + 10) * S), P(ly + 190 * S),
          P(lx + (D - PR - 60) * S), P(ly + Z_PLATE * S))
c.drawPath(p, stroke=1, fill=0)
c.setDash()
balloon(lx + (SLOT_Y0 - 22) * S, ly + 150 * S, 9, r=1.5)
balloon(lx + MB_Y * S + 2, ly + (MB_Z + 12) * S, 7, r=1.5)
text(lx + (D - PR) * S + 1.5, ly + 60 * S, "I/O", 4.6, bold=True)
for zz in (260, 300, 340, 60, 120):
    arrow(lx + 50 * S, ly + zz * S, lx + 90 * S, ly + zz * S, 0.4)
arrow(lx + (D - 5) * S, ly + 300 * S, lx + (D + 30) * S, ly + 300 * S, 0.4)
arrow(lx + (D - 5) * S, ly + 100 * S, lx + (D + 30) * S, ly + 100 * S, 0.4)
text(lx + (D + 8) * S, ly + 304 * S, "ar sai", 4.4)
dim_h(lx, lx + D * S, ly - 6, "440", ext_from=ly)
dim_h(lx + MB_Y * S, lx + (D - PR) * S, ly + H * S + 5, "244 (placa)", ext_from=ly + MB_Z * S)
text(lx, ly - 15, "VISTA LATERAL DIREITA (1:4)", 7, bold=True)
text(lx, ly - 19.5, "FRENTE à esquerda; risers sobem do slot até a baia", 5)

# ---- planta do nível de cima (1:5) ----
S5 = 1 / 5
ux, uy = 32, 46
rect(ux, uy, W * S5, D * S5, 0.8)
rect(ux + PR * S5, uy + PR * S5, (W - 2 * PR) * S5, (D - 2 * PR) * S5, 0.25, fill=0.95)
for i in range(N):
    cx = X0 + PITCH * (i + 0.5)
    rect(ux + (cx - GPU_T / 2) * S5, uy + (D - PR - GPU_L) * S5, GPU_T * S5, GPU_L * S5, 0.45, fill=0.85)
    rect(ux + (cx - 30) * S5, uy + (D - PR - 95) * S5, 60 * S5, 20 * S5, 0.3, dash=(1, 0.7))
    text(ux + cx * S5, uy + D * S5 / 2 - 1, f"G{i + 1}", 5, "c", bold=True)
for k in range(3):
    rect(ux + (W / 2 + (k - 1) * 135 - FAN / 2) * S5, uy + PR * S5, FAN * S5, 25 * S5, 0.4, fill=0.6)
dim_h(ux, ux + W * S5, uy - 5, "480", ext_from=uy)
dim_v(ux - 5, uy, uy + D * S5, "440", ext_from=ux)
text(ux, uy - 13, "PLANTA - NÍVEL DE CIMA (1:5)", 7, bold=True)
text(ux, uy - 17.5, "tracejado: rasgo da chapa por onde sobe o riser", 4.8)
text(ux + W * S5 / 2, uy + D * S5 + 2, "TRÁS", 4.8, "c", bold=True)

# ---- planta do nível de baixo (1:5) ----
bx, by = 150, 46
rect(bx, by, W * S5, D * S5, 0.8)
rect(bx + PR * S5, by + PR * S5, (W - 2 * PR) * S5, (D - 2 * PR) * S5, 0.25, fill=0.95)
rect(bx + MB_X * S5, by + MB_Y * S5, MB_W * S5, MB_D * S5, 0.6, fill=0.82)
text(bx + (MB_X + 60) * S5, by + (MB_Y + 30) * S5, "ROMED8-2T", 4.6, bold=True)
for sx in SLOT_X:
    rect(bx + sx * S5, by + SLOT_Y0 * S5, 2.2, SLOT_L * S5, 0.25, fill=0.25)
rect(bx + (COOL_X - 30) * S5, by + (COOL_Y - 10) * S5, 6, COOL[1] * S5 + 4, 0.25, fill=0.6)
rect(bx + (COOL_X + COOL[0] + 5) * S5, by + (COOL_Y - 10) * S5, 6, COOL[1] * S5 + 4, 0.25, fill=0.6)
rect(bx + COOL_X * S5, by + COOL_Y * S5, COOL[0] * S5, COOL[1] * S5, 0.45, fill=0.7)
text(bx + (COOL_X + COOL[0] / 2) * S5, by + (COOL_Y + COOL[1] / 2) * S5 - 1, "CPU", 4.6, "c", bold=True)
rect(bx + PSU_X * S5, by + PSU_Y * S5, PSU[0] * S5, PSU[1] * S5, 0.5, fill=0.62)
text(bx + (PSU_X + PSU[0] / 2) * S5, by + (PSU_Y + PSU[1] / 2) * S5 - 1, "fonte", 4.6, "c", bold=True)
rect(bx + 40 * S5, by + PR * S5, FAN * S5, 25 * S5, 0.4, fill=0.5)
text(bx + MB_X * S5 + 1, by + (SLOT_Y0 - 12) * S5, "7 slots x16", 4.2)
text(bx + (COOL_X + COOL[0] + 16) * S5, by + (COOL_Y + 40) * S5, "RAM 8x", 4.2)
arrow(bx + 100 * S5, by + 60 * S5, bx + 100 * S5, by + 140 * S5, 0.35)
arrow(bx + (COOL_X + 47) * S5, by + (COOL_Y - 40) * S5, bx + (COOL_X + 47) * S5, by + (COOL_Y - 2) * S5, 0.35)
text(bx + W * S5 / 2, by + D * S5 + 2, "TRÁS (I/O, rede, BMC)", 4.8, "c", bold=True)
dim_h(bx + MB_X * S5, bx + (MB_X + MB_W) * S5, by - 5, "305", ext_from=by + MB_Y * S5)
text(bx, by - 13, "PLANTA - NÍVEL DE BAIXO (1:5)", 7, bold=True)
balloon(bx + MB_X * S5 - 2, by + (MB_Y + MB_D) * S5 - 2, 7, r=1.5)
balloon(bx + PSU_X * S5 - 2, by + (PSU_Y + PSU[1]) * S5 - 2, 6, r=1.5)

# ---- perfil ----
px, py = 262, 98
rect(px, py, 20, 20, 0.6, fill=0.85)
for (ax, ay, aw, ah) in ((7.6, 0, 4.8, 3), (7.6, 17, 4.8, 3), (0, 7.6, 3, 4.8), (17, 7.6, 3, 4.8)):
    rect(px + ax, py + ay, aw, ah, 0.3, fill=1)
circ(px + 10, py + 10, 2.1, 0.4, fill=1)
dim_h(px, px + 20, py - 4, "20")
text(px, py + 24, "PERFIL 2020 (1:1)", 6.4, bold=True)

# ---- itens ----
rows = [("N", "Item", "Qtd / medida")]
spec = [
    (1, "Perfil 2020 (verticais / largura / prof.)", "4x400 · 8x440 · 8x400"),
    (2, "Barra traseira dos suportes PCIe", "1 (no canal)"),
    (3, "Chapa do meio 3 mm, 5 rasgos", "440 x 400"),
    (4, "Baias de placa de vídeo, passo 80", "5"),
    (5, "Ventoinhas 120 mm, painel frontal de cima", "3"),
    (6, "Fonte ATX 3.1 1600 W Platinum", "200 x 150 x 86"),
    (7, "ASRock Rack ROMED8-2T + EPYC 7302P", "305 x 244"),
    (8, "Entradas de ar de baixo (120 + 80 mm)", "2"),
    (9, "Risers PCIe 4.0 x16 blindados, 30 cm", "5"),
]
rows += [(str(a), b, d) for a, b, d in spec]
text(318, 272, "ITENS", 7.5, bold=True)
table(318, 268, rows, [0, 6, (87,)], 87, size=4.9, rh=4.4)
text(318, 220, "Total de perfil: ~8,5 m.", 5.2, bold=True)
notes(318, 212, "NOTAS", [
    "1. Rev. B: o quadro ganhou 40 mm de",
    "   profundidade (440) para a placa-mãe",
    "   ATX e a fonte caberem lado a lado.",
    "2. Placa-mãe deitada, borda de I/O atrás:",
    "   slots no mesmo sentido das placas de",
    "   vídeo, risers sobem sem torcer.",
    "3. Cooler SP3 de até 125 mm (nível de",
    "   baixo tem 180 livres).",
    "4. Ar da frente para trás nos dois níveis.",
    "5. Placas de vídeo até 320 mm.",
    "6. Rede 10 GbE, BMC e USB ficam atrás.",
    "7. Peso com 5 placas: ~16-20 kg.",
], size=5.3, gap=4.0)

c.showPage()

# ============================ FOLHA 2 ============================
frame_and_title(2, "Host EPYC: especificação, PCIe, energia e materiais", "S/E")

text(25, 272, "HOST DEDICADO", 8, bold=True)
hw = [("Parte", "Escolha", "Por quê"),
      ("Placa-mãe", "ASRock Rack ROMED8-2T (ATX)", "7 slots PCIe 4.0 x16, BMC/IPMI, 2x 10 GbE, 2x M.2"),
      ("Processador", "AMD EPYC 7302P (16 núcleos, 155 W)", "128 pistas PCIe; 'P' = um soquete, mais barato"),
      ("Memória", "8 x 16 GB DDR4-3200 RDIMM ECC", "Um pente por canal (8 canais) = 128 GB"),
      ("Cooler", "Noctua NH-U9 TR4-SP3 (125 mm)", "Cabe no nível de baixo, ar frente -> trás"),
      ("Disco", "NVMe 2 TB PCIe 4.0", "Proxmox, VM e modelos"),
      ("Fonte", "ATX 3.1 1600 W 80+ Platinum", ">= 10 saídas PCIe 8 pinos ou 12V-2x6"),
      ("Placas de vídeo", "5 x RTX 3060 12 GB (depois 3090)", "60 GB de VRAM, CUDA direto")]
table(25, 268, hw, [0, 30, 95], 215, size=5.6, rh=5.0)

text(25, 218, "DIVISÃO DAS PLACAS", 8, bold=True)
dv = [("Baia", "Função", "Software"),
      ("G1-G4", "Modelo principal dividido em 4 placas", "vLLM (tensor parallel = 4)"),
      ("G5", "Transcrição, embeddings, modelos pequenos", "faster-whisper + Ollama")]
table(25, 214, dv, [0, 20, 120], 215, size=5.6, rh=5.0)
text(25, 195, "5 placas não dividem bem um modelo (as cabeças de atenção pedem 1, 2, 4 ou 8): por isso 4 + 1.", 5.5)

text(25, 186, "ENERGIA (PLACAS COM LIMITE: nvidia-smi -pl)", 8, bold=True)
en = [("Estado", "5 x 3060 @150 W", "5 x 3090 @220 W"),
      ("Desligado (só o BMC)", "~5 W", "~5 W"),
      ("Ligado, ocioso", "~140 W", "~170 W"),
      ("Gerando texto (todas)", "~950 W", "~1.300 W"),
      ("Mês 24/7 ocioso", "~R$ 100", "~R$ 125"),
      ("Mês sob demanda (4 h/dia)", "~R$ 50", "~R$ 65")]
table(25, 182, en, [0, 70, 115], 160, size=5.6, rh=4.8)
text(25, 147, "Tomada 20 A exclusiva com DPS; 5 x 3090 pedem circuito dedicado feito por eletricista.", 5.5, bold=True)

bom = [
    ("ASRock Rack ROMED8-2T (usada ou importada)", 3500),
    ("AMD EPYC 7302P usado SEM trava de fabricante (PSB)", 900),
    ("8 x 16 GB DDR4-3200 RDIMM ECC", 1300),
    ("Cooler Noctua NH-U9 TR4-SP3", 700),
    ("NVMe 2 TB PCIe 4.0", 900),
    ("Fonte ATX 3.1 1600 W Platinum", 2600),
    ("5 risers PCIe 4.0 x16 blindados, 30 cm", 900),
    ("Quadro 2020 rev. B + chapas + ventoinhas", 1500),
    ("Tomada 20 A dedicada com DPS (eletricista)", 400),
]
tot = sum(v for _, v in bom)
gpus3060, gpus3090 = 7000, 25000


def brl(v):
    return f"{v:,.0f}".replace(",", ".")


rows = [("It.", "Descrição", "R$ (estim.)")]
rows += [(str(i + 1), d, f"~{brl(v)}") for i, (d, v) in enumerate(bom)]
rows += [("", "Host + quadro (sem placas de vídeo)", f"~{brl(tot)}")]
rows += [("10", "5 x RTX 3060 12 GB usadas", f"~{brl(gpus3060)}")]
rows += [("", "Total com 5 x 3060", f"~{brl(tot + gpus3060)}")]
rows += [("", "Alternativa: 5 x RTX 3090 24 GB usadas", f"~{brl(gpus3090)}")]
text(25, 138, "LISTA DE MATERIAIS", 8, bold=True)
table(25, 134, rows, [0, 9, (215,)], 215, size=5.6, rh=4.7)

notes(255, 272, "CAMINHO DE COMPRA", [
    "1. Quadro + 1 placa no nó 5 (OCuLink), como na fase 5.",
    "2. Host: placa-mãe, CPU, RAM, cooler, NVMe e fonte.",
    "   A placa do nó 5 muda para a baia G1.",
    "3. Uma placa de vídeo por vez nas baias G2 a G5.",
    "4. Troca gradual de 3060 por 3090 (24 GB).",
], size=5.5, gap=4.4)
notes(255, 238, "ANTES DE COMPRAR", [
    "- EPYC usado: exigir 'sem PSB / unlocked'. CPU travada",
    "  num servidor Dell ou Lenovo pode não funcionar aqui.",
    "- Memória RDIMM (registrada). Pente comum não liga.",
    "- Risers PCIe 4.0; se der erro, fixar os slots em Gen3.",
    "- Fonte com cabos PCIe suficientes, sem adaptadores.",
], size=5.5, gap=4.4)
notes(255, 205, "IMPLEMENTAÇÃO", [
    "Passo a passo completo (BIOS, Proxmox, VM com 5",
    "placas, vLLM, monitoramento, liga/desliga pelo",
    "IPMI e testes) no guia: homelab_host_ia_epyc.pdf",
    "",
    "Preços estimados, out/2026; usados variam muito.",
], size=5.5, gap=4.4)

c.showPage()
c.save()
print("ok", OUT, tot)
