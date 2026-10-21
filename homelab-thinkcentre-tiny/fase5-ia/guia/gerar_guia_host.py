import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _base import *  # noqa: F401,F403
from xml.sax.saxutils import escape

pdfmetrics.registerFont(TTFont("DVM", F + "DejaVuSansMono.ttf"))
ss["h1"].keepWithNext = 1
ss["h2"].keepWithNext = 1
ss["code"] = ParagraphStyle("code", fontName="DVM", fontSize=7.4, leading=10, textColor=INK)


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


W2 = [42 * mm, 128 * mm]
story = []

# ---------- capa ----------
story += [Spacer(1, 45 * mm),
          P("Homelab Lenovo Tiny · fase 5 · v1.0", "subtitle"), Spacer(1, 3 * mm),
          P("Host de IA dedicado:<br/>EPYC com 5 placas de vídeo", "title"), Spacer(1, 6 * mm),
          P("Implementação detalhada do computador que comanda o rack de GPU em perfil 2020: compra, "
            "montagem, BIOS, Proxmox, máquina virtual com as 5 placas, modelos de IA, rede, monitoramento, "
            "liga/desliga sob demanda e testes", "subtitle"),
          Spacer(1, 18 * mm),
          P("João Victor Paixão Zolim · github.com/joaovpzdev", "small"),
          P("Outubro de 2026 · acompanha o desenho técnico \"Rack de GPU 2020 + host EPYC\" rev. B (2 folhas A3)", "small"),
          PageBreak()]

# ---------- 1 ----------
story += [P("1. Visão geral", "h1"),
          P("O nó 5 (M720q) só consegue comandar uma placa de vídeo pelo OCuLink. Para chegar a cinco, o rack de GPU "
            "ganha um <b>computador próprio no nível de baixo</b>: uma placa-mãe de servidor com processador AMD EPYC, "
            "que tem 128 pistas PCIe e liga as cinco placas em x16 completo, sem divisão de banda."),
          table([["Peça", "Papel"],
                 ["Host EPYC (\"host-ia\")", "Sexto nó do cluster Proxmox; fica desligado quando não está em uso"],
                 ["VM \"ia\" (Ubuntu Server 24.04)", "Recebe as 5 placas por passthrough e roda os serviços de IA em Docker"],
                 ["Placas G1 a G4", "Um modelo grande dividido em quatro (vLLM, tensor parallel = 4)"],
                 ["Placa G5", "Transcrição (Whisper), embeddings e modelos pequenos (Ollama)"],
                 ["Open WebUI", "Interface de chat, documentos e usuários; acesso só pela VLAN 20 e Tailscale"],
                 ["Nó 1 (Grafana, Zabbix)", "Painéis de GPU, temperatura e consumo; sensores do BMC por IPMI"],
                 ["Nó 2 (Node-RED)", "Botão para ligar o host pelo IPMI e fluxos que usam a IA (triagem de alertas)"]],
                [55 * mm, 115 * mm]),
          Spacer(1, 4),
          callout("<b>Por que 4 + 1 e não 5 juntas:</b> para dividir um modelo entre placas (tensor parallel), o número "
                  "de placas precisa dividir as cabeças de atenção do modelo, que quase sempre são potências de 2. "
                  "Com 5 placas, o modelo principal usa 4 e a quinta fica livre para os serviços de apoio, que de outro "
                  "jeito disputariam memória com o modelo."),
          ]

