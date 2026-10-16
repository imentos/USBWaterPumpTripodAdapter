"""V5: Tyler pump adapter with the universal bayonet hub integrated.

The original centered 1/4-20 opening is closed. The three-lug male connector is
printed directly on the adapter underside. The 1/4-20 interface exists only in
the detachable tripod base.
"""

from pathlib import Path

import cadquery as cq
from cadquery import exporters

import v4_geometry as g


HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)


def make_integrated_tyler_adapter():
    tyler = cq.importers.importStep(str(g.TYLER_V3_STEP))

    # Male pilot extends 6 mm below Tyler's original flat bottom and overlaps
    # the existing body by 1 mm so the result is a true single solid.
    neck = g.cyl(g.HUB_NECK_D, g.HUB_NECK_H + 1.0, -g.HUB_NECK_H)
    connector = neck
    for angle in (0, 120, 240):
        lug = g.radial_box(
            g.HUB_LUG_INNER_R,
            g.HUB_LUG_OUTER_R,
            g.HUB_LUG_W,
            g.HUB_LUG_H,
            -g.HUB_NECK_H + g.HUB_LUG_Z,
            angle,
        )
        connector = connector.union(lug)

    # Close the old central tripod-thread opening only through its original
    # depth. The larger hose space higher in the Tyler adapter stays untouched.
    thread_fill = g.cyl(6.4, 8.7, -0.2)

    result = tyler.union(connector).union(thread_fill)
    try:
        result = result.clean()
    except Exception:
        pass
    return result


def export_part(name, shape):
    exporters.export(shape, str(OUT / f"{name}.step"))
    exporters.export(shape, str(OUT / f"{name}.stl"), tolerance=0.08, angularTolerance=0.12)
    exporters.export(
        shape,
        str(OUT / f"{name}.svg"),
        opt={"projectionDir": (1.0, -1.0, 0.8), "showAxes": False, "showHidden": True},
    )


def export_reference_assembly(name, base, base_top_z, adapter):
    installed = adapter.rotate((0, 0, 0), (0, 0, 1), g.BAYONET_ROTATION_DEG).translate((0, 0, base_top_z))
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
        "v5_tyler_adapter_integrated_hub": make_integrated_tyler_adapter(),
        "v5_weighted_base_body": g.make_weighted_base_body(),
        "v5_weighted_base_cover": g.make_weighted_base_cover(),
        "v5_tripod_base_1-4_20": g.make_tripod_base(),
        "v5_magnetic_base": g.make_magnetic_base(),
        "v5_receiver_fit_coupon": g.make_fit_coupon(),
    }

    for name, part in parts.items():
        export_part(name, part)
        solid = part.val()
        bbox = solid.BoundingBox()
        print(
            f"{name}: valid={solid.isValid()} solids={len(solid.Solids())}; "
            f"{bbox.xlen:.2f} x {bbox.ylen:.2f} x {bbox.zlen:.2f} mm"
        )

    adapter = parts["v5_tyler_adapter_integrated_hub"]
    export_reference_assembly(
        "v5_weighted_reference_assembly",
        parts["v5_weighted_base_body"],
        38.0,
        adapter,
    )
    export_reference_assembly(
        "v5_tripod_reference_assembly",
        parts["v5_tripod_base_1-4_20"],
        18.0,
        adapter,
    )
    export_reference_assembly(
        "v5_magnetic_reference_assembly",
        parts["v5_magnetic_base"],
        24.0,
        adapter,
    )


if __name__ == "__main__":
    main()
