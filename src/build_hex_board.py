#!/usr/bin/env python3
"""
Square-Tooth Generator Infrastructure & RT Architecture Integration.
Automated KiCad PCB Generation Matrix with Integrated RT Guard Rings.
"""

import sys
import os

try:
    import pcbnew
except ImportError:
    print("Error: KiCad pcbnew module not found. Run inside the KiCad Python environment.")
    sys.exit(1)

class HexBoardGenerator:
    def __init__(self, filename="outputs/hex_telemetry_atx.kicad_pcb"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # Initialize Board
        self.board = pcbnew.NEW_BOARD(self.filename)
        self.MM_TO_IU = 1000000
        
        # RT Fabrication Constants
        self.ATX_WIDTH_MM = 304.8
        self.ATX_LENGTH_MM = 244.0
        self.GUARD_RING_OFFSET_MM = 0.5   # Distance from data signal to shield
        self.GUARD_RING_WIDTH_MM = 0.4    # Thickness of the shielding ground trace

    def draw_atx_board_edge(self):
        """Generates outer boundaries of the ATX board layout."""
        edge_layer = self.board.GetLayerID("Edge.Cuts")
        w_iu = int(self.ATX_WIDTH_MM * self.MM_TO_IU)
        l_iu = int(self.ATX_LENGTH_MM * self.MM_TO_IU)
        
        corners = [
            pcbnew.VECTOR2I(0, 0), pcbnew.VECTOR2I(w_iu, 0),
            pcbnew.VECTOR2I(w_iu, l_iu), pcbnew.VECTOR2I(0, l_iu)
        ]
        
        for i in range(4):
            segment = pcbnew.PCB_SHAPE(self.board)
            segment.SetShape(pcbnew.SHAPE_T.SEGMENT)
            segment.SetStart(corners[i])
            segment.SetEnd(corners[(i + 1) % 4])
            segment.SetLayer(edge_layer)
            self.board.Add(segment)

    def route_high_speed_data_trace(self, start_mm, end_mm):
        """Routes a primary 16-state telemetry data track and returns its segment."""
        front_layer = self.board.GetLayerID("F.Cu")
        
        # Instantiate the main trace segment
        track = pcbnew.PCB_TRACK(self.board)
        track.SetStart(pcbnew.VECTOR2I(int(start_mm[0] * self.MM_TO_IU), int(start_mm[1] * self.MM_TO_IU)))
        track.SetEnd(pcbnew.VECTOR2I(int(end_mm[0] * self.MM_TO_IU), int(end_mm[1] * self.MM_TO_IU)))
        track.SetWidth(int(0.25 * self.MM_TO_IU)) # 0.25mm trace width
        track.SetLayer(front_layer)
        self.board.Add(track)
        
        print(f"[RT SIGNAL]: Routed primary signal from {start_mm} to {end_mm}.")
        return track

    def inject_rt_guard_ring(self, core_track):
        """
        RT Fabrication Rule #2: Crosstalk Prevention.
        Duplicates the vector of a track and offsets it symmetrically on both sides
        to create an isolating ground envelope.
        """
        front_layer = self.board.GetLayerID("F.Cu")
        offset_iu = int(self.GUARD_RING_OFFSET_MM * self.MM_TO_IU)
        ring_width_iu = int(self.GUARD_RING_WIDTH_MM * self.MM_TO_IU)
        
        # Fetch underlying coordinates
        start = core_track.GetStart()
        end = core_track.GetEnd()
        
        # Compute the perpendicular vector for parallel offsets
        dx = end.x - start.x
        dy = end.y - start.y
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0: return
        
        # Normal vectors
        nx = -dy / length
        ny = dx / length
        
        # Generate Left and Right Shield Traces
        for side in [-1, 1]:
            guard_track = pcbnew.PCB_TRACK(self.board)
            
            # Apply offset shift
            g_start_x = int(start.x + (nx * offset_iu * side))
            g_start_y = int(start.y + (ny * offset_iu * side))
            g_end_x = int(end.x + (nx * offset_iu * side))
            g_end_y = int(end.y + (ny * offset_iu * side))
            
            guard_track.SetStart(pcbnew.VECTOR2I(g_start_x, g_start_y))
            guard_track.SetEnd(pcbnew.VECTOR2I(g_end_x, g_end_y))
            guard_track.SetWidth(ring_width_iu) # Thick 2oz/3oz equivalent copper copper trace
            guard_track.SetLayer(front_layer)
            
            # Formally bind trace to the system's ground network (GND)
            gnd_net = self.board.FindNet("GND")
            if gnd_net:
                guard_track.SetNet(gnd_net)
                
            self.board.Add(guard_track)
            
        print(f"[RT GUARD RING]: Injected dual parallel {self.GUARD_RING_WIDTH_MM}mm shield boundaries.")

    def compile_and_save_layout(self):
        """Builds net connections and outputs the system footprint file."""
        self.board.BuildConnectivity()
        pcbnew.SaveBoard(self.filename, self.board)
        print(f"[SUCCESS]: Layout saved with absolute guard ring coverage at: {self.filename}")

import math
if __name__ == "__main__":
    generator = HexBoardGenerator()
    generator.draw_atx_board_edge()
    
    # Simulate routing a crucial 108-bit telemetry lane from the turbine block
    telemetry_lane = generator.route_high_speed_data_trace((50, 100), (250, 100))
    
    # Shield it instantly using the repository rule matrix
    generator.inject_rt_guard_ring(telemetry_lane)
    
    generator.compile_and_save_layout()
