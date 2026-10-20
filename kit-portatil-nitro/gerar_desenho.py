import math
import os

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit_observacao_notebook_desenho_tecnico.pdf")
S = 1 / 3

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))

# Case Vonder MAI 415 (mm)
EXT = (406, 330, 174)
INT = (375, 270, 150)
# Notebook Acer Nitro V 15 ANV15-51
NB = (362.3, 239.9, 26.9)

c = canvas.Canvas(OUT, pagesize=landscape(A3))
c.setTitle("Kit de observação portátil - notebook")
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
    text(x0 + 2, y0 + 36, "KIT DE OBSERVAÇÃO PORTÁTIL - NOTEBOOK", 8.6, bold=True)
    text(x0 + 2, y0 + 32, title2, 6.3)
    text(x0 + 2, y0 + 26, "Autor: João Victor Paixão Zolim", 6.3)
    text(x0 + 2, y0 + 22, "github.com/joaovpzdev", 6.3)
    for (xx, a, b) in ((2, "Data", "17/10/2026 - rev. B"), (77, "Escala", scale), (114, "Folha", f"{sheet}/2")):
        text(x0 + xx, y0 + 16, a, 5.3)
        text(x0 + xx, y0 + 12, b, 6.8)
    for (xx, a, b) in ((2, "Unidade", "mm"), (77, "Projeção", "1º diedro"), (114, "Formato", "A3")):
        text(x0 + xx, y0 + 6, a, 5.3)
        text(x0 + xx, y0 + 2, b, 6.8)


# ============================ FOLHA 1 ============================
frame_and_title(1, "Case Vonder MAI 415: 3 camadas, corte e itens", "1:3")

W, D = INT[0] * S, INT[1] * S
WALL = 15 * S  # parede ~15 mm


def case_outline(x0, y0):
    rect(x0 - WALL, y0 - WALL, W + 2 * WALL, D + 2 * WALL, 0.8, r=4)
    rect(x0, y0, W, D, 0.5, fill=0.97, r=3)


def draw_items(x0, y0, items, light=()):
    for n, name, x, y, w, h in items:
        X, Y = x0 + x * S, y0 + y * S
        rect(X, Y, w * S, h * S, 0.45, fill=0.92 if n in light else 0.84, r=0.8)
        if w * S > 14 and name:
            text(X + w * S / 2, Y + h * S / 2 - 1.2 - (1.4 if h * S > 9 else 0), name, 4.6, "c")
        if n:
            balloon(X + 3 if w * S > 8 else X + w * S / 2, Y + h * S - 3 if h * S > 7 else Y + h * S / 2, n, r=1.9)


def dims(x0, y0, title):
    dim_h(x0, x0 + W, y0 + D + WALL + 6, "375 (interno)", ext_from=y0 + D)
    dim_v(x0 - WALL - 6, y0, y0 + D, "270", ext_from=x0 - WALL)
    text(x0 + W / 2, y0 - WALL - 11, title, 7.6, "c", bold=True)
    text(x0 - WALL, y0 - WALL - 4, "FRENTE (fechos)", 5.2, "l", bold=True)


# ---- Camada 1: eletrônicos ----
c1x, c1y = 35, 168
case_outline(c1x, c1y)
draw_items(c1x, c1y, [
    (2, "Power bank", 8, 8, 160, 80),
    (3, "Carregador", 176, 8, 150, 70),
    (4, "Wi-Fi", 8, 98, 100, 70),
    (5, "Hub USB-C", 116, 98, 110, 45),
    (7, "SSD", 234, 98, 85, 57),
    (9, "SDR 1", 8, 178, 70, 27),
    (10, "SDR 2", 8, 213, 70, 27),
    (11, "Heltec", 86, 178, 60, 35),
    (6, "GPS", 154, 178, 50, 45),
    (16, "Reserva", 212, 178, 110, 80),
    (14, "", 334, 8, 33, 254),
], light=(14, 16))
text(c1x + 350.5 * S, c1y + 135 * S, "USB", 4.6, "c")
dims(c1x, c1y, "CAMADA 1 - ELETRÔNICOS (fundo, h ~32)")
line(c1x - WALL - 4, c1y + 48 * S, c1x + W + WALL + 4, c1y + 48 * S, 0.4, dash=([6, 2, 1, 2],))
text(c1x - WALL - 6, c1y + 48 * S - 1, "A", 7, "r", bold=True)
text(c1x + W + WALL + 6, c1y + 48 * S - 1, "A", 7, "l", bold=True)

