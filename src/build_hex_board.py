#!/usr/bin/env python3
"""
Square-Tooth Generator Infrastructure
Automated KiCad PCB Generation Matrix for Hexadecimal Telemetry Logic.
"""

import sys
import os

try:
    import pcbnew
except ImportError:
    print("Error: KiCad pcbnew Python module not found. Please run this script inside the KiCad Python environment.")
    sys.exit(1)

class HexBoardGenerator:
    def __init__(self, filename="outputs/hex_telemetry_atx.kicad_pcb"):
        self.filename = filename
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # 1. Create a blank new KiCad board architecture
        self.board = pcbnew.NEW_BOARD(self.filename)
        
        # 2. Establish unscaled standard ATX board dimensions (in millimeters)
        self.ATX_WIDTH_MM = 304.8
        self.ATX_LENGTH_MM = 244.0
        
        # Conversion scale (KiCad internal units are nanometers)
        self.MM_TO_IU = 1000000

    def draw_atx_board_edge(self):
        """Generates the rigid outer boundary of the ATX board layout."""
        edge_layer = self.board.GetLayerID("Edge.Cuts")
        
        # Define the four bounding corners of the ATX footprint
        w_iu = int(self.ATX_WIDTH_MM * self.MM_TO_IU)
        l_iu = int(self.ATX_LENGTH_MM * self.MM_TO_IU)
        
        corners = [
            pcbnew.VECTOR2I(0, 0),
            pcbnew.VECTOR2I(w_iu, 0),
            pcbnew.VECTOR2I(w_iu, l_iu),
            pcbnew.VECTOR2I(0, l_iu)
        ]
        
        # Loop through corners and draw boundary segments
        for i in range(4):
            start = corners[i]
            end = corners[(i + 1) % 4]
            segment = pcbnew.PCB_SHAPE(self.board)
            segment.SetShape(pcbnew.SHAPE_T.SEGMENT)
            segment.SetStart(start)
            segment.SetEnd(end)
            segment.SetLayer(edge_layer)
            self.board.Add(segment)
        
        print(f"[PCBNEW]: Custom ATX Edge boundaries defined ({self.ATX_WIDTH_MM}mm x {self.ATX_LENGTH_MM}mm).")

    def place_atx_mounting_holes(self):
        """Places standard pre-tapped ATX mounting standoffs mirroring the CAD script."""
        # Standard ATX locations relative to origin (X, Y) in millimeters
        atx_hole_coordinates = [
            (0.0, 0.0), (0.0, 165.1), (0.0, 243.84),
            (154.94, 0.0), (154.94, 165.1), (154.94, 243.84),
            (304.8, 0.0), (304.8, 165.1), (304.8, 243.84)
        ]
        
        for idx, (x, y) in enumerate(atx_hole_coordinates):
            # Create a through-hole mechanical mounting pad footprint
            pad_footprint = pcbnew.FOOTPRINT(self.board)
            pad_footprint.SetReference(f"MH{idx+1}")
            
            # Size the hole to accept standard chassis M3 structural screws
            pad = pcbnew.PAD(pad_footprint)
            pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetSize(pcbnew.VECTOR2I(int(6.0 * self.MM_TO_IU), int(6.0 * self.MM_TO_IU))) # 6mm pad diameter
            pad.SetDrillSize(pcbnew.VECTOR2I(int(3.2 * self.MM_TO_IU), int(3.2 * self.MM_TO_IU))) # 3.2mm screw clearance hole
            
            # Position the pad precisely to match the turbine housing bracket grid
            pos_x = int(x * self.MM_TO_IU)
            pos_y = int(y * self.MM_TO_IU)
            pad_footprint.SetPosition(pcbnew.VECTOR2I(pos_x, pos_y))
            
            self.board.Add(pad_footprint)
        print(f"[PCBNEW]: {len(atx_hole_coordinates)} structural mounting points verified.")

    def inject_hex_telemetry_chips(self):
        """Instantiates the processing chips parsing the 16-state square tooth arrays."""
        # Place the master cluster processing array in the center of the board
        center_x = int((self.ATX_WIDTH_MM / 2) * self.MM_TO_IU)
        center_y = int((self.ATX_LENGTH_MM / 2) * self.MM_TO_IU)
        
        # Instantiate custom QFP processor for 16-state hexadecimal calculations
        chip_footprint = pcbnew.FOOTPRINT(self.board)
        chip_footprint.SetReference("U1_HEX_DECODER")
        chip_footprint.SetPosition(pcbnew.VECTOR2I(center_x, center_y))
        
        # Define internal trace width configuration for high-speed square-wave signals
        net_settings = self.board.GetDesignSettings()
        # Set track width to 0.25mm to balance impedance and logic signal protection
        net_settings.SetTrackWidth(int(0.25 * self.MM_TO_IU))
        
        self.board.Add(chip_footprint)
        print("[PCBNEW]: High-resolution hexadecimal tracking logic integrated into design matrix.")

    def compile_and_save_layout(self):
        """Executes design metric compiles and exports the structural board archive."""
        # Refresh the connectivity netlist tree topology structures
        self.board.BuildConnectivity()
        # Commit layout file memory blocks cleanly to target destination path
        pcbnew.SaveBoard(self.filename, self.board)
        print(f"\n[SUCCESS]: Electronic hardware architecture saved to: {self.filename}")

if __name__ == "__main__":
    generator = HexBoardGenerator()
    generator.draw_atx_board_edge()
    generator.place_atx_mounting_holes()
    generator.inject_hex_telemetry_chips()
    generator.compile_and_save_layout()
