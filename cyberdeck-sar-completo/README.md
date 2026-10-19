# Cyberdeck SAR – Pelican 1450

Kit de campo para operações de busca e salvamento (SAR): rede mesh LoRa (Meshtastic) com GPS, tela touch, rádio SDR, Wi-Fi em modo monitor e link 4G, montado num Pelican 1450 com estrutura interna impressa em 3D.

Autor: João Victor Paixão Zolim · github.com/joaovpzdev

## Conteúdo do pacote

| Arquivo | O que é |
|---|---|
| `cyberdeck_sar_pelican1450_desenho_tecnico.pdf` | Desenho técnico A3, 4 folhas: case, layout interno, peças 3D, blocos, materiais e energia |
| `modelo3d/cyberdeck_3d.py` | Fonte paramétrica das peças (Python + manifold3d + trimesh) |
| `modelo3d/stl/*.stl` | Peças prontas para fatiar |
| `modelo3d/render/*.png` | Pré-visualização das peças |
| `gerar_pdf.py` | Gera o PDF a partir dos mesmos parâmetros do modelo 3D |

Para alterar medidas, edite os parâmetros no topo de `cyberdeck_3d.py` e rode:

```sh
pip install manifold3d trimesh reportlab
python modelo3d/cyberdeck_3d.py   # regenera os STL
python gerar_pdf.py               # regenera o desenho técnico
```

## Conceito

- **Transporte:** case fechado, sem nenhum furo, para manter a vedação IP67.
- **Operação:** case aberto. A tela fica na tampa e todos os conectores e ventoinhas ficam no painel impresso.
- **Ar:** entra pela ventoinha sobre o Raspberry Pi, atravessa a bandeja e sai pela ventoinha do lado direito.
- **Antenas:** desrosqueadas e guardadas no porta-antenas (3 canais) antes de fechar o case.
- **Recarga sem desmontar e sem furos:** com a tampa aberta, plugue no USB-C do painel. O caminho da energia é USB-C do painel → power bank interno → UPS X1202 → Pi 5.

## Case

