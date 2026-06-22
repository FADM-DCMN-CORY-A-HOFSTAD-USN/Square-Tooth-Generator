/*
 * REVOLUTIONARY TECHNOLOGY: ATX-TO-HEX ADAPTER BRACKET
 * Function: Mounts the Square-Tooth Generator telemetry board into a standard 
 * ATX chassis slot, featuring physical EMI Guard Ring moats.
 * Material: Non-conductive ABS or Carbon-infused PETG.
 */

$fn = 64;

// Standard ATX Mounting Dimensions (mm)
atx_hole_spacing_x = 155.0;
atx_hole_spacing_y = 105.0;
bracket_thickness = 3.0;

module atx_base_plate() {
    color("DarkSlateGray") {
        difference() {
            // Main Bracket Body
            minkowski() {
                cube([atx_hole_spacing_x + 20, atx_hole_spacing_y + 20, bracket_thickness], center=true);
                cylinder(r=5, h=0.1, center=true);
            }
            
            // ATX Standoff Holes
            for (x = [-atx_hole_spacing_x/2, atx_hole_spacing_x/2]) {
                for (y = [-atx_hole_spacing_y/2, atx_hole_spacing_y/2]) {
                    translate([x, y, 0])
                        cylinder(r=2.1, h=bracket_thickness + 5, center=true); // M3 screw holes
                }
            }
            
            // Central cutout for the Hex Processor cooling
            cube([80, 80, bracket_thickness + 5], center=true);
        }
    }
}

module physical_guard_ring_moat() {
    /* * The Guard Ring acts as a physical EMI barrier. We cut a trench 
     * around the delicate telemetry sensor interface. During assembly, 
     * a continuous loop of heavy copper wire is laid in this trench and 
     * grounded to the ATX chassis.
     */
    color("Gold") {
        difference() {
            // Outer bounding of the moat
            cube([100, 100, bracket_thickness + 2], center=true);
            // Inner bounding
            cube([96, 96, bracket_thickness + 5], center=true);
        }
    }
}

module pcie_support_tab() {
    // Standard PCIe slot insert tab for structural rigidity
    color("DarkSlateGray") {
        translate([-atx_hole_spacing_x/2 - 10, 0, -5])
            cube([20, 12, 10], center=true);
    }
}

module master_assembly() {
    difference() {
        union() {
            atx_base_plate();
            pcie_support_tab();
        }
        // Subtractive cutout for the Guard Ring copper
        physical_guard_ring_moat();
    }
    
    // Visualize the Copper Guard Ring
    physical_guard_ring_moat();
}

// Render the Bracket
master_assembly();
