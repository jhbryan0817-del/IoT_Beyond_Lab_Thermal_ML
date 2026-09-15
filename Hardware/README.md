# Hardware

This folder contains CrowdAware Node Rev 1.1, a first carrier-board revision for the thermal-occupancy proof of concept. It is derived from [`crowdaware-node`](https://github.com/crowdaware-inno-wing-iot/crowdaware-node) and remains subject to its GPL-3.0 licence; see `COPYING-CrowdAware-GPL-3.0.txt`.

## What changed and why

| Change from the original carrier | Reason |
|---|---|
| Changed the outline to a simple 80 × 40 mm rectangle and repositioned four M3 holes | Creates a separate sensor region and simplifies the first CAD enclosure. |
| Moved the MLX90640 to the right of the Heltec footprint | Reduces thermal coupling from the ESP32, OLED, regulator, and radio. |
| Moved C1 and C2 beside the sensor | Shorter supply-decoupling path. |
| Changed C1 from 100 µF to 100 nF; retained C2 as 10 µF | Matches the MLX90640 datasheet's local-decoupling arrangement. |
| Changed the SDA/SCL pull-up supply from always-on `3V3` to switchable `V_EXT` | Avoids partially back-powering the sensor when `V_EXT` is disabled. |
| Corrected J1 from two 1×20 sockets to two 1×18 sockets | Matches the Heltec WiFi LoRa 32 V3 footprint. |
| Corrected the MLX90640 tube-pack order code and replaced NRND/EOL capacitor selections | Makes prototype procurement less error-prone. |

The photographed legacy assembly also contains a switch and a separate power module. Those circuits are not present in the repository's KiCad source and therefore are not recreated in Rev 1.1. For initial bring-up, power the Heltec by USB; add the battery/power subsystem only after its requirements and connector polarity are confirmed.

## What an outsourced order includes

There are two distinct order types:

1. **Bare PCB fabrication:** the supplier makes only the FR-4 board—copper tracks and vias, drilled/plated holes, solder mask, and silkscreen. It includes no electronic components.
2. **PCBA:** the supplier makes the board and places the components specified in an assembly BOM and component-placement file. For this revision, only `C1`, `C2`, `R1`, and `R2` are intended as straightforward outsourced SMT placements.

Order and install separately unless a manufacturer explicitly quotes through-hole assembly:

- one MLX90640 thermal sensor;
- two 1×18 female socket strips;
- one Heltec WiFi LoRa 32 V3 of the correct frequency variant;
- the matching LoRa antenna/lead;
- optional protected battery;
- enclosure, standoffs, and fasteners.

## Interpreting the original CrowdAware BOM

The original CSV was a **carrier-board procurement BOM**, not a complete-node BOM and not a turnkey PCBA package:

- It included carrier designators such as the MLX90640 (`A1`), passives, and the composite socket footprint (`J1`).
- It omitted the plug-in Heltec, antenna, battery, enclosure, and other system-level items.
- It used Mouser numbers and the repository did not provide a component-placement/CPL file. Therefore, the CSV alone was insufficient to instruct an automated PCB assembler.

This repository deliberately uses two BOMs:

- `BOM/BOM-PCBA-SMD.csv` — send to an assembler together with a validated CPL/position file.
- `BOM/BOM-NODE-COMPLETE.csv` — purchasing and build list for one complete node, including items installed manually.

## Before generating Gerbers

1. Open `KiCad/CrowdAware Node Rev1.1.kicad_pro` in KiCad 10.
2. Run schematic ERC.
3. Update PCB from schematic (`F8`).
4. Press `B` in PCB Editor to refill the GND zones.
5. Run PCB DRC and require zero unconnected, clearance, and board-edge errors.
6. Print at 100% scale and check the real Heltec, sockets, sensor, antenna, USB access, and all mounting holes.
7. Only then generate and inspect Gerber and Excellon drill files.

The committed Rev 1.1 source has passed JSON/S-expression balance, duplicate-UUID, and CSV parsing checks, but KiCad ERC/DRC could not be run in the authoring environment. It must not be submitted for manufacturing without the checks above.

## Suggested first build

Order five bare two-layer prototypes using the board manufacturer's standard 1.6 mm FR-4 and 1 oz copper options. Assemble and test one node before populating the remaining boards. Connect the correct antenna before enabling LoRa transmission.

## Primary references

- [Original CrowdAware repository](https://github.com/crowdaware-inno-wing-iot/crowdaware-node)
- [MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf)
- [KiCad PCB fabrication-output documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)
