# Thermal enclosure — Rev B

Revised in the existing `Thermal_Enclosure` Autodesk Fusion design on 24 September 2026. This revision supersedes the original sloped front and 500 mAh battery arrangement.

## Changes

- Flat 2.4 mm front plate with the original engraved labels. An 11.2 mm opening exposes the thermal camera; the nominal optical face projects 1.03 mm above the plate.
- Separate removable rear battery lid, with four M3 screws. The front lid also has four M3 screws, independent of the PCB.
- Four PCB mounts at the existing 72 × 32 mm hole pattern, with blind 2.6 mm pilot holes for M3 screws to form threads directly in plastic. No nuts or inserts.
- Removed the four original battery shelves that blocked top insertion of the PCB.
- Both lids have 2 mm deep external locating collars, with 0.30 mm nominal clearance per side. They register the lids before screws are installed; they are not snap fits or interference fits.
- Rear pocket for the specified 3.7 V 2000 mAh 804050 battery, nominally 50 × 40 × 8 mm. The pocket is 51.6 × 41.4 mm, leaving 0.8 mm at each end and 0.7 mm at each side with the reference battery centered.
- Battery reference sits 0.2 mm above the rear lid for a thin insulating retention layer, with 3.6 mm clearance above the nominal pouch to the existing service floor. The pack lifts out through the back.
- A 6 × 10 mm passage through the existing floor connects the rear battery bay to the controller compartment. Route leads away from the screw tips and leave a service loop for opening the lid.
- A 15 × 28 × 8 mm antenna envelope is reserved beside the battery, accessible from the rear. This is an allocation, not a model of a specific SX1262-compatible antenna. Confirm antenna size and frequency before glue mounting. The existing SMA port is retained.

## Preserved geometry and necessary envelope changes

The carrier PCB, thermal camera, Heltec, 8.51 mm female sockets, assumed 2.54 mm male spacers, USB corridor, side vents, SMA port, and original OLED/button service openings retain their original positions. The larger rear battery covers the OLED access: open the rear lid and lift the battery to access it, as agreed.

The main wall footprint remains 85 × 45 mm. External screw bosses keep lid fasteners outside the PCB insertion path; the maximum width becomes 96.8 mm. Lid collars make the maximum depth 48 mm. Overall enclosure height is 41.6 mm, excluding the protruding camera and screw heads. The original internal coordinate system is retained, so some exported Z coordinates are negative.

## Files

- `HKU-thermal-enclosure.f3d`: editable Fusion design with the original timeline and revision features.
- `HKU-thermal-enclosure-assembly.step`: complete assembly with simplified hardware references.
- `main-housing.stl`, `front-lid.stl`, `rear-lid.stl`: the three printable parts, in millimetres. Corresponding STEP files are also supplied.
- `Revise-enclosure-in-Fusion.py`: revision script for the original Rev A design; run once, not on Rev B.
- `verification.json`, `mesh-verification.json`: CAD and mesh checks.

Do not print hardware reference bodies. The old battery tray and original shells are superseded.

## Fasteners and assembly

Use twelve M3 screws: four **M3 × 8 mm** for the PCB and four **M3 × 10 mm** for each lid. Lengths exclude the heads; use pan/button/socket heads, not countersunk heads. Lid holes are 3.4 mm clearance. Lid pilots are 8.5 mm deep; the 10 mm screws engage about 7.6 mm. PCB screws engage about 6.4 mm below the 1.6 mm board.

1. Print and deburr the three parts. Test each collar and the direct-thread pilots before fitting electronics. Pilot fit depends on printer and material; the CAD uses 2.6 mm, not modeled machine threads.
2. Insert the assembled PCB/Heltec stack from the front and seat it on the four posts. Install its four M3 × 8 mm screws with light torque.
3. Attach the antenna and route its coax and battery leads through the available corridor. Glue should not obstruct the lid or battery extraction.
4. Fit the front lid over the sensor and secure its four M3 × 10 mm screws.
5. Position the battery in the rear pocket with removable insulating retention material. Avoid squeezing the pouch. Close the rear lid and install its four M3 × 10 mm screws.

Print both lids with the flat outer face on the bed, collars upward. For the main housing, place the rear rim on the bed and inspect slicer support requirements for the existing internal service floor and side openings. PETG and a 0.4 mm nozzle are the original design assumptions. Do a first-article fit check before printing a batch.

## Verification limits

Fusion reports one solid per printable part, no unhealthy timeline features, and no volume intersections between the revised enclosure parts and the modeled hardware. The front PCB stack and rear battery extraction were checked at 0.5 mm increments over 50 mm with the lids removed; no housing collisions were found. All three STL meshes have closed two-face edges, consistent winding and positive volume. These are digital checks, not a physical fit certification.

CAD checks concern the supplied simplified component envelopes, not a physical assembly. Actual header stack, battery protection board/taped leads, antenna dimensions, connector access, thermal performance and RF performance still need a real fit check. The enclosure remains vented, with an open thermal aperture. See the retained Rev A build script and hardware documentation for original source dimensions and attribution.
