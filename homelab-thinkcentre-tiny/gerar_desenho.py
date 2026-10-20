import os
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homelab_rack_desenho_tecnico.pdf")
W, H = landscape(A3)
S = 1 / 3  # escala 1:3

# Medidas reais (mm)
RACK_W, RACK_D, RACK_H = 280, 260, 406
U = 44.45
FRAME_TB = (RACK_H - 8 * U) / 2
POST = 29
TINY_W, TINY_D, TINY_H = 179, 183, 34.5
SW_W, SW_D, SW_H = 158, 101, 25
SHELF = 2.5
PHONE_W, PHONE_T, PHONE_L = 77, 9, 166
PSU_W, PSU_H, PSU_D = 46, 30, 108

c = canvas.Canvas(OUT, pagesize=landscape(A3))
c.setTitle("Homelab Lenovo Tiny - Mini rack 10 pol 8U")
c.setAuthor("João Victor Paixão Zolim")


def P(v):
    return v * mm


def rect(x, y, w, h, lw=0.5, dash=None, fill=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    if fill is not None:
        c.setFillGray(fill)
        c.rect(P(x), P(y), P(w), P(h), stroke=1, fill=1)
        c.setFillGray(0)
    else:
        c.rect(P(x), P(y), P(w), P(h), stroke=1, fill=0)
    c.setDash()


def line(x1, y1, x2, y2, lw=0.35, dash=None):
    c.setLineWidth(lw)
    c.setDash(*dash) if dash else c.setDash()
    c.line(P(x1), P(y1), P(x2), P(y2))
    c.setDash()


def text(x, y, s, size=7, anchor="l", bold=False):
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    fn = {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[anchor]
    fn(P(x), P(y), s)


def arrowhead(x, y, ang_deg, size=1.6):
    import math
    a = math.radians(ang_deg)
    p = c.beginPath()
    p.moveTo(P(x), P(y))
    for d in (155, -155):
        b = a + math.radians(d)
        p.lineTo(P(x + size * math.cos(b)), P(y + size * math.sin(b)))
    p.close()
    c.setLineWidth(0.2)
    c.drawPath(p, stroke=1, fill=1)


def dim_h(x1, x2, y, label, ext_from=None):
    """Cota horizontal em y; linhas de chamada até ext_from (y do objeto)."""
    if ext_from is not None:
        off = 1 if y > ext_from else -1
        line(x1, ext_from, x1, y + off * 1.5, 0.2)
        line(x2, ext_from, x2, y + off * 1.5, 0.2)
    line(x1, y, x2, y, 0.25)
    arrowhead(x1, y, 180)
    arrowhead(x2, y, 0)
    text((x1 + x2) / 2, y + 1, label, 6.5, "c")


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
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(0, 0, label)
    c.restoreState()


def frame_and_title(sheet, title2):
    rect(10, 10, 400, 277, 0.8)
    rect(15, 15, 390, 267, 0.4)
    # Carimbo
    x0, y0, w, h = 255, 15, 150, 42
    rect(x0, y0, w, h, 0.6)
    line(x0, y0 + 30, x0 + w, y0 + 30, 0.4)
    line(x0, y0 + 20, x0 + w, y0 + 20, 0.4)
    line(x0, y0 + 10, x0 + w, y0 + 10, 0.4)
    line(x0 + 75, y0, x0 + 75, y0 + 20, 0.4)
    line(x0 + 112, y0, x0 + 112, y0 + 20, 0.4)
    text(x0 + 2, y0 + 36, "HOMELAB LENOVO TINY - MINI RACK 10\" 8U", 9, bold=True)
    text(x0 + 2, y0 + 32, title2, 6.5)
    text(x0 + 2, y0 + 26, "Autor: João Victor Paixão Zolim", 6.5)
    text(x0 + 2, y0 + 22, "github.com/joaovpzdev", 6.5)
    text(x0 + 2, y0 + 16, "Data", 5.5)
    text(x0 + 2, y0 + 12, "17/10/2026 - rev. D", 7)
    text(x0 + 77, y0 + 16, "Escala", 5.5)
    text(x0 + 77, y0 + 12, "1:3" if sheet == 1 else "S/E", 7)
    text(x0 + 114, y0 + 16, "Folha", 5.5)
    text(x0 + 114, y0 + 12, f"{sheet}/3", 7)
    text(x0 + 2, y0 + 6, "Unidade", 5.5)
    text(x0 + 2, y0 + 2, "mm", 7)
    text(x0 + 77, y0 + 6, "Projeção", 5.5)
    text(x0 + 77, y0 + 2, "1º diedro", 7)
    text(x0 + 114, y0 + 6, "Formato", 5.5)
    text(x0 + 114, y0 + 2, "A3", 7)


# ---------------- FOLHA 1 ----------------
frame_and_title(1, "Vistas ortogonais, ocupação do rack e lista de materiais")

# Vista frontal
fx, fy = 40, 136
w, h = RACK_W * S, RACK_H * S
rect(fx, fy, w, h, 0.7)
post = POST * S
rect(fx, fy, post, h, 0.4)
rect(fx + w - post, fy, post, h, 0.4)
inner_x, inner_w = fx + post, w - 2 * post
top_inner = fy + h - FRAME_TB * S
line(fx + post, top_inner, fx + w - post, top_inner, 0.4)
line(fx + post, fy + FRAME_TB * S, fx + w - post, fy + FRAME_TB * S, 0.4)

labels = {}
for i in range(8):
    u_top = top_inner - i * U * S
    u_bot = u_top - U * S
    if i > 0:
        line(fx + 2, u_top, fx + post - 2, u_top, 0.2)
        line(fx + w - post + 2, u_top, fx + w - 2, u_top, 0.2)
    text(fx + post / 2, u_bot + U * S / 2 - 1, f"U{i+1}", 5.5, "c")
    labels[i + 1] = (u_bot, u_top)

cx = fx + w / 2


def shelf(ub):
    rect(inner_x, ub, inner_w, SHELF * S, 0.3, fill=0.75)


# U1 switch
ub, ut = labels[1]
shelf(ub)
rect(cx - SW_W * S / 2, ub + SHELF * S, SW_W * S, SW_H * S, 0.5, fill=0.92)
for k in range(8):
    rect(cx - SW_W * S / 2 + 6 + k * 3.6, ub + SHELF * S + 2.2, 2.6, 2.6, 0.2)
# U2-U5 Tiny
for u in (2, 3, 4, 5):
    ub, ut = labels[u]
    shelf(ub)
    tx = cx - TINY_W * S / 2
    rect(tx, ub + SHELF * S, TINY_W * S, TINY_H * S, 0.6, fill=0.92)
    rect(tx + 3, ub + SHELF * S + 4.5, 1.6, 4, 0.3)  # USB
    rect(tx + 5.5, ub + SHELF * S + 4.5, 1.6, 4, 0.3)
    c.circle(P(tx + TINY_W * S - 5), P(ub + SHELF * S + TINY_H * S / 2), P(1.2), stroke=1, fill=0)
    text(cx + 4, ub + SHELF * S + 5, f"NÓ {u-1}", 6, "c", bold=True)
# U6 celulares deitados
ub, ut = labels[6]
shelf(ub)
gap = 6
px1 = cx - PHONE_W * S - gap / 2
rect(px1, ub + SHELF * S, PHONE_W * S, PHONE_T * S, 0.5, fill=0.85)
rect(cx + gap / 2, ub + SHELF * S, PHONE_W * S, PHONE_T * S, 0.5, fill=0.85)
text(px1 + PHONE_W * S / 2, ub + SHELF * S + 5, "REDMI", 5.5, "c")
text(cx + gap / 2 + PHONE_W * S / 2, ub + SHELF * S + 5, "A11", 5.5, "c")
# U7 fontes
ub, ut = labels[7]
shelf(ub)
for k in range(4):
    rect(cx - 33 + k * 17, ub + SHELF * S, 14, PSU_H * S, 0.4, fill=0.8)
    text(cx - 26 + k * 17, ub + SHELF * S + 3.8, "65 W", 5.5, "c")
# U8 régua
ub, ut = labels[8]
rect(inner_x + 2, ub + 4, inner_w - 4, 7, 0.5, fill=0.9)
for k in range(4):
    c.circle(P(inner_x + 10 + k * 9), P(ub + 7.5), P(1.6), stroke=1, fill=0)
text(cx + 12, ub + 6.6, "RÉGUA", 5.5, "l")

# Cotas vista frontal
dim_h(fx, fx + w, fy - 7, "280", ext_from=fy)
dim_v(fx - 6, fy, fy + h, "406", ext_from=fx)
dim_v(fx + w + 6, labels[8][0], top_inner, "8U = 355,6", ext_from=fx + w, side="r")
ub2 = labels[2][0] + SHELF * S
dim_v(fx + w + 15, ub2, ub2 + TINY_H * S, "34,5", ext_from=fx + w - post, side="r")
text(fx + w / 2, fy - 13, "VISTA FRONTAL", 8, "c", bold=True)

# Vista lateral (esquerda)
sx, sy = 158, 136
sw, sh = RACK_D * S, RACK_H * S
rect(sx, sy, sw, sh, 0.7)
rect(sx, sy, 6, sh, 0.4)
rect(sx + sw - 6, sy, 6, sh, 0.4)
s_top_inner = sy + sh - FRAME_TB * S
front_off = 8
for i in range(8):
    u_bot = s_top_inner - (i + 1) * U * S
    if i in range(7):
        rect(sx + 6, u_bot, sw - 12, SHELF * S, 0.3, fill=0.75)
    if i == 0:
        rect(sx + front_off, u_bot + SHELF * S, SW_D * S, SW_H * S, 0.5, dash=(1.5, 1))
    if i in (1, 2, 3, 4):
        rect(sx + front_off, u_bot + SHELF * S, TINY_D * S, TINY_H * S, 0.5, dash=(1.5, 1))
    if i == 5:
        rect(sx + front_off, u_bot + SHELF * S, PHONE_L * S, PHONE_T * S, 0.4, dash=(1.5, 1))
        rect(sx + sw - 6 - 80 * S, u_bot + SHELF * S, 74 * S, 25 * S, 0.5, fill=0.8)
        text(sx + sw - 6 - 43 * S, u_bot + SHELF * S + 2.5, "BASE", 4.5, "c", bold=True)
    if i == 6:
        rect(sx + front_off + 20, u_bot + SHELF * S, PSU_D * S, PSU_H * S, 0.4, dash=(1.5, 1))
# setas de ar na U3
yu3 = s_top_inner - 3 * U * S + SHELF * S + TINY_H * S / 2
line(sx - 8, yu3, sx + 2, yu3, 0.35)
arrowhead(sx + 2, yu3, 0)
xe = sx + front_off + TINY_D * S
line(xe + 3, yu3, sx + sw + 8, yu3, 0.35)
arrowhead(sx + sw + 8, yu3, 0)
text(sx - 8, yu3 + 2, "AR FRIO", 5, "l")
text(sx + sw - 4, yu3 + 2, "AR QUENTE", 5, "l")
text(sx + 8, sy + sh - 6, "FRENTE", 6, "l", bold=True)
text(sx + sw - 8, sy + sh - 6, "FUNDO", 6, "r", bold=True)
dim_h(sx, sx + sw, sy - 7, "260", ext_from=sy)
yb = s_top_inner - 2 * U * S + SHELF * S
dim_h(sx + front_off, sx + front_off + TINY_D * S, sy + sh + 6, "183 (Tiny)", ext_from=yb + TINY_H * S)
dim_h(sx + front_off + TINY_D * S, sx + sw, sy + sh + 6, "~69 cabos", ext_from=yb + TINY_H * S)
text(sx + sw / 2, sy - 13, "VISTA LATERAL ESQUERDA", 8, "c", bold=True)

# Vista superior (abaixo da frontal)
tx0, ty0 = 40, 32
tw, th = RACK_W * S, RACK_D * S
rect(tx0, ty0, tw, th, 0.7)
rect(tx0, ty0, post, th, 0.4)
rect(tx0 + tw - post, ty0, post, th, 0.4)
# Tiny (frente embaixo)
tiny_x = tx0 + tw / 2 - TINY_W * S / 2
rect(tiny_x, ty0 + front_off, TINY_W * S, TINY_D * S, 0.6, fill=0.92)
text(tx0 + tw / 2, ty0 + front_off + TINY_D * S / 2, "LENOVO TINY", 6, "c", bold=True)
text(tx0 + tw / 2, ty0 + front_off + TINY_D * S / 2 - 4, "M720q", 6, "c")
# fonte atrás
rect(tx0 + tw / 2 - 8, ty0 + front_off + TINY_D * S + 3, 16, 8, 0.3, dash=(1.5, 1))
text(tx0 + tw / 2, ty0 + th - 4, "CABOS / FONTE", 5, "c")
text(tx0 + tw / 2, ty0 + 2, "FRENTE", 6, "c", bold=True)
dim_h(tx0, tx0 + tw, ty0 - 7, "280", ext_from=ty0)
dim_v(tx0 - 6, ty0, ty0 + th, "260", ext_from=tx0)
dim_v(tx0 + tw + 6, ty0 + front_off, ty0 + front_off + TINY_D * S, "183", ext_from=tiny_x + TINY_W * S, side="r")
yd = ty0 + front_off + TINY_D * S - 7
dim_h(tiny_x, tiny_x + TINY_W * S, yd, "179")
text(tx0 + tw / 2, ty0 - 13, "VISTA SUPERIOR (U3, PRATELEIRA)", 8, "c", bold=True)

# Tabela de ocupação
ox, oy = 255, 268
text(ox, oy + 2, "OCUPAÇÃO DO RACK", 8, bold=True)
rows = [
    ("U", "Equipamento", "Função"),
    ("U1", "Switch TL-SG108E", "VLAN 10 casa / 20 lab / 30 alvos"),
    ("U2", "Lenovo M720q - nó 1", "Zabbix, Wazuh, Pi-hole, Grafana, Loki, Kuma"),
    ("U3", "Lenovo M720q - nó 2", "Kiwix, MISP, Node-RED, MQTT, Minecraft, GLPI"),
    ("U4", "Lenovo M720q - nó 3", "AD, alvos isolados, honeypot Cowrie"),
    ("U5", "Lenovo M720q 32 GB - nó 4", "Security Onion + ntopng (porta espelho)"),
    ("U6", "Celulares (frente) + base de encaixe (fundo)", "netwatch / rádios do kit + ADS-B fixo"),
    ("U7", "4 fontes Lenovo 65 W", "Alimentação dos nós"),
    ("U8", "Régua de tomadas", "Ligada ao nobreak (fora do rack)"),
]
cols = [0, 12, 62]
for r, row in enumerate(rows):
    y = oy - 4 - r * 5.2
    if r == 0:
        rect(ox, y - 1.6, 150, 5.2, 0.3, fill=0.88)
    else:
        line(ox, y - 1.6, ox + 150, y - 1.6, 0.2)
    for k, val in enumerate(row):
        text(ox + 1.5 + cols[k], y, val, 6.3, bold=(r == 0))
rect(ox, oy - 4 - 8 * 5.2 - 1.6, 150, 9 * 5.2, 0.4)

# Lista de materiais
bx, by = 255, 205
text(bx, by + 2, "LISTA DE MATERIAIS", 8, bold=True)
bom = [
    ("It.", "Qtd", "Descrição", "Dimensões (mm)"),
    ("1", "1", "Mini rack 10\" 8U DeskPi RackMate T1 Plus", "280 x 260 x 406 *"),
    ("2", "6", "Prateleira ventilada 1U, prof. 260 mm", "222 x 260"),
    ("3", "4", "Lenovo ThinkCentre M720q Tiny, i5 8ª", "179 x 183 x 34,5"),
    ("4", "3+2", "SODIMM DDR4: +8 GB nós 1-3; 2 x 16 GB nó 4", "-"),
    ("5", "1", "Switch gerenciável 8p Gigabit TL-SG108E", "158 x 101 x 25"),
    ("6", "4", "Fonte Lenovo 65 W, ponta retangular", "~108 x 46 x 30"),
    ("7", "1", "Régua de tomadas / filtro de linha", "-"),
    ("8", "5", "Cabo de rede Cat6, 0,25 m", "-"),
    ("9", "1", "Nobreak 600-700 VA (fora do rack)", "-"),
    ("10", "1", "SSD SATA 2,5\" 1 TB (nó 2: Kiwix + imagens)", "100 x 70 x 7"),
    ("11", "1", "Nó 4: riser PCIe + Intel i350-T2 + NVMe 1 TB", "meia altura"),
    ("12", "1", "Base de encaixe: hub USB 3 + painel coaxial (U6)", "~110 x 70 x 25"),
    ("13", "1", "Antenas fixas, coaxiais e RTL-SDR ADS-B: folha 3", "-"),
]
cols = [0, 8, 17, 108]
for r, row in enumerate(bom):
    y = by - 4 - r * 5.2
    if r == 0:
        rect(bx, y - 1.6, 150, 5.2, 0.3, fill=0.88)
    else:
        line(bx, y - 1.6, bx + 150, y - 1.6, 0.2)
    for k, val in enumerate(row):
        text(bx + 1.5 + cols[k], y, val, 6.3, bold=(r == 0))
rect(bx, by - 4 - (len(bom) - 1) * 5.2 - 1.6, 150, len(bom) * 5.2, 0.4)

# Notas
nx, ny = 255, 126
text(nx, ny, "NOTAS", 8, bold=True)
notas = [
    "1. * Medidas externas do rack aproximadas: confirmar com o fabricante antes da montagem.",
    "2. Fluxo de ar dos Tiny: entrada pela frente, saída pelo fundo. Manter ~69 mm livres atrás.",
    "3. Dual channel: 2 pentes iguais por nó (2 x 8 GB nos nós 1-3, 2 x 16 GB no nó 4).",
    "4. Fontes na prateleira U7, afastadas dos nós para não aquecer a entrada de ar.",
    "5. Celulares deitados, sem capa, com limite de carga ativado.",
    "6. Nobreak fora do rack, alimentando a régua da U8.",
    "7. Rack cheio (8U). O 5º nó pede um rack 12U. Switch com 7 de 8 portas em uso.",
    "8. Nó 4: placa i350 no riser PCIe (sniffer, sem IP) + rede onboard (gerência).",
    "9. Rádios do kit portátil encaixam na U6 (fundo): coaxiais do mastro e hub do nó 2.",
    "10. Vistas em 1º diedro. Escala 1:3 nas vistas ortogonais.",
]
for i, n in enumerate(notas):
    text(nx, ny - 6 - i * 5, n, 6.3)

c.showPage()


# ---------------- FOLHA 2 ----------------
frame_and_title(2, "Topologia de rede, central de observação e diagrama elétrico")


def box(x, y, w, h, title, sub=None, fill=0.93, dash=None, ts=7.5, ss_=6):
    rect(x, y, w, h, 0.5, dash=dash, fill=fill)
    if sub:
        text(x + w / 2, y + h / 2 + 1, title, ts, "c", bold=True)
        text(x + w / 2, y + h / 2 - 3.5, sub, ss_, "c")
    else:
        text(x + w / 2, y + h / 2 - 1.2, title, ts, "c", bold=True)


def arrow(x1, y1, x2, y2, lw=0.4, dash=None):
    import math
    line(x1, y1, x2, y2, lw, dash)
    arrowhead(x2, y2, math.degrees(math.atan2(y2 - y1, x2 - x1)))


text(25, 272, "TOPOLOGIA DE REDE", 10, bold=True)
box(25, 250, 62, 14, "FONTES PÚBLICAS", "FIRMS, INPE, USGS, Cemaden, CVE/RSS", fill=1, dash=(3, 2), ss_=5.5)
box(97, 250, 46, 14, "INTERNET")
box(153, 250, 92, 14, "REDES COLABORATIVAS", "RIPE Atlas, FlightAware, ADSBx, SondeHub, SatNOGS", fill=1, dash=(3, 2), ss_=5.5)
arrow(97, 257, 87, 257, dash=(2, 1.5))
arrow(143, 257, 153, 257, dash=(2, 1.5))
box(97, 228, 46, 13, "Roteador da casa", "gateway / DHCP / Wi-Fi")
arrow(120, 250, 120, 241)
box(165, 228, 80, 13, "Wi-Fi da casa (VLAN 10)", "Sensor.Community, Shelly, Blitzortung", ss_=5.5)
arrow(143, 234.5, 165, 234.5)
box(85, 198, 70, 16, "Switch TL-SG108E", "802.1Q + espelho porta 1 -> 7")
arrow(120, 228, 120, 214)

nodes = [(25, "Nó 1 - monitoramento", "Zabbix, Wazuh, Grafana, Loki"),
         (70, "Nó 2 - dados", "Kiwix, MISP, Node-RED, MQTT"),
         (115, "Nó 3 - lab", "AD, alvos, Cowrie (VLAN 30)"),
         (160, "Nó 4 - sensor", "Security Onion, ntopng"),
         (205, "Base de encaixe", "rádios do kit + ADS-B fixo")]
for x, t, s_ in nodes:
    box(x, 162, 42, 16, t, s_, ts=6.6, ss_=5.3)
    if x not in (160, 205):
        arrow(120, 198, x + 21, 178)
arrow(120, 198, 176, 178)
arrow(150, 198, 186, 178, dash=(2, 1.5))
text(166, 190, "espelho (i350, sem IP)", 5.5)
line(226, 162, 226, 157, 0.4)
line(226, 157, 91, 157, 0.4)
arrow(91, 157, 91, 162)
text(160, 153.6, "USB (passthrough por porta para a VM do nó 2)", 5.2, "c")

text(25, 150, "VLANs e espelhamento", 7.5, bold=True)
vl = [("VLAN 10 - CASA", "roteador, notebook, celulares, TV, sensores IoT"),
      ("VLAN 20 - LAB", "Proxmox, serviços, VM de rádio no nó 2; kit portátil via Tailscale"),
      ("VLAN 30 - ALVOS", "Metasploitable, DVWA, AD vulnerável, Cowrie: sem rota para a VLAN 10"),
      ("ESPELHO", "porta 1 (uplink do roteador) copiada para a porta 7 (sniffer do nó 4)")]
for i, (a, b) in enumerate(vl):
    y = 143 - i * 6
    text(25, y, a, 6.5, bold=True)
    text(62, y, b, 6.5)

box(25, 106, 220, 12, "TAILSCALE (rede overlay)", "alertas, métricas e dados -> nós 1 e 2, de qualquer lugar", fill=1, dash=(3, 2))
for k, (t, s_) in enumerate([("Redmi", "Minecraft / serviços"), ("Galaxy A11", "netwatch"),
                             ("Cyberdeck", "Suricata / Meshtastic"), ("Kit notebook", "MQTT, Influx, ADS-B")]):
    box(25 + k * 56, 86, 52, 13, t, s_)
    arrow(51 + k * 56, 99, 51 + k * 56, 106, dash=(2, 1.5))

text(25, 72, "CENTRAL DE OBSERVAÇÃO (GRAFANA, NÓ 1)", 7.5, bold=True)
srcs = [("Zabbix / Wazuh", "hosts e alertas"), ("Security Onion", "Suricata, Zeek"),
        ("InfluxDB", "feeds do Node-RED"), ("MQTT", "rádio e sensores"), ("Loki", "logs")]
for k, (t, s_) in enumerate(srcs):
    x = 25 + k * 45
    box(x, 50, 40, 13, t, s_, ts=6.6, ss_=5.5)
    arrow(x + 20, 50, x + 20, 38)
box(25, 22, 220, 16, "Painéis do Grafana",
    "mapa (aviões, balões, drones, incêndios, sismos, kit portátil)  |  rede  |  satélites  |  ambiente", ss_=5.8)

# Diagrama elétrico
ex = 270
text(ex, 272, "DIAGRAMA ELÉTRICO", 10, bold=True)
box(ex + 35, 250, 60, 12, "Tomada 127/220 V")
box(ex + 35, 228, 60, 12, "Nobreak 600-700 VA")
arrow(ex + 65, 250, ex + 65, 240)
box(ex + 35, 206, 60, 12, "Régua (U8)")
arrow(ex + 65, 228, ex + 65, 218)
loads = ["Nó 1", "Nó 2", "Nó 3", "Nó 4", "Switch", "Hub"]
for k, t in enumerate(loads):
    x = ex + k * 22
    box(x, 180, 20, 12, t, "65 W" if k < 4 else ("12 V" if k == 4 else "base"), ts=6.5, ss_=5.5)
    arrow(ex + 65, 206, x + 10, 192)
text(ex, 170, "Consumo estimado (24/7)", 7.5, bold=True)
cons = [
    ("Nós 1-3 em repouso", "~30-45 W"),
    ("Nó 4 (Security Onion em carga contínua)", "~25-35 W"),
    ("Switch", "~5 W"),
    ("Base de encaixe (hub + rádios + LNA)", "~10 W"),
    ("Celulares carregando", "~10 W"),
    ("Uso típico", "~90-110 W"),
    ("Pico total estimado", "~170 W"),
]
for i, (a, b) in enumerate(cons):
    text(ex, 164 - i * 5, a, 6.5, bold=(i >= 5))
    text(ex + 110, 164 - i * 5, b, 6.5, "r", bold=(i >= 5))
text(ex, 124, "Nobreak 600 VA (~360 W) com folga para o pico.", 6.5)
text(ex, 119, "Autonomia curta (~10 min a 100 W): só para desligar com segurança.", 6.5)
text(ex, 114, "Valores estimados; medir com a tomada Shelly (Fase 4).", 6.5)

c.showPage()

# ---------------- FOLHA 3 ----------------
frame_and_title(3, "Antenas fixas, painel coaxial e base de encaixe do kit portátil")
text(25, 272, "LIGAÇÃO: MASTRO -> PAINEL COAXIAL -> BASE DE ENCAIXE -> NÓ 2", 10, bold=True)

ants = [("1090 colinear", "+ LNA (bias-tee)"), ("QFH 137", "caseira"), ("GP 400", "1/4 onda ~18 cm"),
        ("GP 433", "1/4 onda ~17 cm"), ("Fibra 915", "5-6 dBi")]
devs = [("SDR ADS-B fixo", "fica em casa", 1), ("SDR 1 (kit)", "SatDump 137", 0.8),
        ("SDR 2 (kit)", "rtl_433 / sonda", 0.8), ("SDR 2 (kit)", "alterna 400/433", 0.8),
        ("Heltec V3 (kit)", "base Meshtastic", 0.8)]
rows_y = [248, 234, 220, 206, 192]
for k, ((t, s_), y) in enumerate(zip(ants, rows_y)):
    box(25, y, 38, 11, t, s_, ts=6.2, ss_=5)
    rect(68, y + 3.5, 5, 4, 0.4, fill=0.6)              # DPS
    line(73, y + 5.5, 105, y + 5.5, 0.6)                 # coax
    c.circle(P(108), P(y + 5.5), P(1.6), stroke=1, fill=1)
    text(112, y + 4.5, f"P{k + 1}", 5.5)
text(70.5, 261, "DPS", 5.5, "c")
text(89, 261, "coaxial ~10 m", 5.5, "c")
rect(103, 186, 17, 72, 0.6, dash=(2, 1.5))
text(111.5, 259.5, "PAINEL", 5.5, "c", bold=True)
c.circle(P(108), P(186 + 3.5), P(1.6), stroke=1, fill=0)
text(112, 188.5, "P6", 5.5)
# pigtails para dispositivos (P3 e P4 vão para o mesmo SDR 2, um por vez)
dev_y = [248, 234, 213, None, 192]
for k, y in enumerate(rows_y):
    ty = dev_y[k] if dev_y[k] is not None else 213
    line(109.6, y + 5.5, 140, ty + 5.5, 0.4, dash=None if k != 3 else (2, 1.5))
for k, y in enumerate([248, 234, 213, 192]):
    t, s_, f = [devs[0], devs[1], devs[2], devs[4]][k]
    box(140, y, 42, 11, t, s_, fill=f, ts=6.2, ss_=5)
box(140, 176, 42, 11, "GPS USB (kit)", "na janela", fill=0.8, ts=6.2, ss_=5)
box(140, 162, 42, 11, "Wi-Fi MT7612U (kit)", "Kismet do Wi-Fi", fill=0.8, ts=6.2, ss_=5)
rect(195, 180, 30, 76, 0.6, fill=0.93)
text(210, 222, "HUB", 7, "c", bold=True)
text(210, 217, "USB 3", 5.8, "c")
text(210, 212, "7 portas", 5.8, "c")
text(210, 207, "alimentado", 5.8, "c")
for y in (253.5, 239.5, 218.5, 197.5, 181.5):
    arrow(182, y, 195, min(max(y, 183), 254))
line(182, 167.5, 188, 167.5, 0.4)
line(188, 167.5, 188, 183, 0.4)
arrow(188, 183, 195, 183)
box(195, 162, 50, 13, "Nó 2 - VM \"radio\"", "passthrough por porta USB", ts=6.4, ss_=5.2)
arrow(225, 180, 225, 175)
rect(25, 150, 4, 3, 0.4, fill=0.8)
text(31, 150.3, "viaja com o kit portátil", 5.6)
rect(80, 150, 4, 3, 0.4, fill=1)
text(86, 150.3, "fica em casa", 5.6)
rect(118, 150, 4, 3, 0.4, fill=0.6)
text(124, 150.3, "DPS: protetor de surto coaxial, na entrada da casa", 5.6)

# Rotina
text(25, 140, "ROTINA", 8, bold=True)
rot = [
    "SAIR: 1. Pôr os serviços do kit em manutenção no Uptime Kuma.  2. Desligar a VM \"radio\" ou parar o perfil casa.",
    "      3. Soltar os pigtails P2-P5 e o hub dos dispositivos do kit.  4. Guardar tudo no case Vonder MAI 415 (desenho do kit).",
    "VOLTAR: 1. Reconectar os dispositivos no hub e os pigtails no painel.  2. Subir o perfil casa (docker compose).",
    "        3. O Syncthing, a fila do InfluxDB e a ponte MQTT descarregam o que o kit coletou fora.",
    "O ADS-B fixo nunca para: os feeders (FlightAware, ADSBx) continuam no ar com o kit fora.",
]
for i, r_ in enumerate(rot):
    text(25, 134 - i * 5, r_, 5.9, bold=(i == 4))

# Lista de materiais
text(25, 104, "LISTA DE MATERIAIS - ANTENAS FIXAS E BASE", 8, bold=True)
bom3 = [
    ("It.", "Qtd", "Descrição"),
    ("1", "1", "RTL-SDR Blog V3 dedicado ao ADS-B (fica em casa)"),
    ("2", "1", "LNA + filtro 1090 MHz no mastro, alimentado por bias-tee do V3"),
    ("3", "5", "Antenas fixas: colinear 1090, QFH 137, GP 400, GP 433, fibra 915"),
    ("4", "5", "Coaxial ~10 m: 4 x LMR-240 + 1 x LMR-400 (915 MHz), conectores"),
    ("5", "5", "DPS coaxial + aterramento do mastro"),
    ("6", "1", "Mastro galvanizado 1\" + braços e braçadeiras inox"),
    ("7", "1", "Painel coaxial: chapa com 6 SMA passa-parede + 6 pigtails SMA"),
    ("8", "1", "Hub USB 3 alimentado, 7 portas (base de encaixe)"),
]
for r, row in enumerate(bom3):
    y = 104 - 4 - r * 5.2
    if r == 0:
        rect(25, y - 1.6, 220, 5.2, 0.3, fill=0.88)
    else:
        line(25, y - 1.6, 245, y - 1.6, 0.2)
    for k, val in enumerate(row):
        text(25 + 1.5 + [0, 8, 18][k], y, val, 6.2, bold=(r == 0))
rect(25, 104 - 4 - (len(bom3) - 1) * 5.2 - 1.6, 220, len(bom3) * 5.2, 0.4)
text(25, 104 - 4 - len(bom3) * 5.2 - 3, "SDR 1, SDR 2, Heltec, GPS e Wi-Fi são os do kit portátil (lista no desenho do kit).", 5.8)

# Tabela casa x campo
tx, ty = 255, 268
text(tx, ty + 2, "CADA RÁDIO: EM CASA x NO CAMPO", 8, bold=True)
rad = [
    ("Equip.", "Em casa (nó 2)", "No campo (kit)", "Viaja"),
    ("SDR ADS-B", "readsb + feeders", "-", "não"),
    ("SDR 1", "SatDump 137 (QFH)", "ADS-B", "sim"),
    ("SDR 2", "rtl_433 / sonda", "multiuso", "sim"),
    ("Heltec V3", "base Meshtastic", "rede da equipe", "sim"),
    ("GPS USB", "hora (chrony)", "hora e posição", "sim"),
    ("Wi-Fi MT7612U", "Kismet: Wi-Fi da casa", "auditoria autoriz.", "sim"),
    ("SSD 1 TB", "backup", "gravações, mapas", "sim"),
]
cols = [0, 22, 66, 108, 135]
for r, row in enumerate(rad):
    y = ty - 4 - r * 5.2
    if r == 0:
        rect(tx, y - 1.6, 150, 5.2, 0.3, fill=0.88)
    else:
        line(tx, y - 1.6, tx + 150, y - 1.6, 0.2)
    for k, val in enumerate(row):
        text(tx + 1.5 + cols[k] if k < 3 else tx + 1.5 + cols[k + 1] - 8, y, val, 5.9, bold=(r == 0))
rect(tx, ty - 4 - (len(rad) - 1) * 5.2 - 1.6, 150, len(rad) * 5.2, 0.4)

# Mastro
mx = 285
text(255, 214, "MASTRO (ELEVAÇÃO, S/E)", 8, bold=True)
line(255, 92, 330, 92, 0.6)
line(255, 92, 268, 104, 0.6)
line(268, 104, 330, 104, 0.6)
text(318, 96, "TELHADO", 5.5, "c")
line(mx, 104, mx, 196, 1.2)
line(mx, 196, mx, 207, 0.8)
rect(mx + 1.5, 192, 6, 4, 0.4, fill=0.6)
text(mx + 9, 201, "1090 colinear + LNA", 5.5)
for k in range(5):
    c.ellipse(P(mx - 5), P(174 + k * 3), P(mx + 5), P(176 + k * 3), stroke=1, fill=0)
text(mx + 8, 180, "QFH 137", 5.5)
line(mx, 160, mx - 18, 160, 0.5)
line(mx - 18, 160, mx - 18, 169, 0.6)
for d in (-3, 3):
    line(mx - 18, 160, mx - 18 + d * 1.6, 157, 0.4)
text(mx - 30, 171, "GP 400", 5.5)
line(mx, 148, mx + 18, 148, 0.5)
line(mx + 18, 148, mx + 18, 156, 0.6)
for d in (-3, 3):
    line(mx + 18, 148, mx + 18 + d * 1.6, 145, 0.4)
text(mx + 21, 152, "GP 433", 5.5)
line(mx, 134, mx - 14, 134, 0.5)
line(mx - 14, 134, mx - 14, 146, 1.0)
text(mx - 31, 140, "fibra 915", 5.5)
line(mx + 2, 130, mx + 2, 106, 0.8)
line(mx + 2, 106, mx + 25, 106, 0.8)
arrow(mx + 25, 106, mx + 25, 98)
text(mx + 27, 108, "5 coaxiais", 5.3)
text(mx + 27, 100, "-> DPS -> rack", 5.3)
line(mx, 104, mx, 96, 0.4, dash=(1.5, 1))
line(mx - 3, 96, mx + 3, 96, 0.6)
text(mx - 22, 96.5, "aterramento", 5.3)
dim_v(mx + 45, 104, 196, "~2 m acima do telhado", ext_from=mx + 2, side="r")

# Perdas
nx3 = 345
text(nx3, 214, "PERDA NO COAXIAL (10 m)", 7.5, bold=True)
loss = [("137 MHz LMR-240", "~1,4 dB"), ("400/433 LMR-240", "~2,5 dB"), ("915 LMR-400", "~1,3 dB"),
        ("1090 LMR-240", "~3,9 dB *"), ("* compensada pelo LNA", "")]
for i, (a, b) in enumerate(loss):
    text(nx3, 208 - i * 5, a, 6.1)
    text(nx3 + 58, 208 - i * 5, b, 6.1, "r")
text(nx3, 180, "Consumo da base", 7.5, bold=True)
for i, (a, b) in enumerate([("Hub + 3 SDR + LNA", "~6 W"), ("Heltec, GPS, Wi-Fi", "~3 W"), ("Total", "~10 W")]):
    text(nx3, 174 - i * 5, a, 6.1, bold=(i == 2))
    text(nx3 + 58, 174 - i * 5, b, 6.1, "r", bold=(i == 2))

text(255, 84, "NOTAS", 8, bold=True)
notas3 = [
    "1. Perdas típicas de catálogo: confirmar com o cabo comprado.",
    "2. Pigtails curtos do painel ao SDR; nada de coaxial longo no kit.",
    "3. Antenas a >= 1 m entre si; a de 1090 no topo, sem obstáculos.",
    "4. Mastro aterrado e DPS em todos os coaxiais. Em tempestade, solte o painel.",
]
for i, n in enumerate(notas3):
    text(255, 78 - i * 4.6, n, 5.9)

c.showPage()
c.save()
print("ok", OUT)
