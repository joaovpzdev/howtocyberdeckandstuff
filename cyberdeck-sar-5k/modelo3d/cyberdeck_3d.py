"""Peças impressas em 3D do cyberdeck SAR - edição R$ 5 mil (case Patola MP-0039).

Gera STLs paramétricos com manifold3d + trimesh.
    pip install manifold3d trimesh
    python cyberdeck_3d.py

Coordenadas (mm): x = comprimento (esquerda->direita), y = frente(0) -> fundo/dobradiça,
z = altura a partir do fundo interno do case.
"""
import os
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection, JoinType

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
os.makedirs(OUT, exist_ok=True)

# ---------------- Parâmetros principais ----------------
CASE_INT = (390, 315)          # interno do Patola MP-0039 (base 95 + tampa 40)
CH_W, CH_D = 360, 250          # chassi com folga de ~6 mm por lado
CORNER_R = 14                  # canto arredondado
FLOOR_T = 3
DECK_Z = 80                    # face inferior do painel (base do MP-0039 tem 95 mm)
DECK_T = 3
SPLIT_X = CH_W / 2             # emenda das metades (cabem em mesa 256 x 256)
FAN = 60                       # ventoinhas 60 x 60 x 15 mm (slim), 5 V
FAN_T = 15
FAN_HOLE = 50                  # furação da ventoinha 60 mm
SEG = 64


def box(x, y, z, dx, dy, dz):
    return Manifold.cube([dx, dy, dz]).translate([x, y, z])


def cbox(cx, cy, z, dx, dy, dz):
    return box(cx - dx / 2, cy - dy / 2, z, dx, dy, dz)


def cyl(cx, cy, z, h, r, seg=SEG):
    return Manifold.cylinder(h, r, r, seg).translate([cx, cy, z])


def rounded_plate(w, d, t, r, z=0):
    cs = CrossSection.square([w - 2 * r, d - 2 * r]).translate([r, r]).offset(r, JoinType.Round, 2.0, SEG)
    return Manifold.extrude(cs, t).translate([0, 0, z])