**Pelican 1450**
- Interno: 372 x 260 x 155 mm
- Profundidade: base 111 mm, tampa 44 mm
- Vedação: IP67
- Revenda no Brasil: [CasesBR](https://casesbr.com/produto/pelican-1450/), que se apresenta como distribuidor autorizado Pelican
- Preço: R$ 1.850 (5% de desconto no Pix), consultado em out/2026
- **Alternativa:** Vonder MAI 415 (~R$ 400), mesmas medidas externas (406 x 330 x 174 mm), interno 375 x 270 x 150 mm. Confirme a altura da base e teste a vedação (o anúncio diz IP67, uma ficha cita IP54).

## Peças impressas

| STL | Qtd | Medidas (mm) | Posição na mesa |
|---|---|---|---|
| 01_bandeja_esquerda | 1 | 180 x 250 x 95 | pilares para cima |
| 02_bandeja_direita | 1 | 180 x 250 x 95 | pilares para cima |
| 03_painel_esquerdo | 1 | 180 x 250 x 3 | plano |
| 04_painel_direito | 1 | 180 x 250 x 3 | plano |
| 05_moldura_tela | 1 | 215 x 146 x 19 | face (janela) para baixo |
| 06_travessa_tela | 2 | 12 x 143 x 4 | plano |
| 07_tala_emenda | 4 | 40 x 16 x 4 | plano |

**Configuração de impressão**
- Material: **ASA** (o melhor contra sol e calor) ou PETG. Evite PLA, que deforma acima de ~55 °C.
- Bico 0,4 mm, camada 0,2 mm, 4 perímetros, 25% de preenchimento giroide.
- Mesa mínima: 256 x 256 mm. Por isso a bandeja e o painel são divididos ao meio e unidos por talas.
- Filamento estimado: ~1 kg.
- Furos M3 com Ø3,2 para parafuso autoatarraxante. Se usar insertos de latão, alargue para Ø4,2.

**Confira antes de imprimir**
- [ ] A furação da UPS Geekworm X1202 bate com os standoffs (padrão do Pi 5, 58 x 49 mm)?
- [ ] As baterias 18650 ficam acima do piso com standoffs de 24 mm?
- [ ] A área útil da Touch Display 2 está centralizada na moldura (janela de 157 x 90)?
- [ ] As medidas dos dongles USB (SDR, Wi-Fi, modem, gaveta do SSD) cabem nos berços?
- [ ] O power bank cabe no compartimento (até 152 x 68 x 30 mm)? Se não couber, ajuste `PB_IN` em `cyberdeck_3d.py` e gere os arquivos de novo.
- [ ] O fundo interno do Pelican está plano onde a bandeja vai apoiar? (Use pés de borracha se precisar.)

## Montagem

1. Imprima as peças e una as metades da bandeja e do painel com as talas (parafusos M3).
2. Monte a pilha: UPS X1202 nos standoffs, depois o Pi 5 com dissipador baixo, depois o HAT RAK6421 com barra de pinos estendida.
3. Prenda os dongles USB nos berços com abraçadeiras, passando-as pelos rasgos do piso.
4. Coloque o power bank no compartimento e prenda com duas cintas de velcro de 20 mm, passando-as pelos rasgos das orelhas. Ligue o USB-C do painel na entrada do power bank e a saída do power bank na entrada da UPS X1202.
5. Instale no painel:
   - as 6 SMA de painel: LoRa 1, LoRa 2, GPS, Wi-Fi A, Wi-Fi B e SDR;
   - o keystone RJ45, o USB-C de painel e a chave das ventoinhas;
   - as duas ventoinhas de 60 mm, com filtro de espuma na de entrada.
6. Ligue os cabos (pigtails SMA, extensões USB curtas, cabo DSI) e parafuse o painel nos 12 pilares.
7. Prenda a moldura da tela na tampa com fita VHB 3M, sem furar o case. Encaixe a tela e feche com as travessas.
8. Coloque a bandeja no case. Guarde as antenas e os sachês de sílica gel. Feche.

## Fases de compra

| Fase | Itens | Estimativa |
|---|---|---|
| 1. Núcleo LoRa/GPS | Pi 5 16 GB, HAT + LoRa 1 W + GPS, antenas, SSD, microSD | ~R$ 3.310 |
| 2. Case e energia | Pelican 1450, UPS + baterias, power bank 20.000 mAh pass-through, ventoinhas, conectores, filamento | ~R$ 3.460 |
| 3. Interface | Touch Display 2 7" + teclado Bluetooth | ~R$ 910 |
| 4. Rádios extras | RTL-SDR Blog V3, adaptador Wi-Fi MT7612U, 2º rádio LoRa, sensor ambiental | ~R$ 920 |
| 5. Campo | Modem 4G USB, carregador veicular USB-C PD, painel solar dobrável USB-C | ~R$ 900 |
| **Total** | | **~R$ 9.500** |

Preços com "~" são estimativas. Itens importados variam com frete e impostos.

## Energia

| | |
|---|---|
| Consumo com tudo ligado | ~18–20 W |
| Energia interna: UPS (~37 Wh) + power bank 20.000 mAh (~60 Wh úteis) | ~97 Wh |
| Autonomia com tudo ligado | ~5 h |
| Recarga | tomada, viatura 12 V ou painel solar USB-C PD, pelo USB-C do painel |

O power bank precisa ter carga com passagem de energia (pass-through): ele alimenta o kit e carrega ao mesmo tempo. Se ele cortar a saída por um instante ao trocar a fonte, a UPS segura o Pi.

## Clima hostil

- **Fechado:** IP67. **Aberto:** opere sob abrigo, com capa ou toldo; a tela e o painel não são vedados.
- Use filtro de espuma na entrada de ar contra poeira.
- Passe verniz conformal (tropicalização) nas placas contra umidade e maresia.
- Deixe sílica gel no case fechado.
- Baterias Li-ion só devem ser carregadas entre 0 e 45 °C.
- O Pi 5 reduz o clock perto de 85 °C. Monitore com `vcgencmd measure_temp` ou pelo agente Zabbix.

## Regras e segurança

- O LoRa usa a faixa de 915 MHz. Confira no regulamento de radiação restrita da Anatel o limite de potência e o ganho de antena antes de usar o rádio em 1 W.
- O SDR e o ADS-B só recebem.
- Faça auditoria Wi-Fi apenas em redes próprias ou com autorização.
- Para operar com drone: cadastro no SISANT (ANAC) e autorização de voo no SARPAS (DECEA).
