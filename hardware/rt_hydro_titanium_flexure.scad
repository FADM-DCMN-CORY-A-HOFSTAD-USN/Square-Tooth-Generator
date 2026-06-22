/*
 * REVOLUTIONARY TECHNOLOGY: HYDRO-GRADE TITANIUM FLEXURE MOUNT
 * Material: Solid Titanium Grade 5 (Ti-6Al-4V)
 * Function: Replaces rubber elastomer plugs in high-shear fluid environments.
 * Uses a monolithic wire-EDM serpentine cut to create a structural metal spring
 * that isolates acoustic vibration without tearing under water pressure.
 */

$fn = 64;

// Mount Dimensions
mount_length = 40;
mount_width = 40;
mount_thickness = 10;

// Flexure Cut Parameters
cut_width = 1.5; // Wire-EDM cut thickness
beam_thickness = 2.5; // Thickness of the resulting titanium spring beams
num_folds = 4;

module monolithic_titanium_flexure() {
    color("Silver") {
        difference() {
            // Main Solid Block
            minkowski() {
                cube([mount_length - 4, mount_width - 4, mount_thickness], center=true);
                cylinder(r=2, h=0.1, center=true);
            }
            
            // Central Mounting Hole (For the Turbine Bolt)
            cylinder(r=4.5, h=mount_thickness + 5, center=true);
            
            // Outer Mounting Holes (To bolt to the chassis)
            for (x = [-mount_length/2 + 5, mount_length/2 - 5]) {
                for (y = [-mount_width/2 + 5, mount_width/2 - 5]) {
                    translate([x, y, 0])
                        cylinder(r=2.5, h=mount_thickness + 5, center=true);
                }
            }
            
            // The Serpentine EDM Cuts (Creating the Flexure Spring)
            // These cuts sever the direct physical connection between the center 
            // and the outer edge, forcing vibrations to travel a long, bending path.
            for (i = [1 : num_folds]) {
                // Cut from the Left
                if (i % 2 != 0) {
                    translate([2, (i * (cut_width + beam_thickness)) - (mount_width/2) + 5, 0])
                        cube([mount_length - 12, cut_width, mount_thickness + 2], center=true);
                }
                // Cut from the Right
                else {
                    translate([-2, (i * (cut_width + beam_thickness)) - (mount_width/2) + 5, 0])
                        cube([mount_length - 12, cut_width, mount_thickness + 2], center=true);
                }
                
                // Mirror the cuts on the bottom half
                if (i % 2 != 0) {
                    translate([2, -((i * (cut_width + beam_thickness)) - (mount_width/2) + 5), 0])
                        cube([mount_length - 12, cut_width, mount_thickness + 2], center=true);
                }
                else {
                    translate([-2, -((i * (cut_width + beam_thickness)) - (mount_width/2) + 5), 0])
                        cube([mount_length - 12, cut_width, mount_thickness + 2], center=true);
                }
            }
        }
    }
}

// Render the Flexure
monolithic_titanium_flexure();
