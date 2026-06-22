#!/usr/bin/env python3
"""
Square-Tooth Generator Quality Gate.
Parses the engineering Bill of Materials (BOM) to enforce strict material integrity.
Bans commercial-grade components and enforces specialized high-vibration alternatives.
"""

import sys
import os
import csv

class BomMaterialValidator:
    def __init__(self, bom_path="outputs/manufacturing/bom.csv"):
        self.bom_path = bom_path
        
        # Adjust path if executed from inside the tools subdirectory
        if not os.path.exists(self.bom_path) and os.path.exists(os.path.join("..", self.bom_path)):
            self.bom_path = os.path.join("..", self.bom_path)

    def enforce_material_compliance(self):
        """Audits BOM line items against military/industrial temperature and vibration specs."""
        print(f"=== Component Material Integrity Audit: {os.path.basename(self.bom_path)} ===")
        
        if not os.path.exists(self.bom_path):
            print(f"[CRITICAL ERROR]: Target BOM file not found at: {self.bom_path}")
            print("Please ensure your KiCad script exports the component list to the manufacturing directory.")
            return False

        violations_found = 0
        total_components = 0

        with open(self.bom_path, mode='r', encoding='utf-8') as f:
            # Assumes standard KiCad CSV export columns: Reference, Value, Footprint, MPN (Manufacturer Part Number), Description
            reader = csv.DictReader(f)
            
            for line_idx, row in enumerate(reader, start=2):
                total_components += 1
                ref = row.get("Reference", "").upper()
                value = row.get("Value", "").upper()
                description = row.get("Description", "").upper()
                mpn = row.get("MPN", "").upper()

                # 1. Enforce Operating Temperature Ranges (Ban standard commercial grades: 0°C to 70°C)
                if "COMMERCIAL" in description or "COMMERCIAL" in value:
                    violations_found += 1
                    print(f"  ❌ [MATERIAL VIOLATION] Line {line_idx} ({ref}): Commercial-grade component detected.")
                    print("     Enforcement: Must upgrade to Extended Industrial (-40°C to 85°C) or Military (-55°C to 125°C) grade.")

                # 2. Enforce Timing Reference Integrity (Ban legacy quartz crystal part profiles)
                if ref.startswith("Y") or ref.startswith("X"): # Timing oscillator designators
                    if "CRYSTAL" in description or "QUARTZ" in description or "XTAL" in description:
                        violations_found += 1
                        print(f"  ❌ [MATERIAL VIOLATION] Line {line_idx} ({ref}): Quartz crystal part number found: '{mpn}'.")
                        print("     Enforcement: Prohibited under vibration guidelines. Substitute with a silicon MEMS oscillator.")

                # 3. Enforce Capacitor Dielectric Integrity (Ban microphonic Class II MLCC structures)
                if ref.startswith("C") and ("FILTER" in ref or "TELEM" in ref):
                    if "X7R" in description or "Y5V" in description or "X5R" in description:
                        violations_found += 1
                        print(f"  ❌ [MATERIAL VIOLATION] Line {line_idx} ({ref}): Piezoceramic Class II dielectric '{value}' on telemetry track.")
                        print("     Enforcement: High microphonic noise risk. Enforce Class I COG/NPO or solid tantalum capacitors.")

        print("\n=== Material Integrity Audit Summary ===")
        if violations_found > 0:
            print(f"[REJECTED]: Found {violations_found} material grade compliance failures. Purchasing halted.")
            print("[REASON]: Lower-grade materials cannot sustain the 66.66mV logic thresholds under active generator loads.")
            return False
        
        print(f"[PASSED]: All {total_components} components conform to high-reliability performance baselines.")
        return True

if __name__ == "__main__":
    validator = BomMaterialValidator()
    compliance_passed = validator.enforce_material_compliance()
    
    if not compliance_passed:
        sys.exit(5) # Exit code 5 isolates material non-compliance in the deployment tree
    sys.exit(0)
