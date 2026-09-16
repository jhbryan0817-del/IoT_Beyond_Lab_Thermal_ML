# Hardware

HKU Thermal Node Rev 1.1 is a carrier board for a low-resolution thermal occupancy node. Its upstream hardware lineage and GPL-3.0 acknowledgement are recorded in the repository-level `README.md`; the retained licence is in `COPYING-HARDWARE-GPL-3.0.txt`.

## Current status

The Rev 1.1 source now connects the MLX90640 I²C bus to the intended Heltec WiFi LoRa 32 V3 pins:

| Signal | Heltec GPIO | Heltec header | Carrier pad |
|---|---:|---:|---:|
| SDA | 41 | J3 pin 15 | J1 pad 7 |
| SCL | 42 | J3 pin 16 | J1 pad 5 |

The inherited connections to GPIO34/GPIO33 (carrier pads 21/23) were removed because those pins are reserved on the Heltec V3. The schematic and PCB routing were corrected in place; the board is still Rev 1.1.

**Production status:** source correction complete; KiCad verification and manufacturing-output generation are still required. Do not send the repository contents directly to a manufacturer and do not reuse outputs made before this correction.

## What Rev 1.1 changes from the upstream carrier

| Change | Concise reason |
|---|---|
| Moves the MLX90640 outside the Heltec module area | Reduces thermal contamination and gives the sensor a clearer optical/mechanical region. |
| Uses 100 nF local plus 10 µF bulk decoupling | Matches the sensor's practical local power-decoupling needs. |
| Pulls SDA/SCL up to switchable `V_EXT` | Prevents back-powering and pull-up current while the sensor rail is off. |
| Maps I²C to GPIO41/GPIO42 and corrects the Rev 1.1 header pads | Avoids reserved Heltec V3 pins and matches the intended firmware mapping. |
| Uses an 80 × 40 mm outline with four M3 holes | Provides a regular prototype/enclosure interface. |
| Uses two 1×18 sockets, corrected order codes, and project-local KiCad libraries | Matches the Heltec V3 and makes the design portable. |
| Uses an explicit `V_EXT` trace | Makes the switched sensor-power path unambiguous. |

The photographed legacy assembly includes a switch and a separate power module. Those circuits are absent from the original repository's KiCad source and are not part of Rev 1.1.

## Rev 1.1 specification

| Property | Specification |
|---|---|
| Board | 80 × 40 mm, two copper layers, four M3 mounting holes |
| Sensor | MLX90640ESF-BAA-000-TU, 32 × 24 pixels, 110° × 75° field of view |
| I²C | SDA GPIO41; SCL GPIO42 |
| Sensor power | Switchable 3.3 V `V_EXT`; GPIO36 active-low enable |
| Pull-ups | `R1`, `R2`: 1 kΩ to `V_EXT` |
| Decoupling | `C1`: 100 nF; `C2`: 10 µF |
| Controller/radio | Heltec WiFi LoRa 32 V3, frequency variant selected separately |
| Factory-SMT scope | `C1`, `C2`, `R1`, `R2` |
| Manual scope | `A1`, two socket strips represented by `J1`, Heltec module, antenna, and mechanics |

## What the hardware files are

Think of the source as one project plus its parts catalogue:

| File or folder | Plain-language purpose |
|---|---|
| `README.md` | This design summary and production checklist. |
| `COPYING-HARDWARE-GPL-3.0.txt` | The inherited hardware licence. Keep it with redistributed source. |
| `BOM/BOM-PCBA-SMD.csv` | The four parts intended for factory SMT assembly. |
| `BOM/BOM-NODE-COMPLETE.csv` | The broader shopping list for one complete node, including manual and mechanical parts. |
| `KiCad/HKU Thermal Node Rev1.1.kicad_pro` | The KiCad project file. Open this file first. |
| `KiCad/HKU Thermal Node Rev1.1.kicad_sch` | The electrical circuit and net connections. |
| `KiCad/HKU Thermal Node Rev1.1.kicad_pcb` | The board outline, component positions, pads, copper routing, and zones. |
| `KiCad/IoT_Thermal.kicad_sym` | Project-local schematic symbols. |
| `KiCad/IoT_Thermal.pretty/` | Project-local PCB footprint library. |
| `*.kicad_mod` inside `.pretty/` | One physical pad/outline pattern for a particular component. |
| `KiCad/sym-lib-table` and `KiCad/fp-lib-table` | Tell KiCad where the local symbol and footprint libraries are. |

The `.kicad_sch` and `.kicad_pcb` files are editable design sources. Gerbers, drill files, and placement files are generated manufacturing outputs; they are deliberately not committed yet because they must be regenerated after the checks below.

