# =============================================================================
#  RB5009 - Configuracao do Homelab (ThinkCentre Tiny)
#  Autor: Joao Victor Paixao Zolim
#  RouterOS v7.x
#
#  ATENCAO: script de REFERENCIA. Ajuste os nomes de interface (ether1,
#  ether2, sfp-sfpplus1) conforme o cabeamento real antes de aplicar.
#  Teste primeiro em um CHR (RouterOS virtual) para nao se trancar fora.
#
#  Topologia:
#    ether1            -> WAN (uplink para o roteador da operadora)
#    ether2            -> TRUNK para o switch gerenciavel (todas as VLANs)
#    bridge1           -> bridge com vlan-filtering ativo
#
#  Mapa de VLANs:
#    VLAN 10  Gerencia     10.10.10.0/24
#    VLAN 20  Servidores   10.10.20.0/24
#    VLAN 30  Radio/Sensor 10.10.30.0/24
#    VLAN 40  Lab ofensivo 10.10.40.0/24  (isolado)
#    VLAN 50  IA / GPU     10.10.50.0/24
#    VLAN 99  Espelho SPAN sem IP (Security Onion)
# =============================================================================

# -----------------------------------------------------------------------------
# 1. BRIDGE
# -----------------------------------------------------------------------------
/interface bridge
add name=bridge1 vlan-filtering=no comment="Bridge principal do lab"
# vlan-filtering fica 'no' ate o fim; so ativamos apos tudo pronto (passo 9)

# -----------------------------------------------------------------------------
# 2. PORTAS NA BRIDGE
# -----------------------------------------------------------------------------
/interface bridge port
# Porta trunk para o switch gerenciavel (carrega todas as VLANs com tag)
add bridge=bridge1 interface=ether2 comment="TRUNK -> switch"

# -----------------------------------------------------------------------------
# 3. VLANs NA BRIDGE (quais tags trafegam em cada porta)
# -----------------------------------------------------------------------------
/interface bridge vlan
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=10
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=20
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=30
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=40
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=50
add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=99

# -----------------------------------------------------------------------------
# 4. INTERFACES VLAN (gateway L3 de cada segmento)
#    A VLAN 99 (espelho) NAO recebe interface L3 nem IP: e so escuta.
# -----------------------------------------------------------------------------
/interface vlan
add interface=bridge1 name=vlan10-mgmt   vlan-id=10 comment="Gerencia"
add interface=bridge1 name=vlan20-srv    vlan-id=20 comment="Servidores"
add interface=bridge1 name=vlan30-radio  vlan-id=30 comment="Radio/Sensores"
add interface=bridge1 name=vlan40-lab    vlan-id=40 comment="Lab ofensivo"
add interface=bridge1 name=vlan50-ia     vlan-id=50 comment="IA / GPU"

# -----------------------------------------------------------------------------
# 5. ENDERECAMENTO IP
# -----------------------------------------------------------------------------
/ip address
add address=10.10.10.1/24 interface=vlan10-mgmt  comment="GW Gerencia"
add address=10.10.20.1/24 interface=vlan20-srv   comment="GW Servidores"
add address=10.10.30.1/24 interface=vlan30-radio comment="GW Radio"
add address=10.10.40.1/24 interface=vlan40-lab   comment="GW Lab ofensivo"
add address=10.10.50.1/24 interface=vlan50-ia    comment="GW IA/GPU"

# WAN: cliente DHCP recebendo IP do roteador da operadora
/ip dhcp-client
add interface=ether1 comment="WAN - recebe IP da operadora"

# -----------------------------------------------------------------------------
# 6. POOLS E SERVIDORES DHCP (um por VLAN)
# -----------------------------------------------------------------------------
/ip pool
add name=pool-mgmt  ranges=10.10.10.100-10.10.10.200
add name=pool-srv   ranges=10.10.20.100-10.10.20.200
add name=pool-radio ranges=10.10.30.100-10.10.30.200
add name=pool-lab   ranges=10.10.40.100-10.10.40.200
add name=pool-ia    ranges=10.10.50.100-10.10.50.200

/ip dhcp-server
add name=dhcp-mgmt  interface=vlan10-mgmt  address-pool=pool-mgmt  lease-time=1d
add name=dhcp-srv   interface=vlan20-srv   address-pool=pool-srv   lease-time=1d
add name=dhcp-radio interface=vlan30-radio address-pool=pool-radio lease-time=1d
add name=dhcp-lab   interface=vlan40-lab   address-pool=pool-lab   lease-time=1d
add name=dhcp-ia    interface=vlan50-ia    address-pool=pool-ia    lease-time=1d

