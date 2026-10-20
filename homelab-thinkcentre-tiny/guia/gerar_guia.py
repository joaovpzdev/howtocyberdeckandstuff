import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _base import *  # noqa: F401,F403
from xml.sax.saxutils import escape

pdfmetrics.registerFont(TTFont("DVM", F + "DejaVuSansMono.ttf"))
ss["h1"].keepWithNext = 1
ss["code"] = ParagraphStyle("code", fontName="DVM", fontSize=7.8, leading=10.6, textColor=INK)


def code(txt):
    html = "<br/>".join(escape(l).replace(" ", "&nbsp;") for l in txt.strip("\n").split("\n"))
    t = Table([[Paragraph(html, ss["code"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINT),
                           ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    t.spaceAfter = 5
    return t


def h2(t, *flow):
    return KeepTogether([P(t, "h2"), *flow])


story = []

# ---------- Capa ----------
story += [Spacer(1, 45 * mm),
          P("Homelab Lenovo Tiny", "subtitle"),
          Spacer(1, 3 * mm),
          P("Estação de satélite e<br/>biblioteca offline", "title"),
          Spacer(1, 6 * mm),
          P("Guia de compra, instalação e operação no nó 2 do Proxmox", "subtitle"),
          Spacer(1, 18 * mm),
          P("João Victor Paixão Zolim · github.com/joaovpzdev", "small"),
          P("Versão 1.0 · outubro de 2026 · acompanha o desenho técnico rev. B", "small"),
          PageBreak()]

# ---------- 1 ----------
story += [P("1. O que entra no homelab", "h1"),
          P("Dois serviços novos, os dois no <b>nó 2</b> (U3 do rack), na VLAN 20 do lab:"),
          bullets([
              "<b>Estação de satélite:</b> uma antena de 137 MHz fora de casa, um RTL-SDR no USB do nó 2 e o "
              "SatDump numa VM. Ele calcula as passagens, grava e decodifica sozinho as imagens dos satélites "
              "meteorológicos russos <b>Meteor-M</b> (sinal digital LRPT).",
              "<b>Biblioteca offline:</b> o Kiwix serve a Wikipédia em português e outras bases inteiras pelo "
              "navegador, sem internet. O Calibre-Web guarda seus livros e PDFs.",
          ]),
          callout("<b>Por que Meteor e não NOAA:</b> os satélites NOAA-15, 18 e 19, alvo clássico desse tipo de "
                  "projeto, foram desativados em 2025. Hoje o alvo para iniciantes é o Meteor-M em 137 MHz. "
                  "Frequências e satélites ativos mudam: confira o status antes de cada sessão."),
          Spacer(1, 4 * mm),
          h2("Compras",
             table([
                 ["Item", "Para quê", "R$ (estim.)"],
                 ["SSD SATA 2,5\" 1 TB", "ZIMs do Kiwix, livros e imagens, na baia 2,5\" do M720q", "~350"],
                 ["RTL-SDR Blog V3 (kit com dipolo)", "Receptor; o kit já vira um V-dipolo de 137 MHz", "~350"],
                 ["Cabo coaxial baixa perda até 10 m + conectores", "Da antena até o rack", "~100"],
                 ["Mastro (tubo de PVC/alumínio) + abraçadeiras", "Antena acima do telhado ou muro", "~50"],
                 ["LNA com filtro para 137 MHz (opcional)", "Só se o coaxial passar de ~5 m", "~300"],
                 ["<b>Total</b>", "", "<b>~R$ 850 (~R$ 550 sem LNA)</b>"],
             ], [62 * mm, 82 * mm, 26 * mm])),
          P("Preços estimados; o RTL-SDR e o LNA são importados e variam com frete e impostos.", "small"),
          Spacer(1, 3 * mm),
          h2("Recursos no nó 2",
             table([
                 ["Serviço", "Tipo no Proxmox", "vCPU", "RAM", "Disco"],
                 ["SatDump", "VM Debian 12 (USB do RTL-SDR passado para ela)", "2", "2 GB", "16 GB + pasta no SSD"],
                 ["kiwix-serve", "Contêiner LXC Debian 12", "1", "512 MB", "8 GB + SSD 1 TB"],
                 ["Calibre-Web", "No mesmo LXC do Kiwix (Docker) ou LXC próprio", "1", "512 MB", "pasta no SSD"],
             ], [26 * mm, 70 * mm, 14 * mm, 18 * mm, 42 * mm])),
          P("Somados, cabem com folga nos 16 GB do nó 2, ao lado do Minecraft e do GLPI.", "small"),
          ]

# ---------- 2 ----------
story += [P("2. Biblioteca offline (Kiwix)", "h1"),
          h2("2.1 Disco",
             P("Instale o SSD na baia 2,5\" do M720q. No Proxmox: <i>Datacenter → Storage → Add → Directory</i>, "
               "apontando para o SSD formatado em ext4 (ex.: <font name='DVM'>/mnt/ssd</font>). Crie as pastas:"),
             code("mkdir -p /mnt/ssd/zim /mnt/ssd/livros /mnt/ssd/satelite")),
          h2("2.2 Contêiner",
             P("Crie um LXC Debian 12 sem privilégios (1 vCPU, 512 MB, 8 GB), na bridge da VLAN 20. "
               "Depois, no shell do Proxmox, monte a pasta do SSD dentro dele (troque 102 pelo ID do seu LXC):"),
             code("pct set 102 -mp0 /mnt/ssd/zim,mp=/srv/zim -mp1 /mnt/ssd/livros,mp=/srv/livros")),
          h2("2.3 Instalação e conteúdo",
             P("Dentro do LXC:"),
             code("""apt update && apt install -y kiwix-tools wget
cd /srv/zim
# Baixe os arquivos .zim de https://download.kiwix.org/zim/
# Ex.: Wikipedia em português com imagens (wikipedia_pt_all_maxi_AAAA-MM.zim)
wget -c https://download.kiwix.org/zim/wikipedia/<arquivo>.zim
kiwix-manage /srv/zim/library.xml add /srv/zim/*.zim""")),
          P("Sugestões de conteúdo (procure pelo nome na biblioteca do Kiwix):"),
          bullets([
              "<b>Wikipédia em português</b>, versão <i>maxi</i> (com imagens, dezenas de GB) ou <i>nopic</i> (sem imagens, bem menor);",
              "<b>WikiMed / MDWiki</b>: enciclopédia médica;",
              "<b>iFixit</b>: guias de conserto;",
              "<b>Stack Exchange</b>: Unix &amp; Linux, Super User, Server Fault, Security;",
              "<b>Projeto Gutenberg</b>: livros de domínio público;",
              "<b>Wikilivros e Wikivoyage</b>.",
          ]),
          h2("2.4 Serviço permanente",
             P("Crie <font name='DVM'>/etc/systemd/system/kiwix.service</font>:"),
             code("""[Unit]
Description=Kiwix
After=network.target

[Service]
ExecStart=/usr/bin/kiwix-serve --port=8080 --library --monitorLibrary /srv/zim/library.xml
Restart=always
User=nobody

[Install]
WantedBy=multi-user.target"""),
             code("systemctl daemon-reload && systemctl enable --now kiwix")),
          P("Para adicionar um ZIM novo depois, basta o <font name='DVM'>kiwix-manage ... add</font>: "
            "o <font name='DVM'>--monitorLibrary</font> recarrega a biblioteca sozinho."),
          h2("2.5 Livros e PDFs (Calibre-Web)",
             P("Opcional. Com Docker instalado num LXC (ative <i>nesting</i> nas opções do contêiner):"),
             code("""docker run -d --name calibre-web --restart unless-stopped \\
  -p 8083:8083 -v /srv/livros:/books -v /srv/calibre-config:/config \\
  lscr.io/linuxserver/calibre-web:latest""")),
          h2("2.6 Nomes na rede",
             P("No Pi-hole (nó 1): <i>Local DNS → DNS Records</i>, crie <font name='DVM'>wiki.lab</font> e "
               "<font name='DVM'>livros.lab</font> apontando para o IP do LXC. Em casa, abra "
               "<font name='DVM'>http://wiki.lab:8080</font>. Fora de casa, use o IP do Tailscale."),
             callout("Não abra essas portas no roteador. Acesso de fora só pelo Tailscale.")),
          ]

# ---------- 3 ----------
story += [P("3. Estação de satélite (SatDump)", "h1"),
          h2("3.1 Antena V-dipolo",
             bullets([
                 "Use as duas hastes do kit do RTL-SDR V3 abertas em <b>~53 cm</b> cada e com <b>120°</b> entre elas.",
                 "Monte na <b>horizontal</b>, com o \"V\" apontando para o <b>norte ou o sul</b> (os Meteor passam de "
                 "polo a polo).",
                 "Céu aberto, longe de paredes, calhas e fontes de ruído (inversores, carregadores, roteador).",
                 "Coaxial o mais curto possível. Com mais de ~5 m, use o LNA com filtro no mastro.",
                 "Depois de testar, a <b>QFH</b> (a antena helicoidal do post) é o upgrade: feita com tubo de cobre "
                 "e PVC, recebe melhor as passagens baixas.",
             ])),
          h2("3.2 VM e USB",
             P("Crie uma VM Debian 12 (2 vCPU, 2 GB). Com o RTL-SDR plugado no USB traseiro do nó 2: "
               "<i>VM → Hardware → Add → USB Device → Use USB Vendor/Device ID</i> e escolha o RTL2838. "
               "Monte a pasta de imagens do SSD na VM (por NFS ou disco extra) em "
               "<font name='DVM'>/srv/satelite</font>."),
             P("Dentro da VM, impeça o driver de TV de pegar o rádio e instale o driver do RTL-SDR Blog (serve para o V3 e o V4):"),
             code("""echo 'blacklist dvb_usb_rtl28xxu' > /etc/modprobe.d/rtlsdr.conf
apt install -y git cmake build-essential libusb-1.0-0-dev
git clone https://github.com/rtlsdrblog/rtl-sdr-blog && cd rtl-sdr-blog
mkdir build && cd build && cmake .. -DINSTALL_UDEV_RULES=ON && make && make install
ldconfig && reboot
# depois:
rtl_test -t""")),
          h2("3.3 SatDump",
             numbered([
                 "Instale o SatDump pelo pacote da página de releases do projeto no GitHub "
                 "(<font name='DVM'>github.com/SatDump/SatDump</font>) ou compile seguindo o README.",
                 "Primeiro teste à mão: atualize os TLE (dados de órbita), escolha a próxima passagem de um "
                 "Meteor-M com <b>elevação acima de 30°</b>, selecione o pipeline <i>Meteor M2-x LRPT</i> e grave.",
                 "Com a recepção funcionando, ative o <b>rastreamento automático</b> (auto track) para agendar e "
                 "decodificar todas as passagens sozinho, salvando em <font name='DVM'>/srv/satelite</font>. "
                 "Os nomes das opções mudam entre versões: confira na documentação da versão instalada.",
                 "Rode o SatDump como serviço systemd para voltar sozinho depois de um reboot.",
             ])),
          h2("3.4 Galeria",
             P("Sirva a pasta de imagens com um nginx na própria VM e crie <font name='DVM'>sat.lab</font> no Pi-hole:"),
             code("""apt install -y nginx
# em /etc/nginx/sites-available/default:
#   root /srv/satelite;  autoindex on;
systemctl reload nginx""")),
          ]

# ---------- 4 ----------
story += [P("4. Operação e segurança", "h1"),
          table([
              ["Tema", "Como fica"],
              ["Rede", "Os dois serviços na VLAN 20. Casa (VLAN 10) só lê pelo navegador; nada exposto à internet."],
              ["Monitoramento", "Agente Zabbix na VM e no LXC (espaço no SSD, serviço no ar, temperatura do nó 2). "
                                "Agente Wazuh para logs de acesso."],
              ["Backup", "vzdump semanal da VM e do LXC (são pequenos). Os ZIMs se baixam de novo; as imagens de "
                         "satélite e os livros vão para um disco externo."],
              ["Atualização", "Os ZIMs da Wikipédia saem a cada poucos meses: troque o arquivo e rode o kiwix-manage."],
              ["Energia", "RTL-SDR + LNA somam ~2 W; o pico do rack fica em ~125 W, dentro do nobreak."],
              ["Regras", "Receber satélites meteorológicos é só recepção, sem transmissão. As imagens são públicas."],
          ], [32 * mm, 138 * mm]),
          Spacer(1, 4 * mm),
          h2("Para o portfólio (GitHub)",
             bullets([
                 "README com fotos da antena e do rack, o diagrama da folha 2 do desenho técnico e os arquivos de configuração;",
                 "uma galeria das melhores imagens recebidas, com data, satélite e elevação da passagem;",
                 "um gráfico do Zabbix mostrando uptime e uso de disco dos serviços;",
                 "o que deu errado e como resolveu (ruído, antena, driver): é o que mais conta numa entrevista.",
             ])),
          h2("Checklist",
             table([
                 ["", "Etapa"],
                 ["☐", "SSD instalado e montado no Proxmox"],
                 ["☐", "LXC do Kiwix com a Wikipédia pt respondendo em wiki.lab:8080"],
                 ["☐", "Acesso pelo Tailscale testado fora de casa"],
                 ["☐", "Antena montada, V na horizontal apontando norte–sul"],
                 ["☐", "rtl_test sem erros dentro da VM"],
                 ["☐", "Primeira imagem Meteor decodificada à mão"],
                 ["☐", "Rastreamento automático ligado e galeria em sat.lab"],
                 ["☐", "Agentes Zabbix e Wazuh e backup vzdump configurados"],
             ], [10 * mm, 160 * mm])),
          ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=18 * mm, bottomMargin=22 * mm,
                        title="Homelab – estação de satélite e biblioteca offline",
                        author="João Victor Paixão Zolim")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("ok", OUT)
