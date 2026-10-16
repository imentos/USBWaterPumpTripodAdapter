# V5 Integrated Universal Pump Adapter

V5 implements the revised architecture:

```text
Pump
  |
Tyler adapter + male hub (one printed part, no tripod thread)
  |
30-degree three-lug quick lock
  +-- flat weighted base
  +-- detachable 1/4-20 tripod base
  +-- flat magnetic base
```

## What changed from V4

- The separate universal hub and its fastening screw are removed.
- Tyler V3 and the male bayonet are fused into one printable solid.
- The old central tripod-thread opening is closed through its original depth.
- The Tyler side-hose and upper pump-fit geometry remain unchanged.
- The adapter sits 7 mm lower than the separate-hub V4 arrangement.
- Only the detachable tripod base contains a 1/4-20 insert.
- Weighted and magnetic base undersides remain flat after their covers/pads are installed.

## First print

Print these two files first:

1. `v5_tyler_adapter_integrated_hub.stl`
2. `v5_receiver_fit_coupon.stl`

Confirm that the adapter inserts freely, rotates clockwise approximately 30
degrees, reaches all three stops, and has no vertical wobble. Validate the fit
coupon before printing the full weighted or magnetic base.

## Receiver safety lock

Each full base includes a radial pocket for an M4 heat-set insert and a short
M4 nylon-tip screw. After rotating the adapter into the locked position, tighten
this screw lightly against the integrated neck to prevent reverse rotation.

## Suggested materials

- Adapter and bases: PETG or ASA, five walls, six top/bottom layers, 35-45% infill.
- Weighted base: up to four nominal 4-inch mild-steel discs, maximum 103.5 mm
  measured diameter and 19 mm total stack thickness.
- Magnetic base: six 20 x 5 mm magnets, epoxy, full underside silicone pad, and
  a safety tether whenever mounted above a surface.

## Important prototype note

The integrated part is created from Tyler V3 STEP geometry. The former tripod
opening is filled only to 8.5 mm above the original bottom so the larger upper
hose passage remains open. Verify hose clearance and water flow on the first
physical prototype before production.
