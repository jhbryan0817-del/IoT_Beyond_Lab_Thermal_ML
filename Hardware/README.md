# Hardware

CrowdAware Node Rev 1.1 is a carrier board for a low-resolution thermal occupancy node. It is derived from [`crowdaware-node`](https://github.com/crowdaware-inno-wing-iot/crowdaware-node) and remains subject to its GPL-3.0 licence; see `COPYING-CrowdAware-GPL-3.0.txt`.

## Rev 1.1 technical specification

| Property | Specification |
|---|---|
| Carrier outline | 80 × 40 mm rectangular PCB |
| Mounting | Four M3 mounting holes |
| Thermal sensor | Melexis MLX90640ESF-BAA-000-TU, 32 × 24 pixels, 110° × 75° field of view |
| Sensor interface | I²C: SDA and SCL |
| Sensor supply | Switchable `V_EXT` rail |
| I²C pull-ups | `R1` and `R2`, 1 kΩ to `V_EXT` |
| Sensor decoupling | `C1` 100 nF and `C2` 10 µF |
| Controller/radio module | Heltec WiFi LoRa 32 V3 |
| Module connection | Two 1×18, 2.54 mm female socket strips |
| Radio antenna | External, matched to the Heltec frequency variant |
| Factory-SMT partition | `C1`, `C2`, `R1`, and `R2` |
| Manual through-hole partition | `A1` thermal sensor and `J1` socket strips |
| System-level components | Heltec module, antenna, optional battery, enclosure, standoffs, and fasteners |

## Changes from the CrowdAware carrier

| Change | Technical rationale |
|---|---|
| Replaced the original outline with an 80 × 40 mm rectangle and repositioned four M3 holes | Separates the sensor region from the controller region and defines a regular enclosure interface. |
| Moved the MLX90640 to the right of the Heltec footprint | Increases separation from heat sources on the ESP32 module, OLED, regulator, and radio. |
| Moved `C1` and `C2` beside the sensor | Shortens the local supply-decoupling path. |
| Changed `C1` from 100 µF to 100 nF and retained `C2` as 10 µF | Matches the MLX90640 local-decoupling arrangement. |
| Changed the SDA/SCL pull-up supply from always-on `3V3` to switchable `V_EXT` | Prevents the I²C lines from partially back-powering the sensor while `V_EXT` is disabled. |
| Corrected `J1` from two 1×20 sockets to two 1×18 sockets | Matches the Heltec WiFi LoRa 32 V3 footprint. |
| Corrected the MLX90640 tube-pack order code and substituted active capacitor selections | Aligns the BOM with the specified sensor package and currently active passive components. |

The photographed legacy assembly contains a switch and a separate power module. Those circuits are absent from the CrowdAware repository KiCad source and are not part of Rev 1.1.

## BOM and assembly partition

The original CrowdAware CSV describes the carrier assembly rather than a complete thermal node. It includes the MLX90640 (`A1`), passives, and composite socket footprint (`J1`), while excluding the plug-in Heltec module, antenna, battery, enclosure, and mechanical hardware.

Rev 1.1 separates those scopes into two files:

| File | Scope |
|---|---|
| `BOM/BOM-PCBA-SMD.csv` | SMD components associated with the populated carrier board |
| `BOM/BOM-NODE-COMPLETE.csv` | Carrier, sensing, controller, radio, power-option, and mechanical components for one node |

## Manufacturing-data scope

- The `KiCad/` directory contains the project, schematic, and PCB layout sources.
- No Gerber, Excellon drill, or validated component-position file is included in this revision.
- Bare-PCB fabrication covers the substrate, copper, plated holes and vias, solder mask, and silkscreen.
- PCBA scope is defined by the factory-SMT partition in `BOM-PCBA-SMD.csv`.
- Structural file checks and CSV parsing have been completed; KiCad ERC, DRC, copper-zone refill, and physical-fit validation are not recorded for Rev 1.1.

## Primary references

- [Original CrowdAware repository](https://github.com/crowdaware-inno-wing-iot/crowdaware-node)
- [MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf)
- [KiCad PCB fabrication-output documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)