# ---------- 2 ----------
story += [P("2. Hardware escolhido", "h1"),
          table([["Parte", "Escolha", "Por quê / alternativa"],
                 ["Placa-mãe", "ASRock Rack ROMED8-2T (ATX, 305 × 244 mm)",
                  "7 slots PCIe 4.0 x16, 8 slots de memória, 2 × M.2, 2 × 10 GbE, BMC com IPMI e porta própria. "
                  "Alternativa: Supermicro H12SSL-i (menos slots x16)."],
                 ["Processador", "AMD EPYC 7302P (16 núcleos, 155 W)",
                  "128 pistas PCIe e 8 canais de memória. O \"P\" é a versão de um soquete, mais barata. "
                  "Para IA nas placas, mais núcleos não ajudam muito."],
                 ["Memória", "8 × 16 GB DDR4-3200 RDIMM ECC (128 GB)",
                  "Um pente por canal: os 8 canais preenchidos dão a banda máxima. Precisa ser RDIMM (registrada)."],
                 ["Cooler", "Noctua NH-U9 TR4-SP3 (125 mm)",
                  "Cabe nos 180 mm do nível de baixo e sopra da frente para trás, como o resto do quadro."],
                 ["Disco", "NVMe 2 TB PCIe 4.0 no M.2",
                  "Proxmox, disco da VM e os modelos (um modelo de 70B em 4 bits ocupa ~40 GB)."],
                 ["Fonte", "ATX 3.1 1600 W 80+ Platinum",
                  "Precisa de saídas PCIe suficientes para todas as placas, sem adaptadores. ATX 3.1 aguenta melhor os "
                  "picos rápidos das placas de vídeo."],
                 ["Risers", "5 × PCIe 4.0 x16 blindados, 30 cm",
                  "Ligam cada slot à sua baia, atravessando a chapa do meio pelo rasgo."],
                 ["Placas de vídeo", "5 × RTX 3060 12 GB (60 GB no total)",
                  "CUDA funciona direto. Upgrade natural: RTX 3090 24 GB (120 GB no total)."]],
                [26 * mm, 52 * mm, 92 * mm]),
          ]

# ---------- 3 ----------
story += [P("3. Antes de comprar", "h1"),
          bullets([
              "<b>Processador sem trava de fabricante.</b> Dell e Lenovo usam o AMD Platform Secure Boot (PSB) para "
              "prender o EPYC às placas deles. Um processador usado que veio desses servidores pode não funcionar na "
              "ROMED8-2T. Compre anúncios que digam <i>unlocked</i>, <i>sem PSB</i> ou <i>tray</i>, e peça foto da "
              "etiqueta sem marca de fabricante.",
              "<b>Versão da BIOS.</b> A ROMED8-2T aceita EPYC 7002 e 7003; para os 7003, a placa pode precisar de "
              "BIOS mais nova. Com o 7302P (7002) ela liga em qualquer versão, e a BIOS pode ser atualizada depois "
              "pela interface do BMC.",
              "<b>Memória RDIMM.</b> Pente comum (UDIMM) de computador de mesa não funciona. Os 8 pentes iguais, "
              "mesma marca e velocidade.",
              "<b>Fonte.</b> Conte os conectores: RTX 3060 usa 1 × 8 pinos (alguns modelos 2); RTX 3090 usa 2 ou 3. "
              "A placa-mãe precisa do 24 pinos, de um EPS 8 pinos e de um 4 pinos.",
              "<b>Risers.</b> Prefira PCIe 4.0 blindado, todos do mesmo comprimento. Riser USB de mineração não serve.",
              "<b>Importação.</b> Placa-mãe de servidor quase sempre vem de fora: conte imposto, prazo e a falta de garantia; "
              "teste tudo assim que chegar.",
              "<b>Elétrica.</b> Com 5 placas, o rack vai a ~950 W (3060) ou ~1.300 W (3090). Peça a um eletricista "
              "uma tomada de 20 A exclusiva, com DPS, antes de passar de três placas."]),
          ]

