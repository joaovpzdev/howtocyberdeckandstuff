# Cyberdeck SAR – Edição R$ 5 mil

Versão enxuta do Cyberdeck SAR. Mantém a missão central (rede mesh LoRa 1 W, GPS, tela touch, mapa offline, UPS e proteção IP67) dentro de R$ 5.000. Usa o case **Patola MP-0039** no lugar do Pelican 1450.

Autor: João Victor Paixão Zolim · github.com/joaovpzdev

## Conteúdo

| Arquivo | O que é |
|---|---|
| `documento/cyberdeck_sar_edicao_5k.pdf` | Análise do projeto completo, materiais, montagem, comparativo e evolução |
| `cyberdeck_sar_5k_desenho_tecnico.pdf` | Desenho técnico A3 (4 folhas) |
| `modelo3d/stl/*.stl` | Peças para impressão |
| `modelo3d/cyberdeck_3d.py` | Fonte paramétrica das peças (`DECK_Z = 80` para o MP-0039) |

## Materiais (R$ 5.000)

| Fase | Item | R$ |
|---|---|---|
| 1 | Raspberry Pi 5 8 GB (lacrado) | 1.560 |
| 1 | HAT RAK6421 + RAK13302 (LoRa 1 W) + RAK12501 (GPS) | ~550 |
| 1 | Antena LoRa 915 + antena GPS ativa | ~190 |
| 1 | microSD 128 GB High Endurance + dissipador baixo | ~150 |
| 2 | Patola MP-0039 IP67 | 486 |
| 2 | UPS X1202 + 4 x 18650 | ~560 |
| 2 | 2 ventoinhas 60 x 15 mm 5 V + filtro | ~150 |
| 2 | SMA de painel x2, keystone RJ45, USB-C de painel, chave, cabos | ~150 |
| 2 | Filamento PETG/ASA ~1 kg + parafusos | ~170 |
| 3 | Raspberry Pi Touch Display 2 7" | 759 |
| – | Reserva (frete, impostos, imprevistos) | ~275 |

"~" = estimativa.

## Peças impressas (17)

São as mesmas da versão completa, mais 6 calços:

- bandeja e painel, ambos divididos ao meio;
- moldura da tela e 2 travessas;
- 4 talas de emenda;
- **4 calços de frente/fundo e 2 laterais**, que travam a bandeja no case maior.

Imprima em ASA ou PETG, numa mesa mínima de 256 x 256 mm.

## Diferenças para a versão completa

- Case Patola MP-0039 (base com 95 mm): painel a 80 mm do fundo e ventoinhas slim de 15 mm.
- Painel com só 2 SMA (LoRa e GPS). Os demais furos são abertos quando cada expansão for instalada.
- Os berços de SDR, Wi-Fi, 4G e SSD já vêm impressos, vazios.
- O compartimento do power bank fica pronto, com o power bank como opcional.

## Evolução sugerida

1. Power bank 20.000 mAh pass-through (~R$ 300): autonomia de ~3,5 h para ~9 h
2. RTL-SDR Blog V3
3. 2º rádio LoRa
4. Modem 4G
5. SSD
6. Adaptador Wi-Fi MT7612U (modo monitor)
7. Pelican 1450 ou Vonder MAI 415 (mesmas medidas externas, ~R$ 400): mude `DECK_Z` para 95 e gere os STL de novo; na MAI 415, confirme antes a altura da base

## Antes de imprimir

Confira com as peças em mãos:
- a furação da UPS X1202;
- a área útil da tela;
- a altura das baterias sob a UPS;
- a folga entre o compartimento do power bank e a UPS.