### PCB title and branding text

The small text printed on the board is stored in `KiCad/HKU Thermal Node Rev1.1.kicad_pcb` as front- and back-silkscreen text objects. Edit it visually in KiCad PCB Editor rather than editing the file as text. The current front title is `HKU Thermal Node`, with `Rev 1.1` and `HKU IoT Beyond Lab` below it. The upstream board used HKU team text, not an embedded graphical HKU logo; no logo artwork is present in this source.

## What a manufacturer needs

For a **bare PCB**, provide:

- Gerbers for both copper layers, both solder-mask layers, the silkscreen layers actually used, and `Edge.Cuts`.
- Excellon drill files, preferably with plated and non-plated holes separated.
- A short fabrication note or order settings: two-layer FR-4, board thickness, copper weight, surface finish, solder-mask colour, and quantity.

For **SMT assembly**, also provide:

- `BOM-PCBA-SMD.csv`, adapted to the manufacturer's BOM template if required.
- A top-side component-placement file (CPL/POS) in millimetres.
- A top assembly drawing showing references and polarity/orientation.

With the current assembly split, the placement file should contain only `C1`, `C2`, `R1`, and `R2`. `A1` and the two `J1` socket strips are through-hole/manual parts unless a manufacturer separately quotes them.

## First-time KiCad-to-prototype workflow

Use KiCad 10 and perform these steps in order:

1. **Open and preserve the project.** Clone/download the whole repository, then open `KiCad/HKU Thermal Node Rev1.1.kicad_pro`. Confirm there are no missing symbol or footprint warnings. Work from a clean copy and keep this revision named Rev 1.1.
2. **Verify the schematic.** Open Schematic Editor. Confirm SDA is on J1 pad 7/GPIO41 and SCL is on J1 pad 5/GPIO42. Run **Inspect → Electrical Rules Checker**, investigate every error, and save the report or a screenshot with the order records.
3. **Synchronize the PCB.** From the schematic use **Tools → Update PCB from Schematic** (`F8`). Review the change list before accepting it; it should not remap or move unrelated parts.
4. **Refill and check the layout.** In PCB Editor press `B` to refill copper zones. Run **Inspect → Design Rules Checker**. Resolve all violations and confirm the unconnected-items count is zero. Re-run the checker after every routing change.
5. **Perform the physical review.** Inspect both copper layers, `Edge.Cuts`, solder mask, and silkscreen. Use the 3D Viewer and print/export a 1:1 drawing. Check the 80 × 40 mm outline, four M3 holes, Heltec socket spacing/orientation, MLX90640 pin 1, USB/antenna clearance, sensor aperture, and enclosure/standoff fit.
6. **Choose order parameters.** For a first prototype, a conventional starting point is two-layer FR-4, 1.6 mm thickness, 1 oz copper, and lead-free HASL or ENIG. Confirm those choices against your enclosure, budget, and assembler rather than treating them as fixed by the source.
7. **Generate fabrication files.** In PCB Editor use **File → Plot**, select Gerber, plot the required copper/mask/silkscreen layers plus `Edge.Cuts`, then choose **Generate Drill Files** and create Excellon drills. Put these generated files in a new order-output folder, not in the KiCad source folder.
8. **Generate assembly files if ordering PCBA.** Use **File → Fabrication Outputs → Component Placement (.pos)**, millimetres, top side. Export/prepare a top assembly drawing, and convert `BOM-PCBA-SMD.csv` to the assembler's template without changing manufacturer part numbers or references.
9. **Inspect the exact upload.** Zip the Gerbers and drills, upload them to the manufacturer's viewer, and verify outline dimensions, hole types, copper, mask openings, text, and layer alignment. For PCBA, check the viewer places exactly four SMD parts on the top and visually confirm rotations against the PCB.
10. **Order a small batch.** Order roughly 3–5 boards first. Keep the manufacturer's final file set, settings, DRC/ERC evidence, and order number together so the prototype is reproducible.
11. **Assemble and bring up safely.** Fit the sockets and sensor with correct orientation, inspect for shorts before inserting the Heltec, and attach the correct antenna before transmitting. Power from a current-limited supply, verify `V_EXT` switches to about 3.3 V, then test an I²C scan for address `0x33` using SDA 41/SCL 42 before running the application.

Before buying the full-node parts, select the Heltec regional frequency variant and a matching antenna. The enclosure also needs an unobstructed long-wave-infrared sensor opening; ordinary glass and many plastics block LWIR.

## Primary references

- [MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf)
- [KiCad PCB fabrication-output documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)