# ---------- 4 ----------
story += [P("4. Montagem física", "h1"),
          P("Monte primeiro na bancada, com uma placa de vídeo só, e passe para o quadro depois que tudo funcionar.", "body"),
          numbered([
              "<b>Bancada:</b> placa-mãe sobre a caixa dela (nunca sobre o saco antiestático), pulseira antiestática.",
              "<b>Processador:</b> soltar os 3 parafusos Torx T20 da tampa do soquete na ordem 3-2-1, deslizar o "
              "processador (no suporte laranja) no trilho, fechar e apertar na ordem 1-2-3 com chave de torque "
              "(~1,8 N·m; confira no manual). O soquete SP3 tem milhares de pinos: não toque nem deixe cair nada nele.",
              "<b>Cooler:</b> pasta térmica (o Noctua vem com a dele), suporte SP3 e ventoinha soprando para a borda de I/O.",
              "<b>Memória:</b> os 8 pentes, um em cada slot.",
              "<b>NVMe</b> no M.2 e <b>uma placa de vídeo</b> direto no slot 1, sem riser.",
              "<b>Fonte:</b> 24 pinos, EPS 8 pinos, 4 pinos e o cabo da placa de vídeo.",
              "<b>Rede:</b> porta do BMC (IPMI) e uma porta 10 GbE no switch, ambas na VLAN 20.",
              "Ligar e acessar o BMC (seção 5). O primeiro boot de um servidor EPYC demora: 1 a 3 minutos de tela preta é normal.",
              "<b>Quadro:</b> chapa de baixo com os espaçadores ATX, placa-mãe deitada com a borda de I/O para trás, "
              "fonte na frente à direita, ventoinhas de entrada na frente.",
              "<b>Risers e baias:</b> uma placa por vez, de G1 a G5. Cada riser sai de um slot x16, sobe pelo rasgo da "
              "chapa e encaixa na baia; o suporte traseiro da placa é parafusado na barra 2020. Anote qual slot vai "
              "para qual baia.",
              "<b>Cabos de energia</b> das placas sem dobras forçadas; abraçadeiras nos perfis, longe das ventoinhas.",
              "<b>Aterramento:</b> um cabo do quadro ao parafuso da fonte."]),
          ]

# ---------- 5 ----------
story += [P("5. Primeiro boot: BMC e BIOS", "h1"),
          P("O BMC é um computador pequeno dentro da placa-mãe, ligado à porta IPMI. Ele dá tela remota, liga e "
            "desliga o host e lê os sensores, mesmo com o host desligado."),
          numbered([
              "Descubra o IP do BMC no DHCP do roteador ou no Pi-hole; abra no navegador.",
              "Entre com a senha da etiqueta da placa (firmwares antigos usam admin/admin) e <b>troque a senha na hora</b>. "
              "Crie um usuário próprio, por exemplo <i>ia-admin</i>.",
              "Atualize o firmware do BMC e depois a BIOS, pelo próprio BMC.",
              "Fixe o IP do BMC (ex.: 10.0.20.60) e o do host (ex.: 10.0.20.61) no DHCP."]),
          P("Ajustes da BIOS:", "h2"),
          table([["Opção", "Valor", "Para quê"],
                 ["IOMMU (AMD CBS › NBIO)", "Enabled", "Passar as placas de vídeo para a VM"],
                 ["Above 4G Decoding", "Enabled", "Endereçar a memória de 5 placas"],
                 ["Re-Size BAR", "Disabled", "Evita problemas no passthrough"],
                 ["ACS", "Enabled", "Cada placa no seu grupo IOMMU"],
                 ["CSM", "Disabled (só UEFI)", "Boot moderno e OVMF na VM"],
                 ["Velocidade dos slots PCIe", "Auto; Gen3 se aparecer erro", "Risers longos às vezes não aguentam Gen4"],
                 ["Restore on AC Power Loss", "Power Off", "Não ligar sozinho quando a luz volta"]],
                [55 * mm, 45 * mm, 70 * mm]),
          Spacer(1, 4),
          callout("<b>Ventoinhas silenciosas e BMC:</b> o BMC espera ventoinhas de servidor e pode achar que uma Noctua "
                  "girando devagar está parada, acelerando tudo em ciclos. Se isso acontecer, baixe o limite mínimo "
                  "de rotação com o ipmitool (comando abaixo, conferindo o nome do sensor)."),
          code("""ipmitool -I lanplus -H 10.0.20.60 -U ia-admin -f /root/.ipmi_senha sensor list | grep -i fan
ipmitool -I lanplus -H 10.0.20.60 -U ia-admin -f /root/.ipmi_senha sensor thresh FAN1 lower 100 200 300"""),
          ]

