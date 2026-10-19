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
OUT = os.path.join(BASE, "cyberdeck_sar_edicao_5k.pdf")

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", F + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

INK = colors.HexColor("#1F2A33")
ACC = colors.HexColor("#C8501E")   # laranja de resgate
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


def block_diagram():
    d = Drawing(170 * mm, 78 * mm)

    def box(x, y, w, h, t, s=None, fill=TINT, stroke=INK):
        d.add(Rect(x * mm, y * mm, w * mm, h * mm, rx=2, ry=2, fillColor=fill, strokeColor=stroke, strokeWidth=0.6))
        d.add(String((x + w / 2) * mm, (y + h / 2 + (1.2 if s else -1.2)) * mm, t, fontName="DVB", fontSize=7.5,
                     textAnchor="middle", fillColor=INK))
        if s:
            d.add(String((x + w / 2) * mm, (y + h / 2 - 3.2) * mm, s, fontName="DV", fontSize=6.3,
                         textAnchor="middle", fillColor=MUTED))

    def arrow(x1, y1, x2, y2):
        d.add(Line(x1 * mm, y1 * mm, x2 * mm, y2 * mm, strokeColor=MUTED, strokeWidth=0.7))
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        s = 1.6
        pts = [x2, y2, x2 - s * math.cos(a - 0.4), y2 - s * math.sin(a - 0.4),
               x2 - s * math.cos(a + 0.4), y2 - s * math.sin(a + 0.4)]
        d.add(Polygon([p * mm for p in pts], fillColor=MUTED, strokeColor=MUTED, strokeWidth=0.3))

    box(0, 62, 34, 11, "USB-C do painel", "carga")
    box(0, 46, 34, 11, "Power bank", "20.000 mAh")
    box(0, 30, 34, 11, "UPS X1202", "4 x 18650")
    arrow(17, 62, 17, 57)
    arrow(17, 46, 17, 41)
    box(52, 28, 46, 22, "Raspberry Pi 5", "16 GB", fill=colors.HexColor("#FBE9E1"), stroke=ACC)
    arrow(34, 35.5, 52, 37)
    box(52, 62, 46, 11, "Tela touch 7\"", "na tampa")
    arrow(75, 50, 75, 62)
    box(52, 6, 46, 13, "HAT RAK6421", "LoRa + GPS + sensor")
    arrow(75, 28, 75, 19)
    box(116, 62, 54, 11, "RTL-SDR", "ADS-B / espectro")
    box(116, 47, 54, 11, "Wi-Fi monitor", "auditoria autorizada")
    box(116, 32, 54, 11, "Modem 4G", "backhaul Tailscale")
    box(116, 17, 54, 11, "SSD NVMe", "logs e mapas")
    box(116, 2, 54, 11, "RJ45", "sensor Suricata")
    for y in (67.5, 52.5, 37.5, 22.5, 7.5):
        arrow(98, 39, 116, y)
    return d


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("DV", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, 12 * mm, "Cyberdeck SAR – edição R$ 5 mil  ·  v1.0  ·  out/2026")
        canvas.drawRightString(190 * mm, 12 * mm, f"{doc.page}")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    else:
        canvas.setFillColor(ACC)
        canvas.rect(0, 0, 8 * mm, A4[1], stroke=0, fill=1)
    canvas.restoreState()


