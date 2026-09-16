# Edge Thermal Occupancy ML @ HKU

The current hardware is **HKU Thermal Node Rev 1.1**, a two-layer carrier for the Heltec WiFi LoRa 32 V3 and Melexis MLX90640 thermal-array sensor. It is intended for privacy-oriented, low-resolution occupancy sensing in HKU library spaces.

## Current Rev 1.1 hardware

| Property | Rev 1.1 definition |
|---|---|
| PCB | 80 × 40 mm, two copper layers, four M3 mounting holes |
| Thermal sensor | MLX90640ESF-BAA-000-TU, 32 × 24 pixels, 110° × 75° field of view |
| Controller/radio | Heltec WiFi LoRa 32 V3 |
| Module connection | Two 1×18, 2.54 mm female socket strips |
| I²C | SDA on GPIO41 / Heltec J3 pin 15 / carrier J1 pad 7; SCL on GPIO42 / Heltec J3 pin 16 / carrier J1 pad 5 |
| Sensor power | Switchable 3.3 V `V_EXT`; GPIO36 active-low enable |
| I²C pull-ups | `R1` and `R2`, 1 kΩ to `V_EXT` |
| Sensor decoupling | `C1` 100 nF local decoupling and `C2` 10 µF bulk decoupling |
| Factory-SMT components | `C1`, `C2`, `R1`, `R2` |
| Manual components | MLX90640 `A1`, two socket strips represented by `J1`, Heltec module, antenna, and mechanics |

## Changes from CrowdAware

| Rev 1.1 change | Reason |
|---|---|
| Moved the MLX90640 outside the Heltec module area | Reduces thermal contamination and gives the sensor a clearer optical and mechanical region. |
| Replaced the original outline with an 80 × 40 mm rectangle and four positioned M3 holes | Provides a regular enclosure and mounting interface. |
| Changed the local sensor decoupling to 100 nF plus 10 µF | Better matches the MLX90640 local power-decoupling requirement. |
| Moved SDA/SCL pull-ups from always-on `3V3` to switchable `V_EXT` | Prevents pull-up current and possible back-powering while the sensor rail is off. |
| Mapped SDA/SCL to GPIO41/GPIO42 and corrected the carrier connections to J1 pads 7/5 | Avoids the Heltec V3 reserved GPIO34/GPIO33 pins and matches the intended firmware mapping. |
| Replaced the local `V_EXT` copper island with an explicit power trace | Makes the switched sensor-power connection deterministic. |
| Corrected the Heltec connection to two 1×18 sockets | Matches the physical Heltec WiFi LoRa 32 V3 headers. |
| Corrected component order codes and added project-local KiCad symbols and footprints | Keeps the specified parts accurate and the Rev 1.1 design self-contained. |
| Renamed the board and silkscreen for the HKU application | Distinguishes this deployment-specific design from the upstream project. |

## Lineage and licence

Hardware Rev 1.1 is derived from the GPL-3.0 [CrowdAware node](https://github.com/crowdaware-inno-wing-iot/crowdaware-node). Attribution is retained here, and the applicable licence is included in `Hardware/COPYING-HARDWARE-GPL-3.0.txt`.
