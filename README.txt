Universal LCC / CAN Interface  -  Rev B
=======================================

Open LCC_Interface.kicad_pro in KiCad 9 or 10.
The project contains a native .kicad_sch and .kicad_pcb.

The schematic is the authoritative source and passes ERC with 0 errors
(remaining warnings are cosmetic: off-grid endpoints, and the embedded "LCC"
symbol library not being registered in a sym-lib-table - both harmless).


WHAT CHANGED FROM REV A (ChatGPT draft)
---------------------------------------
The Rev A schematic and PCB disagreed. The PCB net assignment was correct, but
the schematic had a systematic Y-axis flip: almost every net label sat on the
WRONG pin (TXD<->RXD swapped, CANH<->CANL swapped, the whole RJ45 pinout
mirrored, MCU header reversed) and the transceiver ground was never tied to the
bus CAN_GND. Rev B fixes the schematic so it matches the (correct) board intent,
and adds the "universal" features:

1. GROUND FIX. Local ground (U1 pin 2, MCU GND) is now one net with the bus
   CAN_GND (RJ45 pins 3 & 6) and the connector shells. This is mandatory on a
   non-isolated CAN tap.
2. UNIVERSAL FAMILY SUPPORT. Pins 5 and 8 of the SOIC-8 now go to DNP 10k
   pulldowns R2/R3. TCAN332 = both pins NC (leave R2/R3 unfitted). Fit R2/R3
   to drop in a TCAN330 (SHDN/S), TCAN334 (SHDN/STB) or TCAN337 (FAULT/S) -
   the pulldowns hold their mode pins low = normal/active operation.
3. BUS ESD PROTECTION. D1 = PESD1CAN CAN-bus TVS (SOT-23) across CAN_H/CAN_L,
   referenced to CAN_GND.
4. BULK CAP. C2 (4.7uF) added at VCC alongside C1 (100nF).
5. CONNECTOR. J1/J2 changed to the shielded Amphenol RJHSE-5380 (vetted KiCad
   library footprint, NO magnetics - correct for LCC). Metal shell pads (SH)
   are on CAN_GND. Do NOT substitute an Ethernet magjack (those have
   transformers and will not pass CAN).


ELECTRICAL
----------
- U1 TCAN332DR, 3.3 V (pins 5 & 8 = NC on the 332)
- J1/J2 dual LCC RJ45, all 8 conductors daisy-chained J1<->J2 (bus pass-through)
- J3 four-pin MCU header: 1 GND, 2 3V3, 3 CAN_TX (->TXD), 4 CAN_RX (<-RXD)
- Board is powered from the MCU 3V3 rail; bus power (PWR_POS/PWR_NEG) is
  pass-through only and is kept separate from CAN_GND. Non-isolated design.
- R1 120R termination, in series with JP1. Fit JP1 ONLY on the two boards at the
  physical ends of the bus.
- LCC = 125 kbit/s (well within the TCAN332's 1 Mbit/s rating).

LCC RJ45 pin assignment (OpenLCB S-9.6.1):
  1 CAN_H
  2 CAN_L
  3 CAN_GND
  4 ALT_L   (reserved, pass-through)
  5 ALT_H   (reserved, pass-through)
  6 CAN_GND
  7 PWR_NEG
  8 PWR_POS
  Shell/shield -> CAN_GND


PCB - COMPLETE
--------------
The Rev A board was regenerated from scratch to match the corrected schematic:
all 18 footprints placed, nets assigned, and every signal autorouted
(Freerouting) on a 60 x 50 mm two-layer board (well under the 100 x 100 mm
budget-fab price break). The bottom layer is a solid CAN_GND ground pour; every
ground and shield pad connects to it. Four M3 mounting holes, 4 mm in from each
corner (52 x 42 mm hole pattern).

Verified with KiCad's design-rule check:
   DRC violations:      0
   Unconnected items:   0   (fully routed)
   Net names match the schematic.

Remaining DRC "schematic parity" notes are cosmetic only: empty Datasheet
metadata fields, and TP1-3 / H1-H2 being board-only (test points + mounting
holes are intentionally not in the schematic).

BEFORE ORDERING, check these mechanical points in the GUI:
1. RJ45 orientation - confirm each socket's cable opening faces off the board
   edge so cables can plug in. Rotate a connector 180 deg if it faces inward.
2. Confirm the Amphenol RJHSE-5380 footprint matches your exact ordered part
   (-5380 plain vs -5385 with LEDs).
3. Component placement is functional but not optimised for looks - nudge parts
   if you want, then re-run DRC (Inspect -> Design Rules Checker).

board_top.png is a 3D render of the finished board.
LCC_Interface.kicad_pcb.revA-bak is the original ChatGPT board, kept as a backup.
