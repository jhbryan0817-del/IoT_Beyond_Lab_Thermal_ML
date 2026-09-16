# Thermal Occupancy Machine Learning @ HKU by IoT Beyond Lab

We introduce the privacy-oriented occupancy inference system using a telemetry of distributed 32 × 24 thermal nodes, which is used to train a model that accurately infers the availability of a specific area with unique context. Libraries at HKU, such as the Chi Wah Learning Commons, are unique in that there are no strictly defined seats. Availability is highly subjective due to many variables present. Therefore, the thermal matrix will be paired directly against the perceived availability score, which would be considered the ground truth. The goal is to create a system that is mature enough to provide useful qualitative information to students who are making decisions throughout their day.

## Target System Architecture

- Each node captures low-resolution thermal frames within a defined zone.
- The edge model maps thermal data directly to an availability estimate.
- The node transmits a packet consisting of the zone identifier, normalized availability estimate, confidence value, timestamp, and system metadata.
- LoRa provides node-to-server communication.
- The server consolidates zone-level estimates for downstream display interfaces and services.

## Repository Structure

- `Hardware/` — revised thermal-node carrier PCB, component specifications, assembly partition, and hardware lineage.

## Lineage and Acknowledgements

Hardware Rev 1.1 is derived from the GPL-3.0 [CrowdAware node](https://github.com/crowdaware-inno-wing-iot/crowdaware-node). Attribution and a copy of the applicable licence are retained in `Hardware/`.

