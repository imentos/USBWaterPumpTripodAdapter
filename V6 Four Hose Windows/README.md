# V6 Integrated Adapter — Four Hose Windows

V6 incorporates the requested hose-routing changes while keeping the V5
quick-lock base interface.

## Adapter changes

- Former central tripod-thread support cylinder removed.
- Old thread opening sealed by the integrated bayonet neck itself.
- A 2.2 mm internal floor remains for structural continuity.
- Lower body rebuilt as one straight cylindrical shell: 57.15 mm OD and 42.0 mm ID.
- Four identical through-windows cut directly through that shell.
- No separate pillars, outward projections, or inward window recesses.
- The four remaining curved shell sections act as flush supports.
- Each window is 29 mm wide and 23 mm high, with 3.5 mm rounded corners.
- Window bottom is 5 mm above the original adapter bottom.
- Upper 57.15 mm collar includes one O-ring retention groove centered at Z=41.32 mm (0.2 inch below the 46.4 mm top).
- Groove is 2.00 mm wide and 0.40 mm deep for a 0.07 inch (1.778 mm) O-ring cross-section.
- Tripod thread exists only in the detachable tripod base.

## Recommended prototype order

1. Print `v6_receiver_fit_coupon.stl`.
2. Print `v6_tyler_integrated_hub_four_windows.stl`.
3. Confirm the 30-degree bayonet lock and M4 safety screw alignment.
4. Install the pump and route its hose through all four windows in turn.
5. Check that the hose does not kink at the window floor or contact a sharp edge.
6. Only then print a complete weighted, tripod, or magnetic base.

## Printing

PETG or ASA; 0.20 mm layers; at least five walls; six top/bottom layers; 35-45%
gyroid infill. Orient with the bayonet lugs on the build plate. Use a brim if
needed and inspect the first layers around all three lugs.

## Validation note

All four windows reduce the circumferential wall area, so the four remaining
curved shell sections carry the side load. Perform a padded 2x expected-load
test before field use. If the first print flexes, narrow the windows or lower
their top from 28 mm to 26 mm.