# ---------- 6 ----------
story += [P("6. Proxmox no host", "h1"),
          numbered([
              "Instale o Proxmox VE no NVMe pela tela remota do BMC (mídia virtual). Hostname <i>host-ia</i>, IP 10.0.20.61, "
              "bridge <i>vmbr0</i> com VLAN aware ligado.",
              "Entre no cluster existente: <i>Datacenter › Cluster › Join</i>. O cluster passa a ter 6 nós; com o host-ia "
              "desligado ficam 5 de 6, e o quórum (4) continua garantido. Não coloque o host-ia em grupos de HA.",
              "Ative o passthrough: carregue os módulos VFIO, prenda as placas NVIDIA ao vfio-pci e impeça o host de "
              "carregar drivers de vídeo nelas."]),
          P("Os IDs mudam com o modelo da placa: se misturar 3060 e 3090, coloque os IDs das duas na linha do vfio.", "small"),
          code("""# IDs das placas (vídeo e áudio de cada GPU)
lspci -nn | grep -i nvidia          # ex.: 10de:2504 (vídeo) e 10de:228e (áudio)

# linha de comando do kernel: acrescente iommu=pt
#   GRUB: GRUB_CMDLINE_LINUX_DEFAULT em /etc/default/grub  -> update-grub
#   ZFS/systemd-boot: /etc/kernel/cmdline                  -> proxmox-boot-tool refresh

cat >> /etc/modules <<'EOF'
vfio
vfio_iommu_type1
vfio_pci
EOF
echo "options vfio-pci ids=10de:2504,10de:228e disable_vga=1" > /etc/modprobe.d/vfio.conf
printf "blacklist nouveau\\nblacklist nvidia\\n" > /etc/modprobe.d/blacklist-gpu.conf
update-initramfs -u -k all && reboot

# depois do reboot: cada placa no seu grupo e presa ao vfio-pci
find /sys/kernel/iommu_groups/ -type l | sort -V | grep -i ":00.0"
lspci -nnk | grep -A3 -i nvidia     # "Kernel driver in use: vfio-pci\""""),
          ]

# ---------- 7 ----------
story += [P("7. VM \"ia\" com as 5 placas", "h1"),
          table([["Configuração", "Valor"],
                 ["Sistema", "Ubuntu Server 24.04 LTS"],
                 ["Máquina / firmware", "q35 / OVMF (UEFI), sem Secure Boot"],
                 ["CPU", "tipo host, 24 vCPUs (sobram 8 threads para o Proxmox)"],
                 ["Memória", "96 GB fixos (balloon desligado: obrigatório com passthrough)"],
                 ["Disco", "400 GB no NVMe (VirtIO SCSI single, iothread)"],
                 ["Rede", "virtio na vmbr0, tag 20"],
                 ["PCI", "5 placas inteiras (todas as funções), PCI-Express ligado"]],
                W2),
          Spacer(1, 4),
          code("""qm create 200 --name ia --machine q35 --bios ovmf --cpu host --cores 24 \\
  --memory 98304 --balloon 0 --scsihw virtio-scsi-single \\
  --net0 virtio,bridge=vmbr0,tag=20 --ostype l26 \\
  --efidisk0 local-lvm:1,efitype=4m,pre-enrolled-keys=0 \\
  --scsi0 local-lvm:400,iothread=1

# endereços de exemplo: use os do seu "lspci | grep -i nvidia"
qm set 200 --hostpci0 0000:01:00,pcie=1
qm set 200 --hostpci1 0000:21:00,pcie=1
qm set 200 --hostpci2 0000:41:00,pcie=1
qm set 200 --hostpci3 0000:61:00,pcie=1
qm set 200 --hostpci4 0000:81:00,pcie=1"""),
          callout("<b>Se a VM não enxergar todas as placas:</b> o OVMF reserva pouco espaço de memória PCI. Aumente com "
                  f"{M('qm set 200 --args \"-fw_cfg name=opt/ovmf/X-PciMmio64Mb,string=65536\"')} e reinicie a VM."),
          ]