def union(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out


# Posições comuns
PILLARS = [(12, 12), (12, 125), (12, 238), (348, 12), (348, 125), (348, 238),
           (168, 70), (192, 70), (168, 150), (192, 150), (168, 238), (192, 238)]
TALA_Y = (100, 200)        # talas do painel
TRAY_TALA_Y = (95, 125)    # talas da bandeja (livres do compartimento do power bank)
TALA_DX = (-16, -8, 8, 16)
PI_ORIGIN = (46, 84.5)  # canto inferior esquerdo da placa do Pi 5 (85 x 56)
PI_HOLES = [(3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)]
FAN_IN = (88, 112)       # ventoinha de entrada, sobre a pilha do Pi
FAN_OUT = (300, 140)     # ventoinha de exaustão
USB_DEVICES = [          # (nome, x0, y0, comprimento, largura)
    ("Expansão: SDR", 205, 65, 72, 27),
    ("Expansão: Wi-Fi", 205, 100, 84, 32),
    ("Expansão: 4G", 205, 140, 95, 30),
    ("Expansão: SSD", 205, 180, 100, 30),
]
TROUGH = (25, 10, 335, 55)  # x0, y0, x1, y1 do porta-antenas
CONN_Y = 228
SMA = [(30, "LoRa"), (80, "GPS")]   # demais SMA ficam para as expansões
RJ45 = (140, CONN_Y)
USBC = (215, CONN_Y)
TOGGLE = (245, CONN_Y)
DSI_NOTCH = (100, 125)
# Compartimento do power bank USB-C PD (20.000 mAh, slim). Ajuste PB_IN ao seu modelo.
PB_IN = (154, 70, 30)      # comprimento x largura x altura útil (mm)
PB_ORIGIN = (22, 162)      # canto interno do compartimento
PB_WALL = 2.5
PB_STRAP_X = (60, 140)     # posições das orelhas da cinta de velcro (20 mm)


def tray():
    parts = [rounded_plate(CH_W, CH_D, FLOOR_T, CORNER_R)]
    # pilares até o painel
    for x, y in PILLARS:
        parts.append(cbox(x, y, 0, 10, 10, DECK_Z))
    # standoffs da pilha UPS X1202 + Pi 5 (baterias ficam sob a UPS)
    for hx, hy in PI_HOLES:
        parts.append(cyl(PI_ORIGIN[0] + hx, PI_ORIGIN[1] + hy, 0, FLOOR_T + 24, 3.5))
    # berços dos dispositivos USB
    for _, x0, y0, L, W in USB_DEVICES:
        parts.append(box(x0, y0 - 2.5, 0, L, 2.5, FLOOR_T + 8))
        parts.append(box(x0, y0 + W + 0.6, 0, L, 2.5, FLOOR_T + 8))
        parts.append(box(x0 + L, y0 - 2.5, 0, 2.5, W + 5.6, FLOOR_T + 8))
    # compartimento do power bank: paredes + orelhas com rasgo para cinta de velcro
    px0, py0 = PB_ORIGIN
    pl, pw, ph = PB_IN
    ring = box(px0 - PB_WALL, py0 - PB_WALL, 0, pl + 2 * PB_WALL, pw + 2 * PB_WALL, FLOOR_T + 14)
    ring = ring - box(px0, py0, FLOOR_T, pl, pw, 20)
    parts.append(ring)
    for sx in PB_STRAP_X:
        for ty in (py0 - PB_WALL - 4, py0 + pw + PB_WALL):
            parts.append(box(sx - 13, ty, 0, 26, 4, FLOOR_T + ph + 9))
    # porta-antenas: 3 canais
    x0, y0, x1, y1 = TROUGH
    for yy in (y0, y0 + 15, y0 + 30, y1 - 2):
        parts.append(box(x0, yy, 0, x1 - x0, 2, FLOOR_T + 14))
    solid = union(parts)
    holes = []
    for x, y in PILLARS:
        holes.append(cyl(x, y, DECK_Z - 15, 16, 1.6))           # M3 autoatarraxante
    for hx, hy in PI_HOLES:
        holes.append(cyl(PI_ORIGIN[0] + hx, PI_ORIGIN[1] + hy, -1, 40, 1.35))  # M2.5
    for _, x0, y0, L, W in USB_DEVICES:                          # passa-abraçadeira
        holes.append(cbox(x0 + L / 2, y0 - 5.5, -1, 4, 3, 10))
        holes.append(cbox(x0 + L / 2, y0 + W + 4.6, -1, 4, 3, 10))
    for ty in TRAY_TALA_Y:
        for dx in TALA_DX:
            holes.append(cyl(SPLIT_X + dx, ty, -1, 10, 1.4))
    for sx in PB_STRAP_X:                                         # rasgos da cinta (22 x 3)
        holes.append(cbox(sx, PB_ORIGIN[1] + PB_IN[1] / 2, FLOOR_T + PB_IN[2] + 2, 22, PB_IN[1] + 30, 3))
    # alívio de peso / passagem de cabos no piso
    holes.append(cbox(150, 112, -1, 20, 50, 10))
    holes.append(cbox(180, 222, -1, 12, 10, 10))
    return solid - union(holes)


def fan_grille(cx, cy, z, t):
    disk = cyl(cx, cy, z - 1, t + 2, FAN / 2 - 1.5)
    slots = union([cbox(cx + k * 7, cy, z - 1, 4, FAN, t + 2) for k in range(-4, 5)])
    cut = disk ^ slots
    screws = union([cyl(cx + sx, cy + sy, z - 1, t + 2, 1.7)
                    for sx in (-FAN_HOLE / 2, FAN_HOLE / 2) for sy in (-FAN_HOLE / 2, FAN_HOLE / 2)])
    return cut + screws


def vent_array(x0, y0, x1, y1, z, t):
    return union([box(x, y0, z - 1, 3, y1 - y0, t + 2) for x in np.arange(x0, x1 - 2, 6)])


def deck():
    z = 0
    plate = rounded_plate(CH_W, CH_D, DECK_T, CORNER_R, z)
    cuts = []
    x0, y0, x1, y1 = TROUGH
    cuts.append(box(x0, y0, z - 1, x1 - x0, y1 - y0, DECK_T + 2))   # acesso ao porta-antenas
    cuts.append(fan_grille(*FAN_IN, z, DECK_T))
    cuts.append(fan_grille(*FAN_OUT, z, DECK_T))
    cuts.append(vent_array(120, 165, 160, 205, z, DECK_T))
    cuts.append(vent_array(200, 180, 262, 205, z, DECK_T))
    for x, _ in SMA:
        cuts.append(cyl(x, CONN_Y, z - 1, DECK_T + 2, 3.3))
    cuts.append(cbox(*RJ45, z - 1, 14.8, 16.4, DECK_T + 2))         # keystone RJ45
    cuts.append(cbox(*USBC, z - 1, 9.6, 4.2, DECK_T + 2))           # USB-C de painel
    cuts.append(cyl(USBC[0] - 10, USBC[1], z - 1, DECK_T + 2, 1.7))
    cuts.append(cyl(USBC[0] + 10, USBC[1], z - 1, DECK_T + 2, 1.7))
    cuts.append(cyl(*TOGGLE, z - 1, DECK_T + 2, 6.1))               # chave das ventoinhas
    cuts.append(box(DSI_NOTCH[0], CH_D - 6, z - 1, DSI_NOTCH[1] - DSI_NOTCH[0], 7, DECK_T + 2))
    for x, y in PILLARS:
        cuts.append(cyl(x, y, z - 1, DECK_T + 2, 1.7))
    for ty in TALA_Y:
        for dx in TALA_DX:
            cuts.append(cyl(SPLIT_X + dx, ty, z - 1, DECK_T + 2, 1.4))
    return plate - union(cuts)


DISP = (189.5, 120.0, 15.0)     # Raspberry Pi Touch Display 2 7"
VIEW = (155.5, 88.0)


def display_frame():
    W, D, T = 215, 146, 3
    inner = (DISP[0] + 2, DISP[1] + 2.5)
    wall_out = (inner[0] + 9.5, inner[1] + 9.5)
    plate = rounded_plate(W, D, T, 6)
    cx, cy = W / 2, D / 2
    ring = cbox(cx, cy, T, *wall_out, DISP[2] + 1) - cbox(cx, cy, T - 1, *inner, DISP[2] + 3)
    solid = plate + ring
    cuts = [cbox(cx, cy, -1, VIEW[0] + 1.5, VIEW[1] + 2, T + 2),
            cbox(cx + wall_out[0] / 2 - 2, cy, T + DISP[2] - 7, 8, 30, 10)]   # saída do cabo DSI/energia
    for sx in (-60, 60):
        for sy in (-(wall_out[1] + inner[1]) / 4, (wall_out[1] + inner[1]) / 4):
            cuts.append(cyl(cx + sx, cy + sy, T + DISP[2] - 9, 11, 1.25))
    return solid - union(cuts)


def travessa():
    span = (DISP[1] + 2.5 + DISP[1] + 2.5 + 9.5) / 2  # distância entre furos
    bar = box(0, 0, 0, 12, span + 16, 4)
    holes = union([cyl(6, 8, -1, 6, 1.7), cyl(6, 8 + span, -1, 6, 1.7)])
    return bar - holes


def tala():
    plate = box(0, 0, 0, 40, 16, 4)
    holes = union([cyl(20 + dx, 8, -1, 6, 1.7) for dx in TALA_DX])
    return plate - holes


def calco(gap):
    """Calço que trava a bandeja no case: encosta na borda do piso e na parede do case."""
    t = gap - 1.0 + 3.0            # 3 mm avançam sobre a borda do piso da bandeja
    return box(0, 0, 0, 60, t, 20) - box(-1, -1, -1, 62, 4, FLOOR_T + 1.5)


def split(m, at_x, width, depth, height):
    left = m ^ box(-1, -1, -1, at_x + 1, depth + 2, height + 2)
    right = (m ^ box(at_x, -1, -1, width, depth + 2, height + 2)).translate([-at_x, 0, 0])
    return left, right


def save(m, name):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts))
    path = os.path.join(OUT, name)
    tm.export(path)
    b = tm.bounds
    print(f"{name:32s} {b[1][0]-b[0][0]:6.1f} x {b[1][1]-b[0][1]:6.1f} x {b[1][2]-b[0][2]:6.1f} mm  "
          f"vol {tm.volume/1000:7.1f} cm3  watertight={tm.is_watertight}")
    return tm


if __name__ == "__main__":
    t = tray()
    d = deck()
    tl, tr = split(t, SPLIT_X, CH_W, CH_D, DECK_Z)
    dl, dr = split(d, SPLIT_X, CH_W, CH_D, DECK_T)
    save(tl, "01_bandeja_esquerda.stl")
    save(tr, "02_bandeja_direita.stl")
    save(dl, "03_painel_esquerdo.stl")
    save(dr, "04_painel_direito.stl")
    save(display_frame(), "05_moldura_tela.stl")
    save(travessa(), "06_travessa_tela_x2.stl")
    save(tala(), "07_tala_emenda_x4.stl")
    gap_y = (CASE_INT[1] - CH_D) / 2
    gap_x = (CASE_INT[0] - CH_W) / 2
    if gap_y > 3:
        save(calco(gap_y), "08_calco_frente_fundo_x4.stl")
    if gap_x > 3:
        save(calco(gap_x), "09_calco_lateral_x2.stl")
    asm = t + d.translate([0, 0, DECK_Z])
    save(asm, "00_montagem_referencia.stl")
