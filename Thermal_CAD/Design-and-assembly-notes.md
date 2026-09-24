# HKU IoT Beyond Lab — Thermal enclosure, Rev A

Created directly in Autodesk Fusion through its local MCP server on 23 September 2026. This is a dimensioned, editable **fit-check prototype**, not a physically validated production enclosure.

## Delivered design

- Maximum assembled size: **85 × 45 × 33.5 mm**. Sensor nose: **29.5 mm** high.
- Three printable parts: rear shell, engraved front shell, removable battery tray.
- Nominal walls: 1.8 mm; rear floor: 2.4 mm; plan-view corner radius: 3 mm. The sloped front transition has about 1.61 mm normal thickness.
- “HKU IoT Beyond Lab” is engraved in the front face, with a smaller “THERMAL NODE” identifier. Main engraving depth is 0.45 mm.
- The Heltec is on the back of the carrier, as defined by the KiCad footprint. The battery sits beside the sensor on the front, rather than adding a layer behind the controller.
- USB cable access, rear OLED service window, two recessed button-tool openings, rear-chamber vents, and a 6.5 mm SMA bulkhead opening.
- The thermal aperture is open air, with a flare. Do not cover it with ordinary glass, acrylic, or printed plastic. This vented enclosure has no weatherproof/IP rating.

## Files

`HKU-thermal-enclosure.f3d` is the editable native Fusion assembly with named sketches, extrusions, lofts, components and reference hardware. `HKU-thermal-enclosure-assembly.step` contains the complete assembly, including hardware envelopes. The separate `rear-shell`, `front-shell`, and `battery-tray` STEP/STL files contain only the respective printable part. STLs are in millimetres and preserve assembly coordinates; use your slicer's place-on-bed command.

The reference bodies are simplified dimensional envelopes, not exact vendor CAD. The official Heltec download directory currently offers a V3.7 STEP and a file explicitly labelled “V3_Non-Exact”; neither was substituted for an exact V3.2 model.

User parameters record important dimensions. PCB thickness, socket height and the front blank height drive selected features; this is **not** a fully constrained, automatically resizing enclosure. A change to the stack must also update the related offsets, supports and openings, then repeat interference and aperture checks.

## Source geometry and tolerances

The source PCB was read from the repository's main tree `e687e52de51aaa4c8ed1e8c2772f6d82eb6fd3b3`, file `Hardware/KiCad/HKU Thermal Node Rev1.1.kicad_pcb`.

Coordinates below use the PCB's lower-left corner viewed from the sensor side as (0,0), with Z toward the sensor.

| Item | Dimension / position | Evidence or status |
|---|---|---|
| Carrier | 80 × 40 × 1.6 mm | KiCad outline and board thickness |
| Four mounting holes | Ø3.2 mm at (4,4), (4,36), (76,4), (76,36) | KiCad; 72 × 32 mm centres |
| Sensor centre | (69,20) mm | KiCad A1 |
| Socket rows | Y = 7.672 and 30.532 mm | KiCad J1 on B.Cu |
| Header positions | X = 12.55 through 55.73 mm, 2.54 mm pitch | KiCad J1, 18 positions per row |
| Female sockets | 8.51 mm high; approximately 46.23 × 2.41 mm body | Samtec SSW-118-01-G-S drawing |
| Heltec V3.2 | 50.2 × 25.5 × 10.2 mm overall | Heltec datasheet, pages 10 and 14 |
| Male-header spacer | 2.54 mm | **Assumed**; actual assembled header must be measured |
| Sensor can | Ø9.30 ±0.15 mm, height 5.70 ±0.30 mm | Melexis BAA mechanical drawing |
| PCB-to-wall clearance | 0.7 mm nominal per side | Design allowance; local wire relief is wider |
| Lid lip clearance | 0.35 mm per side | FDM starting allowance |
| Tray-to-lid retaining pads | 0.20 mm vertical gap | Limits tray lift without squeezing the pouch |

The Heltec outline is positioned approximately relative to the header rows because its published dimension sheet does not fully locate every connector/button from the header datum. **USB, OLED and button positions remain fit-check items.** The service openings are deliberately generous. The SMA hole is a generic pigtail interface; select the antenna and bulkhead to match the radio band and confirm nut/washer clearance.

## Battery choice

The final design uses the **Adafruit 1578 protected 3.7 V, 500 mAh LiPo envelope, 36 × 29 × 4.75 mm**. The smaller pack keeps the front thin and leaves about 17 mm between the pouch end and the sensor flange. Capacity was reduced from the repository's 2000 mAh option to honour the compactness preference; operating runtime has not been established.

The tray's clear plan area is 38 × 30.2 mm. The model allows a 0.2 mm insulating adhesive layer below the pouch and 1.1 mm nominal space above it. The tray floor is 2.2 mm above the carrier's front surface, leaving 1.1 mm above the modelled solder-tail envelope. Do not substitute a pack exceeding the selected envelope without revising the tray and checking taped leads/PCM thickness.

