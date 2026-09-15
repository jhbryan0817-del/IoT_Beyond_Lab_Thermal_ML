# IoT Beyond Lab — Thermal Occupancy ML

Research and prototyping for privacy-oriented occupancy estimation using low-resolution thermal sensing, edge machine learning, and compact zone-level telemetry.

The initial proof of concept targets the HKU Innovation Wing before a possible deployment study in the Chi Wah Learning Commons.

## Repository structure

- `Hardware/` — revised thermal-node carrier PCB, bills of materials, assembly boundary, and manufacturing notes.
- Firmware, model-training, server, and interface components will be added as the prototype develops.

## Current status

Hardware Rev 1.1 is an **unvalidated prototype**. Its KiCad source has received structural checks, but ERC, DRC, copper-zone refill, physical fit checking, and a five-board prototype run are required before deployment.

The hardware revision is derived from the GPL-3.0 [CrowdAware node](https://github.com/crowdaware-inno-wing-iot/crowdaware-node). Its attribution and licence copy are retained inside `Hardware/`.

