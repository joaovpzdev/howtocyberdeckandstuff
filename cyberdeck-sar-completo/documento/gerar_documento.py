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
OUT = os.path.join(BASE, "cyberdeck_sar_conceito_montagem_aplicabilidade.pdf")

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
        canvas.drawString(20 * mm, 12 * mm, "Cyberdeck SAR – conceito, montagem e aplicabilidade  ·  v1.0  ·  out/2026")
        canvas.drawRightString(190 * mm, 12 * mm, f"{doc.page}")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    else:
        canvas.setFillColor(ACC)
        canvas.rect(0, 0, 8 * mm, A4[1], stroke=0, fill=1)
    canvas.restoreState()


story = []

# ---------------- CAPA ----------------
story += [Spacer(1, 45 * mm),
          P("Cyberdeck SAR", "title"),
          Spacer(1, 4 * mm),
          P("Kit portátil de comunicação mesh, posicionamento e consciência situacional para operações de busca e salvamento", "subtitle"),
          Spacer(1, 14 * mm)]
img = os.path.join(ROOT, "modelo3d", "render", "montagem.png")
if os.path.exists(img):
    story += [Image(img, width=120 * mm, height=90 * mm), Spacer(1, 2 * mm),
              P("Estrutura interna impressa em 3D (bandeja e painel) prevista para o Pelican 1450.", "caption")]
story += [Spacer(1, 22 * mm),
          table([["Documento", "Conceito, montagem e aplicabilidade"],
                 ["Autor", "João Victor Paixão Zolim · github.com/joaovpzdev"],
                 ["Versão / data", "1.0 · 17 de outubro de 2026"],
                 ["Documentos relacionados", "Desenho técnico A3 (4 folhas), modelos 3D (STL) e README de montagem"]],
                [45 * mm, 125 * mm], header=False),
          PageBreak()]

# ---------------- 1. RESUMO ----------------
story += [P("1. Resumo", "h1"),
          P("O Cyberdeck SAR é uma estação de campo autônoma, montada num case Pelican 1450, que dá a uma equipe de "
            "busca e salvamento três coisas que costumam faltar justamente onde as operações acontecem: "
            "<b>comunicação sem depender de rede celular</b>, <b>posição de cada equipe num mapa comum</b> e "
            "<b>registro do que foi feito</b>."),
          P("O núcleo é um Raspberry Pi 5 com uma placa de rádio LoRa (Meshtastic) e GPS. Cada socorrista leva um "
            "rádio Meshtastic pequeno; as posições e mensagens chegam ao cyberdeck pela rede mesh, que se estende "
            "de rádio em rádio. A tela touch na tampa mostra o mapa offline da área, as equipes e o histórico. "
            "Recursos extras (receptor SDR, Wi-Fi em modo monitor, modem 4G e sensor Suricata) ampliam o uso para "
            "segurança aérea, diagnóstico de rádio e monitoramento de rede."),
          callout("<b>Em uma frase:</b> uma central de comando de bolso que funciona sem internet, aguenta clima "
                  "hostil fechada e se mantém ligada por cerca de 5 horas com tudo funcionando."),
          Spacer(1, 4 * mm)]

