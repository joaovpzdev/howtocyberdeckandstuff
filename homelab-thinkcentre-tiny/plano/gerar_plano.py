import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _base import *  # noqa: F401,F403
from xml.sax.saxutils import escape

pdfmetrics.registerFont(TTFont("DVM", F + "DejaVuSansMono.ttf"))
ss["h1"].keepWithNext = 1
ss["h2"].keepWithNext = 1
ss["code"] = ParagraphStyle("code", fontName="DVM", fontSize=7.6, leading=10.3, textColor=INK)


def code(txt):
    html = "<br/>".join(escape(l).replace(" ", "&nbsp;") for l in txt.strip("\n").split("\n"))
    t = Table([[Paragraph(html, ss["code"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINT), ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    t.spaceAfter = 6
    return t


def M(t):
    return f"<font name='DVM'>{escape(t)}</font>"


def brl(v):
    return f"{v:,.0f}".replace(",", ".")


def service(name, where, what, how=None, cmd=None):
    out = [P(name, "h2"),
           table([["Onde", where], ["O que faz", what]] + ([["Como", how]] if how else []),
                 [26 * mm, 144 * mm], header=False)]
    out.append(Spacer(1, 3))
    if cmd:
        out.append(code(cmd))
    return out


# ---------- custos ----------
fase2 = [("Lenovo M720q Tiny i5 8ª (nó 4), com fonte", 1250), ("2 x 16 GB DDR4 SODIMM", 500),
         ("SSD NVMe 1 TB", 400), ("Riser PCIe do M720q + suporte meia altura", 120),
         ("Placa Intel i350-T2 (usada)", 250)]
fase3 = [("RTL-SDR Blog V3 dedicado ao ADS-B (fica em casa)", 350),
         ("LNA + filtro 1090 MHz no mastro (bias-tee)", 250),
         ("Antenas fixas: colinear 1090, fibra 915, QFH e GPs caseiros", 610),
         ("Coaxial ~10 m: 4 x LMR-240 + 1 x LMR-400, com conectores", 600),
         ("5 DPS coaxiais + aterramento do mastro", 250), ("Mastro e braçadeiras inox", 200),
         ("Painel coaxial (6 SMA passa-parede) + 6 pigtails", 200),
         ("Hub USB 3 alimentado 7 portas (base de encaixe)", 150)]
fase3_revc = 4940
fase4 = [("Kit Sensor.Community (ESP8266 + SDS011 + BME280)", 200), ("Tomada Shelly com medição", 200)]
s2, s3, s4 = (sum(v for _, v in f) for f in (fase2, fase3, fase4))

story = []

# ---------- Capa ----------
story += [Spacer(1, 45 * mm),
          P("Homelab Lenovo Tiny · rev. D", "subtitle"), Spacer(1, 3 * mm),
          P("Monitoramento e<br/>observação global", "title"), Spacer(1, 6 * mm),
          P("Plano de expansão: sensor de rede, antenas fixas com base de encaixe para o kit portátil, "
            "feeds globais, sensores ambientais e uma central de observação no Grafana", "subtitle"),
          Spacer(1, 18 * mm),
          P("João Victor Paixão Zolim · github.com/joaovpzdev", "small"),
          P("Outubro de 2026 · acompanha o desenho técnico rev. D (3 folhas), o desenho do kit portátil e o guia "
            "\"Estação de satélite e biblioteca offline\" v1.0", "small"),
          PageBreak()]

# ---------- 1 ----------
story += [P("1. Visão geral", "h1"),
          P("O homelab passa a observar três coisas: <b>a própria rede</b> (o que entra e sai de casa), "
            "<b>o céu sobre São Paulo</b> (aviões, balões meteorológicos, satélites, rádio LoRa) e "
            "<b>o mundo</b> (incêndios, terremotos, alertas, saúde da internet e ameaças). Tudo termina "
            "numa só tela: a central de observação no Grafana."),
          table([
              ["Bloco", "O que entra", "Onde"],
              ["Sensor de rede", "Security Onion (Suricata + Zeek), ntopng, espelhamento de porta", "Nó 4 (novo, U5)"],
              ["Rádio", "ADS-B fixo 24 h; SatDump, rtl_433, radiossondas, Meshtastic e Kismet com os rádios do kit", "Mastro + base na U6 + VM no nó 2"],
              ["Kit portátil", "Notebook com os mesmos rádios no campo, sincronizando com o homelab", "Case Vonder MAI 415, Tailscale"],
              ["Feeds globais", "NASA FIRMS, INPE Queimadas, USGS, Cemaden/Defesa Civil, RIPE Atlas", "Nó 2 (Node-RED)"],
              ["Ameaças", "MISP, FreshRSS com feeds de CVE, honeypot Cowrie, CrowdSec", "Nós 1, 2 e 3"],
              ["Disponibilidade", "Uptime Kuma, changedetection.io, Loki (logs)", "Nós 1 e 2"],
              ["Ambiente", "Sensor.Community, Blitzortung, tomada Shelly", "Wi-Fi da casa"],
              ["Central", "Painéis do Grafana com mapa, rede, satélites, ambiente e energia", "Nó 1"],
          ], [30 * mm, 96 * mm, 44 * mm]),
          Spacer(1, 4 * mm),
          callout("<b>Mudança em relação à rev. C:</b> sai a caixa com o Raspberry Pi no telhado. Os rádios do "
                  "kit portátil fazem o papel dela quando você está em casa, encaixados numa base no rack; só o "
                  "RTL-SDR do ADS-B é exclusivo do homelab. O SatNOGS fica para depois. A Fase 3 cai de "
                  "~R$ 4.940 para ~R$ 2.610 (os rádios que viajam entram na conta do kit)."),
          ]

story += [P("Distribuição por nó", "h2"),
          table([
              ["Nó", "Serviços", "RAM usada (estim.)"],
              ["1 – monitoramento (16 GB)", "Zabbix, Wazuh, Pi-hole, Grafana + InfluxDB, Loki, Uptime Kuma, CrowdSec (central)", "~12 GB"],
              ["2 – dados (16 GB)", "Kiwix, Calibre-Web, MISP, Node-RED, Mosquitto, FreshRSS, changedetection.io, sonda RIPE Atlas, Minecraft, GLPI, VM \"radio\" (readsb, SatDump, rtl_433, sonda, gpsd, Kismet)", "~14 GB"],
              ["3 – lab (16 GB)", "AD, alvos (VLAN 30), honeypot Cowrie", "~10 GB"],
              ["4 – sensor (32 GB)", "Security Onion (VM, 26 GB) + ntopng (LXC, 2 GB)", "~30 GB"],
              ["Kit portátil (Acer Nitro V 15)", "Mesmo compose, perfil campo; Grafana + InfluxDB locais", "–"],
          ], [44 * mm, 98 * mm, 28 * mm]),
          P("No nó 2, a VM \"radio\" (2 GB) passa a reunir todos os serviços de rádio.", "small"),
          ]

# ---------- 2 Compras ----------
def fase_table(items):
    rows = [["Item", "R$ (estim.)"]] + [[a, f"~{brl(v)}"] for a, v in items]
    return table(rows, [140 * mm, 30 * mm])


story += [PageBreak(), P("2. Compras por fase", "h1"),
          P("Fase 1 é só software e não custa nada. As outras podem ser feitas em qualquer ordem."),
          P("Fase 2 – Sensor de rede (nó 4)", "h2"), fase_table(fase2),
          P(f"<b>Subtotal: ~R$ {brl(s2)}</b>"),
          P("Fase 3 – Antenas fixas e base de encaixe", "h2"), fase_table(fase3),
          P(f"<b>Subtotal: ~R$ {brl(s3)}</b> (rev. C: ~R$ {brl(fase3_revc)}). Os dois RTL-SDR, a Heltec, o GPS, "
            "o adaptador Wi-Fi e o SSD são comprados com o kit portátil (~R$ 2.635 essencial). O RTL-SDR de satélite da "
            "rev. B vira um dos dois do kit."),
          P("Fase 4 – Ambiente", "h2"), fase_table(fase4),
          P(f"<b>Subtotal: ~R$ {brl(s4)}</b>, mais a estação Blitzortung: o projeto fornece os kits aos "
            "participantes e a disponibilidade e o preço variam; consulte o site antes."),
          Spacer(1, 3 * mm),
          table([["Fase", "Total (estim.)"],
                 ["1 – Software", "R$ 0 (honeypot externo em VPS, se quiser: ~R$ 30/mês)"],
                 ["2 – Sensor de rede", f"~R$ {brl(s2)}"],
                 ["3 – Antenas fixas e base", f"~R$ {brl(s3)}"],
                 ["4 – Ambiente", f"~R$ {brl(s4)} + Blitzortung"],
                 ["<b>Total</b>", f"<b>~R$ {brl(s2 + s3 + s4)}</b>, mais o kit portátil (desenho próprio)"]],
                [50 * mm, 120 * mm]),
          P("Preços estimados em out/2026. Importados (RTL-SDR, LNA, Heltec) variam com frete e impostos; "
            "o M720q e a placa i350 são usados.", "small"),
          ]

# ---------- 3 Fase 1 ----------
story += [P("3. Fase 1 – Software (R$ 0)", "h1"),
          P("Quase tudo roda em Docker dentro de contêineres LXC (ative <i>nesting</i> nas opções do LXC). "
            "Um arquivo docker-compose por serviço, guardados num repositório do GitHub: é o que vai para o portfólio.")]
story += service("Grafana + InfluxDB – a central", "Nó 1, LXC \"observa\" (2 vCPU, 3 GB)",
                 "O InfluxDB guarda as séries (feeds, sensores, rádio). O Grafana desenha os painéis e lê também "
                 "Zabbix, Loki e o Elasticsearch do Security Onion.", None,
                 """services:
  influxdb:
    image: influxdb:2
    volumes: ["./influx:/var/lib/influxdb2"]
    ports: ["8086:8086"]
  grafana:
    image: grafana/grafana-oss
    volumes: ["./grafana:/var/lib/grafana"]
    ports: ["3000:3000"]""")
story += service("Loki – logs centralizados", "Nó 1, mesmo LXC",
                 "Recebe logs de todos os nós e do kit portátil pelo agente Grafana Alloy. É bem mais leve "
                 "que o Graylog, que exigiria outro OpenSearch ao lado do indexador do Wazuh.",
                 "Imagem " + M("grafana/loki") + " no compose; " + M("grafana/alloy") + " em cada host.")
story += service("Uptime Kuma", "Nó 1",
                 "Testa a cada minuto se cada serviço responde (HTTP, porta, DNS) e avisa no Telegram, "
                 "o mesmo bot do netwatch.", "Imagem " + M("louislam/uptime-kuma:1") + ", porta 3001.")
story += service("CrowdSec", "Agente nos hosts com serviço exposto; central no nó 1",
                 "Lê os logs, detecta força bruta e varreduras e bloqueia o IP. Compartilha e recebe listas de "
                 "IPs maliciosos da comunidade.", "Instalação pelo repositório oficial (docs.crowdsec.net).")
story += service("Node-RED – feeds globais", "Nó 2, LXC \"feeds\"",
                 "Busca os dados públicos em intervalos fixos e grava no InfluxDB.",
                 "Imagem " + M("nodered/node-red") + ", porta 1880. Um fluxo por fonte:")
story += [table([
    ["Fonte", "Dado", "Intervalo"],
    ["NASA FIRMS (API, chave gratuita)", "Focos de incêndio (VIIRS/MODIS) num raio escolhido", "15 min"],
    ["INPE – Programa Queimadas", "Focos no Brasil (dados abertos)", "1 h"],
    ["USGS (GeoJSON)", "Terremotos: " + M("earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"), "5 min"],
    ["Cemaden e Defesa Civil", "Alertas públicos (confira as APIs abertas disponíveis)", "15 min"],
    ["Cloudflare Radar / IODA", "Quedas de internet por país e por provedor", "1 h"],
    ["SondeHub, tar1090", "Balões e aviões recebidos pela VM \"radio\" e pelo kit", "1 min"],
], [50 * mm, 98 * mm, 22 * mm]), Spacer(1, 4)]
story += service("Sonda de software RIPE Atlas", "Nó 2, contêiner pequeno",
                 "Faz medições de ping, traceroute e DNS pedidas pela rede RIPE Atlas e ganha créditos para você "
                 "fazer as suas: medir sua rota até qualquer lugar do mundo.",
                 "Crie a conta em atlas.ripe.net, registre a chave pública que o contêiner gera e aguarde a aprovação. "
                 "Imagem comunitária: " + M("jamesits/ripe-atlas") + ".")
story += service("MISP – inteligência de ameaças", "Nó 2 (4 GB)",
                 "Plataforma de IOCs (IPs, domínios, hashes). Assine os feeds gratuitos da CIRCL e do próprio MISP "
                 "e conecte ao Wazuh e ao Security Onion para cruzar alertas com indicadores conhecidos.",
                 "Projeto oficial " + M("github.com/MISP/misp-docker") + ".")
story += service("FreshRSS – notícias e CVEs", "Nó 2",
                 "Leitor de RSS próprio. Feeds sugeridos: CISA KEV (vulnerabilidades exploradas), NVD, CERT.br, "
                 "boletins de fabricantes e sites de notícias de segurança.",
                 "Imagem " + M("freshrss/freshrss") + ".")
story += service("changedetection.io", "Nó 2",
                 "Avisa quando uma página muda: aviso de segurança de um fabricante, preço de peça, edital de vaga.",
                 "Imagem " + M("dgtlmoon/changedetection.io") + ", porta 5000.")
story += service("Honeypot Cowrie (interno)", "Nó 3, VLAN 30",
                 "Finge ser um servidor SSH/Telnet dentro do lab. Ninguém legítimo conecta nele: qualquer acesso é "
                 "alerta. Os logs vão para o Wazuh.",
                 "Imagem " + M("cowrie/cowrie") + ". Não abra porta no roteador. Para ver ataques reais da internet, "
                 "use um VPS separado (T-Pot pede 8–16 GB), nunca a rede de casa.")

# ---------- 4 Fase 2 ----------
story += [P("4. Fase 2 – Sensor de rede (nó 4)", "h1"),
          P("O Security Onion pede no mínimo <b>4 núcleos, 24 GB de RAM, 200 GB de disco e 2 placas de rede</b> "
            "no modo Standalone (o fabricante recomenda 32 GB ou mais). Por isso o nó 4 tem 32 GB e uma placa "
            "Intel i350 no riser PCIe do M720q, só para escutar."),
          P("4.1 Espelhamento no switch", "h2"),
          P("No TL-SG108E: <i>Monitoring → Port Mirror</i>. Porta espelho (destino): <b>7</b>. Porta espelhada: "
            "<b>1</b> (uplink do roteador), entrada e saída. A porta 7 vai para a primeira porta da i350."),
          P("4.2 Proxmox no nó 4", "h2"),
          P("A rede onboard fica na bridge normal (gerência). A porta da i350 vira uma bridge sem IP que repassa "
            "tudo para as VMs:"),
          code("""# /etc/network/interfaces
auto vmbr1
iface vmbr1 inet manual
    bridge-ports enp1s0f0
    bridge-stp off
    bridge-fd 0
    bridge-ageing 0      # repassa todos os pacotes, como um hub"""),
          P("4.3 Security Onion", "h2"),
          bullets([
              "VM com 4 vCPU, 26 GB de RAM, 300 GB no NVMe, duas placas virtio: " + M("vmbr0") + " (gerência) e "
              + M("vmbr1") + " (escuta).",
              "Instale pela ISO oficial no modo <b>Standalone</b>. Na escuta, escolha a placa de " + M("vmbr1") + ".",
              "Teste: gere tráfego de teste (ex.: " + M("curl http://testmynids.org/uid/index.html") +
              ") e veja o alerta no painel em segundos.",
          ]),
          P("4.4 ntopng", "h2"),
          P("LXC Debian (2 vCPU, 2 GB) com uma segunda placa em " + M("vmbr1") + ". Instale o ntopng Community "
            "pelo repositório da ntop e aponte para essa interface. Mostra, ao vivo, quem fala com quem, por qual "
            "protocolo e quanto."),
          callout("<b>Privacidade em casa:</b> o espelho vê o tráfego de todos na casa. Avise quem mora com você, "
                  "guarde o mínimo (retenção curta) e não abra o conteúdo de terceiros."),
          ]

# ---------- 5 Fase 3 ----------
story += [P("5. Fase 3 – Antenas fixas e base de encaixe", "h1"),
          P("As antenas ficam no mastro e descem por coaxial até um painel na U6 do rack. Os rádios do kit "
            "portátil encaixam ali quando você está em casa e vão no case Vonder MAI 415 quando você sai. Só um "
            "RTL-SDR fica sempre em casa: o do ADS-B, para os feeders nunca pararem. Desenho na folha 3."),
          P("5.1 Cada rádio, em casa e no campo", "h2"),
          table([
              ["Equipamento", "Serial", "Em casa (nó 2)", "No campo (kit)", "Viaja"],
              ["RTL-SDR V3 ADS-B", "ADSB", "readsb + feeders, LNA no mastro", "–", "não"],
              ["RTL-SDR V3 kit 1", "KIT1", "SatDump 137 MHz (QFH)", "ADS-B", "sim"],
              ["RTL-SDR V3 kit 2", "KIT2", "rtl_433; radiossonda nas janelas de lançamento", "multiuso", "sim"],
              ["Heltec V3", "–", "base Meshtastic (fibra 915 no mastro)", "rede da equipe", "sim"],
              ["GPS USB", "–", "hora da casa (gpsd + chrony)", "hora e posição", "sim"],
              ["Wi-Fi MT7612U", "–", "Kismet vigiando o Wi-Fi da casa", "auditoria autorizada", "sim"],
              ["SSD 1 TB", "–", "destino de backup", "gravações, mapas, Kiwix", "sim"],
          ], [30 * mm, 14 * mm, 58 * mm, 52 * mm, 16 * mm]),
          Spacer(1, 4),
          P("Grave o serial de cada RTL-SDR, um por vez, conectado sozinho:"),
          code("rtl_eeprom -d 0 -s ADSB      # depois KIT1 e KIT2"),
          KeepTogether([P("5.2 VM \"radio\" no nó 2", "h2"),
          bullets([
              "VM Debian 12 (2 vCPU, 2 GB) com Docker, driver do RTL-SDR Blog (guia v1.0, seção 3.2) e gpsd.",
              "Passe o hub para a VM <b>pela porta USB</b> (<i>Hardware → Add → USB Device → Use USB Port</i>), "
              "não pelo ID do aparelho: ao reconectar os rádios do kit, eles voltam para a VM sozinhos.",
              "O SDR do ADS-B liga o LNA do mastro pelo próprio coaxial (bias-tee), com a opção "
              + M("--enable-biastee") + " do readsb.",
          ])]),
          P("5.3 Um compose, dois perfis", "h2"),
          P("O mesmo arquivo roda no nó 2 e no notebook. Muda só o arquivo de variáveis:"),
          code("""# casa.env                      # campo.env
ADSB_SERIAL=ADSB                ADSB_SERIAL=KIT1
SAT_SERIAL=KIT1                 MULTI_SERIAL=KIT2
ISM_SERIAL=KIT2

services:
  adsb:
    image: ghcr.io/sdr-enthusiasts/docker-adsb-ultrafeeder
    environment:
      - READSB_DEVICE_TYPE=rtlsdr
      - READSB_RTLSDR_DEVICE=${ADSB_SERIAL}
  rtl433:
    profiles: ["casa"]
    command: -d :${ISM_SERIAL} -F "mqtt://no2:1883,user=radio,pass=***"

docker compose --env-file casa.env --profile casa up -d     # no nó 2
docker compose --env-file campo.env --profile campo up -d   # no notebook"""),
          ]
story += service("SatDump", "SDR KIT1, em casa",
                 "Igual ao guia v1.0, agora na VM \"radio\". Imagens em " + M("/srv/satelite") +
                 " no SSD do nó 2.")
story += service("Radiossondas e rtl_433", "SDR KIT2, em casa",
                 "O rtl_433 roda por padrão. Nas janelas de lançamento, o radiosonde_auto_rx assume o rádio "
                 "e envia ao SondeHub. Antes, confira no SondeHub se há lançamentos que cheguem a São Paulo.",
                 "Imagem " + M("ghcr.io/projecthorus/radiosonde_auto_rx") + ", agendada no cron da VM.")
story += service("Base Meshtastic", "Heltec V3 na base, antena fibra 915 no mastro (LMR-400)",
                 "Nó fixo e alto que amplia o alcance da rede do cyberdeck e registra no homelab as posições da "
                 "equipe e dos drones.",
                 "Papel ROUTER ou CLIENT; MQTT para o Mosquitto do nó 2, <b>sem</b> o servidor público "
                 "(posições da equipe ficam em casa, por LGPD).")
story += [callout("<b>SatNOGS:</b> fica para quando houver um RTL-SDR dedicado (~R$ 450 + antena turnstile). "
                  "A rede espera estações sempre disponíveis, o que não combina com rádios que viajam."),
          Spacer(1, 3),
          callout("<b>Raios:</b> mastro aterrado e DPS em todos os coaxiais na entrada da casa. "
                  "Em tempestade, solte os coaxiais do painel.")]

# ---------- 5b Integração com o kit ----------
story += [P("6. Integração com o kit portátil", "h1"),
          P("O notebook entra na rede do homelab pelo Tailscale, de qualquer lugar. Com internet (até o 4G do "
            "celular), os dados chegam ao vivo. Sem internet, ficam em fila e descarregam quando a conexão volta."),
          table([
              ["Dado", "Como chega", "Sem internet"],
              ["Séries (sensores, contagem de aviões, posição do kit)", "Replicação do InfluxDB (kit -> nó 1)", "Fila em disco"],
              ["Meshtastic, rtl_433, GPS", "Ponte do Mosquitto (kit -> nó 2)", "Fila persistente (QoS 1)"],
              ["Aviões", "readsb do kit envia Beast ao ultrafeeder de casa (porta 30004)", "Só ao vivo; histórico no notebook"],
              ["Imagens, gravações, Kismet", "Syncthing (pastas sincronizadas)", "Sincroniza depois"],
              ["Logs", "Grafana Alloy -> Loki", "Buffer em disco"],
          ], [52 * mm, 78 * mm, 40 * mm]),
          P("6.1 Replicação do InfluxDB (no notebook)", "h2"),
          code("""influx remote create --name homelab --remote-url http://no1:8086 \\
  --remote-api-token $TOKEN_KIT --remote-org-id $ORG_CASA
influx replication create --name kit-para-casa --remote-id <id> \\
  --local-bucket-id <bucket do kit> --remote-bucket-id <bucket kit no nó 1> \\
  --max-queue-bytes 1073741824     # até 1 GB de fila offline"""),
          P("6.2 Ponte do Mosquitto (no notebook)", "h2"),
          code("""# /mosquitto/config/mosquitto.conf
persistence true
connection homelab
address no2:1883
topic # out 1
remote_username kit
remote_password ***
cleansession false
max_queued_messages 100000"""),
          P("6.3 Regras do Tailscale", "h2"),
          P("Marque o notebook com a tag <b>kit</b> e libere só o necessário. Se ele for perdido, não alcança "
            "o resto do homelab, e você revoga só as credenciais dele."),
          code("""{
  "hosts": {"no1": "100.x.x.1", "no2": "100.x.x.2"},
  "acls": [
    {"action": "accept", "src": ["tag:kit"],
     "dst": ["no1:8086", "no1:3100", "no2:1883", "no2:30004", "no2:22000"]}
  ]
}"""),
          P("6.4 Sair e voltar", "h2"),
          numbered([
              "Antes de sair: janela de manutenção no Uptime Kuma para os serviços do kit; pare o perfil "
              "casa na VM \"radio\".",
              "Solte os pigtails P2–P5 e os dispositivos do kit do hub; guarde no case.",
              "Na volta: reconecte, suba o perfil casa. A fila do InfluxDB, a ponte MQTT e o Syncthing "
              "descarregam o que foi coletado fora.",
              "O ADS-B fixo nunca para.",
          ]),
          ]

# ---------- 6 Fase 4 ----------
story += [P("7. Fase 4 – Ambiente", "h1")]
story += service("Sensor.Community", "Fora de casa, na sombra, no Wi-Fi da casa",
                 "Mede partículas (PM2,5 e PM10), temperatura, umidade e pressão e publica no mapa mundial "
                 "de qualidade do ar.",
                 "Grave o firmware com a ferramenta do projeto, cadastre o sensor e ative também o envio para "
                 "o seu InfluxDB nas opções do firmware.")
story += service("Tomada Shelly com medição", "Entre o nobreak e a régua do rack",
                 "Mede o consumo real do rack: potência, energia do mês e custo.",
                 "API local HTTP lida pelo Zabbix (item HTTP agent) e enviada ao Grafana.")
story += service("Blitzortung", "Sótão ou forro, longe de fontes de ruído; cabo de rede no roteador",
                 "Estação da rede mundial de detecção de raios (lightningmaps.org). As estações próximas "
                 "triangulam cada descarga.",
                 "O projeto fornece os kits aos participantes e a disponibilidade e o preço variam. "
                 "Peça pelo site e informe a sua localização: regiões com poucas estações têm prioridade.")

# ---------- 7 Central ----------
story += [P("8. Central de observação (Grafana)", "h1"),
          P("Cinco painéis, um por tela. No modo quiosque, rodam sozinhos num monitor ou TV."),
          table([
              ["Painel", "O que mostra", "Fontes"],
              ["Mapa", "Aviões, balões, nós Meshtastic e drones, posição do kit, focos de incêndio 24 h, sismos M4,5+", "tar1090, SondeHub, MQTT, FIRMS, USGS"],
              ["Rede", "Alertas Suricata por gravidade, top conversas, alertas Wazuh, serviços fora do ar", "Security Onion, ntopng, Wazuh, Uptime Kuma"],
              ["Ameaças", "CVEs exploradas novas, IOCs vistos na rede, IPs bloqueados, toques no honeypot", "FreshRSS, MISP, CrowdSec, Cowrie"],
              ["Céu", "Última imagem Meteor, próximas passagens, aviões/hora, balões do dia", "SatDump, readsb, SondeHub"],
              ["Casa", "PM2,5, temperatura, raios perto, consumo do rack, sensores 433 MHz", "Sensor.Community, Blitzortung, Shelly, rtl_433"],
          ], [22 * mm, 86 * mm, 62 * mm]),
          ]

# ---------- 8 Regras ----------
story += [P("9. Rede, segurança e regras", "h1"),
          table([
              ["Tema", "Regra"],
              ["Exposição", "Nenhuma porta aberta no roteador. Acesso de fora só pelo Tailscale."],
              ["VLANs", "VM \"radio\" na VLAN 20; kit portátil só pelo Tailscale, com ACL própria. Sensores Wi-Fi na VLAN 10 com acesso só à porta 1883 "
                        "(MQTT) e 8086 (InfluxDB) do lab. Honeypot e alvos na VLAN 30."],
              ["Credenciais", "MQTT e InfluxDB com usuário e senha por dispositivo. Tokens de API (FIRMS, "
                              "FlightAware) fora do GitHub, em arquivo .env."],
              ["Recepção", "ADS-B, satélites, radiossondas e 433 MHz são só recepção."],
              ["Transmissão", "Só o rádio LoRa transmite (915 MHz, radiação restrita): prefira equipamento "
                              "homologado pela Anatel e respeite o limite de potência."],
              ["Localização", "Ao cadastrar nas redes colaborativas, use a posição aproximada da estação."],
              ["Portas do switch", "7 de 8 em uso (roteador, 4 nós, sniffer, notebook). Blitzortung no roteador."],
              ["Kit perdido", "Revogue o nó no Tailscale e as credenciais kit no MQTT e no InfluxDB. "
                              "Disco do notebook criptografado."],
          ], [32 * mm, 138 * mm]),
          ]

# ---------- 9 Checklist ----------
chk = [
    ("1", "Grafana + InfluxDB no ar; painel Casa com o consumo e a temperatura dos nós"),
    ("1", "Loki recebendo logs dos 3 nós; Uptime Kuma avisando no Telegram"),
    ("1", "Node-RED gravando FIRMS e USGS; mapa com focos e sismos"),
    ("1", "Sonda RIPE Atlas aprovada; primeira medição própria feita"),
    ("1", "MISP com feeds da CIRCL; FreshRSS com CISA KEV; Cowrie gerando alerta no Wazuh"),
    ("2", "Nó 4 com 32 GB e i350; espelho porta 1 -> 7 configurado"),
    ("2", "Security Onion alertando o teste testmynids; ntopng mostrando conversas"),
    ("3", "Seriais ADSB, KIT1 e KIT2 gravados; VM \"radio\" com passthrough por porta"),
    ("3", "Mastro aterrado, DPS instalados, coaxiais no painel da U6"),
    ("3", "ADS-B fixo com LNA e feeders; primeira imagem Meteor pela QFH"),
    ("3", "Base Meshtastic vendo o cyberdeck; posições no mapa do Grafana"),
    ("3", "Saída e volta do kit testadas: fila do InfluxDB e ponte MQTT descarregando"),
    ("4", "Sensor.Community no mapa mundial; Shelly no Zabbix; pedido do kit Blitzortung"),
]
story += [P("10. Checklist", "h1"),
          table([["", "Fase", "Etapa"]] + [["☐", f, e] for f, e in chk], [9 * mm, 13 * mm, 148 * mm]),
          Spacer(1, 5 * mm),
          P("Para o portfólio", "h2"),
          bullets(["Um repositório com todos os docker-compose, a configuração do Proxmox (sem segredos) e o desenho técnico;",
                   "capturas de cada painel do Grafana e um vídeo curto da central rodando;",
                   "o relatório de um alerta real do Security Onion, investigado do início ao fim: é o que mais "
                   "conta numa entrevista de SOC;",
                   "os links públicos da sua estação no FlightAware, SondeHub, Sensor.Community e RIPE Atlas."]),
          ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=18 * mm, bottomMargin=22 * mm,
                        title="Homelab – plano de monitoramento e observação global",
                        author="João Victor Paixão Zolim")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("ok", OUT, s2, s3, s4, s2 + s3 + s4)
