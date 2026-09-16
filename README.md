# IoT Beyond Lab — Thermal Occupancy ML

Privacy-oriented occupancy estimation using 32 × 24 thermal sensing, edge machine learning, and zone-level telemetry for HKU learning spaces.

## System architecture

- Each node captures low-resolution thermal frames within a defined zone.
- The edge model maps thermal data directly to an occupancy or availability estimate without producing identifiable visible-light imagery.
- Node telemetry consists of the zone identifier, normalized availability estimate, confidence value, and system metadata.
- LoRa provides node-to-server communication.
- The server consolidates zone-level estimates for downstream display interfaces and services.

## Repository contents

- `Hardware/` — revised thermal-node carrier PCB, component specifications, assembly partition, and hardware lineage.

## Hardware lineage

Hardware Rev 1.1 is derived from the GPL-3.0 [CrowdAware node](https://github.com/crowdaware-inno-wing-iot/crowdaware-node). Attribution and a copy of the applicable licence are retained in `Hardware/`.