# ---------------- 2. CONCEITO ----------------
story += [P("2. Conceito", "h1"),
          P("2.1 O problema", "h2"),
          bullets([
              "Buscas em mata, serra, áreas rurais e zonas de desastre acontecem com frequência <b>sem sinal de celular</b> "
              "ou com a rede congestionada.",
              "Rádios de voz resolvem a conversa, mas não mostram <b>onde cada equipe está</b> nem guardam o trajeto percorrido.",
              "Sem registro das áreas já vasculhadas, a coordenação repete setores e perde tempo, que é o recurso mais "
              "crítico numa busca.",
          ]),
          P("2.2 A solução", "h2"),
          P("Uma rede de rádios LoRa forma uma <b>malha (mesh)</b>: cada rádio repassa as mensagens dos outros, então o "
            "alcance cresce a cada equipe em campo. O cyberdeck é o ponto central dessa malha. Ele recebe posições GPS "
            "e mensagens curtas, mostra tudo num mapa offline, grava o histórico e, quando há internet (4G ou Wi-Fi), "
            "sincroniza com uma base remota pelo Tailscale."),
          P("2.3 Princípios de projeto", "h2"),
          table([
              ["Princípio", "Como o projeto atende"],
              ["Robustez", "Case Pelican 1450 IP67, sem nenhum furo; peças internas em ASA ou PETG, resistentes ao calor."],
              ["Autonomia", "UPS interna + power bank: ~97 Wh, cerca de 5 h com tudo ligado; recarga por tomada, viatura ou painel solar."],
              ["Operação aberta", "Funciona com a tampa aberta: tela na tampa, conectores e ventoinhas no painel, ar circulando de um lado ao outro."],
              ["Independência de rede", "LoRa e GPS funcionam sem internet; mapas e dados ficam no SSD local."],
              ["Modularidade", "Compra em 5 fases; cada fase já entrega uma capacidade útil."],
              ["Manutenção em campo", "Peças impressas substituíveis, conectores padronizados (SMA, USB-C, RJ45), recarga sem desmontar."],
          ], [42 * mm, 128 * mm]),
          PageBreak()]

# ---------------- 3. ARQUITETURA ----------------
story += [P("3. Arquitetura", "h1"),
          P("O diagrama mostra os blocos principais: o caminho da energia à esquerda, o computador ao centro e os "
            "rádios e periféricos à direita."),
          block_diagram(),
          Spacer(1, 2 * mm),
          P("Figura 1 – Diagrama de blocos simplificado.", "caption"),
          P("3.1 Componentes e funções", "h2"),
          table([
              ["Camada", "Componente", "Função"],
              ["Computação", "Raspberry Pi 5 16 GB + SSD NVMe 512 GB", "Roda o Meshtastic (meshtasticd), mapas offline, Suricata e registros."],
              ["Rádio mesh", "HAT RAK6421 + RAK13302 (LoRa 1 W)", "Rede de mensagens e posições entre equipes, em 915 MHz."],
              ["Rádio extra", "RAK13300 (2º LoRa)", "Canal separado, previsto para o rastreador de um drone (a validar)."],
              ["Posicionamento", "RAK12501 GPS + antena ativa", "Posição e hora precisas da base."],
              ["Ambiente", "RAK1906", "Temperatura, umidade e pressão no local da operação."],
              ["Interface", "Touch Display 2 de 7\" + teclado Bluetooth", "Mapa, mensagens e status sem precisar de outro aparelho."],
              ["Escuta de rádio", "RTL-SDR Blog V3", "Recebe ADS-B (posição de aeronaves) e analisa o espectro."],
              ["Rede", "Adaptador Wi-Fi MT7612U, modem 4G, porta RJ45", "Auditoria Wi-Fi autorizada, link com a base e sensor de rede."],
              ["Energia", "UPS X1202 (4 x 18650) + power bank 20.000 mAh", "Fonte interna com troca de fonte sem desligar."],
          ], [28 * mm, 60 * mm, 82 * mm]),
          KeepTogether([P("3.2 Software", "h2"),
          bullets([
              "<b>Raspberry Pi OS</b> 64 bits como sistema base.",
              "<b>meshtasticd</b>: o Meshtastic rodando direto no Linux, usando o rádio do HAT.",
              "<b>Mapa offline</b> com as camadas da região baixadas antes da operação.",
              "<b>Suricata</b> e <b>agente Zabbix</b> para monitorar rede e saúde do próprio kit (temperatura, bateria, disco).",
              "<b>Tailscale</b> para acesso seguro à base quando houver internet.",
          ])])]

