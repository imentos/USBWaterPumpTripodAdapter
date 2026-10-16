"""CampTapLab V4 universal base system.

The existing Tyler V3 pump adapter stays unchanged. A thin universal hub is
bolted to its existing 1/4-20 insert, then any V4 base locks to that hub with a
three-lug, 30 degree bayonet. All dimensions are millimetres.
"""

from pathlib import Path
import math

import cadquery as cq
from cadquery import exporters


HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

TYLER_V3_STEP = Path(
    "/Users/I818292/Documents/Funs/USBWaterPumpTripodAdapter/"
    "Tyler v2/Tripod Adapter V3 57.15mm Shoulder Pillars.step"
)

# Shared bayonet geometry. Clearance is intentionally generous for an initial
# PETG/ASA FDM prototype and can be tightened after a fit coupon is tested.
HUB_FLANGE_D = 58.0
HUB_FLANGE_H = 7.0
HUB_FLANGE_Z = 6.0
HUB_NECK_D = 36.0
HUB_NECK_H = 6.0
HUB_LUG_OUTER_R = 24.0
HUB_LUG_INNER_R = 16.5
HUB_LUG_W = 10.0
# Lug bottom is coplanar with the male pilot bottom for support-free printing.
HUB_LUG_Z = 0.0
HUB_LUG_H = 3.0

RECEIVER_D = 62.0
RECEIVER_H = 10.0
RECEIVER_NECK_CLEAR_D = 37.0
RECEIVER_TRACK_D = 49.2
RECEIVER_ENTRY_W = 10.8
RECEIVER_CAVITY_DEPTH = 6.2
# Track follows the lugs 0.8 mm downward while preserving the original
# 0.4/0.6 mm vertical clearances below/above the 3.0 mm lugs.
RECEIVER_TRACK_BOTTOM = 6.4
RECEIVER_TRACK_TOP = 2.4
BAYONET_ROTATION_DEG = 30.0


def cyl(diameter, height, z=0.0):
    return cq.Workplane("XY").workplane(offset=z).circle(diameter / 2.0).extrude(height)


def radial_box(r0, r1, width, height, z, angle_deg):
    box = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .center((r0 + r1) / 2.0, 0)
        .box(r1 - r0, width, height, centered=(True, True, False))
    )
    return box.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def add_receiver(base, top_z, include_safety_lock=False):
    """Add the common female bayonet receiver to a base body."""
    receiver_bottom = top_z - RECEIVER_H
    result = base.union(cyl(RECEIVER_D, RECEIVER_H, receiver_bottom))

    # Central pilot bore and the three straight insertion windows.
    center_cut = cyl(RECEIVER_NECK_CLEAR_D, RECEIVER_CAVITY_DEPTH + 0.2,
                     top_z - RECEIVER_CAVITY_DEPTH)
    result = result.cut(center_cut)
    for angle in (0, 120, 240):
        entry = radial_box(
            HUB_LUG_INNER_R - 0.4,
            HUB_LUG_OUTER_R + 0.6,
            RECEIVER_ENTRY_W,
            RECEIVER_CAVITY_DEPTH + 0.2,
            top_z - RECEIVER_CAVITY_DEPTH,
            angle,
        )
        result = result.cut(entry)

    # Annular rotation gallery. The uncut top skin captures the lugs.
    track_height = RECEIVER_TRACK_BOTTOM - RECEIVER_TRACK_TOP
    track = cyl(RECEIVER_TRACK_D, track_height, top_z - RECEIVER_TRACK_BOTTOM)
    result = result.cut(track)

    # Positive stops constrain rotation to approximately 30 degrees.
    for angle in (50, 170, 290):
        stop = radial_box(
            HUB_NECK_D / 2.0 + 0.5,
            RECEIVER_TRACK_D / 2.0 - 0.2,
            2.4,
            track_height,
            top_z - RECEIVER_TRACK_BOTTOM,
            angle,
        )
        result = result.union(stop)

    if not include_safety_lock:
        return result

    # Optional radial M4 safety-lock hole at 60 degrees.
    lock_small = (
        cq.Workplane("YZ", origin=(17.5, 0, top_z - 3.8))
        .circle(2.15)
        .extrude(15.0)
        .rotate((0, 0, 0), (0, 0, 1), 60)
    )
    lock_insert = (
        cq.Workplane("YZ", origin=(25.0, 0, top_z - 3.8))
        .circle(4.05)
        .extrude(7.5)
        .rotate((0, 0, 0), (0, 0, 1), 60)
    )
    return result.cut(lock_small).cut(lock_insert)


def make_universal_hub():
    neck = cyl(HUB_NECK_D, HUB_NECK_H)
    lugs = neck
    for angle in (0, 120, 240):
        lugs = lugs.union(
            radial_box(
                HUB_LUG_INNER_R,
                HUB_LUG_OUTER_R,
                HUB_LUG_W,
                HUB_LUG_H,
                HUB_LUG_Z,
                angle,
            )
        )
    flange = cyl(HUB_FLANGE_D, HUB_FLANGE_H, HUB_FLANGE_Z)
    hub = lugs.union(flange)

    # 1/4-20 bolt clearance and socket-head counterbore.
    hub = hub.cut(cyl(6.8, HUB_FLANGE_Z + HUB_FLANGE_H + 0.4, -0.2))
    hub = hub.cut(cyl(11.2, 4.8, -0.2))

    # Shallow top recess for a 50 mm OD silicone friction washer.
    washer_recess = cyl(50.2, 0.65, HUB_FLANGE_Z + HUB_FLANGE_H - 0.65)
    washer_keepout = cyl(12.0, 0.9, HUB_FLANGE_Z + HUB_FLANGE_H - 0.8)
    return hub.cut(washer_recess.cut(washer_keepout))


