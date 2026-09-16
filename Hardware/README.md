# HKU Thermal Node Rev 1.1

Rev 1.1 is the current carrier-board design for a Heltec WiFi LoRa 32 V3 and MLX90640 low-resolution thermal occupancy node.

## Hardware definition

| Property | Specification |
|---|---|
| Board | 80 × 40 mm, two copper layers, four M3 mounting holes |
| Sensor | MLX90640ESF-BAA-000-TU, 32 × 24 pixels, 110° × 75° field of view |
| Controller/radio | Heltec WiFi LoRa 32 V3 with frequency-matched external antenna |
| Module connection | Two 1×18, 2.54 mm female socket strips |
| SDA | GPIO41, Heltec J3 pin 15, carrier J1 pad 7 |
| SCL | GPIO42, Heltec J3 pin 16, carrier J1 pad 5 |
| Sensor supply | Switchable 3.3 V `V_EXT`; GPIO36 active-low enable |
| Pull-ups | `R1`, `R2`: 1 kΩ to `V_EXT` |
| Decoupling | `C1`: 100 nF; `C2`: 10 µF |
| Factory-SMT scope | `C1`, `C2`, `R1`, `R2` |
| Manual scope | `A1`, two socket strips represented by `J1`, Heltec module, antenna, and mechanics |

## Rev 1.1 changes from CrowdAware

| Change | Reason |
|---|---|
| MLX90640 moved outside the Heltec footprint | Reduces heating influence from the controller, display, regulator, and radio while giving the sensor a clearer field region. |
| Board changed to an 80 × 40 mm rectangle with four M3 holes | Defines a regular mechanical and enclosure interface. |
| Sensor decoupling changed to 100 nF local plus 10 µF bulk capacitance | Improves the local sensor supply arrangement. |
| I²C pull-ups connected to `V_EXT` instead of always-on `3V3` | Keeps the bus high level in the sensor power domain and avoids back-powering when that rail is disabled. |
| SDA moved to GPIO41/J1 pad 7 and SCL moved to GPIO42/J1 pad 5 | Avoids reserved Heltec V3 GPIO34/GPIO33 and matches the intended firmware mapping. |
| `V_EXT` connection changed from a local copper island to an explicit trace | Makes the switched power path unambiguous. |
| Module sockets corrected from 1×20 to 1×18 | Matches the Heltec WiFi LoRa 32 V3 pin count and footprint. |
| MLX90640 and passive order codes corrected | Aligns the design with the specified sensor package and active component selections. |
| Project-local symbols and footprints added | Keeps the Rev 1.1 KiCad source portable and internally consistent. |
| Board title changed to `HKU Thermal Node` with `HKU IoT Beyond Lab` identification | Tailors the carrier to the HKU deployment while preserving the upstream acknowledgement. |

Rev 1.1 is derived from the GPL-3.0 CrowdAware node. The full acknowledgement is in the repository-level `README.md`, and the retained licence is `COPYING-HARDWARE-GPL-3.0.txt`.
