"""V8 support-free threaded universal pump adapter system.

Replaces the V7 three-lug bayonet with a large, single-start trapezoidal thread.
The adapter has a male thread and every base has an upward-open female thread.
No trapped support is required. Dimensions are millimetres.
"""

from pathlib import Path
import math

import cadquery as cq
from cadquery import exporters

import common_geometry as g


HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

TYLER_PRINTED_THREAD_STEP = Path(
    "/Users/I818292/Documents/Funs/USBWaterPumpTripodAdapter/"
    "Tripod Adapter from Tyler (FB)/Tripod Adapter.step"
)

# Pump adapter body retained from V7.
BODY_OD = 57.15
BODY_ID = 42.0
BODY_HEIGHT = 46.4
FLOOR_Z = 2.2
WINDOW_BOTTOM_Z = 5.0
WINDOW_TOP_Z = 28.0
WINDOW_WIDTH = 29.0
WINDOW_CORNER_R = 3.5
O_RING_GROOVE_DEPTH = 0.40
O_RING_GROOVE_WIDTH = 2.00
O_RING_GROOVE_CENTER_Z = 41.32

# Support-free universal thread. A conventional single start makes the helix
# visually obvious and less prone to starting on the wrong lead. Two turns
# provide positive engagement without making installation tedious.
THREAD_STARTS = 1
THREAD_LEAD = 5.0
THREAD_ENGAGEMENT = 10.0
MALE_MINOR_D = 41.6
MALE_MAJOR_D = 44.0
FEMALE_MINOR_D = 42.4
FEMALE_MAJOR_D = 44.8
MALE_ROOT_W = 3.4
MALE_CREST_W = 0.8
FEMALE_ROOT_W = 3.8
FEMALE_CREST_W = 1.2
RECEIVER_OD = 58.0
RECEIVER_HEIGHT = 10.0

# Compact six-magnet base. The 18.5 mm height leaves 2.9 mm of solid material
# between the 5.3 mm-deep magnet pockets and the bottom of the female thread.
MAGNETIC_BASE_D = 84.0
MAGNETIC_BASE_H = 18.5
MAGNETIC_BASE_EDGE_R = 1.5
MAGNET_POCKET_CENTER_R = 27.0
MAGNET_POCKET_D = 20.4
MAGNET_POCKET_DEPTH = 5.3

# Low-profile wood screw-down base. Four countersunk clearance holes accept
# common #8 flat-head wood screws while remaining outside the threaded receiver.
SCREW_DOWN_BASE_D = 90.0
SCREW_DOWN_BASE_H = 14.0
SCREW_DOWN_HOLE_BCD = 72.0
SCREW_DOWN_THROUGH_D = 4.6
SCREW_DOWN_HEAD_D = 9.2
SCREW_DOWN_COUNTERSINK_DEPTH = 2.6


def cyl(diameter, height, z=0.0):
    return cq.Workplane("XY").workplane(offset=z).circle(diameter / 2.0).extrude(height)


def helical_ridges(minor_d, major_d, root_w, crest_w, height, z0):
    """Create cropped two-start trapezoidal helical ridges."""
    minor_r = minor_d / 2.0
    major_r = major_d / 2.0
    radius = (minor_r + major_r) / 2.0
    radial_half = (major_r - minor_r) / 2.0

    long_height = height + 2.0 * THREAD_LEAD
    path = cq.Wire.makeHelix(THREAD_LEAD, long_height, radius)
    profile = (
        cq.Workplane("XZ")
        .center(radius, 0)
        .polyline(
            [
                (-radial_half, -root_w / 2.0),
                (radial_half, -crest_w / 2.0),
                (radial_half, crest_w / 2.0),
                (-radial_half, root_w / 2.0),
            ]
        )
        .close()
    )
    first = profile.sweep(path, isFrenet=True)
    ridges = first
    for start in range(1, THREAD_STARTS):
        ridges = ridges.union(
            first.rotate(
                (0, 0, 0),
                (0, 0, 1),
                360.0 * start / THREAD_STARTS,
            )
        )
    ridges = ridges.translate((0, 0, z0 - THREAD_LEAD))
    crop = cyl(major_d + 0.4, height, z0)
    return ridges.intersect(crop)