# ---- Camada 2: antenas e cabos ----
c2x, c2y = 188, 168
case_outline(c2x, c2y)
for k, (L, lab) in enumerate([(230, "dipolo"), (230, "dipolo"), (200, "1090"), (200, "Wi-Fi"), (200, "Wi-Fi"), (110, "915")]):
    yy = 8 + k * 18
    rect(c2x + 8 * S, c2y + yy * S, L * S, 14 * S, 0.35, fill=0.88, r=0.8)
    text(c2x + (8 + L) * S - 1, c2y + (yy + 4) * S, lab, 4.2, "r")
balloon(c2x + 8 * S + 2.6, c2y + 60 * S, 12, r=1.9)
draw_items(c2x, c2y, [
    (12, "Mini tripé", 8, 122, 200, 40),
    (15, "Cabos USB e adaptadores SMA", 8, 172, 220, 90),
    (8, "Mouse", 250, 8, 105, 62),
    (0, "Sílica / docs", 246, 190, 110, 72),
], light=(15, 0))
c.setLineWidth(0.45)
c.setFillGray(0.84)
c.circle(P(c2x + 300 * S), P(c2y + 125 * S), P(50 * S), stroke=1, fill=1)
c.setFillGray(1)
c.circle(P(c2x + 300 * S), P(c2y + 125 * S), P(22 * S), stroke=1, fill=1)
c.setFillGray(0)
balloon(c2x + 300 * S, c2y + 125 * S, 13, r=1.9)
dims(c2x, c2y, "CAMADA 2 - ANTENAS E CABOS (h ~40)")

# ---- Camada 3: notebook ----
lx, ly = 35, 42
case_outline(lx, ly)
nbx = lx + (INT[0] - NB[0]) / 2 * S
nby = ly + (INT[1] - NB[1]) / 2 * S
rect(nbx, nby, NB[0] * S, NB[1] * S, 0.7, fill=0.8, r=1.5)
rect(nbx + 4, nby + 4, NB[0] * S - 8, NB[1] * S - 8, 0.3, dash=(1.5, 1))
text(nbx + NB[0] * S / 2, nby + NB[1] * S / 2 + 1, "ACER NITRO V 15", 7, "c", bold=True)
text(nbx + NB[0] * S / 2, nby + NB[1] * S / 2 - 3.5, "fechado; EVA 3-5 mm nas pontas", 5.5, "c")
balloon(nbx + 6, nby + NB[1] * S - 6, 1)
text(lx + W / 2, ly + 2.2, "bolso: checklist, cabo HDMI", 4.6, "c")
text(lx + W / 2, nby + NB[1] * S + 2.2, "bolso: mousepad", 4.6, "c")
dim_h(nbx, nbx + NB[0] * S, ly - WALL - 5, "362,3 (folga ~6 por lado)", ext_from=nby)
dim_v(lx + W + WALL + 5, nby, nby + NB[1] * S, "239,9", ext_from=nbx + NB[0] * S, side="r")
dim_v(lx - WALL - 6, ly, ly + D, "270", ext_from=lx - WALL)
text(lx + W / 2, ly + D + WALL + 4, "CAMADA 3 - NOTEBOOK (topo / tampa)", 7.6, "c", bold=True)