# ---------------- 4. ESTRUTURA FÍSICA ----------------
story += [P("4. Estrutura física", "h1"),
          P("4.1 Case", "h2"),
          P("O Pelican 1450 (interno 372 x 260 x 155 mm; base de 111 mm e tampa de 44 mm) foi escolhido pelo tamanho "
            "certo para o conjunto, pela vedação IP67 e pela válvula automática de pressão. É vendido no Brasil pela "
            "CasesBR, que se apresenta como distribuidor autorizado, por cerca de R$ 1.850. <b>O case não recebe nenhum "
            "furo</b>: fechado, a vedação continua intacta."),
          P("<b>Alternativa mais barata:</b> a Vonder MAI 415 tem as mesmas medidas externas do Pelican 1450 "
            "(406 x 330 x 174 mm) e interno de 375 x 270 x 150 mm, por cerca de R$ 400. A bandeja de 360 x 250 mm cabe; "
            "confirme a altura da base antes de imprimir. O anúncio indica IP67, mas uma ficha técnica cita IP54: "
            "teste submerso ao receber."),
          P("4.2 Organização interna", "h2"),
          table([
              ["Nível", "O que tem"],
              ["Bandeja (piso)", "Pilha UPS + Pi 5 + HAT, berços dos dongles USB, compartimento do power bank e porta-antenas de 3 canais."],
              ["Painel (a 95 mm do fundo)", "2 ventoinhas de 60 mm, aberturas de ventilação, 6 conectores SMA, RJ45, USB-C de carga e chave das ventoinhas."],
              ["Tampa", "Moldura impressa com a tela de 7\", presa com fita VHB."],
          ], [45 * mm, 125 * mm])]
img2 = os.path.join(ROOT, "modelo3d", "render", "bandeja.png")
if os.path.exists(img2):
    story += [Spacer(1, 3 * mm), Image(img2, width=72 * mm, height=54 * mm),
              P("Figura 2 – Metade esquerda da bandeja: pilares, apoios da pilha, porta-antenas e compartimento do power bank.", "caption")]
story += [P("4.3 Ventilação", "h2"),
          P("Com a tampa aberta, a ventoinha de entrada joga ar sobre o Raspberry Pi; o ar atravessa a bandeja e sai "
            "pela ventoinha de exaustão do outro lado. Um filtro de espuma na entrada segura a poeira. Fechado, o kit "
            "é guardado desligado ou em espera: o case não foi feito para operar fechado."),
          KeepTogether([P("4.4 Peças impressas", "h2"),
          P("São 7 modelos (11 peças no total). Bandeja e painel são divididos ao meio para caber numa impressora de "
            "256 x 256 mm e unidos por talas. Material recomendado: <b>ASA</b> (melhor contra sol e calor) ou PETG; "
            "PLA não deve ser usado porque deforma acima de ~55 °C. Consumo estimado: ~1 kg de filamento. O modelo é "
            "paramétrico: as medidas ficam no topo do arquivo-fonte e todos os arquivos podem ser gerados de novo.")]),
          Spacer(1, 4 * mm)]

# ---------------- 5. MONTAGEM ----------------
story += [P("5. Montagem", "h1"),
          P("5.1 Fases de compra", "h2"),
          P("Cada fase entrega uma capacidade completa, então o kit é útil antes de estar terminado."),
          table([
              ["Fase", "Entrega", "Itens principais", "Estimativa"],
              ["1", "Rede LoRa + GPS na bancada", "Pi 5 16 GB, HAT RAK6421 com LoRa 1 W e GPS, antenas, SSD", "~R$ 3.310"],
              ["2", "Kit portátil e protegido", "Pelican 1450, UPS + baterias, power bank, ventoinhas, conectores, impressão", "~R$ 3.460"],
              ["3", "Interface própria", "Touch Display 2 de 7\" e teclado Bluetooth", "~R$ 910"],
              ["4", "Rádios extras", "RTL-SDR Blog V3, Wi-Fi MT7612U, 2º rádio LoRa, sensor ambiental", "~R$ 920"],
              ["5", "Operação de campo", "Modem 4G, carregador veicular USB-C PD, painel solar dobrável", "~R$ 900"],
              ["", "<b>Total</b>", "", "<b>~R$ 9.500</b>"],
          ], [13 * mm, 45 * mm, 85 * mm, 27 * mm]),
          P("Valores de outubro de 2026. Itens importados são estimativas e variam com frete e impostos.", "small"),
          P("5.2 Antes de imprimir", "h2"),
          bullets([
              "Confirmar a furação da UPS X1202 (padrão do Pi 5, 58 x 49 mm) e a altura das baterias sob ela.",
              "Medir os dongles USB e o power bank (compartimento de até 152 x 68 x 30 mm).",
              "Conferir onde fica a área útil da tela em relação à borda, para alinhar a janela da moldura.",
              "Se algo não bater, ajustar os parâmetros no arquivo-fonte e gerar os STL de novo.",
          ]),
          P("5.3 Passo a passo", "h2"),
          numbered([
              "Imprimir as peças e unir as metades da bandeja e do painel com as talas (parafusos M3).",
              "Montar a pilha: UPS X1202 nos standoffs, Pi 5 com dissipador baixo e HAT RAK6421 com barra de pinos estendida.",
              "Prender os dongles USB nos berços com abraçadeiras.",
              "Colocar o power bank no compartimento, prender com cintas de velcro e ligar: USB-C do painel -> power bank -> UPS.",
              "Instalar no painel os conectores SMA, o RJ45, o USB-C, a chave e as ventoinhas (com filtro na entrada).",
              "Ligar os cabos, parafusar o painel nos pilares e testar tudo na bancada.",
              "Fixar a moldura com a tela na tampa usando fita VHB, sem furar o case.",
              "Guardar antenas e sílica gel e fechar.",
          ]),
          P("5.4 Validação na bancada", "h2"),
          bullets([
              "O Meshtastic conversa com outro rádio e mostra posições no mapa.",
              "O GPS fixa posição com a antena do lado de fora.",
              "Medir o consumo real e a autonomia com tudo ligado.",
              "Rodar 1 hora em carga e checar a temperatura do Pi (abaixo de ~80 °C).",
              "Simular a troca de fonte (plugar e desplugar o carregador) sem o Pi reiniciar.",
          ]),
          Spacer(1, 4 * mm)]