def block_diagram_5k():
    import math
    d = Drawing(170 * mm, 70 * mm)

    def box(x, y, w, h, t, s=None, fill=TINT, stroke=INK, dash=None):
        r = Rect(x * mm, y * mm, w * mm, h * mm, rx=2, ry=2, fillColor=fill, strokeColor=stroke, strokeWidth=0.6)
        if dash:
            r.strokeDashArray = dash
        d.add(r)
        d.add(String((x + w / 2) * mm, (y + h / 2 + (1.2 if s else -1.2)) * mm, t, fontName="DVB", fontSize=7.5,
                     textAnchor="middle", fillColor=INK))
        if s:
            d.add(String((x + w / 2) * mm, (y + h / 2 - 3.2) * mm, s, fontName="DV", fontSize=6.3,
                         textAnchor="middle", fillColor=MUTED))

    def arrow(x1, y1, x2, y2):
        d.add(Line(x1 * mm, y1 * mm, x2 * mm, y2 * mm, strokeColor=MUTED, strokeWidth=0.7))
        a = math.atan2(y2 - y1, x2 - x1)
        s = 1.6
        pts = [x2, y2, x2 - s * math.cos(a - 0.4), y2 - s * math.sin(a - 0.4),
               x2 - s * math.cos(a + 0.4), y2 - s * math.sin(a + 0.4)]
        d.add(Polygon([p * mm for p in pts], fillColor=MUTED, strokeColor=MUTED, strokeWidth=0.3))

    box(0, 52, 36, 11, "USB-C do painel", "carga")
    box(0, 30, 36, 13, "UPS X1202", "4 x 18650, ~37 Wh")
    arrow(18, 52, 18, 43)
    box(54, 26, 46, 22, "Raspberry Pi 5", "8 GB", fill=colors.HexColor("#FBE9E1"), stroke=ACC)
    arrow(36, 36.5, 54, 37)
    box(54, 56, 46, 11, "Tela touch 7\"", "na tampa")
    arrow(77, 48, 77, 56)
    box(54, 3, 46, 13, "HAT RAK6421", "LoRa 1 W + GPS")
    arrow(77, 26, 77, 16)
    box(118, 44, 52, 11, "RJ45", "sensor Suricata")
    arrow(100, 40, 118, 49.5)
    box(118, 18, 52, 20, "Expansões", "SDR, Wi-Fi, 4G, SSD", fill=colors.white, dash=[3, 2])
    arrow(100, 34, 118, 28)
    box(0, 6, 36, 13, "Power bank", "opcional, 20.000 mAh", fill=colors.white, dash=[3, 2])
    arrow(18, 19, 18, 30)
    return d


story = []

# ---------------- CAPA ----------------
story += [Spacer(1, 45 * mm),
          P("Cyberdeck SAR", "title"),
          Spacer(1, 3 * mm),
          P("Edição R$ 5 mil", "h1"),
          P("Análise do projeto completo e versão enxuta que mantém a missão central: comunicação mesh, posição das equipes e mapa em campo", "subtitle"),
          Spacer(1, 12 * mm)]
img = os.path.join(ROOT, "modelo3d", "render", "montagem.png")
if os.path.exists(img):
    story += [Image(img, width=110 * mm, height=82 * mm), Spacer(1, 2 * mm),
              P("Estrutura interna impressa em 3D, ajustada para o case Patola MP-0039.", "caption")]
story += [Spacer(1, 18 * mm),
          table([["Documento", "Edição R$ 5 mil: análise, materiais, montagem e evolução"],
                 ["Autor", "João Victor Paixão Zolim · github.com/joaovpzdev"],
                 ["Versão / data", "1.0 · 17 de outubro de 2026"],
                 ["Base", "Projeto completo Cyberdeck SAR (Pelican 1450, ~R$ 9.500)"]],
                [45 * mm, 125 * mm], header=False),
          PageBreak()]

# ---------------- 1. RESUMO ----------------
story += [P("1. Resumo", "h1"),
          P("O projeto completo custa cerca de <b>R$ 9.500</b>. Esta edição cabe em <b>R$ 5.000</b>, já com uma reserva de "
            "R$ 275 para frete, impostos e imprevistos, sem abrir mão do que faz o kit ser útil numa operação de busca e "
            "salvamento: <b>rede mesh LoRa de 1 W, GPS, tela touch, mapa offline, UPS interna e proteção IP67</b>."),
          P("A economia vem de três decisões: trocar o Pelican 1450 pelo <b>Patola MP-0039</b> (também IP67, fabricado no "
            "Brasil, R$ 486), usar o <b>Raspberry Pi 5 de 8 GB</b> no lugar do de 16 GB e deixar como <b>expansão futura</b> "
            "tudo o que não é essencial para a missão (SDR, Wi-Fi em modo monitor, modem 4G, SSD, segundo rádio e sensor ambiental)."),
          callout("<b>Nada se perde:</b> as peças impressas são as mesmas da versão completa, com o painel 15 mm mais baixo e "
                  "6 calços para travar a bandeja no case. Os berços das expansões já vêm impressos, então cada upgrade é só "
                  "comprar a peça e encaixar."),
          Spacer(1, 3 * mm)]

