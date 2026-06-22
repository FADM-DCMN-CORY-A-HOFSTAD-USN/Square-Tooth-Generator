import json
import os
from core.physics_engine import SquareToothPhysics
from core.telemetry_bridge import TelemetryBridge

def run_scaling_engine():
    print("=== Square-Tooth Generator Parametric Sizing Engine ===")
    
    # Simple dynamic user inputs
    environment = input("Enter environment type (hydro / wind / combustion_fuel): ").strip()
    target_power = float(input("Enter Target Power Output (Watts): "))
    target_rpm = float(input("Enter Target Operating Speed (RPM): "))
    
    # Load configuration profiles
    config_path = os.path.join(os.path.dirname(__file__), '../config/environment_profiles.json')
    with open(config_path, 'r') as f:
        profiles = json.load(f)
        
    if environment not in profiles:
        print("Invalid environment selection.")
        return

    # Process Physics & Materials
    engine = SquareToothPhysics(profiles[environment])
    min_shaft_dia = engine.calculate_shaft_diameter(target_power, target_rpm, bending_moment=(target_power*0.01))
    
    # Process Telemetry Matrix Alignment
    teeth = TelemetryBridge.calculate_hex_tooth_matrix(target_rpm)
    actual_freq = TelemetryBridge.generate_hex_sync_frequency(target_rpm, teeth)
    
    # Format and Output Results Dynamically
    print("\n--- DESIGN SPECIFICATIONS GENERATED ---")
    print(f"Fluid Density Mapped: {profiles[environment]['fluid_density_rho']} kg/m3")
    print(f"Minimum Titanium Shaft Core Diameter: {min_shaft_dia * 1000:.2f} mm")
    print(f"Optimized Synchronous Square-Tooth Pattern: {teeth} Teeth (Hex-Aligned Cluster)")
    print(f"Resulting Telemetry Signal Wave Frequency: {actual_freq:.1f} Hz")

if __name__ == "__main__":
    run_scaling_engine()
