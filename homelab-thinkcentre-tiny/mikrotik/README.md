# `> ./mikrotik --estudo --nucleo-alternativo`

```text
 Internet
    │
 Roteador da operadora ──► Wi-Fi da casa
    │
 RB5009 (RouterOS) ──► firewall + roteamento entre VLANs
    │
 Switch gerenciável (CSS610 / CRS310) ──► VLANs + espelhamento
    ├── nós Proxmox   ── nó de IA   ── rádio/SDR
    └── porta espelho ──► Security Onion
```

**Estudo de um núcleo de rede alternativo** para o homelab, baseado em **MikroTik RB5009 + RouterOS**. Não é a configuração adotada: o homelab deste repositório usa hoje um **switch TP-Link TL-SG108E + roteador da operadora + Tailscale** (ver [`../README.md`](../README.md)). Este material explora o que mudaria ao colocar um MikroTik como roteador/firewall central, e serve como documentação de estudo e portfólio.

> ⚠️ **Diferenças em relação ao homelab adotado:** aqui o roteamento e o firewall ficam no MikroTik (não no switch TP-Link); o acesso remoto é por **WireGuard no RB5009** (em vez de Tailscale); e o esquema de VLANs é 10/20/30/40/50/99 (o adotado é 10/20/30 + espelho). Reconcilie antes de aplicar.

---

## `$ ls`

| Arquivo | O que é |
|---|---|
| `homelab_mikrotik_arquitetura.pdf` | Documento técnico: topologia, mapa de VLANs, firewall, espelhamento para o Security Onion, VPN e operação |
| `homelab_mikrotik_storage.pdf` | Plano de armazenamento: disco rápido x bulk, distribuição por nó e uso de HD externo para backup |
| `homelab_mikrotik_seguranca_acesso.pdf` | Modelo de acesso em camadas (AAA): autenticação, autorização e endurecimento |
| `homelab_mikrotik_metodologias.pdf` | Metodologias e frameworks (MITRE ATT&CK, Sigma, PTES, OWASP, Atomic Red Team, IaC, CIS) mapeados ao homelab |
| `rb5009_homelab.rsc` | Configuração de referência do RB5009 (RouterOS v7): VLANs, DHCP, NAT, firewall inter-VLAN, WireGuard e hardening |

---

## `$ cat rb5009_homelab.rsc | head`

O `.rsc` é um **modelo de referência**. Antes de aplicar:

- Ajuste os nomes de interface (`ether1`, `ether2`, `sfp-sfpplus1`) ao cabeamento real.
- Teste primeiro em um **CHR** (RouterOS virtual) para não se trancar fora do equipamento.
- O `vlan-filtering` é ativado só no último passo, de propósito.
- Nenhum segredo real (chaves WireGuard, senhas, IP público) entra neste arquivo — eles ficam fora do Git.

```console
$ /import file=rb5009_homelab.rsc     # aplica a configuração no RB5009
$ /export hide-sensitive file=backup  # gera backup legível, sem senhas
```

---

> Documentos gerados em out/2026 como estudo. As metodologias citadas são padrões públicos de mercado; a aplicação é adaptada à escala do homelab.
