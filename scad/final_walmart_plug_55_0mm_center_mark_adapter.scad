$fn = 256;


// FINAL Walmart plug version.
// Adapter upper feature mimics a 5.5 cm water-jar neck and inserts into the pump.
// Only the upper fit changed from the previous thin-wall version. Lower base, side
// exit, four grips, and bottom center mark are retained.

plug_od = 55.0;          // Walmart jar spec target; all dimensions are in mm.
plug_h = 16;
plug_wall = 3.0;
plug_inner_d = 42;       // Open center so hose can pass through.

base_od = 52;
base_wall = 3.0;
base_id = base_od - 2 * base_wall;
base_h = 30;
shoulder_h = 8;
insert_boss_d = 30;
insert_boss_h = 12;
side_opening_w = 24;
side_opening_bottom_z = insert_boss_h;
side_opening_top_z = base_h - 3;
side_opening_h = side_opening_top_z - side_opening_bottom_z;
side_opening_z = (side_opening_top_z + side_opening_bottom_z) / 2;
side_opening_angle = 45;
grip_column_w = 9;
grip_column_depth = 3.2;
grip_column_z0 = 4;
grip_column_h = 20;
lip_chamfer = 1.2;
center_mark_d = 3.0;
center_mark_depth = 1.0;


module water_shedding_chamfer(d, h, chamfer=1.2) {
  cylinder(d1 = d - 2 * chamfer, d2 = d, h = chamfer);
  translate([0, 0, chamfer])
    cylinder(d = d, h = h - 2 * chamfer);
  translate([0, 0, h - chamfer])
    cylinder(d1 = d, d2 = d - 2 * chamfer, h = chamfer);
}

module grip_column(angle) {
  rotate([0, 0, angle])
    translate([base_od / 2 - 0.3, -grip_column_w / 2, grip_column_z0])
      cube([grip_column_depth, grip_column_w, grip_column_h]);
}

module four_grip_columns() {
  for (a = [0, 90, 180, 270])
    grip_column(a);
}

module side_opening() {
  rotate([0, 0, side_opening_angle])
    translate([0, -side_opening_w / 2, side_opening_z - side_opening_h / 2])
      cube([base_od / 2 + grip_column_depth + 8, side_opening_w, side_opening_h]);
}

difference() {
  union() {
    water_shedding_chamfer(base_od, base_h - shoulder_h, 1.1);

    // Printable shoulder from lower body to smaller plug.
    translate([0, 0, base_h - shoulder_h])
      cylinder(d1 = base_od, d2 = plug_od, h = shoulder_h + 0.1);

    // Independent solid boss for heat-set insert.
    cylinder(d = insert_boss_d, h = insert_boss_h);

    // Upper plug that inserts into pump bottom.
    translate([0, 0, base_h - 0.1])
      cylinder(d = plug_od, h = plug_h + 0.1);

    four_grip_columns();
  }

  // Hollow lower shell.
  translate([0, 0, 1.2])
    cylinder(d = base_id, h = base_h - shoulder_h + 0.4);

  // Open center through plug and chamber for hose passage.
  translate([0, 0, insert_boss_h])
    cylinder(d = base_id, h = base_h - insert_boss_h + 2);

  translate([0, 0, base_h - 0.4])
    cylinder(d = plug_inner_d, h = plug_h + 1.5);

  // Lead-in chamfer on plug top.
  translate([0, 0, base_h + plug_h - lip_chamfer])
    cylinder(d1 = plug_inner_d, d2 = plug_inner_d + 2 * lip_chamfer, h = lip_chamfer + 0.2);

  // Side hose exit.
  side_opening();

  // Tiny center mark for heat-set insert alignment.
  translate([0, 0, -0.2])
    cylinder(d = center_mark_d, h = center_mark_depth + 0.2);
}
