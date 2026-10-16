# V8 Threaded Universal Pump Adapter

V8 replaces the trapped-support bayonet interface with a support-free coarse
thread. V7 remains unchanged.

## Universal connection

- Single-start trapezoidal thread with an unmistakable continuous helix.
- 5.0 mm pitch; approximately two turns to fully engage.
- Male major/minor diameter: 44.0 / 41.6 mm.
- Female major/minor diameter: 44.8 / 42.4 mm.
- Nominal radial clearance: 0.4 mm.
- Engagement: 10.0 mm.
- 45-degree-style printable flanks, flat crest/root.
- Upward-open female sockets; no trapped support and no internal roof.
- The adapter shoulder seats on the base top instead of loading only the teeth.

The Tripod Base retains Tyler's exact modeled direct-print 1/4-20 thread on its
underside. No metal threaded insert is required.

## Print the fit coupons first

Print `v8_thread_fit_male.stl` and `v8_thread_fit_female.stl` before printing the
full adapter or a full base. Use the same material, nozzle, layer height, and
wall settings intended for the product.

Starting settings: PETG, 0.20 mm layers, five walls, six top/bottom layers,
35-45% gyroid infill, support off. Print both pieces vertically with their flat
round faces on the bed and the threads pointing upward.

After printing, turn the female coupon upside down over the male coupon to test
the fit. It should begin easily, turn without cross-threading, and become snug
at the shoulder. If too tight, increase female diameters by 0.2 mm. If too
loose, decrease female diameters by 0.2 mm. Do not force the full adapter before
the coupons pass.

## Full-part print orientation

- Adapter: print upside down, with the wide pump-opening rim on the bed and the
  male thread pointing upward. A brim is recommended. This avoids printing the
  wide adapter shoulder in mid-air.
- Tripod, Weighted, and Magnetic bases: print in their normal upright position,
  flat bottom on the bed and the female socket opening upward.
- Support: off for the universal thread and its receiver. The 45-degree thread
  flanks are self-supporting in these orientations.

The exported B-reps are valid single solids. A geometric screw-path check every
1.25 mm from fully seated through 7.5 mm withdrawal showed zero tooth collision
after trimming the intentional shoulder contact.

## Retained V7 features

- 57.15 mm pure cylindrical pump adapter.
- 42.0 mm straight inner bore.
- Four 29 x 23 mm hose windows.
- O-ring groove 0.40 mm deep, centered 0.2 inch below the top.
- Weighted, Tripod, and Magnetic base families.