# ---------- 8 ----------
story += [P("8. Software de IA na VM", "h1"),
          P("Driver, toolkit de contêiner e limite de potência", "h2"),
          code("""sudo apt update && sudo apt full-upgrade -y
sudo ubuntu-drivers install            # driver NVIDIA recomendado
sudo reboot
nvidia-smi                             # precisa listar as 5 placas

# Docker + NVIDIA Container Toolkit (repositório oficial da NVIDIA, ver documentação)
sudo apt install -y docker.io docker-compose-v2 nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker

# limite de potência em todo boot: /etc/systemd/system/gpu-limite.service
[Unit]
Description=Limite de potência das placas
After=multi-user.target
[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -pm 1
ExecStart=/usr/bin/nvidia-smi -pl 150     # 3060; use 220 para 3090
[Install]
WantedBy=multi-user.target"""),
          P("Serviços (docker-compose.yml em /srv/ia)", "h2"),
          code("""services:
  vllm:                                   # modelo principal nas placas 0-3
    image: vllm/vllm-openai:latest
    ipc: host
    command: >
      --model Qwen/Qwen2.5-32B-Instruct-AWQ
      --tensor-parallel-size 4 --gpu-memory-utilization 0.90
      --max-model-len 16384 --api-key ${VLLM_KEY}
    volumes: ["/srv/modelos:/root/.cache/huggingface"]
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, device_ids: ["0","1","2","3"], capabilities: [gpu]}]
    restart: unless-stopped

  ollama:                                 # embeddings e modelos pequenos na placa 4
    image: ollama/ollama:latest
    volumes: ["/srv/ollama:/root/.ollama"]
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, device_ids: ["4"], capabilities: [gpu]}]
    restart: unless-stopped

  whisper:                                # transcrição na placa 4
    image: onerahmet/openai-whisper-asr-webservice:latest-gpu
    environment: [ASR_ENGINE=faster_whisper, ASR_MODEL=medium]
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, device_ids: ["4"], capabilities: [gpu]}]
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports: ["3000:8080"]
    environment:
      - OPENAI_API_BASE_URL=http://vllm:8000/v1
      - OPENAI_API_KEY=${VLLM_KEY}
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes: ["/srv/open-webui:/app/backend/data"]
    restart: unless-stopped"""),
          bullets([
              "O modelo do exemplo (32B em 4 bits, ~19 GB) cabe com folga nos 48 GB das quatro placas e deixa espaço "
              "para contexto longo. Um 70B em 4 bits (~40 GB) também cabe, com contexto curto. Troque pelo modelo da vez.",
              "Se o vLLM travar ao iniciar dentro da VM, teste a variável <i>NCCL_P2P_DISABLE=1</i>: placas de consumo "
              "atrás de risers nem sempre conversam direto entre si.",
              "Depois de criar a conta de administrador no Open WebUI, desligue novos cadastros "
              "(<i>ENABLE_SIGNUP=false</i>).",
              "Imagens e variáveis mudam entre versões: confira o README de cada projeto antes de atualizar."]),
          ]

# ---------- 9 ----------
story += [P("9. Rede e segurança", "h1"),
          table([["Item", "Regra"],
                 ["VLAN", "Host, BMC e VM na VLAN 20 (lab). A VLAN 30 (alvos) não tem rota até eles."],
                 ["BMC", "Nunca exposto. Senha própria, firmware atualizado, acesso só da VLAN 20."],
                 ["Rede 10 GbE", "O TL-SG108E é 1 GbE: a porta negocia 1 Gb/s, suficiente para baixar modelos. "
                                 "A segunda porta 10 GbE fica para um switch 10 GbE no futuro."],
                 ["Acesso de fora", "Tailscale só na VM. Nenhuma porta aberta no roteador."],
                 ["APIs", "vLLM com chave (--api-key); Ollama sem porta publicada, só na rede interna do compose."],
                 ["Dados", "Alertas, logs e documentos ficam em casa. Nada é enviado para serviços de IA externos (LGPD)."],
                 ["Backup", "Configuração da VM e volume do Open WebUI copiados para o SSD do nó 2. Modelos não "
                            "precisam de backup: baixam de novo."]],
                [30 * mm, 140 * mm]),
          ]

