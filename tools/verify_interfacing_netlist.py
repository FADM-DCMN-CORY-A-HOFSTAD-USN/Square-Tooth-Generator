#!/usr/bin/env python3
"""
Square-Tooth Generator Architecture Onboarding Gateway.
Programmatic Verification Script for Third-Party KiCad Netlists and Trace Clearance.
"""

import sys
import os
import math

try:
    import pcbnew
except ImportError:
    print("Error: KiCad pcbnew module not found. Run this script inside the KiCad Python environment.")
    sys.exit(1)

class NetlistOnboardingVerifier:
    def __init__(self, target_pcb_path):
        self.pcb_path = target_pcb_path
        
        if not os.path.exists(self.pcb_path):
            raise FileNotFoundError(f"Provided PCB file path does not exist: {self.pcb_path}")
            
        # Load third-party layout database
        self.board = pcbnew.LoadBoard(self.pcb_path)
        self.MM_TO_IU = 1000000
        
        # Enforced RT Manufacturing Specifications
        self.REQUIRED_CLEARANCE_MM = 0.5
        self.CLEARANCE_TOLERANCE_MM = 0.05  # 50-micron tolerance window
        
    def verify_telemetry_guard_rings(self):
        """Scans the board data structures to verify proper shielding around 16-state logic lines."""
        print(f"=== Onboarding Compliance Scan: {os.path.basename(self.pcb_path)} ===")
        
        tracks = self.board.GetTracks()
        telemetry_tracks = []
        ground_tracks = []
        
        # 1. Sort layout tracks into logic channels vs grounding shield meshes
        for track in tracks:
            net_name = track.GetNetname()
            if "_HEX_" in net_name.upper() or "TELEMETRY" in net_name.upper():
                telemetry_tracks.append(track)
            elif "GND" in net_name.upper() or "GROUND" in net_name.upper():
                ground_tracks.append(track)
                
        if not telemetry_tracks:
            print("[WARNING]: No active high-speed hex telemetry tracks detected on this board file.")
            return True

        print(f"[SCANNING]: Found {len(telemetry_tracks)} telemetry data tracks and {len(ground_tracks)} shielding elements.")
        
        violations_detected = 0
        
        # 2. Geometric Vector Evaluation Loop
        for t_track in telemetry_tracks:
            t_start = t_track.GetStart()
            t_end = t_track.GetEnd()
            t_mid_x = (t_start.x + t_end.x) / 2.0
            t_mid_y = (t_start.y + t_end.y) / 2.0
            
            shielded_left = False
            shielded_right = False
            
            # Locate close parallel ground segments flanking this mid-point
            for g_track in ground_tracks:
                g_start = g_track.GetStart()
                g_end = g_track.GetEnd()
                g_mid_x = (g_start.x + g_end.x) / 2.0
                g_mid_y = (g_start.y + g_end.y) / 2.0
                
                # Calculate absolute Euclidean distance between midpoints in millimeters
                distance_mm = math.sqrt((t_mid_x - g_mid_x)**2 + (t_mid_y - g_mid_y)**2) / self.MM_TO_IU
                
                # Check if this ground track satisfies our strict 0.5mm clearance rule
                if abs(distance_mm - self.REQUIRED_CLEARANCE_MM) <= self.CLEARANCE_TOLERANCE_MM:
                    # Determine physical vector orientation relative to the data track
                    # (Simplified orientation assignment for pipeline grouping check)
                    if g_mid_x < t_mid_x:
                        shielded_left = True
                    else:
                        shielded_right = True
                        
            # Enforce that every single trace segment must have full bilateral shielding
            if not (shielded_left and shielded_right):
                violations_detected += 1
                print(f"  [VIOLATION]: Trace segment on net '{t_track.GetNetname()}' at "
                      f"coordinates ({t_mid_x/self.MM_TO_IU:.2f}, {t_mid_y/self.MM_TO_IU:.2f}) "
                      f"lacks a continuous double-sided ground envelope.")

        # 3. Final Boundary Summary Reporting
        print("\n=== Compliance Audit Summary ===")
        if violations_detected > 0:
            print(f"[REJECTED]: Found {violations_detected} shielding layout errors. Board construction halted.")
            print("[REASON]: Exposed lines will create analog crosstalk, destabilizing the 66.66mV steps.")
            return False
        else:
            print("[PASSED]: All 16-state data lanes possess validated guard ring shielding envelopes.")
            return True

if __name__ == "__main__":
    # Expect board path variable assignment passed as a runtime parameter string
    if len(sys.argv) < 2:
        print("Usage: python tools/verify_interfacing_netlist.py <path_to_third_party_board.kicad_pcb>")
        sys.exit(1)
        
    target_pcb = sys.argv[1]
    
    try:
        verifier = NetlistOnboardingVerifier(target_pcb)
        compliance_passed = verifier.verify_telemetry_guard_rings()
        
        if not compliance_passed:
            sys.exit(2) # Return failure flag code to halt automated build setups
    except Exception as err:
        print(f"[CRITICAL ERROR]: Validation runtime aborted unexpectedly: {err}")
        sys.exit(1)
