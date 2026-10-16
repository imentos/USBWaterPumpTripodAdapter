"""V7 pure-cylinder universal pump adapter.

This model is constructed from scratch. It imports none of Tyler's lower-body
or shoulder-pillar geometry: one cylinder, one straight internal bore, and four
through-windows, plus the integrated bayonet connector and O-ring groove.
"""

from pathlib import Path

import cadquery as cq
from cadquery import exporters

import v4_geometry as g


HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

TYLER_PRINTED_THREAD_STEP = Path(
    "/Users/I818292/Documents/Funs/USBWaterPumpTripodAdapter/"
    "Tripod Adapter from Tyler (FB)/Tripod Adapter.step"
)

BODY_OD = 57.15
BODY_ID = 42.0
BODY_HEIGHT = 46.4
FLOOR_Z = 2.2

WINDOW_BOTTOM_Z = 5.0
WINDOW_TOP_Z = 28.0
WINDOW_WIDTH = 29.0
WINDOW_CORNER_R = 3.5

O_RING_CROSS_SECTION = 1.778  # 0.07 inch
O_RING_GROOVE_DEPTH = 0.40
O_RING_GROOVE_WIDTH = 2.00
O_RING_GROOVE_CENTER_Z = 41.32  # 0.2 inch below the 46.4 mm top


def rounded_through_window(angle_deg):
    """Cut straight through the cylindrical wall; no pocket or inset."""
    height = WINDOW_TOP_Z - WINDOW_BOTTOM_Z
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=WINDOW_BOTTOM_Z)
        .center(25.0, 0)
        .box(22.0, WINDOW_WIDTH, height, centered=(True, True, False))
        .edges("|X")
        .fillet(WINDOW_CORNER_R)
    )
    return cutter.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def make_v7_adapter():
    # The complete visible adapter body is literally one cylinder.
    adapter = g.cyl(BODY_OD, BODY_HEIGHT)

    # One vertical internal bore leaves a constant 7.575 mm radial wall. The
    # bore starts above a 2.2 mm structural floor and runs through the top.
    bore = g.cyl(BODY_ID, BODY_HEIGHT - FLOOR_Z + 0.5, FLOOR_Z)
    adapter = adapter.cut(bore)

    # Integrated male bayonet below the floor.
    connector = g.cyl(g.HUB_NECK_D, g.HUB_NECK_H + FLOOR_Z, -g.HUB_NECK_H)
    for angle in (0, 120, 240):
        connector = connector.union(
            g.radial_box(
                g.HUB_LUG_INNER_R,
                g.HUB_LUG_OUTER_R,
                g.HUB_LUG_W,
                g.HUB_LUG_H,
                -g.HUB_NECK_H + g.HUB_LUG_Z,
                angle,
            )
        )
    adapter = adapter.union(connector)

    # Four identical through-holes at 90-degree intervals.
    for angle in (45, 135, 225, 315):
        adapter = adapter.cut(rounded_through_window(angle))

    # Shallow O-ring retention groove near the top pump-fit area.
    groove_z0 = O_RING_GROOVE_CENTER_Z - O_RING_GROOVE_WIDTH / 2.0
    groove_root_d = BODY_OD - 2.0 * O_RING_GROOVE_DEPTH
    groove_outer = g.cyl(BODY_OD + 4.0, O_RING_GROOVE_WIDTH, groove_z0)
    groove_inner = g.cyl(groove_root_d, O_RING_GROOVE_WIDTH + 0.2, groove_z0 - 0.1)
    adapter = adapter.cut(groove_outer.cut(groove_inner))

    try:
        adapter = adapter.clean()
    except Exception:
        pass
    return adapter


def make_v7_tripod_base_with_printed_thread():
    """Tripod base using Tyler's exact modeled 1/4-20 internal thread."""
    body = g.cyl(64.0, 18.0)
    body = body.edges().fillet(3.0)
    body = g.add_receiver(body, 18.0, include_safety_lock=False)

    # Extract the negative threaded volume from Tyler's original STEP and cut
    # that exact geometry into this base. This preserves Tyler's thread pitch,
    # profile, entry, fit allowance, and approximately 8 mm blind-hole depth.
    tyler = cq.importers.importStep(str(TYLER_PRINTED_THREAD_STEP))
    extraction_envelope = g.cyl(8.0, 8.2, -0.1)
    tyler_thread_void = extraction_envelope.cut(tyler)
    return body.cut(tyler_thread_void)


def export_part(name, shape):
    exporters.export(shape, str(OUT / f"{name}.step"))
    exporters.export(shape, str(OUT / f"{name}.stl"), tolerance=0.08, angularTolerance=0.12)
    exporters.export(
        shape,
        str(OUT / f"{name}.svg"),
        opt={"projectionDir": (1.0, -1.0, 0.8), "showAxes": False, "showHidden": True},
    )


def export_reference_assembly(name, base, base_top_z, adapter):
    installed = (
        adapter
        .rotate((0, 0, 0), (0, 0, 1), g.BAYONET_ROTATION_DEG)
        .translate((0, 0, base_top_z))
    )
    assembly = base.union(installed)
    exporters.export(assembly, str(OUT / f"{name}.step"))
    exporters.export(assembly, str(OUT / f"{name}.stl"), tolerance=0.1, angularTolerance=0.15)


def main():
    parts = {
        "v7_pure_cylinder_four_windows": make_v7_adapter(),
        "v7_weighted_base_body": g.make_weighted_base_body(),
        "v7_weighted_base_cover": g.make_weighted_base_cover(),
        "v7_tripod_base_1-4_20_printed_thread": make_v7_tripod_base_with_printed_thread(),
        "v7_magnetic_base": g.make_magnetic_base(),
        "v7_receiver_fit_coupon": g.make_fit_coupon(),
    }

    for name, part in parts.items():
        export_part(name, part)
        solid = part.val()
        bbox = solid.BoundingBox()
        print(
            f"{name}: valid={solid.isValid()} solids={len(solid.Solids())}; "
            f"{bbox.xlen:.2f} x {bbox.ylen:.2f} x {bbox.zlen:.2f} mm"
        )

    adapter = parts["v7_pure_cylinder_four_windows"]
    export_reference_assembly(
        "v7_weighted_reference_assembly",
        parts["v7_weighted_base_body"], 38.0, adapter,
    )
    export_reference_assembly(
        "v7_tripod_reference_assembly",
        parts["v7_tripod_base_1-4_20_printed_thread"], 18.0, adapter,
    )
    export_reference_assembly(
        "v7_magnetic_reference_assembly",
        parts["v7_magnetic_base"], 24.0, adapter,
    )


if __name__ == "__main__":
    main()