# ---------------- 6. OPERAÇÃO ----------------
story += [P("6. Operação em campo", "h1"),
          table([
              ["Momento", "Rotina"],
              ["Antes de sair", "Carga completa; mapas da área baixados; canal privado configurado e chaves distribuídas aos rádios da equipe; teste rápido de todos os rádios."],
              ["Instalação", "Abrir em local alto e à sombra; rosquear antenas; antena GPS do lado de fora com vista do céu; ligar e conferir posições."],
              ["Durante", "Acompanhar equipes no mapa; registrar setores vasculhados; monitorar temperatura e bateria; usar o ADS-B antes de qualquer voo de drone."],
              ["Ao encerrar", "Exportar trajetos e mensagens para o relatório; desligar pelo sistema; guardar antenas; recarregar."],
          ], [32 * mm, 138 * mm]),
          P("6.1 Energia", "h2"),
          bullets([
              "Interna: ~37 Wh da UPS e ~60 Wh úteis do power bank, cerca de 5 horas com tudo ligado.",
              "Recarga com a tampa aberta pelo USB-C do painel: tomada, viatura 12 V (USB-C PD) ou painel solar dobrável.",
              "O power bank precisa ter carga com passagem de energia (pass-through); a UPS segura o Pi nos cortes ao trocar a fonte.",
              "Para economizar, desligue o que não estiver em uso: SDR, Wi-Fi monitor e modem 4G.",
          ]),
          P("6.2 Clima hostil", "h2"),
          bullets([
              "<b>Chuva:</b> fechado é IP67; aberto, a tela e o painel não são vedados. Operar sob toldo ou abrigo.",
              "<b>Poeira:</b> filtro de espuma na entrada de ar, limpo após cada uso.",
              "<b>Umidade e maresia:</b> verniz conformal nas placas e sílica gel no case.",
              "<b>Calor:</b> o Pi reduz o desempenho perto de 85 °C; deixar à sombra com a tampa aberta.",
              "<b>Baterias:</b> carregar apenas entre 0 e 45 °C; nunca deixar carregando fechado ao sol.",
          ]),
          PageBreak()]