# ---------------- 2. ANÁLISE ----------------
story += [P("2. Análise do projeto completo", "h1"),
          P("2.1 Onde está o dinheiro", "h2"),
          table([
              ["Grupo", "Itens", "R$", "% do total"],
              ["Computação", "Pi 5 16 GB, SSD NVMe + gaveta, microSD, dissipador", "2.570", "27%"],
              ["Expansões", "SDR, Wi-Fi monitor, 2º rádio, sensor ambiental, modem 4G, carregador veicular, painel solar", "1.820", "19%"],
              ["Case", "Pelican 1450", "1.850", "19%"],
              ["Interface", "Touch Display 2 + teclado Bluetooth", "910", "10%"],
              ["Energia", "UPS X1202 + baterias, power bank", "860", "9%"],
              ["Estrutura", "Ventoinhas, conectores de painel, filamento, parafusos", "750", "8%"],
              ["Rádio principal", "HAT RAK6421 + LoRa 1 W + GPS + antenas", "740", "8%"],
              ["<b>Total</b>", "", "<b>9.500</b>", "<b>100%</b>"],
          ], [30 * mm, 98 * mm, 20 * mm, 22 * mm]),
          P("O rádio LoRa e o GPS, que são o coração da missão, custam só 8% do total. Quase metade do dinheiro está em "
            "computação de sobra, no case de marca e em recursos que não são usados em toda operação."),
          P("2.2 Pontos fortes", "h2"),
          bullets([
              "Arquitetura clara: computador, rádio e energia bem separados, com caminho de expansão definido.",
              "Case sem furos e operação com a tampa aberta: boa solução para vedação e calor ao mesmo tempo.",
              "Modelo 3D paramétrico: muda o case ou uma medida e todas as peças são geradas de novo.",
              "Compra por fases, cada uma entregando uma capacidade completa.",
          ]),
          P("2.3 Riscos e pontos a resolver", "h2"),
          table([
              ["Ponto", "Risco", "Encaminhamento"],
              ["Medidas não conferidas", "Furação da UPS X1202, área útil da tela e medidas dos dongles vieram de catálogo.", "Conferir com as peças em mãos antes de imprimir (checklist no README)."],
              ["Dois rádios no meshtasticd", "Suporte não confirmado.", "Edição 5 mil usa um rádio; o 2º fica para depois de testado."],
              ["Potência de 1 W", "Limites de potência e de antena na faixa de 915 MHz.", "Conferir o regulamento da Anatel antes de transmitir em 1 W."],
              ["Folga UPS x power bank", "Só 0,5 mm entre a parede do compartimento e a UPS.", "Medir; se preciso, reduzir PB_IN ou mover PB_ORIGIN."],
              ["Mistura de propósitos", "Recursos de Blue Team (Suricata, Wi-Fi monitor) aumentam custo e consumo sem servir à busca.", "Separados como expansão; o Suricata leve continua pela porta RJ45."],
              ["Dependência de importação", "RAK e Geekworm vêm de fora: prazo e imposto incertos.", "Reserva de R$ 275 e compra antecipada desses itens."],
              ["Consumo com tudo ligado", "~18–20 W derrubam a autonomia interna para ~2 h.", "Na edição 5 mil o consumo cai para ~10 W (~3,5 h na UPS)."],
          ], [36 * mm, 64 * mm, 70 * mm]),
          P("2.4 Critério de corte", "h2"),
          P("Ficou tudo o que serve diretamente à missão central (comunicar, saber onde cada equipe está, registrar e "
            "aguentar o campo). Saiu, como expansão, tudo o que amplia o kit mas não é indispensável em toda operação."),
          Spacer(1, 4 * mm)]