def male_threaded_spigot():
    # One millimetre of unthreaded lead at the print-bed end prevents first-
    # layer elephant foot from damaging the thread start.
    core = cyl(MALE_MINOR_D, THREAD_ENGAGEMENT + FLOOR_Z, -THREAD_ENGAGEMENT)
    ridges = helical_ridges(
        # Sink the swept ridge 0.2 mm into the core. A merely tangent join can
        # produce an invalid seam on a single-start thread in OpenCascade.
        MALE_MINOR_D - 0.4,
        MALE_MAJOR_D,
        MALE_ROOT_W,
        MALE_CREST_W,
        THREAD_ENGAGEMENT - 1.0,
        -THREAD_ENGAGEMENT + 1.0,
    )
    return core.union(ridges)


def cut_female_thread(body, top_z):
    socket_bottom = top_z - THREAD_ENGAGEMENT - 0.4
    bore = cyl(FEMALE_MINOR_D, THREAD_ENGAGEMENT + 0.8, socket_bottom)
    groove = helical_ridges(
        # Overlap the bore by 0.2 mm so the subtraction has no tangent seam.
        FEMALE_MINOR_D - 0.4,
        FEMALE_MAJOR_D,
        FEMALE_ROOT_W,
        FEMALE_CREST_W,
        THREAD_ENGAGEMENT + 0.4,
        socket_bottom,
    )
    result = body.cut(bore)
    # CadQuery keeps the two thread starts as separate solids. Cutting the
    # Workplane in one operation can silently miss pending solids when they
    # merely touch the bore, so cut each helical clearance explicitly.
    for groove_start in groove.solids().vals():
        result = result.cut(cq.Workplane(obj=groove_start))

    # One millimetre 45-degree entrance chamfer at the upward-open socket.
    lead_in = (
        cq.Workplane("XY")
        .workplane(offset=top_z - 1.0)
        .circle(FEMALE_MINOR_D / 2.0)
        .workplane(offset=1.2)
        .circle((FEMALE_MAJOR_D + 1.2) / 2.0)
        .loft(combine=True)
    )
    return result.cut(lead_in)


def rounded_through_window(angle_deg):
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


def make_v8_adapter():
    adapter = cyl(BODY_OD, BODY_HEIGHT)
    adapter = adapter.cut(cyl(BODY_ID, BODY_HEIGHT - FLOOR_Z + 0.5, FLOOR_Z))
    adapter = adapter.union(male_threaded_spigot())

    for angle in (45, 135, 225, 315):
        adapter = adapter.cut(rounded_through_window(angle))

    groove_z0 = O_RING_GROOVE_CENTER_Z - O_RING_GROOVE_WIDTH / 2.0
    groove_root_d = BODY_OD - 2.0 * O_RING_GROOVE_DEPTH
    groove_outer = cyl(BODY_OD + 4.0, O_RING_GROOVE_WIDTH, groove_z0)
    groove_inner = cyl(groove_root_d, O_RING_GROOVE_WIDTH + 0.2, groove_z0 - 0.1)
    return adapter.cut(groove_outer.cut(groove_inner)).clean()


def add_receiver(base, top_z):
    receiver = cyl(RECEIVER_OD, RECEIVER_HEIGHT, top_z - RECEIVER_HEIGHT)
    return cut_female_thread(base.union(receiver), top_z).clean()


def tyler_printed_tripod_thread_void():
    tyler = cq.importers.importStep(str(TYLER_PRINTED_THREAD_STEP))
    extraction_envelope = cyl(8.0, 8.2, -0.1)
    return extraction_envelope.cut(tyler)


def make_tripod_base():
    body = cyl(64.0, 18.0).edges().fillet(3.0)
    body = add_receiver(body, 18.0)
    return body.cut(tyler_printed_tripod_thread_void()).clean()


def make_weighted_base_body():
    body = cyl(140.0, 28.0).edges().fillet(4.0)
    body = body.cut(cyl(135.6, 3.4, -0.1))
    body = body.cut(cyl(104.0, 20.2, 3.2))
    for angle in (45, 135, 225, 315):
        x = 61.0 * math.cos(math.radians(angle))
        y = 61.0 * math.sin(math.radians(angle))
        hole = cq.Workplane("XY", origin=(x, y, -0.1)).circle(2.15).extrude(10.0)
        insert = cq.Workplane("XY", origin=(x, y, -0.1)).circle(4.05).extrude(6.5)
        body = body.cut(hole).cut(insert)
    return add_receiver(body, 38.0)


