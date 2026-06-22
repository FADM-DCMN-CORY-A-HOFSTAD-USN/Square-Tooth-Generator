// =========================================================================
// SQUARE-TOOTH GENERATOR: PARAMETRIC HOUSING & ATX ELECTRONICS BAY MOUNT
// =========================================================================

// Global Scaling Parameter (Set from your python coordinator tool)
lambda = 1.0; 

// Master Turbine Variables Scaled Dynamically
housing_radius = 250 * lambda;
housing_length = 500 * lambda;
wall_thickness = 15 * lambda;

// =========================================================================
// INDUSTRY STANDARD MECHANICAL DIMENSIONS (Keep unscaled for standard hardware)
// =========================================================================
ATX_WIDTH       = 304.8;
ATX_LENGTH      = 244.0;
M2_STANDOFF_X   = 22.0;
M2_STANDOFF_Y   = 80.0;
SSD_25_WIDTH    = 69.85;
SSD_25_LENGTH   = 100.0;
CDROM_525_WIDTH = 146.0;

module turbine_outer_shell() {
    difference() {
        // Outer core casing
        cylinder(h=housing_length, r=housing_radius + wall_thickness, center=true, $fn=100);
        // Internal fluid path cavity
        cylinder(h=housing_length + 2, r=housing_radius, center=true, $fn=100);
    }
}

module electronic_mounting_bay() {
    // Generate a flat external electronics box integrated directly on top of the housing
    box_w = ATX_WIDTH + 40;
    box_l = ATX_LENGTH + 60;
    box_h = 120;
    
    translate([0, housing_radius + (box_h/2) - 5, 0]) {
        difference() {
            // Main solid bracket block
            cube([box_w, box_h, box_l], center=true);
            // Hollow interior space for KiCad boards
            cube([box_w - 10, box_h - 10, box_l - 10], center=true);
            
            // Cutouts for standard PCIe Rear I/O expansion bracket pass-throughs
            translate([-(box_w/2), -20, 0])
                cube([20, 30, box_l - 40], center=true);
        }
        
        // Generate Standard Standard ATX Motherboard Standoff Hole Grids
        color("Gold") {
            atx_standoff_grid();
        }
        
        // Generate Standard M.2 Solid State Module Slot Footprints
        color("Silver") {
            translate([50, -45, 80]) m2_slot_mounts();
        }
    }
}

module atx_standoff_grid() {
    // Standard ATX Mounting Positions relative to board origin
    standoffs = [, [0, 165.1], [0, 243.84],
        [154.94, 0], [154.94, 165.1], [154.94, 243.84],
        [304.8, 0], [304.8, 165.1], [304.8, 243.84]
    ];
    
    for (pos = standoffs) {
        translate([pos[0] - (ATX_WIDTH/2), -48, pos[1] - (ATX_LENGTH/2)]) {
            rotate([90, 0, 0])
                cylinder(h=6, r=1.75, center=true, $fn=20); // Pre-tapped for M3 threads
        }
    }
}

module m2_slot_mounts() {
    // M.2 2280 Layout Specification Profiles
    cube([M2_STANDOFF_X, 4, 5], center=true); // Interface Connector Block
    translate([0, 0, -M2_STANDOFF_Y])
        cylinder(h=8, r=1.0, center=true, $fn=12); // Tail retaining screw pin
}

// Assemble the entire parametric mechanical model
union() {
    turbine_outer_shell();
    electronic_mounting_bay();
}
