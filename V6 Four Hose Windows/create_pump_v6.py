"""V6 integrated Tyler adapter with four selectable hose-exit windows.

The lower body is intentionally simple: one straight cylindrical shell with
four through-windows. There are no separate or projecting shoulder pillars.
"""

from pathlib import Path

import cadquery as cq
from cadquery import exporters

import v4_geometry as g


HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

FLOOR_Z = 2.2
WINDOW_BOTTOM_Z = 5.0
WINDOW_TOP_Z = 28.0
WINDOW_WIDTH = 29.0
WINDOW_CORNER_R = 3.5

# 0.07 inch O-ring cross-section = 1.778 mm. The requested half-depth groove
# leaves about 0.88 mm of the O-ring above the original 57.15 mm surface.
O_RING_CROSS_SECTION = 1.778
O_RING_GROOVE_DEPTH = 0.40
O_RING_GROOVE_WIDTH = 2.00
O_RING_GROOVE_CENTER_Z = 41.32
UPPER_ADAPTER_OD = 57.15
LOWER_SHELL_TOP_Z = 30.0
LOWER_SHELL_ID = 42.0


def rounded_side_window(angle_deg):
    """Radial cutter with a rounded rectangular opening profile."""
    center_z = (WINDOW_BOTTOM_Z + WINDOW_TOP_Z) / 2.0
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


def make_v6_adapter():
    tyler = cq.importers.importStep(str(g.TYLER_V3_STEP))

    # Keep only Tyler's proven upper pump-fit collar. Rebuild everything below
    # it as one flush, constant-wall cylinder: 57.15 mm OD / 42.0 mm ID.
    upper_keep = g.cyl(80.0, 20.0, LOWER_SHELL_TOP_Z - 0.2)
    flush_outer_limit = g.cyl(UPPER_ADAPTER_OD, 20.0, LOWER_SHELL_TOP_Z - 0.2)
    upper = tyler.intersect(upper_keep).intersect(flush_outer_limit)
    lower = g.cyl(UPPER_ADAPTER_OD, LOWER_SHELL_TOP_Z + 0.2)
    lower_bore = g.cyl(
        LOWER_SHELL_ID,
        LOWER_SHELL_TOP_Z - FLOOR_Z + 0.4,
        FLOOR_Z,
    )
    lower = lower.cut(lower_bore)
    adapter = upper.union(lower)

    # Integrated male pilot. It extends up to the new interior floor, sealing
    # the old threaded opening without retaining the tall cylindrical boss.
    neck = g.cyl(g.HUB_NECK_D, g.HUB_NECK_H + FLOOR_Z, -g.HUB_NECK_H)
    connector = neck
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

    # Four simple through-windows. The remaining cylinder arcs form four flush
    # supports; both outer and inner walls stay vertical with no recesses.
    for angle in (45, 135, 225, 315):
        adapter = adapter.cut(rounded_side_window(angle))

    # External O-ring retention groove in the straight upper collar.
    groove_z0 = O_RING_GROOVE_CENTER_Z - O_RING_GROOVE_WIDTH / 2.0
    groove_root_d = UPPER_ADAPTER_OD - 2.0 * O_RING_GROOVE_DEPTH
    groove_outer = g.cyl(UPPER_ADAPTER_OD + 4.0, O_RING_GROOVE_WIDTH, groove_z0)
    groove_inner = g.cyl(groove_root_d, O_RING_GROOVE_WIDTH + 0.2, groove_z0 - 0.1)
    adapter = adapter.cut(groove_outer.cut(groove_inner))

    try:
        adapter = adapter.clean()
    except Exception:
        pass
    return adapter


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
    exporters.export(
        assembly,
        str(OUT / f"{name}.svg"),
        opt={"projectionDir": (1.0, -1.0, 0.75), "showAxes": False, "showHidden": True},
    )


def main():
    parts = {
        "v6_tyler_integrated_hub_four_windows": make_v6_adapter(),
        "v6_weighted_base_body": g.make_weighted_base_body(),
        "v6_weighted_base_cover": g.make_weighted_base_cover(),
        "v6_tripod_base_1-4_20": g.make_tripod_base(),
        "v6_magnetic_base": g.make_magnetic_base(),
        "v6_receiver_fit_coupon": g.make_fit_coupon(),
    }

    for name, part in parts.items():
        export_part(name, part)
        solid = part.val()
        bbox = solid.BoundingBox()
        print(
            f"{name}: valid={solid.isValid()} solids={len(solid.Solids())}; "
            f"{bbox.xlen:.2f} x {bbox.ylen:.2f} x {bbox.zlen:.2f} mm"
        )

    adapter = parts["v6_tyler_integrated_hub_four_windows"]
    export_reference_assembly(
        "v6_weighted_reference_assembly",
        parts["v6_weighted_base_body"],
        38.0,
        adapter,
    )
    export_reference_assembly(
        "v6_tripod_reference_assembly",
        parts["v6_tripod_base_1-4_20"],
        18.0,
        adapter,
    )
    export_reference_assembly(
        "v6_magnetic_reference_assembly",
        parts["v6_magnetic_base"],
        24.0,
        adapter,
    )


if __name__ == "__main__":
    main()