def make_weighted_base_cover():
    cover = cyl(135.0, 3.0).edges().fillet(1.0)
    for angle in (45, 135, 225, 315):
        x = 61.0 * math.cos(math.radians(angle))
        y = 61.0 * math.sin(math.radians(angle))
        hole = cq.Workplane("XY", origin=(x, y, -0.1)).circle(2.25).extrude(3.4)
        head = cq.Workplane("XY", origin=(x, y, -0.1)).circle(4.2).extrude(1.9)
        cover = cover.cut(hole).cut(head)
    return cover.cut(cyl(122.0, 1.0, -0.1)).clean()


def make_magnetic_base():
    body = cyl(MAGNETIC_BASE_D, MAGNETIC_BASE_H).edges().fillet(MAGNETIC_BASE_EDGE_R)
    body = add_receiver(body, MAGNETIC_BASE_H)
    for angle in range(0, 360, 60):
        x = MAGNET_POCKET_CENTER_R * math.cos(math.radians(angle))
        y = MAGNET_POCKET_CENTER_R * math.sin(math.radians(angle))
        body = body.cut(
            cq.Workplane("XY", origin=(x, y, -0.1))
            .circle(MAGNET_POCKET_D / 2.0)
            .extrude(MAGNET_POCKET_DEPTH)
        )
    return body.clean()


def make_screw_down_base():
    """Make a wood-mount base with four flush #8 wood-screw holes."""
    body = cyl(SCREW_DOWN_BASE_D, SCREW_DOWN_BASE_H).edges().fillet(3.0)
    body = add_receiver(body, SCREW_DOWN_BASE_H)

    hole_radius = SCREW_DOWN_HOLE_BCD / 2.0
    countersink_z = SCREW_DOWN_BASE_H - SCREW_DOWN_COUNTERSINK_DEPTH
    for angle in (45, 135, 225, 315):
        x = hole_radius * math.cos(math.radians(angle))
        y = hole_radius * math.sin(math.radians(angle))
        through_hole = (
            cq.Workplane("XY", origin=(x, y, -0.1))
            .circle(SCREW_DOWN_THROUGH_D / 2.0)
            .extrude(SCREW_DOWN_BASE_H + 0.2)
        )
        countersink = (
            cq.Workplane("XY", origin=(x, y, countersink_z))
            .circle(SCREW_DOWN_THROUGH_D / 2.0)
            .workplane(offset=SCREW_DOWN_COUNTERSINK_DEPTH + 0.1)
            .circle(SCREW_DOWN_HEAD_D / 2.0)
            .loft(combine=True)
        )
        body = body.cut(through_hole).cut(countersink)

    return body.clean()


def make_female_fit_coupon():
    return add_receiver(cyl(60.0, 10.0), 10.0)


def make_male_fit_coupon():
    grip = cyl(54.0, 4.0)
    coupon = grip.union(male_threaded_spigot()).clean()
    # Rotate the already-fused solid as a rigid body. This keeps the exact V8
    # adapter connector while putting the broad grip on the print bed.
    return coupon.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, 4.0))


def export_part(name, shape):
    exporters.export(shape, str(OUT / f"{name}.step"))
    exporters.export(shape, str(OUT / f"{name}.stl"), tolerance=0.06, angularTolerance=0.10)
    exporters.export(
        shape,
        str(OUT / f"{name}.svg"),
        opt={"projectionDir": (1.0, -1.0, 0.5), "showAxes": False, "showHidden": False},
    )


def main():
    parts = {
        "v8_adapter_male_thread": make_v8_adapter(),
        "v8_tripod_base_printed_1-4_20": make_tripod_base(),
        "v8_weighted_base_body": make_weighted_base_body(),
        "v8_weighted_base_cover": make_weighted_base_cover(),
        "v8_magnetic_base": make_magnetic_base(),
        "v8_screw_down_base": make_screw_down_base(),
        "v8_thread_fit_male": make_male_fit_coupon(),
        "v8_thread_fit_female": make_female_fit_coupon(),
    }
    for name, part in parts.items():
        export_part(name, part)
        solid = part.val()
        box = solid.BoundingBox()
        print(
            f"{name}: valid={solid.isValid()} solids={len(solid.Solids())}; "
            f"{box.xlen:.2f} x {box.ylen:.2f} x {box.zlen:.2f} mm"
        )


if __name__ == "__main__":
    main()
