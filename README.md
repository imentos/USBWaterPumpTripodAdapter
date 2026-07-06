# USB Water Pump to Tripod Adapter

Three competing FDM-printable concepts for adapting a common USB rechargeable water pump to the photography ecosystem via a standard 1/4"-20 camera mount.

## Shared Assumptions

- Pump bottom has two screws at 32 mm spacing and a center locating cylinder.
- Screw holes are M3 clearance at 3.4 mm.
- Top locating pocket is 18.5 mm diameter by 3.0 mm deep.
- Tripod interface uses a brass 1/4"-20 heat-set insert or metal threaded insert.
- Bottom insert socket assumes 8.2 mm OD by 9.8 mm depth; tune to the actual insert datasheet.
- Print material: PETG or ASA preferred for water resistance; PLA acceptable for fit prototypes.

## Concepts

### Concept A: Low-Profile Round Puck

Smallest and simplest MVP. A 76 mm round adapter with chamfered water-shedding edges, pump screw holes, a top locating pocket, and a reinforced center insert boss.

Best for:
- Fastest iteration
- Easiest print
- Lowest manufacturing complexity

Tradeoff:
- Wider disk than strictly necessary.

### Concept B: Bone Bridge

Material-efficient bridge shape connecting the two pump screw bosses and the center tripod insert boss. Includes side scallops to reduce weight and drying time.

Best for:
- Lower material use
- Distinct product shape
- Keeping strength along the screw-to-insert load path

Tradeoff:
- More exposed edges; less splash shielding than Concept C.

### Concept C: Sealed Tall Boss

Stronger, taller adapter with a pump-foot skirt and shallow groove for silicone or an O-ring style seal. Designed for higher torque from magic arms or cabinet-edge mounts.

Best for:
- Higher load margin
- Better splash resistance
- More confidence with off-axis mounting

Tradeoff:
- Heaviest and slowest to print.

## Print Recommendations

- Orientation: flat on the tripod side, pump side up.
- Layer height: 0.20 mm.
- Perimeters: 4.
- Top/bottom layers: 5.
- Infill: 35% gyroid or cubic.
- Material: PETG for MVP field testing.
- Insert installation: heat-set from bottom after print; use a 1/4"-20 screw as an alignment mandrel while cooling.
- Waterproofing: add thin silicone under pump contact face; avoid sealing screw heads permanently until fit is validated.

## Estimated Print Time and Material

Estimates are based on STL sampled volume, 35% infill, 4 perimeters, 1.24 g/cm3 PETG/PLA density, and a conservative desktop FDM rate. Use a slicer for final numbers.

| Concept | Solid Equivalent | Estimated Printed Mass | Estimated Time |
| --- | ---: | ---: | ---: |
| A Low-Profile Round | 49.3 cm3 | 36-43 g | 2.0-2.7 hr |
| B Bone Bridge | 16.6 cm3 | 14-19 g | 1.1-1.6 hr |
| C Sealed Tall Boss | 68.6 cm3 | 50-60 g | 2.8-3.8 hr |

## Files

- `scad/concept_a_low_profile_round.scad`
- `scad/concept_b_bone_bridge.scad`
- `scad/concept_c_sealed_tall_boss.scad`
- `scad/_pump_adapter_common.scad`
- `stl/*.stl`
- `scripts/generate_stl.py`

## OpenSCAD Export

When OpenSCAD is installed:

```sh
openscad -o stl/concept_a_low_profile_round.stl scad/concept_a_low_profile_round.scad
openscad -o stl/concept_b_bone_bridge.stl scad/concept_b_bone_bridge.scad
openscad -o stl/concept_c_sealed_tall_boss.stl scad/concept_c_sealed_tall_boss.scad
```

The included STLs are generated locally without OpenSCAD and are useful for quick envelope review. They include the main through holes but use faceted sampled geometry. The OpenSCAD files are the production-editable source for smooth final exports.


## V2 Direction: Tall Center-Tripod Side-Hose Base

The latest direction keeps the tripod mount centered. The adapter becomes taller, with the 1/4"-20 brass insert in the bottom center for stability. Instead of a center water pass-through, the water tube enters from the side and turns upward toward the pump intake. This preserves the idea that the pump bottom already matches common 5 gallon / Costco-style bottle mouths, while still allowing the pump to be mounted to a tripod, clamp, or magic arm.

Recommended V2 parts:

- 1/4"-20 UNC brass heat-set insert, about 8-10 mm OD and 8-10 mm long
- M3 stainless screws for the pump's original bottom screw locations
- Silicone hose matched to the pump intake; current CAD side hole is 12.5 mm clearance
- PETG or ASA filament
- Optional silicone gasket or sealant around the hose exit

Estimated V2 print:

| Concept | Solid Equivalent | Estimated Printed Mass | Estimated Time |
| --- | ---: | ---: | ---: |
| D Tall Center-Tripod Side-Hose | 111.2 cm3 | 75-95 g | 4.0-5.5 hr |

New files:

- `scad/concept_d_tall_center_tripod_side_hose.scad`
- `stl/concept_d_tall_center_tripod_side_hose.stl`


## V3 Direction: Friction-Fit Collar, No Pump Screws

The pump bottom is treated as an existing molded bucket-mouth adapter with no required screw fastening. The 3D printed part becomes a slip-on collar: the pump drops into the upper cup, thin silicone/rubber pads take up tolerance, and two optional side clamp screws provide light retention. The centered 1/4"-20 tripod insert remains in the lower body, and the water tube enters from the side.

Critical measurements before printing:

- Pump bottom outside diameter where the collar will grip
- Required insertion depth before the printed part hits the molded pump shape
- Hose outside diameter
- Whether side clamp screws can touch a strong plastic area without damaging the pump

Recommended V3 parts:

- 1/4"-20 UNC brass heat-set insert, about 8-10 mm OD and 8-10 mm long
- Thin silicone/rubber pad sheet, 0.5-1.5 mm thick
- Optional two M4 nylon-tip thumb screws or stainless M4 screws
- Optional M4 heat-set inserts if you want real threaded side clamps
- Silicone hose matched to pump intake; current CAD side hole is 12.5 mm clearance
- PETG or ASA filament


Estimated V3 print:

| Concept | Solid Equivalent | Estimated Printed Mass | Estimated Time |
| --- | ---: | ---: | ---: |
| E Friction-Fit Collar Side-Hose | 122.8 cm3 | 82-105 g | 4.4-6.0 hr |

New files:

- `scad/concept_e_friction_fit_collar_side_hose.scad`
- `stl/concept_e_friction_fit_collar_side_hose.stl`