# ---- Corte A-A ----
sx, sy = 188, 72
CW = INT[0] * S
H_INT = INT[2]
rect(sx - WALL, sy - 4 * S, CW + 2 * WALL, (H_INT + 8) * S, 0.8, r=2)
layers = [  # (z0, h, tipo, rótulo)
    (0, 10, "foam", ""), (10, 32, "l1", "Camada 1"), (42, 5, "foam", ""),
    (47, 40, "l2", "Camada 2"), (87, 5, "foam", ""), (92, 27, "nb", "Notebook"),
    (119, 20, "foam", ""), (139, 11, "free", "folga ~11"),
]
for z0, h, kind, lab in layers:
    y = sy + z0 * S
    if kind == "foam":
        rect(sx, y, CW, h * S, 0.3, fill=0.92)
    elif kind == "free":
        rect(sx, y, CW, h * S, 0.25, dash=(1.5, 1))
        text(sx + CW / 2, y + 0.8, lab, 4.6, "c")
    elif kind == "nb":
        rect(sx + (INT[0] - NB[0]) / 2 * S, y, NB[0] * S, h * S, 0.6, fill=0.7)
        balloon(sx + CW / 2, y + h * S / 2, 1, r=1.7)
for x, w, h, z, lab in [(8, 160, 30, 10, "2"), (176, 150, 30, 10, "3"), (334, 33, 20, 10, "14"),
                        (8, 200, 15, 47, "12"), (250, 105, 38, 47, "8"), (250, 100, 20, 47, "")]:
    if not lab:
        continue
    rect(sx + x * S, sy + z * S, w * S, h * S, 0.4, fill=0.75)
    balloon(sx + (x + w / 2) * S, sy + (z + h / 2) * S, lab, r=1.6)
line(sx - WALL - 3, sy + 111 * S, sx + CW + WALL + 3, sy + 111 * S, 0.4, dash=(3, 1.5))
text(sx + CW + WALL + 4, sy + 111 * S - 1, "tampa/base: medir", 4.6)
dim_v(sx + CW + WALL + 6, sy, sy + H_INT * S, "150 (interno)", ext_from=sx + CW + WALL, side="r")
dim_v(sx - WALL - 5, sy - 4 * S, sy + (H_INT + 4) * S, "174 (externo)", ext_from=sx - WALL)
text(sx - WALL, sy - 11, "CORTE A-A (espuma em cinza claro)", 7.6, "l", bold=True)

# ---- Tabela de itens ----
rows = [("N", "Item", "Medidas ~ (mm)")]
spec = [
    (1, "Notebook Acer Nitro V 15", "362 x 240 x 27"),
    (2, "Power bank 100 W PD", "160 x 80 x 30"),
    (3, "Carregador do notebook", "150 x 70 x 30"),
    (4, "Wi-Fi MT7612U (opc.)", "100 x 70 x 20"),
    (5, "Hub USB-C com PD 100 W", "110 x 45 x 18"),
    (6, "GPS USB u-blox", "50 x 45 x 16"),
    (7, "SSD externo 1 TB", "85 x 57 x 8"),
    (8, "Mouse sem fio", "105 x 62 x 38"),
    (9, "RTL-SDR Blog V3 - ADS-B", "70 x 27 x 14"),
    (10, "RTL-SDR Blog V3 - multiuso", "70 x 27 x 14"),
    (11, "Heltec V3, case branco", "60 x 35 x 18 *"),
    (12, "Antenas (6) e mini tripé", "até 230"),
    (13, "Coaxial 3 m enrolado", "Ø ~100"),
    (14, "Cabos USB curtos", "-"),
    (15, "Adaptadores SMA", "-"),
    (16, "Reserva (vídeo, 2º PB)", "110 x 80"),
]
rows += [(str(a), b, d) for a, b, d in spec]
tbx = 330
table(tbx, 200, rows, [0, 6, 50], 75, size=5.3, rh=4.5)
text(tbx, 202, "ITENS (balões)", 7.5, bold=True)

# ---- Notas folha 1 ----
nx, ny = 330, 272
text(nx, ny, "NOTAS", 7.5, bold=True)
notas = [
    "1. Case Vonder MAI 415: interno",
    "   375 x 270 x 150; ext. 406 x 330 x 174;",
    "   2,7 kg; válvula de pressão.",
    "2. Vedação: anúncio diz IP67, uma ficha",
    "   diz IP54. Testar submerso ao receber.",
    "3. Medir altura da tampa e da base",
    "   antes de cortar a espuma.",
    "4. Antenas desrosqueadas; nada conectado.",
    "5. Ordem de abertura: notebook, antenas,",
    "   eletrônicos. Sílica gel na camada 2.",
    "6. Peso total estimado: ~6,3 kg.",
]
for i, n in enumerate(notas):
    text(nx, ny - 6 - i * 4.4, n, 5.6)

