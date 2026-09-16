# Edge Thermal Occupancy ML @ HKU

We introduce the privacy-oriented occupancy inference system using a telemetry of distributed 32 × 24 thermal nodes, which is used to train a model that accurately infers the availability of a specific area with unique context. Libraries at HKU, such as the Chi Wah Learning Commons, are unique in that there are no strictly defined seats. Availability is highly subjective due to many variables present. Therefore, the thermal matrix will be paired directly against the perceived availability score, which would be considered the ground truth. The goal is to create a system that is mature enough to provide useful qualitative information to students who are making decisions throughout their day.

## Target System Architecture

- Each node captures low-resolution thermal frames within a defined zone.
- The edge model maps thermal data directly to an availability estimate.
- The node transmits a packet consisting of the zone identifier, normalized availability estimate, confidence value, timestamp, and system metadata.
- LoRa provides node-to-server communication.
- The server consolidates zone-level estimates for downstream display interfaces and services.

## Repository Structure

- `Hardware/` — Rev 1.1 thermal-node carrier: sensor moved away from module heat, corrected MLX90640 power conditioning, regular enclosure-friendly mechanics, and I²C remapped to the Heltec V3 GPIO41/GPIO42 header pads to avoid reserved pins. Includes KiCad sources, local libraries, BOMs, and a first-prototype production checklist.

## Lineage and Acknowledgements

Hardware Rev 1.1 is derived from the GPL-3.0 [CrowdAware node](https://github.com/crowdaware-inno-wing-iot/crowdaware-node). It keeps the original low-resolution thermal-node concept while improving thermal separation, decoupling, mechanics, source portability, and Heltec V3 pin compatibility. Attribution and a copy of the applicable licence are retained in `Hardware/`.

## About IoT Beyond Lab

Established in September 2026, the team is based in Innovation Wing at the University of Hong Kong. The mission is to build and **deploy** different IoT applications that will leave a lasting impact, hence inspiring the name "IoT Beyond Lab". Other than this thermal ML project, the team also partners with Chulalongkorn University (CSII) in Thailand to develop IoT-based solutions that mitigates flood-induced disaster impact.