/ip dhcp-server network
add address=10.10.10.0/24 gateway=10.10.10.1 dns-server=10.10.10.1
add address=10.10.20.0/24 gateway=10.10.20.1 dns-server=10.10.20.1
add address=10.10.30.0/24 gateway=10.10.30.1 dns-server=10.10.30.1
add address=10.10.40.0/24 gateway=10.10.40.1 dns-server=10.10.40.1
add address=10.10.50.0/24 gateway=10.10.50.1 dns-server=10.10.50.1

# -----------------------------------------------------------------------------
# 7. DNS e NAT
# -----------------------------------------------------------------------------
/ip dns
set allow-remote-requests=yes servers=1.1.1.1,9.9.9.9

/ip firewall nat
add chain=srcnat out-interface=ether1 action=masquerade comment="NAT de saida (WAN)"

# -----------------------------------------------------------------------------
# 8. WIREGUARD (acesso remoto)
#    Gere as chaves e preencha o peer. Atencao ao CGNAT da operadora.
# -----------------------------------------------------------------------------
/interface wireguard
add name=wg0 listen-port=51820 comment="VPN de acesso remoto"
/ip address
add address=10.10.200.1/24 interface=wg0 comment="Rede da VPN"
# Exemplo de peer (preencher public-key do cliente):
# /interface wireguard peers
# add interface=wg0 public-key="<CHAVE_PUBLICA_DO_CLIENTE>" \
#     allowed-address=10.10.200.2/32

# =============================================================================
# 9. FIREWALL
#    Politica: negar por padrao, permitir por excecao.
# =============================================================================
/ip firewall filter

# ---- Cadeia INPUT (protege o proprio roteador) ----
add chain=input action=accept connection-state=established,related \
    comment="Permite trafego ja estabelecido"
add chain=input action=drop connection-state=invalid \
    comment="Descarta invalidos"
add chain=input action=accept protocol=icmp comment="Permite ping"
add chain=input action=accept in-interface=vlan10-mgmt \
    comment="Gerencia pode administrar o roteador"
add chain=input action=accept protocol=udp dst-port=51820 \
    comment="Permite handshake WireGuard"
add chain=input action=accept in-interface=wg0 \
    comment="Clientes da VPN"
add chain=input action=drop comment="Bloqueia o resto do INPUT"

# ---- Cadeia FORWARD (politica entre VLANs) ----
add chain=forward action=accept connection-state=established,related \
    comment="Permite retorno de trafego ja estabelecido"
add chain=forward action=drop connection-state=invalid \
    comment="Descarta invalidos"

# Gerencia alcanca todas as VLANs
add chain=forward action=accept in-interface=vlan10-mgmt \
    comment="Gerencia -> todas"

# Isolamento TOTAL do lab ofensivo (jaula)
add chain=forward action=drop in-interface=vlan40-lab \
    out-interface=!vlan40-lab comment="Lab ofensivo nao sai da propria VLAN"

# Radio: so sai para a internet, nao conversa com o resto do lab
add chain=forward action=accept in-interface=vlan30-radio \
    out-interface=ether1 comment="Radio -> internet"
add chain=forward action=drop in-interface=vlan30-radio \
    comment="Radio nao fala com o resto do lab"

# IA/GPU pode gravar resultados nos servidores
add chain=forward action=accept in-interface=vlan50-ia \
    out-interface=vlan20-srv comment="IA -> Servidores"

# Servidores e IA saem para a internet (updates/feeds)
add chain=forward action=accept in-interface=vlan20-srv \
    out-interface=ether1 comment="Servidores -> internet"
add chain=forward action=accept in-interface=vlan50-ia \
    out-interface=ether1 comment="IA -> internet"

# VPN alcanca gerencia e servidores
add chain=forward action=accept in-interface=wg0 \
    out-interface=vlan10-mgmt comment="VPN -> Gerencia"
add chain=forward action=accept in-interface=wg0 \
    out-interface=vlan20-srv comment="VPN -> Servidores"

# Bloqueia todo o resto entre segmentos
add chain=forward action=drop comment="DROP padrao entre VLANs"

# -----------------------------------------------------------------------------
# 10. HARDENING DE SERVICOS
#     Desativa servicos inseguros e restringe a gerencia a VLAN 10.
# -----------------------------------------------------------------------------
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set api disabled=yes
set api-ssl disabled=yes
set ssh address=10.10.10.0/24
set winbox address=10.10.10.0/24

/tool mac-server
set allowed-interface-list=none
/tool mac-server mac-winbox
set allowed-interface-list=none

/ip neighbor discovery-settings
set discover-interface-list=none

# -----------------------------------------------------------------------------
# 11. ATIVA O VLAN-FILTERING (ultimo passo!)
#     So depois de tudo configurado, para nao perder acesso no meio.
# -----------------------------------------------------------------------------
/interface bridge
set bridge1 vlan-filtering=yes

# =============================================================================
# FIM. Lembrete de backup:
#   /export hide-sensitive file=backup-config
#   /system backup save name=backup-full
# =============================================================================