c.showPage()

# ============================ FOLHA 2 ============================
frame_and_title(2, "Ligações, energia, software e lista de materiais", "S/E")

text(25, 272, "LIGAÇÕES USB E RF", 10, bold=True)
# notebook central
rect(95, 205, 70, 40, 0.6, fill=0.85)
text(130, 234, "Notebook Nitro V 15", 8, "c", bold=True)
text(130, 226, "Linux Mint · Docker", 6, "c")
text(130, 217, "16/32 GB · RTX 3050 sob demanda", 5.6, "c")
text(130, 212, "3x USB-A · 1x USB-C · RJ45 · HDMI", 5.6, "c")
# direto nas USB-A
direct = [(25, 250, "SDR 1 (ADS-B)", "1090 MHz, fixo"), (25, 228, "Wi-Fi MT7612U", "2,4/5 GHz, monitor"),
          (25, 206, "Dongle do mouse", "")]
for x, y, t, s_ in direct:
    box(x, y, 50, 13, t, s_ or None, ts=6.6, ss_=5.4)
    arrow(x + 50, y + 6.5, 95, 225 if y > 230 else (222 if y > 210 else 210))
text(77, 252, "USB-A", 5.5)
# hub
box(185, 215, 50, 20, "Hub USB-C", "PD 100 W pass-through", ts=7, ss_=5.4)
arrow(185, 225, 165, 225)
text(169, 227, "USB-C", 5.5)
hub_items = [(250, "SDR 2 (multiuso)", "137 / 400 / 433 MHz"), (232, "Heltec V3", "LoRa 915 MHz"),
             (214, "GPS u-blox", "posição e hora"), (196, "SSD 1 TB", "gravações, mapas, ZIM")]
for y, t, s_ in hub_items:
    box(250, y, 52, 13, t, s_, ts=6.6, ss_=5.4)
    arrow(250, y + 6.5, 235, 225)
box(185, 186, 50, 13, "Power bank 100 W", "USB-C PD", ts=6.6, ss_=5.4)
arrow(210, 199, 210, 215)
text(212, 204, "PD in", 5.5)
# antenas
ants = [(25, 250, "colinear 1090"), (25, 228, "2 antenas 5 dBi")]
text(25, 178, "RF: SDR 1 -> antena 1090 · SDR 2 -> dipolo telescópico (137 em V, 400 e 433 retos)", 5.8)
text(25, 173, "Heltec -> antena 915 · Wi-Fi -> 2 antenas 2,4/5 GHz · GPS com cabo de 1,5 m, fora do case", 5.8)
box(95, 186, 70, 13, "RJ45 do notebook", "auditoria de rede autorizada", ts=6.6, ss_=5.4, fill=1, dash=(2, 1.5))

# ---- Energia ----
text(320, 272, "ENERGIA", 10, bold=True)
box(320, 250, 80, 12, "Tomada / viatura (inversor)", None, ts=6.6)
box(320, 230, 80, 12, "Carregador Acer (P4)", None, ts=6.6)
arrow(360, 250, 360, 242)
text(320, 222, "No campo: power bank -> hub (PD) -> notebook", 6)
text(320, 217, "e periféricos, se o USB-C carregar o Nitro.", 6)
text(320, 212, "Testar com carregador USB-C de 100 W antes.", 6)
pw = [("Item", "W (estim.)"), ("Notebook, uso de decodificação", "~25-40"), ("2 x RTL-SDR", "~3"),
      ("Adaptador Wi-Fi (ligado)", "~2-3"), ("Heltec + GPS + SSD", "~2-4"), ("Total", "~32-50")]
