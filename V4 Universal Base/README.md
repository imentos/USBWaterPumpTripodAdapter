# CampTapLab V4 Universal Pump Base

This V4 system is backward-compatible with the existing Tyler V3 pump adapter.
The Tyler part is not modified: a thin universal hub is fastened to its existing
1/4-20 threaded insert, and all new bases attach to that hub.

## Parts

- `v4_universal_hub`: permanent pump-side hub; three-lug bayonet underneath.
- `v4_receiver_fit_coupon`: print this first to validate bayonet clearance.
- `v4_weighted_base_body`: 140 mm base shell with a bottom-loading steel cavity.
- `v4_weighted_base_cover`: recessed screw-on cover for the weighted base.
- `v4_tripod_base`: detachable base with an 8.2 mm socket for a 1/4-20 insert.
- `v4_magnetic_base`: detachable six-magnet base with a safety-tether eyelet.

Each printable part is exported as STEP and STL. SVG files are reference views.

## Interface

- 36.0 mm male pilot / 37.0 mm female pilot.
- Three lugs at 120 degrees.
- Approximately 30 degree clockwise lock rotation.
- 0.5 mm radial pilot clearance for an initial PETG/ASA FDM prototype.
- An M4 nylon-tip safety screw in every base prevents accidental unlocking.
- A 50 mm OD silicone washer sits between Tyler V3 and the universal hub.

## Hardware

### Universal hub

- One 1/4-20 socket-head screw, length selected to suit the installed Tyler insert.
- One 50 mm OD, 12 mm ID, 0.5-0.8 mm silicone friction washer.

### Each detachable base

- One M4 heat-set insert, approximately 8.0 mm OD.
- One short M4 nylon-tip thumb screw.

### Weighted base

- Four nominal 4 inch steel discs, up to 19 mm total stack height and no more
  than 103.5 mm actual diameter. Verify purchased steel before printing.
- Four M4 heat-set inserts and four M4 cover screws.
- One die-cut 122 mm silicone non-slip pad, about 1 mm thick.

The final weight depends on steel thickness. Four 4 inch x 3/16 inch mild-steel
discs are approximately 2.4 kg total; verify supplier dimensions and mass.

### Tripod base

- One 1/4-20 heat-set or press-fit brass insert, 8.2 mm OD maximum and up to
  10 mm long.

### Magnetic base

- Six 20 mm diameter x 5 mm magnets.
- Epoxy suitable for the magnet coating and printed polymer.
- One continuous 1 mm silicone sheet covering the completed underside.
- Safety tether. Do not rely on magnets alone above people or fragile objects.

## Print sequence

1. Print the universal hub and receiver fit coupon in PETG.
2. Insert the hub, rotate clockwise until it contacts the stops, and check for
   wobble and reliable removal. Do not force it.
3. If loose, reduce receiver dimensions in the CAD source by 0.15-0.25 mm. If
   tight, increase them by the same amount.
4. Only after the coupon passes, print the selected full base.

Recommended starting settings: 0.20 mm layers, five walls, six top/bottom layers,
35-45% gyroid infill, PETG or ASA. Use 100% infill around heat-set inserts if the
slicer supports modifier regions.

## Safety and validation

This is an engineering prototype, not a certified load-bearing product. Test the
installed pump at 2x expected side load over a padded surface. Confirm that the
water hose does not pull the pump off-axis. Inspect the hub, lugs, receiver roof,
and heat-set inserts after every early test cycle.

The magnetic base should not be used near pacemakers or other magnet-sensitive
devices, and it always requires the tether for elevated mounting.

## Regenerating

Run `create_pump_v4.py` with CadQuery 2.5 or newer. Output files are written to
the adjacent `output` directory.