# ---------- 10 ----------
story += [P("10. Monitoramento", "h1"),
          bullets([
              "<b>Zabbix (nó 1):</b> host novo com interface IPMI apontando para o BMC: temperatura do processador, "
              "ventoinhas, tensões e consumo, mesmo com o host desligado.",
              "<b>Telegraf na VM</b> com o plugin <i>nvidia_smi</i>, enviando para o InfluxDB do nó 1: uso, memória, "
              "temperatura e potência de cada placa.",
              "<b>Grafana:</b> painel \"IA\" com as 5 placas lado a lado e o consumo total.",
              "<b>Alertas:</b> placa acima de 83 °C, erros PCIe (AER) no log, uma placa sumindo do nvidia-smi."]),
          code("""# /etc/telegraf/telegraf.d/gpu.conf (na VM)
[[inputs.nvidia_smi]]
  bin_path = "/usr/bin/nvidia-smi"
  timeout = "5s"

# conferir link PCIe de cada placa (geração e largura)
nvidia-smi -q -d PCIE | grep -E "Bus Id|Current"
sudo dmesg | grep -iE "aer|pcie bus error\""""),
          ]

# ---------- 11 ----------
story += [P("11. Liga/desliga sob demanda e energia", "h1"),
          P("Ligado e parado, o host gasta cerca de 140 W: ~R$ 100 por mês só para esperar. A ideia é deixá-lo "
            "desligado e ligar quando for usar. O BMC continua acordado (~5 W) e liga o host pela rede."),
          table([["Estado", "5 × 3060 @150 W", "5 × 3090 @220 W"],
                 ["Desligado (só o BMC)", "~5 W", "~5 W"],
                 ["Ligado, ocioso", "~140 W", "~170 W"],
                 ["Gerando texto com todas", "~950 W", "~1.300 W"],
                 ["Mês 24/7 (ocioso)", "~R$ 100", "~R$ 125"],
                 ["Mês sob demanda (~4 h/dia)", "~R$ 50", "~R$ 65"]],
                [70 * mm, 50 * mm, 50 * mm]),
          P("Tarifa considerada: ~R$ 1,00/kWh. Valores estimados.", "small"),
          P("Ligar (botão no Node-RED do nó 2 ou terminal do nó 1)", "h2"),
          code("""ipmitool -I lanplus -H 10.0.20.60 -U ia-admin -f /root/.ipmi_senha chassis power on
ipmitool -I lanplus -H 10.0.20.60 -U ia-admin -f /root/.ipmi_senha chassis power status"""),
          P("Desligar sozinho após 60 minutos parado (na VM, pelo cron a cada 5 min)", "h2"),
          code("""#!/bin/bash
# /usr/local/bin/ia-ocioso.sh
LIMITE=60
ARQ=/var/lib/ia-ultimo-uso
USO=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | awk '{s+=$1} END {print s}')
if [ "$USO" -gt 5 ] || [ ! -f "$ARQ" ]; then date +%s > "$ARQ"; exit 0; fi
PARADO=$(( ( $(date +%s) - $(cat "$ARQ") ) / 60 ))
if [ "$PARADO" -ge "$LIMITE" ]; then
  ssh -i /root/.ssh/desligar root@10.0.20.61     # chave que só pode rodar "poweroff"
fi"""),
          P(f"No host, a chave pública vai em {M('/root/.ssh/authorized_keys')} com "
            f"{M('command=\"/sbin/poweroff\",no-port-forwarding,no-pty')} na frente: ela só sabe desligar. "
            "O Proxmox desliga a VM com segurança antes de apagar o host."),
          ]

# ---------- 12 ----------
story += [P("12. Testes de aceitação", "h1"),
          table([["Teste", "Como", "Passa se"],
                 ["Memória", "MemTest86 pela mídia virtual do BMC, 1 passada completa", "Zero erros"],
                 ["Grupos IOMMU", "Comando da seção 6", "Cada placa no seu grupo"],
                 ["Link PCIe", "nvidia-smi -q -d PCIE", "x16 em todas; Gen4 (ou Gen3 fixado)"],
                 ["Estresse das placas", "gpu-burn por 30 min com o limite de potência", "Sem erro, abaixo de 83 °C"],
                 ["Risers", "dmesg durante o gpu-burn", "Nenhum erro AER"],
                 ["Fonte", "As 5 placas no máximo ao mesmo tempo", "Não desarma"],
                 ["Modelo", "vLLM com tensor parallel 4, 30 min de perguntas", "Sem travar"],
                 ["Liga/desliga", "Desligar pelo script e ligar pelo IPMI", "Volta com a VM e os serviços"],
                 ["Disjuntor", "Tudo no máximo por 1 h", "Não desarma; tomada fria"]],
                [32 * mm, 80 * mm, 58 * mm]),
          ]