# ---------------- 7. APLICABILIDADE ----------------
story += [P("7. Aplicabilidade", "h1"),
          P("O mesmo kit serve a vários cenários em que é preciso coordenar pessoas sem infraestrutura de comunicação."),
          table([
              ["Cenário", "Como o kit ajuda"],
              ["Busca e salvamento (SAR)", "Posição das equipes num mapa comum, mensagens sem celular, histórico de setores vasculhados e base para o relatório."],
              ["Desastres e Defesa Civil", "Comunicação quando a rede celular cai ou congestiona; ponto de coordenação temporário em abrigos e áreas atingidas."],
              ["Apoio a drones", "Com um rastreador LoRa no drone: última posição conhecida, drone como repetidor da malha e checagem de aeronaves pelo ADS-B antes do voo."],
              ["Eventos e grandes áreas", "Coordenação de brigadas, socorristas e voluntários em trilhas, provas de montanha e eventos rurais."],
              ["Expedições e trilhas", "Rastreamento do grupo, mensagens entre equipes separadas e dados ambientais da área."],
              ["Monitoramento de rede", "Sensor Suricata portátil e agente Zabbix, ligado à base pelo Tailscale (uso de Blue Team)."],
              ["Ensino e portfólio", "Projeto documentado de ponta a ponta: hardware, rádio, Linux, redes, segurança e impressão 3D."],
          ], [42 * mm, 128 * mm]),
          P("7.1 Integração com outros projetos", "h2"),
          bullets([
              "<b>Homelab:</b> em casa ou com 4G, os registros e alertas vão para o Zabbix/Wazuh do servidor central.",
              "<b>Drone (fase futura):</b> o segundo rádio LoRa fica reservado para um canal só do drone.",
          ]),
          P("8. Limitações", "h1"),
          bullets([
              "LoRa transmite pouca informação: posições, mensagens curtas e telemetria leve. Não serve para voz, vídeo ou controle de drone.",
              "O alcance depende do relevo e da altura das antenas; em vales e mata fechada pode cair muito sem repetidores.",
              "Aberto, o kit não é vedado contra chuva.",
              "Peças e furações foram projetadas com medidas de catálogo e precisam ser conferidas antes da impressão.",
              "O uso de dois rádios ao mesmo tempo no meshtasticd ainda precisa ser validado.",
          ]),
          KeepTogether([P("9. Conformidade e segurança", "h1"),
          bullets([
              "<b>Rádio:</b> o LoRa opera em 915 MHz. Antes de usar 1 W, conferir no regulamento de radiação restrita da Anatel o limite de potência e de ganho de antena. Usar equipamentos homologados.",
              "<b>SDR e ADS-B:</b> apenas recepção.",
              "<b>Wi-Fi:</b> auditoria somente em redes próprias ou com autorização expressa.",
              "<b>Drones:</b> cadastro no SISANT (ANAC) e autorização de voo no SARPAS (DECEA); operações com órgãos públicos seguem regras próprias.",
              "<b>Dados pessoais:</b> posições de equipes e de vítimas são dados sensíveis (LGPD). Usar canal criptografado, limitar o acesso e apagar o que não for necessário após o relatório.",
          ]),
          Spacer(1, 2 * mm),
          P("As regras citadas podem mudar; confirme nas fontes oficiais antes de operar.", "small")])]

# ---------------- 10. PRÓXIMOS PASSOS ----------------
story += [P("10. Próximos passos", "h1"),
          numbered([
              "Comprar a fase 1 e validar Meshtastic e GPS na bancada.",
              "Conferir as medidas reais das peças e ajustar o modelo 3D.",
              "Imprimir e montar a estrutura no Pelican (fase 2) e medir autonomia e temperatura.",
              "Escrever o procedimento operacional (checklist de saída, instalação e encerramento) e testar em campo.",
              "Desenvolver o nó LoRa do drone e testar o drone como repetidor.",
          ]),
          P("Arquivos do projeto", "h2"),
          table([
              ["Arquivo", "Conteúdo"],
              ["cyberdeck_sar_pelican1450_desenho_tecnico.pdf", "Desenho técnico A3: case, layout interno, peças 3D, blocos, materiais e energia."],
              ["modelo3d/stl/*.stl", "Peças prontas para impressão."],
              ["modelo3d/cyberdeck_3d.py", "Fonte paramétrica do modelo 3D."],
              ["README.md", "Guia rápido de montagem e impressão."],
              ["documento/…aplicabilidade.pdf", "Este documento."],
          ], [70 * mm, 100 * mm]),
          ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                        bottomMargin=22 * mm, title="Cyberdeck SAR – conceito, montagem e aplicabilidade",
                        author="João Victor Paixão Zolim")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("ok", OUT)