def make_weighted_base_body():
    body = cyl(140.0, 28.0)
    body = body.edges().fillet(4.0)

    # Recessed cover plus cavity for four nominal 4 inch steel discs.
    body = body.cut(cyl(135.6, 3.4, -0.1))
    body = body.cut(cyl(104.0, 20.2, 3.2))

    for angle in (45, 135, 225, 315):
        x = 61.0 * math.cos(math.radians(angle))
        y = 61.0 * math.sin(math.radians(angle))
        hole = cq.Workplane("XY", origin=(x, y, -0.1)).circle(2.15).extrude(10.0)
        insert = cq.Workplane("XY", origin=(x, y, -0.1)).circle(4.05).extrude(6.5)
        body = body.cut(hole).cut(insert)

    return add_receiver(body, 38.0, include_safety_lock=False)


def make_weighted_base_cover():
    cover = cyl(135.0, 3.0)
    cover = cover.edges().fillet(1.0)
    for angle in (45, 135, 225, 315):
        x = 61.0 * math.cos(math.radians(angle))
        y = 61.0 * math.sin(math.radians(angle))
        hole = cq.Workplane("XY", origin=(x, y, -0.1)).circle(2.25).extrude(3.4)
        head = cq.Workplane("XY", origin=(x, y, -0.1)).circle(4.2).extrude(1.9)
        cover = cover.cut(hole).cut(head)
    return cover.cut(cyl(122.0, 1.0, -0.1))


def make_tripod_base():
    body = cyl(64.0, 18.0)
    body = body.edges().fillet(3.0)
    # Tripod prototype relies only on the three-lug bayonet track and positive
    # 30-degree stops. No M4 safety screw or heat-set-insert hole.
    body = add_receiver(body, 18.0, include_safety_lock=False)
    # Bottom socket for an 8.2 mm OD, up-to-10 mm long 1/4-20 insert.
    insert_socket = cyl(8.2, 10.2, -0.1)
    lead_in = (
        cq.Workplane("XY")
        .circle(5.1)
        .workplane(offset=1.2)
        .circle(4.1)
        .loft(combine=True)
    )
    return body.cut(insert_socket).cut(lead_in)


def make_magnetic_base():
    body = cyl(90.0, 24.0)
    body = body.edges().fillet(3.0)
    body = add_receiver(body, 24.0, include_safety_lock=False)

    # Six bottom-entry pockets for 20 mm x 5 mm magnets.
    for angle in range(0, 360, 60):
        x = 27.0 * math.cos(math.radians(angle))
        y = 27.0 * math.sin(math.radians(angle))
        pocket = cq.Workplane("XY", origin=(x, y, -0.1)).circle(10.2).extrude(5.3)
        body = body.cut(pocket)

    # Integrated safety-tether eyelet on the +X side.
    bridge = (
        cq.Workplane("XY")
        .box(12.0, 12.0, 9.0, centered=(True, True, False))
        .translate((45.0, 0, 4.0))
    )
    eyelet = (
        cq.Workplane("YZ", origin=(43.0, 0, 8.5))
        .circle(6.0)
        .circle(3.0)
        .extrude(10.0)
    )
    return body.union(bridge).union(eyelet)


def make_fit_coupon():
    return add_receiver(cyl(66.0, 4.0), 14.0, include_safety_lock=False)


def export_part(name, shape):
    exporters.export(shape, str(OUT / f"{name}.step"))
    exporters.export(shape, str(OUT / f"{name}.stl"), tolerance=0.08, angularTolerance=0.12)
    exporters.export(
        shape,
        str(OUT / f"{name}.svg"),
        opt={
            "projectionDir": (1.0, -1.0, 0.8),
            "showAxes": False,
            "showHidden": True,
            "strokeWidth": 0.5,
        },
    )


def main():
    parts = {
        "v4_universal_hub": make_universal_hub(),
        "v4_weighted_base_body": make_weighted_base_body(),
        "v4_weighted_base_cover": make_weighted_base_cover(),
        "v4_tripod_base": make_tripod_base(),
        "v4_magnetic_base": make_magnetic_base(),
        "v4_receiver_fit_coupon": make_fit_coupon(),
    }

    for name, part in parts.items():
        export_part(name, part)
        bbox = part.val().BoundingBox()
        print(
            f"{name}: {bbox.xlen:.2f} x {bbox.ylen:.2f} x {bbox.zlen:.2f} mm; "
            f"volume {part.val().Volume() / 1000.0:.1f} cm^3"
        )

    # Reference assembly only; printable parts remain separate files.
    if TYLER_V3_STEP.exists():
        tyler = cq.importers.importStep(str(TYLER_V3_STEP))
        weighted = parts["v4_weighted_base_body"]
        hub_in_base = parts["v4_universal_hub"].translate((0, 0, 32.0))
        tyler_on_hub = tyler.translate((0, 0, 45.0))
        assembly = weighted.union(hub_in_base).union(tyler_on_hub)
        exporters.export(assembly, str(OUT / "v4_weighted_base_reference_assembly.step"))
        exporters.export(
            assembly,
            str(OUT / "v4_weighted_base_reference_assembly.stl"),
            tolerance=0.1,
            angularTolerance=0.15,
        )
        exporters.export(
            assembly,
            str(OUT / "v4_weighted_base_reference_assembly.svg"),
            opt={"projectionDir": (1.0, -1.0, 0.7), "showAxes": False, "showHidden": True},
        )


if __name__ == "__main__":
    main()
