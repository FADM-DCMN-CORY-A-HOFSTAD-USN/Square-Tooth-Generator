#!/usr/bin/env python3
"""
Square-Tooth Generator Architecture Quality Gate.
Scans KiCad board components to detect and ban vibration-vulnerable footprints.
"""

import sys
import os

try:
    import pcbnew
except ImportError:
    print("Error: KiCad pcbnew module not found. Run this script inside the KiCad Python environment.")
    sys.exit(1)

class VibrationComplianceScanner:
    def __init__(self, pcb_path="outputs/hex_telemetry_atx.kicad_pcb"):
        self.pcb_path = pcb_path
        
        # Look one directory up if called from inside the tools folder
        if not os.path.exists(self.pcb_path) and os.path.exists(os.path.join("..", self.pcb_path)):
            self.pcb_path = os.path.join("..", self.pcb_path)
            
        if not os.path.exists(self.pcb_path):
            raise FileNotFoundError(f"Target PCB file not found: {self.pcb_path}")
            
        self.board = pcbnew.LoadBoard(self.pcb_path)

    def scan_for_vulnerable_components(self):
        """Audits all board footprints against high-vibration survival standards."""
        print(f"=== Anti-Vibration Compliance Audit: {os.path.basename(self.pcb_path)} ===")
        
        footprints = self.board.GetFootprints()
        vulnerabilities_found = 0
        
        # Prohibited keywords inside vulnerable footprint names/references
        BANNED_FOOTPRINTS = {
            "QFP": "Perimeter-leaded Quad Flat Package. High risk of lead flexing and solder cracking. Upgrade to QFN or BGA.",
            "SOIC": "Small Outline Integrated Circuit. Long flexible side pins. Upgrade to DFN or QFN.",
            "CRYSTAL": "Quartz Crystal Resonator. Highly vulnerable to mechanical resonance and phase jitter. Upgrade to a silicon MEMS oscillator.",
            "XTAL": "Quartz Crystal Resonator. Vulnerable to mechanical phase jitter. Upgrade to a silicon MEMS oscillator."
        }
        
        for fp in footprints:
            fp_name = fp.GetFPID().GetLibItemName().upper()
            ref_des = fp.GetReference().upper()
            
            # 1. Audit check for vulnerable IC packaging geometries & quartz timing crystals
            for key, reason in BANNED_FOOTPRINTS.items():
                if key in fp_name or key in ref_des:
                    vulnerabilities_found += 1
                    print(f"  ❌ [VULNERABILITY]: Component {fp.GetReference()} uses footprint '{fp.GetFPID().GetLibItemName()}'.")
                    print(f"     Reason: {reason}")
            
            # 2. Audit check for vulnerable ceramic capacitors (Piezoceramic microphonics risk)
            # Standard surface mount capacitors (e.g., C_0805) are flagged if they sit on critical telemetry filters
            if ref_des.startswith("C") and ("FILTER" in ref_des or "TELEM" in ref_des):
                if "0805" in fp_name or "1206" in fp_name:
                    print(f"  ⚠️  [ADVISORY]: Filter Capacitor {fp.GetReference()} ({fp_name}) flags microphonic risk if Class II (X7R/Y5V).")
                    print(f"     Recommendation: Ensure Bill of Materials explicitly enforces Class I (COG/NPO) or Tantalum silicon chips.")

        print("\n=== Anti-Vibration Audit Summary ===")
        if vulnerabilities_found > 0:
            print(f"[REJECTED]: Found {vulnerabilities_found} critical vibration vulnerabilities. Board decertified.")
            print("[REASON]: Microphonics, phase noise, or lead flexing will distort the 16-state logic thresholds.")
            return False
        
        print("[PASSED]: No high-profile structural vulnerabilities located. Component profiles certified for high-vibration.")
        return True

if __name__ == "__main__":
    try:
        scanner = VibrationComplianceScanner()
        certified = scanner.scan_for_vulnerable_components()
        if not certified:
            sys.exit(4)  # Exit code 4 isolates vibration rule failures in the pipeline
        sys.exit(0)
    except Exception as err:
        print(f"[CRITICAL ERROR]: Compliance scanner aborted unexpectedly: {err}")
        sys.exit(1)