end = table(320, 207, pw, [0, (80,)], 80, size=5.9, rh=4.8)
text(320, end - 5, "Bateria 57 Wh + power bank (<100 Wh, ~70 úteis):", 5.8)
text(320, end - 9.5, "~2,5-3,5 h com tudo ligado.", 5.8, bold=True)
text(320, end - 14, "Power bank até 100 Wh: permitido em avião.", 5.8)

# ---- Software ----
text(25, 163, "SOFTWARE (DOCKER COMPOSE NO NOTEBOOK)", 8, bold=True)
sw = [("Equipamento", "Serviço", "Uso"),
      ("SDR 1", "readsb + tar1090", "Aviões no mapa, offline"),
      ("SDR 2", "SatDump / radiosonde_auto_rx / rtl_433", "Um por vez: satélite, balão, 433 MHz"),
      ("Heltec V3", "Meshtastic (CLI/web por serial) + Mosquitto", "Rede do cyberdeck e dos drones"),
      ("GPS", "gpsd + chrony", "Posição da estação e hora sem internet"),
      ("Wi-Fi MT7612U", "Kismet", "Redes e aparelhos (só com autorização)"),
      ("SSD", "Kiwix, tiles de mapa, gravações IQ", "Wikipédia, WikiMed, mapas offline"),
      ("Notebook", "Grafana + InfluxDB, Tailscale", "Central portátil; sincroniza com o homelab")]
table(25, 159, sw, [0, 28, 102], 220, size=5.9, rh=5.0)

# ---- Lista de materiais ----
bom = [
    ("Case Vonder MAI 415 (com espuma)", 397),
    ("EVA 3-5 mm e divisórias de espuma extras", 60),
    ("2 x RTL-SDR Blog V3 com kit de dipolo", 700),
    ("Antena 1090 MHz portátil (SMA)", 150),
    ("Heltec V3 863-928 MHz, case branco [COMPRADO 18/10]", 198),
    ("GPS USB u-blox", 80),
    ("Hub USB-C com PD 100 W pass-through", 150),
    ("Power bank 100 W PD (< 100 Wh)", 350),
    ("SSD externo USB-C 1 TB", 450),
    ("Cabos: coaxial 3 m SMA, extensões USB, adaptadores", 100),
]
opc = [("Adaptador Wi-Fi MT7612U", 200), ("Mouse sem fio (se não tiver)", 80),
       ("DDR5 SODIMM 16 GB (upgrade para 32 GB)", 350)]
tot = sum(v for _, v in bom)
topc = sum(v for _, v in opc)


def brl(v):
    return f"{v:,.0f}".replace(",", ".")


rows = [("It.", "Descrição", "R$ (estim.)")]
rows += [(str(i + 1), d, f"~{brl(v)}") for i, (d, v) in enumerate(bom)]
rows += [("", "Subtotal essencial", f"~{brl(tot)}")]
rows += [(str(len(bom) + i + 1), d + " (opcional)", f"~{brl(v)}") for i, (d, v) in enumerate(opc)]
rows += [("", "Total com opcionais", f"~{brl(tot + topc)}")]
text(25, 112, "LISTA DE MATERIAIS", 8, bold=True)
table(25, 108, rows, [0, 9, (220,)], 220, size=5.9, rh=4.85)

# ---- Notas folha 2 ----
nx, ny = 255, 140
text(nx, ny, "NOTAS", 8, bold=True)
n2 = [
    "1. Notebook e carregador já existentes: fora da lista.",
    "2. SDR 1 e Wi-Fi direto nas USB-A (mais banda e corrente).",
    "3. Um serviço por SDR. O SDR 2 troca de função por perfil",
    "   do docker compose (sat / sonde / ism).",
    "4. Gravar serial nos SDR: rtl_eeprom -s ADSB / MULTI.",
    "5. RTX 3050 em modo on-demand (prime-select) no campo.",
    "6. Só recepção, exceto Heltec (915 MHz, radiação restrita).",
    "7. Kismet e RJ45 só em redes próprias ou com autorização.",
    "8. Preços estimados, out/2026; importados variam.",
]
for i, n in enumerate(n2):
    text(nx, ny - 6 - i * 4.8, n, 6)

c.showPage()
c.save()
print("ok", OUT, tot, tot + topc)