# ---------------- 3. A EDIÇÃO ----------------
story += [P("3. A edição R$ 5 mil", "h1"),
          table([
              ["Fica", "Muda", "Vira expansão"],
              ["Rede mesh LoRa 1 W (RAK13302)<br/>GPS (RAK12501)<br/>Tela touch 7\"<br/>UPS X1202 com 4 x 18650<br/>"
               "Proteção IP67, sem furos<br/>Operação aberta com 2 ventoinhas<br/>Porta RJ45 (Suricata leve)<br/>Peças impressas e porta-antenas",
               "Pelican 1450 → Patola MP-0039<br/>Pi 5 16 GB → Pi 5 8 GB<br/>SSD NVMe → microSD 128 GB High Endurance<br/>"
               "Ventoinhas 60 x 25 → 60 x 15 mm<br/>Painel a 80 mm do fundo + 6 calços<br/>Power bank vira opcional",
               "RTL-SDR (ADS-B)<br/>Wi-Fi em modo monitor<br/>Modem 4G<br/>SSD NVMe<br/>2º rádio LoRa<br/>Sensor ambiental<br/>"
               "Teclado Bluetooth<br/>Carregador veicular e painel solar"],
          ], [56 * mm, 60 * mm, 54 * mm], header=False),
          Spacer(1, 4 * mm),
          block_diagram_5k(),
          Spacer(1, 2 * mm),
          P("Figura 1 – Blocos da edição R$ 5 mil. Tracejado = opcional ou expansão.", "caption"),
          KeepTogether([P("3.1 Lista de materiais", "h2"),
          table([
              ["Fase", "Item", "R$"],
              ["1", "Raspberry Pi 5 8 GB (lacrado)", "1.560"],
              ["1", "HAT RAK6421 + RAK13302 (LoRa 1 W) + RAK12501 (GPS) *", "~550"],
              ["1", "Antena LoRa 915 MHz + antena GPS ativa *", "~190"],
              ["1", "microSD 128 GB High Endurance + dissipador baixo *", "~150"],
              ["2", "Case Patola MP-0039 IP67 (Patola Store)", "486"],
              ["2", "UPS Geekworm X1202 + 4 baterias 18650 *", "~560"],
              ["2", "2 ventoinhas 60 x 15 mm 5 V + filtro de espuma *", "~150"],
              ["2", "SMA de painel x2, keystone RJ45, USB-C de painel, chave, cabos *", "~150"],
              ["2", "Filamento PETG/ASA ~1 kg + parafusos *", "~170"],
              ["3", "Raspberry Pi Touch Display 2 7\"", "759"],
              ["", "<b>Subtotal das peças</b>", "<b>~4.725</b>"],
              ["", "Reserva para frete, impostos e imprevistos", "~275"],
              ["", "<b>Total</b>", "<b>5.000</b>"],
          ], [14 * mm, 132 * mm, 24 * mm]),
          P("* Estimativa. Preços conferidos em outubro de 2026: Pi 5 8 GB lacrado (OLX), Touch Display 2 (RoboCore) e "
            "Patola MP-0039 (Patola Store). Itens importados variam com frete e impostos.", "small")]),
          Spacer(1, 4 * mm)]

# ---------------- 4. COMPARATIVO ----------------
story += [P("4. Completo x R$ 5 mil", "h1"),
          table([
              ["Item", "Projeto completo", "Edição R$ 5 mil"],
              ["Case", "Pelican 1450, IP67, 372 x 260 x 155", "Patola MP-0039, IP67, 390 x 315 x 135"],
              ["Computador", "Pi 5 16 GB", "Pi 5 8 GB"],
              ["Armazenamento", "SSD NVMe 512 GB + microSD", "microSD 128 GB High Endurance"],
              ["Rádios", "2 LoRa + SDR + Wi-Fi monitor + 4G", "1 LoRa 1 W"],
              ["GPS e sensores", "GPS + sensor ambiental", "GPS"],
              ["Tela", "Touch 7\" + teclado Bluetooth", "Touch 7\""],
              ["Energia", "UPS + power bank, ~97 Wh", "UPS ~37 Wh (power bank opcional)"],
              ["Consumo / autonomia", "~18–20 W / ~5 h", "~10 W / ~3,5 h (~9 h com power bank)"],
              ["Ventilação", "2 x 60 x 25 mm", "2 x 60 x 15 mm (slim)"],
              ["Peças impressas", "11 peças", "17 peças (as mesmas + 6 calços)"],
              ["Custo", "~R$ 9.500", "R$ 5.000 com reserva"],
          ], [36 * mm, 67 * mm, 67 * mm]),
          P("A autonomia sobe por proporção: sem SDR, Wi-Fi monitor e modem 4G, o consumo cai pela metade e a UPS sozinha "
            "dura quase o dobro do que duraria com tudo ligado."),
          P("5. Estrutura física", "h1"),
          bullets([
              "<b>Case:</b> Patola MP-0039, 420 x 365 x 150 mm por fora e 390 x 315 x 135 por dentro (base com 95 mm), IP67, 1,96 kg. "
              "Sem furos.",
              "<b>Bandeja e painel:</b> os mesmos arquivos da versão completa, gerados com o painel a 80 mm do fundo. "
              "A pilha do Pi fica 8 mm abaixo da ventoinha de entrada.",
              "<b>Calços:</b> 4 de frente/fundo (60 x 34,5 x 20 mm) e 2 laterais (60 x 17 x 20 mm) apoiam na borda do piso e travam a bandeja no case maior.",
              "<b>Ventoinhas slim de 60 x 15 mm</b> para caber sob o painel mais baixo.",
              "<b>Painel:</b> só os furos SMA de LoRa e GPS; os das expansões são abertos quando elas forem instaladas.",
              "<b>Tampa:</b> a mesma moldura da tela (23 mm de espessura), com folga na tampa de ~40 mm.",
          ])]
