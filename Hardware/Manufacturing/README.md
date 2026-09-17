# JLCPCB production package — HKU Thermal Node Rev 1.1

Upload `HKU_Thermal_Node_Rev1.1_Gerbers.zip` as the PCB file, then upload `JLCPCB_BOM.csv` and `JLCPCB_CPL.csv` for assembly.

## Order settings

| Setting | Value |
|---|---|
| Quantity | 10 boards / 10 assembled boards |
| PCB | 2-layer FR-4, 80 × 40 mm, 1.6 mm, 1 oz copper |
| Finish | Lead-free HASL |
| Solder mask / silkscreen | Green / white |
| Stack-up | JLCPCB default 2-layer stack-up |
| Via covering | Tented |
| Panelization | Individual boards; no customer panel |
| Controlled impedance | No |
| Assembly | Economic PCBA, top side only |
| Factory-fitted references | C1, C2, R1, R2 only |

Do not factory-fit A1, J1, the Heltec module, antenna, battery, or mechanical parts. Fit these manually after delivery.

Use a Heltec WiFi LoRa 32 V3.2, 902–928 MHz variant, with a matching 920–925 MHz antenna. The module plugs into two 1×18, 2.54 mm female socket strips. Fit A1 as `MLX90640ESF-BAA-000-TU` and observe its pin-1 mark.

Before payment, confirm JLCPCB's previews show one 80 × 40 mm board and four top-side placements per board. C1, C2, R1, and R2 are non-polarized.
