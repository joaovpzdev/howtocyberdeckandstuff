import math
import os
import sys

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelo3d"))
import cyberdeck_3d as M  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cyberdeck_sar_5k_desenho_tecnico.pdf")
c = canvas.Canvas(OUT, pagesize=landscape(A3))
c.setTitle("Cyberdeck SAR - Edição R$ 5 mil")
c.setAuthor("João Victor Paixão Zolim")
SHEETS = 4


def P(v):
    return v * mm


def rect(x, y, w, h, lw=0.5, dash=None, fill=None, r=0):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    if fill is not None:
        c.setFillGray(fill)
    f = 1 if fill is not None else 0
    if r:
        c.roundRect(P(x), P(y), P(w), P(h), P(r), stroke=1, fill=f)
    else:
        c.rect(P(x), P(y), P(w), P(h), stroke=1, fill=f)
    c.setFillGray(0)
    c.setDash()


def line(x1, y1, x2, y2, lw=0.35, dash=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    c.line(P(x1), P(y1), P(x2), P(y2))
    c.setDash()


def circle(x, y, r, lw=0.4, fill=None, dash=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    if fill is not None:
        c.setFillGray(fill)
    c.circle(P(x), P(y), P(r), stroke=1, fill=1 if fill is not None else 0)
    c.setFillGray(0)
    c.setDash()


def text(x, y, s, size=7, anchor="l", bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[anchor](P(x), P(y), s)


def arrowhead(x, y, ang, size=1.6):
    a = math.radians(ang)
    p = c.beginPath()
    p.moveTo(P(x), P(y))
    for d in (155, -155):
        b = a + math.radians(d)
        p.lineTo(P(x + size * math.cos(b)), P(y + size * math.sin(b)))
    p.close()
    c.setLineWidth(0.2)
    c.drawPath(p, stroke=1, fill=1)


def arrow(x1, y1, x2, y2, lw=0.4, dash=None, size=1.6):
    line(x1, y1, x2, y2, lw, dash)
    arrowhead(x2, y2, math.degrees(math.atan2(y2 - y1, x2 - x1)), size)


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
    c.setFont("Helvetica", 6.2)
    c.drawCentredString(0, 0, label)
    c.restoreState()


def balloon(x, y, n, tx=None, ty=None):
    if tx is not None:
        line(x, y, tx, ty, 0.25)
        circle(tx, ty, 0.6, 0.2, fill=0)
    circle(x, y, 2.6, 0.4, fill=1)
    text(x, y - 1.1, str(n), 6, "c", bold=True)


def table(x, y, rows, cols, width, size=6.2, rh=5.0):
    for r_, row in enumerate(rows):
        yy = y - 5 - r_ * rh
        if r_ == 0:
            rect(x, yy - 1.6, width, rh, 0.3, fill=0.88)
        else:
            line(x, yy - 1.6, x + width, yy - 1.6, 0.2)
        for k, val in enumerate(row):
            text(x + 1.5 + cols[k], yy, val, size, bold=(r_ == 0))
    rect(x, y - 5 - (len(rows) - 1) * rh - 1.6, width, len(rows) * rh, 0.4)
    return y - 5 - len(rows) * rh


def frame(sheet, subtitle, scale):
    rect(10, 10, 400, 277, 0.8)
    rect(15, 15, 390, 267, 0.4)
    x0, y0, w = 255, 15, 150
    rect(x0, y0, w, 42, 0.6)
    for yy in (10, 20, 30):
        line(x0, y0 + yy, x0 + w, y0 + yy, 0.4)
    line(x0 + 75, y0, x0 + 75, y0 + 20, 0.4)
    line(x0 + 112, y0, x0 + 112, y0 + 20, 0.4)
    text(x0 + 2, y0 + 36, "CYBERDECK SAR - EDIÇÃO R$ 5 MIL", 9, bold=True)
    text(x0 + 2, y0 + 32, subtitle, 6.2)
    text(x0 + 2, y0 + 26, "Autor: João Victor Paixão Zolim", 6.5)
    text(x0 + 2, y0 + 22, "github.com/joaovpzdev", 6.5)
    for xx, lab, val in ((2, "Data", "17/10/2026"), (77, "Escala", scale), (114, "Folha", f"{sheet}/{SHEETS}")):
        text(x0 + xx, y0 + 16, lab, 5.5)
        text(x0 + xx, y0 + 12, val, 7)
    for xx, lab, val in ((2, "Unidade", "mm"), (77, "Projeção", "1º diedro"), (114, "Formato", "A3")):
        text(x0 + xx, y0 + 6, lab, 5.5)
        text(x0 + xx, y0 + 2, val, 7)


# ========================= FOLHA 1: CASE =========================
frame(1, "Patola MP-0039: vistas fechado e aberto em operação", "1:4")
S = 0.25
EXT = (420, 365, 150)
INT = (390, 315, 135)
LID, BASE = 40, 95
WALL = (EXT[2] - INT[2]) / 2

# Vista frontal fechada
fx, fy = 40, 200
w, h = EXT[0] * S, EXT[2] * S
base_h = (BASE + WALL) * S
rect(fx, fy, w, base_h, 0.7, r=2)
rect(fx, fy + base_h, w, h - base_h, 0.7, r=2)
for lx in (0.2, 0.5, 0.8):
    rect(fx + w * lx - 5, fy + base_h - 3, 10, 6, 0.4, fill=0.75)
rect(fx + w / 2 - 14, fy + h, 28, 4, 0.5, fill=0.85)
text(fx + w / 2, fy + h + 5.5, "ALÇA", 5.3, "c")
dim_h(fx, fx + w, fy - 6, "420", ext_from=fy)
dim_v(fx - 6, fy, fy + h, "150", ext_from=fx)
text(fx + w / 2, fy - 13, "VISTA FRONTAL - FECHADO (IP67)", 7.5, "c", bold=True)

# Vista lateral fechada
sx = 175
sw = EXT[1] * S
rect(sx, fy, sw, base_h, 0.7, r=2)
rect(sx, fy + base_h, sw, h - base_h, 0.7, r=2)
circle(sx + sw - 4, fy + base_h + 1, 2, 0.4)
text(sx + sw - 4, fy + base_h + 5, "DOBRADIÇA", 5, "c")
dim_h(sx, sx + sw, fy - 6, "365", ext_from=fy)
text(sx + sw / 2, fy - 13, "VISTA LATERAL ESQUERDA - FECHADO", 7.5, "c", bold=True)

# Vista lateral em operação (tampa aberta ~100°)
ox, oy = 40, 70
bw = EXT[1] * S
bh = (BASE + WALL) * S
rect(ox, oy, bw, bh, 0.7, r=2)
hx, hy = ox + bw, oy + bh
ang = math.radians(100)
lid_len = EXT[1] * S
lid_thk = (LID + WALL) * S
p1 = (hx, hy)
p2 = (hx + lid_len * math.cos(ang), hy + lid_len * math.sin(ang))
nx, ny = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
p3 = (p2[0] + lid_thk * nx, p2[1] + lid_thk * ny)
p4 = (p1[0] + lid_thk * nx, p1[1] + lid_thk * ny)
for a, b in ((p1, p2), (p2, p3), (p3, p4), (p4, p1)):
    line(a[0], a[1], b[0], b[1], 0.7)
# tela na tampa
t0 = 0.27
t1 = 0.73
q1 = (p1[0] + (p2[0] - p1[0]) * t0 - nx * 1.2, p1[1] + (p2[1] - p1[1]) * t0 - ny * 1.2)
q2 = (p1[0] + (p2[0] - p1[0]) * t1 - nx * 1.2, p1[1] + (p2[1] - p1[1]) * t1 - ny * 1.2)
line(q1[0], q1[1], q2[0], q2[1], 1.6)
text(q2[0] - 18, (q1[1] + q2[1]) / 2 + 12, "TELA 7\"", 6, "r", bold=True)
line(q2[0] - 17, (q1[1] + q2[1]) / 2 + 12.8, (q1[0] + q2[0]) / 2 - 1, (q1[1] + q2[1]) / 2, 0.25)
# painel e antenas
deck_y = oy + (M.DECK_Z + M.DECK_T) * S * 0.9
line(ox + 2, deck_y, ox + bw - 2, deck_y, 0.6)
for k, ax in enumerate((0.15, 0.3, 0.45)):
    line(ox + bw * ax, deck_y, ox + bw * ax - 6 + k * 3, deck_y + 32, 0.6)
text(ox + bw * 0.15 - 8, deck_y + 34, "ANTENAS", 5.5, "c")
arrow(ox + bw * 0.6, deck_y + 14, ox + bw * 0.6, deck_y + 2, 0.4)
text(ox + bw * 0.6, deck_y + 16, "AR ENTRA", 5.3, "c")
arrow(ox + bw * 0.85, deck_y + 2, ox + bw * 0.85, deck_y + 14, 0.4)
text(ox + bw * 0.85, deck_y + 16, "AR SAI", 5.3, "c")
dim_v(ox - 6, oy, oy + bh, "~103 base", ext_from=ox)
text(ox + bw / 2 + 10, oy - 13, "VISTA LATERAL - ABERTO EM OPERAÇÃO", 7.5, "c", bold=True)

# Tabela do case
cx0 = 175
yq = table(cx0, 140, [
    ("Característica", "Patola MP-0039 (fabricado no Brasil)"),
    ("Externo (C x L x A)", "420 x 365 x 150"),
    ("Interno (C x L x A)", "390 x 315 x 135"),
    ("Altura interna da base / tampa", "95 / ~40"),
    ("Peso vazio", "1,96 kg"),
    ("Vedação", "IP67 (impacto, poeira e água)"),
    ("Volume interno", "16,6 litros"),
    ("Compra", "Patola Store (loja oficial)"),
    ("Preço (out/2026)", "R$ 486 (MP-0039/1: R$ 440)"),
], [0, 50], 120)
text(cx0, yq - 3, "Sem furos no case: a vedação IP67 fica intacta para transporte.", 6.3)
text(cx0, yq - 8, "Em operação, o kit trabalha aberto e a ventilação é feita pelo painel.", 6.3)

# Notas de clima
nx0 = 300
text(nx0, 272, "PROTEÇÃO PARA CLIMA HOSTIL", 8.5, bold=True)
notas = [
    "1. Fechado: IP67 (poeira e submersão temporária).",
    "2. Aberto: operar sob abrigo; chuva direta molha",
    "   a tela e o painel. Prever capa/toldo.",
    "3. Filtro de espuma na entrada de ar contra poeira.",
    "4. Verniz conformal (tropicalização) nas placas",
    "   contra umidade e maresia.",
    "5. Sachês de sílica gel no case fechado.",
    "6. Peças impressas em ASA ou PETG: PLA deforma",
    "   acima de ~55 °C (sol, carro fechado).",
    "7. Li-ion: carregar só entre 0 e 45 °C; no calor",
    "   extremo, deixar a tampa aberta e à sombra.",
    "8. Pi 5 reduz o clock a ~85 °C: monitorar via",
    "   vcgencmd / agente Zabbix.",
    "9. Recarga sem desmontar: USB-C do painel (tampa",
    "   aberta) -> UPS (power bank opcional). Sem furos.",
]
for i, n in enumerate(notas):
    text(nx0, 265 - i * 4.6, n, 6.2)

# ========================= FOLHA 2: LAYOUT INTERNO =========================
c.showPage()
frame(2, "Layout interno da bandeja, fluxo de ar e corte A-A", "1:2")
S2 = 0.5
X0, Y0 = 30, 135


def T(x, y):
    return X0 + x * S2, Y0 + y * S2


# bandeja
rect(X0, Y0, M.CH_W * S2, M.CH_D * S2, 0.7, r=M.CORNER_R * S2)
line(X0 + M.SPLIT_X * S2, Y0 - 3, X0 + M.SPLIT_X * S2, Y0 + M.CH_D * S2 + 3, 0.3, dash=([6, 2, 1, 2],))
text(X0 + M.SPLIT_X * S2, Y0 + M.CH_D * S2 + 4, "EMENDA", 5.3, "c")
for px, py in M.PILLARS:
    x, y = T(px - 5, py - 5)
    rect(x, y, 5, 5, 0.4, fill=0.6)
# pilha
xa, ya = T(M.PI_ORIGIN[0] + 42.5 - 48.7, M.PI_ORIGIN[1] + 28 - 42.5)
rect(xa, ya, 97.4 * S2, 85 * S2, 0.6, fill=0.9)
xp, yp = T(*M.PI_ORIGIN)
rect(xp, yp, 85 * S2, 56 * S2, 0.4, dash=(1.5, 1))
for hx_, hy_ in M.PI_HOLES:
    circle(*T(M.PI_ORIGIN[0] + hx_, M.PI_ORIGIN[1] + hy_), 1.2, 0.3)
# ventoinhas (projeção do painel)
circle(*T(*M.FAN_IN), M.FAN / 2 * S2, 0.4, dash=(2, 1.2))
circle(*T(*M.FAN_OUT), M.FAN / 2 * S2, 0.4, dash=(2, 1.2))
# dispositivos USB
for name, x0_, y0_, L, W in M.USB_DEVICES:
    x, y = T(x0_, y0_)
    rect(x, y, L * S2, W * S2, 0.5, fill=0.92)
    text(x + L * S2 / 2, y + W * S2 / 2 - 1, name, 5.3, "c")
# porta-antenas
tx0, ty0, tx1, ty1 = M.TROUGH
x, y = T(tx0, ty0)
rect(x, y, (tx1 - tx0) * S2, (ty1 - ty0) * S2, 0.4)
for k in (15, 30):
    line(x, y + k * S2, x + (tx1 - tx0) * S2, y + k * S2, 0.3)
text(x + (tx1 - tx0) * S2 / 2, y + (ty1 - ty0) * S2 / 2 - 1, "PORTA-ANTENAS (3 CANAIS)", 5.5, "c")
# compartimento do power bank
pbx, pby = M.PB_ORIGIN
pbl, pbw, pbh = M.PB_IN
bx_, by_ = T(pbx - M.PB_WALL, pby - M.PB_WALL)
rect(bx_, by_, (pbl + 2 * M.PB_WALL) * S2, (pbw + 2 * M.PB_WALL) * S2, 0.5)
bx_, by_ = T(pbx, pby)
rect(bx_, by_, pbl * S2, pbw * S2, 0.4, fill=0.9)
text(bx_ + pbl * S2 / 2, by_ + pbw * S2 / 2 + 1, "POWER BANK USB-C PD", 5.5, "c", bold=True)
text(bx_ + pbl * S2 / 2, by_ + pbw * S2 / 2 - 3.5, f"até {pbl - 2:.0f} x {pbw - 2:.0f} x {pbh} mm", 5, "c")
for sx_ in M.PB_STRAP_X:
    for ty_ in (pby - M.PB_WALL - 4, pby + pbw + M.PB_WALL):
        a_, b_ = T(sx_ - 13, ty_)
        rect(a_, b_, 26 * S2, 4 * S2, 0.4, fill=0.6)
# fluxo de ar
ax1, ay1 = T(M.FAN_IN[0] + 40, M.FAN_IN[1] + 50)
ax2, ay2 = T(M.FAN_OUT[0] - 40, M.FAN_OUT[1] + 30)
arrow(ax1, ay1, ax2, ay2, 0.5, dash=(3, 1.5), size=2)
text((ax1 + ax2) / 2, (ay1 + ay2) / 2 + 3, "FLUXO DE AR", 5.5, "c", bold=True)
# cotas
dim_h(X0, X0 + M.CH_W * S2, Y0 - 7, "360", ext_from=Y0)
dim_v(X0 - 7, Y0, Y0 + M.CH_D * S2, "250", ext_from=X0)
text(X0 + M.CH_W * S2 / 2, Y0 - 15, "VISTA SUPERIOR - BANDEJA (PAINEL REMOVIDO)", 7.5, "c", bold=True)
text(X0, Y0 - 21, "Folga para o interno de 390 x 315 travada por 6 calços impressos. Tracejado = projeção das ventoinhas.", 6)

# balões
items = [
    (1, M.PI_ORIGIN[0] + 10, M.PI_ORIGIN[1] + 50, "Pilha: UPS X1202 + Pi 5 8 GB + HAT RAK6421 (standoffs M2.5 x 24)"),
    (2, *M.FAN_IN, "Ventoinha de entrada 60 x 15 mm, 5 V (no painel)"),
    (3, *M.FAN_OUT, "Ventoinha de exaustão 60 x 15 mm, 5 V (no painel)"),
    (4, 241, 78, "Berço de expansão (RTL-SDR, fase futura)"),
    (5, 247, 116, "Berço de expansão (Wi-Fi MT7612U, fase futura)"),
    (6, 252, 155, "Berço de expansão (modem 4G, fase futura)"),
    (7, 255, 195, "Berço de expansão (SSD USB, fase futura)"),
    (8, 100, 32, "Porta-antenas: 3 canais de ~13 mm"),
    (9, 12, 125, "Pilar 10 x 10 com furo M3 (12 un.)"),
    (10, 150, 112, "Passagem de cabos no piso"),
    (11, 40, 200, "Compartimento do power bank (opcional) + orelhas para velcro"),
]
for n, ix, iy, _ in items:
    bx, by = T(ix, iy)
    balloon(bx + 6, by + 6, n, bx, by)
yl = table(220, 272, [("Nº", "Descrição")] + [(str(n), d) for n, _, _, d in items], [0, 8], 120, size=6)

# Corte A-A
CX, CY = 225, 120
S3 = 0.5
INTD, INTH = 315, 135


def C(y, z):
    return CX + y * S3, CY + z * S3


rect(CX, CY, INTD * S3, INTH * S3, 0.4, dash=(3, 1.5))
line(*C(0, 95), *C(INTD, 95), 0.6)
text(*C(INTD + 2, 96), "BORDA", 5)
off = (INTD - M.CH_D) / 2
rect(*C(off, 0), M.CH_D * S3, M.FLOOR_T * S3, 0.4, fill=0.6)
rect(*C(off, M.DECK_Z), M.CH_D * S3, M.DECK_T * S3, 0.4, fill=0.6)
for py_ in (12, 238):
    rect(*C(off + py_ - 5, M.FLOOR_T), 10 * S3, (M.DECK_Z - M.FLOOR_T) * S3, 0.3, dash=(1.5, 1))
# pilha
y_st = off + M.PI_ORIGIN[1] + 28
st0 = M.FLOOR_T + 24
for dz, hh, g, lab in ((M.FLOOR_T + 5, 19, 0.8, "18650"), (st0, 2, 0.5, ""), (st0 + 6, 2, 0.5, "PI 5"),
                       (st0 + 22, 2, 0.5, ""), (st0 + 24, 6, 0.75, "HAT")):
    rect(*C(y_st - 42.5, dz), 85 * S3, hh * S3, 0.3, fill=g)
text(*C(y_st, st0 + 13), "PILHA ~57", 5, "c")
# power bank
rect(*C(off + M.PB_ORIGIN[1], M.FLOOR_T), M.PB_IN[1] * S3, 28 * S3, 0.4, fill=0.8)
text(*C(off + M.PB_ORIGIN[1] + M.PB_IN[1] / 2, M.FLOOR_T + 12), "POWER BANK", 5, "c")
# ventoinha
rect(*C(off + M.FAN_IN[1] - 30, M.DECK_Z - M.FAN_T), 60 * S3, M.FAN_T * S3, 0.4, dash=(1.5, 1))
text(*C(off + M.FAN_IN[1], M.DECK_Z - 9), "FAN 60x15", 4.6, "c")
# conectores SMA no painel
for k in range(2):
    rect(*C(off + M.CONN_Y - 3 + k * 8, M.DECK_Z + M.DECK_T), 6 * S3, 14 * S3, 0.3, fill=0.7)
# tampa e moldura
fr_y0 = (INTD - 146) / 2
rect(*C(fr_y0, INTH - 23), 146 * S3, 23 * S3, 0.4, fill=0.85)
rect(*C(fr_y0 + 13, INTH - 19), 120 * S3, 15 * S3, 0.4, fill=0.55)
text(*C(INTD / 2, INTH - 13), "MOLDURA + TELA", 5.3, "c")
# cotas
dim_v(CX - 6, CY, CY + 95 * S3, "95", ext_from=CX)
dim_v(CX - 6, CY + 95 * S3, CY + INTH * S3, "40", ext_from=CX)
dim_v(CX + INTD * S3 + 6, CY, CY + M.DECK_Z * S3, str(M.DECK_Z), ext_from=CX + INTD * S3, side="r")
text(CX + INTD * S3 / 2, CY - 9, "CORTE A-A (CASE FECHADO)", 7.5, "c", bold=True)

# ========================= FOLHA 3: PEÇAS 3D =========================
c.showPage()
frame(3, "Painel com ventoinhas e conectores, moldura da tela e peças impressas", "1:2")
X0, Y0 = 30, 135
rect(X0, Y0, M.CH_W * S2, M.CH_D * S2, 0.7, r=M.CORNER_R * S2)
line(X0 + M.SPLIT_X * S2, Y0 - 3, X0 + M.SPLIT_X * S2, Y0 + M.CH_D * S2 + 3, 0.3, dash=([6, 2, 1, 2],))
x, y = T(tx0, ty0)
rect(x, y, (tx1 - tx0) * S2, (ty1 - ty0) * S2, 0.5)
text(x + (tx1 - tx0) * S2 / 2, y + (ty1 - ty0) * S2 / 2 - 1, "ABERTURA DO PORTA-ANTENAS", 5.5, "c")
for f in (M.FAN_IN, M.FAN_OUT):
    fx_, fy_ = T(*f)
    circle(fx_, fy_, (M.FAN / 2 - 1.5) * S2, 0.5)
    for k in range(-4, 5):
        line(fx_ + k * 3.5 - 1, fy_ - 12, fx_ + k * 3.5 - 1, fy_ + 12, 0.2)
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            circle(fx_ + sx_ * M.FAN_HOLE / 2 * S2, fy_ + sy_ * M.FAN_HOLE / 2 * S2, 0.85, 0.3)
for (vx0, vy0, vx1, vy1) in ((120, 165, 160, 205), (200, 180, 262, 205)):
    for xx in range(vx0, vx1 - 2, 6):
        a, b = T(xx, vy0)
        rect(a, b, 3 * S2, (vy1 - vy0) * S2, 0.25)
for xs, lab in M.SMA:
    a, b = T(xs, M.CONN_Y)
    circle(a, b, 3.3 * S2, 0.5)
    text(a, b + 3.5, lab, 4.8, "c")
a, b = T(*M.RJ45)
rect(a - 14.8 * S2 / 2, b - 16.4 * S2 / 2, 14.8 * S2, 16.4 * S2, 0.5)
text(a, b - 7.5, "RJ45", 4.8, "c")
a, b = T(*M.USBC)
rect(a - 4.8 * S2, b - 1.05, 9.6 * S2, 2.1, 0.5)
circle(a - 5, b, 0.85, 0.3)
circle(a + 5, b, 0.85, 0.3)
text(a, b - 5, "USB-C", 4.8, "c")
a, b = T(*M.TOGGLE)
circle(a, b, 6.1 * S2, 0.5)
text(a, b - 5.5, "CHAVE", 4.8, "c")
a, b = T(M.DSI_NOTCH[0], M.CH_D - 6)
rect(a, b, (M.DSI_NOTCH[1] - M.DSI_NOTCH[0]) * S2, 3.5, 0.4)
text(a + 6, b - 3, "CABO DSI", 4.8, "c")
for px, py in M.PILLARS:
    circle(*T(px, py), 0.85, 0.3)
dim_h(X0, X0 + M.CH_W * S2, Y0 - 7, "360", ext_from=Y0)
dim_v(X0 - 7, Y0, Y0 + M.CH_D * S2, "250", ext_from=X0)
fa, fb = T(*M.FAN_IN)
fa2, _ = T(*M.FAN_OUT)
dim_h(fa, fa2, Y0 + M.CH_D * S2 + 6, "212 entre ventoinhas", ext_from=fb + 15)
text(X0 + M.CH_W * S2 / 2, Y0 - 15, f"VISTA SUPERIOR - PAINEL (z = {M.DECK_Z} a {M.DECK_Z + M.DECK_T})", 7.5, "c", bold=True)
text(X0, Y0 - 21, "Furos: SMA Ø6,6 (LoRa e GPS; demais na expansão) | ventoinha Ø3,4 a 50 mm | keystone 14,8 x 16,4 | chave Ø12,2", 6)

# moldura da tela
MX, MY = 225, 175
SW_, SD_ = 215 * S2, 146 * S2
rect(MX, MY, SW_, SD_, 0.7, r=3)
wo = (M.DISP[0] + 2 + 9.5) * S2, (M.DISP[1] + 2.5 + 9.5) * S2
wi = (M.DISP[0] + 2) * S2, (M.DISP[1] + 2.5) * S2
rect(MX + (SW_ - wo[0]) / 2, MY + (SD_ - wo[1]) / 2, wo[0], wo[1], 0.4)
rect(MX + (SW_ - wi[0]) / 2, MY + (SD_ - wi[1]) / 2, wi[0], wi[1], 0.3, dash=(1.5, 1))
vw, vh = (M.VIEW[0] + 1.5) * S2, (M.VIEW[1] + 2) * S2
rect(MX + (SW_ - vw) / 2, MY + (SD_ - vh) / 2, vw, vh, 0.5, fill=0.85)
text(MX + SW_ / 2, MY + SD_ / 2 - 1, "JANELA 157 x 90", 5.5, "c")
for sx_ in (-60, 60):
    for sy_ in (-63.6, 63.6):
        circle(MX + SW_ / 2 + sx_ * S2, MY + SD_ / 2 + sy_ * S2, 0.7, 0.3)
dim_h(MX, MX + SW_, MY - 6, "215", ext_from=MY)
dim_v(MX + SW_ + 6, MY, MY + SD_, "146", ext_from=MX + SW_, side="r")
text(MX + SW_ / 2, MY - 13, "MOLDURA DA TELA (VAI NA TAMPA)", 7.5, "c", bold=True)
text(MX, MY + SD_ + 3, "Fixar na tampa com fita VHB 3M (sem furar o case). Altura total 19 + travessas 4.", 5.8)

# tabela de peças impressas
yy = table(225, 150, [
    ("Arquivo STL", "Qtd", "Medidas (mm)", "Obs."),
    ("01_bandeja_esquerda", "1", "180 x 250 x 80", "pilares para cima"),
    ("02_bandeja_direita", "1", "180 x 250 x 80", "pilares para cima"),
    ("03_painel_esquerdo", "1", "180 x 250 x 3", "plano"),
    ("04_painel_direito", "1", "180 x 250 x 3", "plano"),
    ("05_moldura_tela", "1", "215 x 146 x 19", "face para baixo"),
    ("06_travessa_tela", "2", "12 x 143 x 4", "-"),
    ("07_tala_emenda", "4", "40 x 16 x 4", "2 bandeja + 2 painel"),
    ("08_calco_frente_fundo", "4", "60 x 34,5 x 20", "trava no case"),
    ("09_calco_lateral", "2", "60 x 17 x 20", "trava no case"),
], [0, 50, 62, 100], 170)
text(225, yy - 3, "IMPRESSÃO", 7.5, bold=True)
imp = [
    "Material: ASA (melhor contra sol e calor) ou PETG. Evitar PLA.",
    "Mesa mínima: 256 x 256 mm (por isso bandeja e painel são divididos ao meio).",
    "Bico 0,4 | camada 0,2 mm | 4 perímetros | preenchimento 25% giroide.",
    "Filamento total estimado: ~1 kg. Furos M3 para parafuso autoatarraxante",
    "ou insertos de latão (alargar para Ø4,2 se usar insertos).",
    "Arquivo-fonte paramétrico: modelo3d/cyberdeck_3d.py (manifold3d + trimesh).",
]
for i, s in enumerate(imp):
    text(225, yy - 9 - i * 4.6, s, 6.2)

# ========================= FOLHA 4: BLOCOS, BOM, ENERGIA =========================
c.showPage()
frame(4, "Diagrama de blocos, materiais (R$ 5 mil) e energia", "S/E")


def box(x, y, w, h, t, s=None, fill=0.93, dash=None):
    rect(x, y, w, h, 0.5, dash=dash, fill=fill)
    if s:
        text(x + w / 2, y + h / 2 + 1, t, 6.8, "c", bold=True)
        text(x + w / 2, y + h / 2 - 3.3, s, 5.6, "c")
    else:
        text(x + w / 2, y + h / 2 - 1.2, t, 6.8, "c", bold=True)


text(25, 272, "DIAGRAMA DE BLOCOS", 10, bold=True)
box(25, 250, 46, 13, "USB-C de painel", "entrada de carga")
box(82, 250, 46, 13, "Power bank (opcional)", "20.000 mAh pass-through", dash=(2, 1.5))
arrow(71, 256.5, 82, 256.5)
arrow(105, 250, 105, 243)
box(25, 220, 46, 13, "4 x 18650", "~43 Wh")
box(82, 230, 46, 13, "UPS X1202", "5,1 V / 5 A")
arrow(71, 226, 82, 234)
box(140, 222, 58, 28, "Raspberry Pi 5", "8 GB - meshtasticd")
arrow(128, 236, 140, 236)
box(140, 190, 58, 16, "HAT RAK6421", "LoRa + GPS")
arrow(169, 222, 169, 206)
box(110, 158, 52, 15, "RAK13302", "LoRa 1 W - equipe")
box(176, 158, 52, 15, "RAK12501", "GPS")
arrow(169, 190, 136, 173)
arrow(169, 190, 202, 173)
box(240, 158, 52, 15, "Slots livres", "2º rádio / sensor", fill=1, dash=(2, 1.5))
box(212, 254, 50, 13, "Touch Display 2", "DSI, touch")
arrow(198, 246, 212, 258)
box(212, 214, 100, 26, "EXPANSÃO FUTURA", "SDR, Wi-Fi monitor, modem 4G, SSD (berços já impressos)", fill=1, dash=(2, 1.5))
arrow(198, 230, 212, 228, dash=(1.5, 1))
box(25, 190, 46, 13, "2 x ventoinha 60x15", "5 V, chave no painel")
arrow(71, 196, 140, 226, dash=(1.5, 1))
box(25, 170, 46, 13, "RJ45 de painel", "eth0 -> espelho")
arrow(71, 176, 140, 224)

# BOM
yb = table(25, 140, [
    ("Fase", "Item", "R$"),
    ("1", "Raspberry Pi 5 8 GB (lacrado)", "1.560"),
    ("1", "HAT RAK6421 + RAK13302 1 W + RAK12501 GPS *", "~550"),
    ("1", "Antenas LoRa 915 + GPS ativa *", "~190"),
    ("1", "microSD 128 GB High Endurance + dissipador *", "~150"),
    ("2", "Patola MP-0039 IP67 (Patola Store)", "486"),
    ("2", "UPS X1202 + 4 x 18650 *", "~560"),
    ("2", "2 ventoinhas 60 x 15 mm 5 V + filtro *", "~150"),
    ("2", "SMA de painel x2, keystone RJ45, USB-C, chave, cabos *", "~150"),
    ("2", "Filamento PETG/ASA ~1 kg + parafusos *", "~170"),
    ("3", "Raspberry Pi Touch Display 2 7\"", "759"),
    ("-", "Reserva para frete, impostos e imprevistos", "~275"),
], [0, 10, 103], 120, size=6)
text(25, yb - 3, "Total: R$ 5.000 (4.725 em peças + 275 de reserva)  * estimativa", 6.6, bold=True)
text(25, yb - 8, "Depois do orçamento: power bank (~R$ 300) e as expansões, uma de cada vez.", 6.2)

# Energia
ex = 160
ye = 140
text(ex, ye, "ORÇAMENTO DE ENERGIA (estimado)", 8.5, bold=True)
en = [
    ("Pi 5 + meshtasticd + Suricata leve", "5-6 W"),
    ("Touch Display 2", "~2-3 W"),
    ("Rádio LoRa 1 W (média)", "~1 W"),
    ("GPS + 2 ventoinhas", "~1 W"),
    ("Tudo ligado", "~9-11 W"),
    ("UPS interna (~37 Wh úteis)", "~3,5 h"),
    ("+ power bank opcional (~60 Wh úteis)", "~9 h"),
]
for i, (a_, b_) in enumerate(en):
    yy_ = ye - 6 - i * 5
    text(ex, yy_, a_, 6.2, bold=i >= 4)
    text(ex + 75, yy_, b_, 6.2, "r", bold=i >= 4)

# Notas
nx0 = 250
text(nx0, ye, "NOTAS", 8.5, bold=True)
nn = [
    "1. Mesmas peças impressas da versão completa,",
    "   com painel a 80 mm e 6 calços para o MP-0039.",
    "2. Ventoinhas slim (15 mm): a pilha do Pi fica",
    "   8 mm abaixo da ventoinha de entrada.",
    "3. LoRa em 915 MHz: conferir na Anatel o limite",
    "   de potência e o ganho de antena antes de usar 1 W.",
    "4. Furação da UPS X1202 e área útil da tela",
    "   devem ser conferidas com as peças em mãos.",
    "5. Sem SSD: usar microSD High Endurance e",
    "   mandar logs ao homelab quando houver rede.",
    "6. Para migrar ao Pelican 1450: mudar DECK_Z",
    "   para 95 e gerar os STL de novo.",
]
for i, n in enumerate(nn):
    text(nx0, ye - 6 - i * 4.5, n, 6.1)

c.showPage()
c.save()
print("ok", OUT)