img2 = os.path.join(ROOT, "modelo3d", "render", "bandeja.png")
if os.path.exists(img2):
    story += [Image(img2, width=70 * mm, height=52 * mm),
              P("Figura 2 – Metade esquerda da bandeja (pilares de 80 mm).", "caption")]
story += [Spacer(1, 4 * mm)]

# ---------------- 6. MONTAGEM ----------------
story += [P("6. Montagem", "h1"),
          table([
              ["Fase", "Entrega", "Custo acumulado"],
              ["1", "Rede LoRa + GPS funcionando na bancada (acesso por SSH ou pelo navegador)", "~R$ 2.450"],
              ["2", "Kit portátil e protegido, com UPS e ventilação", "~R$ 3.966"],
              ["3", "Tela touch: o kit funciona sozinho, sem outro aparelho", "~R$ 4.725"],
          ], [14 * mm, 124 * mm, 32 * mm]),
          P("6.1 Passo a passo", "h2"),
          numbered([
              "Conferir as medidas reais da UPS, da tela e das baterias; ajustar o modelo 3D se precisar.",
              "Imprimir as 17 peças e unir as metades com as talas (parafusos M3).",
              "Montar a pilha: UPS X1202 nos standoffs, Pi 5 com dissipador baixo e HAT RAK6421.",
              "Instalar no painel as 2 SMA (LoRa e GPS), o RJ45, o USB-C, a chave e as ventoinhas slim com filtro.",
              "Ligar os cabos, parafusar o painel nos pilares e testar na bancada.",
              "Colocar a bandeja no case e encaixar os 6 calços.",
              "Fixar a moldura com a tela na tampa com fita VHB.",
          ]),
          P("6.2 Validação", "h2"),
          bullets([
              "Meshtastic conversando com outro rádio e mostrando posições no mapa.",
              "GPS com posição fixa usando a antena do lado de fora.",
              "1 hora em carga com o Pi abaixo de ~80 °C (ventoinhas slim movem menos ar: medir).",
              "Autonomia real com tudo ligado e troca de fonte sem o Pi reiniciar.",
          ]),
          P("7. Aplicabilidade", "h1"),
          table([
              ["Uso", "Edição R$ 5 mil"],
              ["Busca e salvamento", "Atende: mesh, posição das equipes, mapa offline e registro."],
              ["Desastres e Defesa Civil", "Atende como ponto de coordenação sem rede celular."],
              ["Trilhas, expedições e eventos", "Atende: rastreamento do grupo e mensagens."],
              ["Monitoramento de rede", "Parcial: Suricata leve pela porta RJ45."],
              ["Apoio a drones", "Parcial: precisa do 2º rádio; sem ADS-B até instalar o SDR."],
              ["Link com a base em campo", "Só com Wi-Fi disponível; sem modem 4G."],
          ], [50 * mm, 120 * mm]),
          P("8. Caminho de evolução", "h1"),
          P("Ordem sugerida, da melhoria que mais rende para a menos urgente:"),
          table([
              ["Ordem", "Upgrade", "R$ aprox."],
              ["1", "Power bank 20.000 mAh pass-through (autonomia de ~3,5 h para ~9 h)", "300"],
              ["2", "RTL-SDR Blog V3 + antena (ADS-B antes de voar drone)", "350"],
              ["3", "2º rádio LoRa (canal do drone), depois de validado no meshtasticd", "250"],
              ["4", "Modem 4G USB (link com a base em campo)", "300"],
              ["5", "SSD NVMe + gaveta USB (logs e mapas grandes)", "450"],
              ["6", "Adaptador Wi-Fi MT7612U (modo monitor)", "200"],
              ["7", "Pelican 1450 (~R$ 1.850) ou Vonder MAI 415 (~R$ 400, mesmas medidas externas): DECK_Z = 95 e STL de novo", "400–1.850"],
          ], [16 * mm, 128 * mm, 26 * mm]),
          P("9. Conformidade", "h1"),
          bullets([
              "LoRa em 915 MHz: conferir na Anatel o limite de potência e de ganho de antena antes de usar 1 W; usar equipamentos homologados.",
              "Posições de equipes e vítimas são dados pessoais (LGPD): canal criptografado, acesso restrito e descarte após o relatório.",
              "As regras podem mudar; confirmar nas fontes oficiais antes de operar.",
          ]),
          ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                        bottomMargin=22 * mm, title="Cyberdeck SAR – edição R$ 5 mil",
                        author="João Victor Paixão Zolim")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("ok", OUT)