# ---------- 13 ----------
story += [P("13. Problemas comuns", "h1"),
          table([["Sintoma", "Causa provável", "Solução"],
                 ["Não liga, sem vídeo nem BMC", "Processador travado (PSB) ou BIOS antiga",
                  "Testar outro processador; atualizar a BIOS pelo BMC"],
                 ["Placa some do nvidia-smi", "Riser ou cabo de energia", "Fixar o slot em Gen3; trocar o riser"],
                 ["Erros AER no log", "Sinal ruim no riser", "Riser mais curto e blindado; Gen3"],
                 ["Host desliga no pico", "Picos rápidos das placas", "Limite de potência; fonte ATX 3.1"],
                 ["Ventoinhas acelerando em ciclos", "Limite do BMC para rotação baixa", "Ajustar limites (seção 5)"],
                 ["VM não vê as 5 placas", "Pouco espaço PCI no OVMF", "Opção X-PciMmio64Mb (seção 7)"],
                 ["vLLM trava na inicialização", "Comunicação direta entre placas", "NCCL_P2P_DISABLE=1"],
                 ["Disjuntor desarma", "Circuito comum", "Tomada 20 A exclusiva com eletricista"]],
                [45 * mm, 55 * mm, 70 * mm]),
          ]

# ---------- 14 ----------
bom = [("ASRock Rack ROMED8-2T (usada ou importada)", 3500),
       ("AMD EPYC 7302P usado sem trava de fabricante", 900),
       ("8 × 16 GB DDR4-3200 RDIMM ECC", 1300),
       ("Cooler Noctua NH-U9 TR4-SP3", 700),
       ("NVMe 2 TB PCIe 4.0", 900),
       ("Fonte ATX 3.1 1600 W Platinum", 2600),
       ("5 risers PCIe 4.0 x16 blindados, 30 cm", 900),
       ("Quadro 2020 rev. B, chapas e ventoinhas", 1500),
       ("Tomada 20 A exclusiva com DPS (eletricista)", 400)]
tot = sum(v for _, v in bom)
rows = [["Item", "R$ (estim.)"]] + [[d, f"~{brl(v)}"] for d, v in bom]
rows += [["<b>Host + quadro, sem placas de vídeo</b>", f"<b>~{brl(tot)}</b>"],
         ["5 × RTX 3060 12 GB usadas", "~7.000"],
         ["<b>Total com 5 × 3060</b>", f"<b>~{brl(tot + 7000)}</b>"],
         ["Alternativa: 5 × RTX 3090 24 GB usadas", "~25.000"]]
story += [P("14. Custos e caminho de compra", "h1"),
          table(rows, [130 * mm, 40 * mm]),
          Spacer(1, 4),
          numbered([
              "<b>Agora:</b> quadro + uma RTX 3060 ligada ao nó 5 por OCuLink (fase 5). Já dá para usar.",
              "<b>Host:</b> placa-mãe, processador, memória, cooler, NVMe e fonte. A placa de vídeo do nó 5 muda "
              "para a baia G1 e o nó 5 volta a ser um nó comum.",
              "<b>Crescer:</b> uma placa por vez, de G2 a G5. Com 4 placas o vLLM já roda em tensor parallel.",
              "<b>Depois:</b> trocar 3060 por 3090 aos poucos. Com placas misturadas, o vLLM fica limitado pela menor; "
              "agrupe placas iguais em G1–G4."]),
          P("Preços estimados em outubro de 2026; usados e importados variam muito.", "small"),
          ]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=18 * mm, bottomMargin=22 * mm,
                        title="Homelab – host de IA EPYC com 5 placas de vídeo",
                        author="João Victor Paixão Zolim")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("ok", OUT, tot)
