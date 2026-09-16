# Hardware

CrowdAware Node Rev 1.1 is a carrier board for a low-resolution thermal occupancy node. It is derived from [`crowdaware-node`](https://github.com/crowdaware-inno-wing-iot/crowdaware-node) and remains subject to its GPL-3.0 licence; see `COPYING-CrowdAware-GPL-3.0.txt`.

## Rev 1.1 technical specification

| Property | Specification |
|---|---|
| Carrier outline | 80 × 40 mm rectangular PCB |
| Mounting | Four M3 mounting holes |
| Thermal sensor | Melexis MLX90640ESF-BAA-000-TU, 32 × 24 pixels, 110° × 75° field of view |
| Sensor interface | I²C: SDA on Heltec GPIO41 and SCL on Heltec GPIO42 |
| Sensor supply | Switchable 3.3 V `V_EXT` rail; GPIO36 active-low enable |
| I²C pull-ups | `R1` and `R2`, 1 kΩ to `V_EXT` |
| Sensor decoupling | `C1` 100 nF adjacent to the MLX90640 supply pins and `C2` 10 µF bulk decoupling |
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
| Positioned `C1` immediately below the MLX90640 and connected it directly between the local `V_EXT` branch and ground plane; positioned `C2` behind it on the same branch | Reduces the high-frequency decoupling loop while retaining local bulk capacitance. |
| Changed `C1` from 100 µF to 100 nF and retained `C2` as 10 µF | Matches the MLX90640 local-decoupling arrangement. |
| Changed the SDA/SCL pull-up supply from always-on `3V3` to switchable `V_EXT` | Keeps the I²C high level in the sensor power domain and removes pull-up current while `V_EXT` is disabled. |
| Mapped SDA to Heltec GPIO41 and SCL to GPIO42, with separate bottom-layer fan-out near the socket | Aligns the carrier with the Heltec V3 pin definition and removes the inherited signal crossover. |
| Defined GPIO36/V_EXT as active-low in the schematic | Aligns the power-control documentation with the Heltec V3 electrical behavior. |
| Replaced the local `V_EXT` copper island at Heltec pads 30/32 with an explicit 0.5 mm trace | Removes a single-spoke thermal-relief dependency and makes the power connection deterministic. |
| Corrected `J1` from two 1×20 sockets to two 1×18 sockets | Matches the Heltec WiFi LoRa 32 V3 footprint. |
| Corrected the MLX90640 tube-pack order code and substituted active capacitor selections | Aligns the BOM with the specified sensor package and currently active passive components. |
| Standardized passive and mounting-hole identifiers; assigned board-only references `H1`–`H4`; added project-local MLX90640, Heltec, resistor, and capacitor definitions | Makes the Rev 1.1 source self-contained and preserves schematic-to-PCB parity. |
| Removed the unresolved external MLX90640 STEP-model reference and updated standard 3D-library variables to KiCad 10 | Eliminates broken project paths while retaining the sensor envelope on fabrication and courtyard layers. |

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
- `KiCad/IoT_Thermal.kicad_sym`, `KiCad/IoT_Thermal.pretty/`, `sym-lib-table`, and `fp-lib-table` contain the project-local custom definitions.
- No Gerber, Excellon drill, or validated component-position file is included in this revision.
- Bare-PCB fabrication covers the substrate, copper, plated holes and vias, solder mask, and silkscreen.
- PCBA scope is defined by the factory-SMT partition in `BOM-PCBA-SMD.csv`.
- The source incorporates corrected I²C routing, current Rev 1.1 component placement, and a board-wide two-layer ground-zone definition.

## Design verification

KiCad 10.0.6 verification of the committed Rev 1.1 sources produced:

- ERC: 0 violations.
- DRC: 0 violations.
- Unconnected pads: 0.
- Schematic-to-PCB parity issues: 0.

## Primary references

- [Original CrowdAware repository](https://github.com/crowdaware-inno-wing-iot/crowdaware-node)
- [MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf)
- [KiCad PCB fabrication-output documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)