The selected battery ships with a **JST-PH connector**, while Heltec specifies **SH1.25-2**. Use a correctly wired adapter or professionally terminated lead, with polarity verified against the board. There is room beside the tray for the connection; route the individual insulated conductors through the left edge bypass. The battery supplier specifies charging at no more than 500 mA; verify the actual board's charge current before commissioning. No claim about runtime, RF performance, charging temperature or thermal accuracy has been validated on hardware.

## Stack, measured from the rear exterior

| Surface / envelope | Z, mm |
|---|---:|
| Rear exterior / interior floor | 0 / 2.4 |
| OLED outer face, nominal | 3.4 |
| Heltec PCB | 8.4–10.0 |
| Assumed male spacer | 10.0–12.54 |
| Female sockets | 12.54–21.05 |
| Carrier PCB | 21.05–22.65 |
| Tray floor | 24.85–25.65 |
| Battery, with 0.2 mm adhesive allowance | 25.85–30.60 |
| Sensor optical face, nominal | 28.35 |
| Front at sensor | 29.5 |
| Front above battery | 33.5 |

The full female socket height and male-header spacer are included; the 10.2 mm Heltec specification was not treated as the entire mounted assembly height.

## Fasteners and assembly

1. Print the three enclosure parts and remove supports/burrs. Check the lid lip slides freely before installing hardware.
2. Install four M3 heat-set inserts in the front columns. Pockets are Ø4.2 × 4.2 mm, intended as a starting size for approximately Ø4.6 × 4 mm inserts. Confirm the chosen insert manufacturer's hole guidance and calibrate for your print material. The final clearance below the sensor-side outer face is limited; do not over-insert.
3. Seat the carrier on the four rear-shell columns with the Heltec already plugged into its **back-side** sockets. Confirm the display, USB cable and button-tool access. The nominal OLED-to-floor gap is 1.0 mm.
4. Place the insulated tray on the four shell shelves. Retain the battery with a thin removable insulating adhesive and/or loose 5 mm ribbon through the tray slots; do not compress the pouch.
5. Connect the battery and route wires through the bypass. Fit a frequency-matched U.FL-to-SMA antenna pigtail to the side opening; keep coax out of screw columns and the thermal aperture.
6. Close the lid and use four **M3 × 28 mm, 90° countersunk screws**. If unavailable, trim M3 × 30 mm screws to 28 mm and deburr. Length is measured including the countersunk head. Tip clearance ends at Z28.25 mm, so an unshortened 30 mm screw is too long. Tighten lightly: the columns clamp the PCB at its mounting-hole keepouts.

## Printing

PETG is the intended prototype material. Start with a 0.4 mm nozzle, 0.2 mm layers and at least four perimeters where wall thickness permits. Print the rear floor on the bed; support the internal tray shelves if needed. Print the tray flat. The front has a stepped outer face: orient the large lettered face toward the bed and support the lowered sensor region, or use a supported angled orientation to protect the lettering. Check the chosen slicer's preview; the front is not claimed to be support-free. Clean the thermal flare carefully without leaving strings or burrs.

No printer-specific shrink compensation is built in. Inspect the first print for the 0.35 mm lip clearance and heat-set insert fit before assembling electronics.

## Verification and remaining fit checks

Fusion reports one solid per printable part, no unhealthy timeline features, and zero volume interference among the final shells, tray and modelled hardware. `verification.json` records the CAD checks, volumes and bounding boxes. The aperture check uses the full 110° × 75° FOV, a minimum sensor height of 5.4 mm and the 2.7 mm maximum optical opening diameter; it samples a conservative circular bound around the rectangular FOV.

These checks apply to the modelled envelopes. Before printing a batch, measure the actual male-header stack, sensor seating height, protected battery and taped cable, USB overmould, button/OLED alignment, SMA fitting and insert dimensions. Confirm a real thermal frame is unvignetted and compare settled readings with/without the enclosure; geometry alone cannot validate thermal gradients or RF detuning.

## Public source documents

- [Repository and PCB](https://github.com/jhbryan0817-del/IoT_Beyond_Lab_Thermal_ML)
- [Heltec WiFi LoRa 32 V3.2 datasheet](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/HTIT-WB32LA_V3.2.pdf)
- [Heltec V3.2 schematic](https://resource.heltec.cn/download/WiFi_LoRa_32_V3/WiFi_LoRa_32_V3.2_Schematic_Diagram.pdf)
- [Samtec SSW mechanical drawing](https://suddendocs.samtec.com/prints/ssw-1xx-xx-xxx-x-xx-xxx-xx-mkt.pdf)
- [Melexis MLX90640 datasheet, BAA drawing on page 57](https://media.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf)
- [Adafruit 1578 battery dimensions and charging specification](https://www.adafruit.com/product/1578)

The carrier reference follows the repository's Rev1.1 design, itself derived from CrowdAware. The original repository retains the hardware attribution and GPL-3.0 licence. No repository files were modified or published.
