import time
import math
from physics_engine import HexNativeSquareToothEngine
from telemetry_bridge import HexTelemetryBridge
from univac_serializer import UnivacIXSerializer

class ATXGuardRingBus:
    """
    Hardware Abstraction Layer (HAL) for the ATX Motherboard Slot.
    Simulates the physical Guard Ring stripping EMI noise from the raw analog sensor lines.
    """
    def __init__(self):
        self.emi_noise_floor = 0.02 # Expected voltage ripple from the generator
        
    def scrub_sensor_input(self, raw_voltage):
        """Passes the signal through the virtual guard ring moat."""
        if raw_voltage is None:
            return 0.0
        # The physical guard ring bleeds noise to the ATX ground pin
        clean_voltage = max(0.0, raw_voltage - self.emi_noise_floor)
        return clean_voltage
        
    def write_actuator_voltage(self, hex_voltage):
        """Pushes exact Hexadecimal voltage to the active gap flaps."""
        # Hardware limits ensure we don't blow the ATX bus
        return min(1.0, max(0.0, hex_voltage))

class TurbineControlUnit:
    """
    Master Orchestrator for the Square-Tooth Generator.
    Runs on the ATX-slotted Hex Board. Manages active clearance control,
    acoustic dampening verification, and Univac-IX telemetry serialization.
    """
    def __init__(self, fluid_type="hydro", location_id="STG-ALPHA"):
        print(f"[TCU INIT] Booting ATX Master Controller ({location_id})...")
        
        self.bus = ATXGuardRingBus()
        self.physics = HexNativeSquareToothEngine(fluid_type=fluid_type)
        
        # Calculate optimal configuration dynamically
        self.z_teeth, self.max_hz = self.physics.calculate_hex_tooth_matrix()
        self.target_gap, _ = self.physics.calculate_active_clearance_gap(rotor_diameter_mm=500.0)
        
        self.telemetry = HexTelemetryBridge(z_teeth=self.z_teeth)
        self.univac = UnivacIXSerializer(location_id=location_id)
        
        self.current_gap_mm = self.target_gap

    def execute_control_cycle(self, raw_rpm_sensor_v, raw_gap_sensor_v, temp_c):
        """
        The continuous operational loop (100Hz to 1000Hz depending on CPU).
        """
        # 1. Scrub inputs through the ATX Guard Ring
        clean_rpm_v = self.bus.scrub_sensor_input(raw_rpm_sensor_v)
        clean_gap_v = self.bus.scrub_sensor_input(raw_gap_sensor_v)
        
        # Map voltage back to physical values (Assuming 1V = 3000 RPM, 1V = 10mm gap)
        actual_rpm = clean_rpm_v * 3000.0
        self.current_gap_mm = clean_gap_v * 10.0
        
        # 2. Process Telemetry via Hexadecimal Bridge
        f_hex, hex_v, hex_char = self.telemetry.process_rotor_pulse(actual_rpm)
        
        # 3. Active Clearance Control (Gap Flaps)
        correction_voltage = self.telemetry.active_clearance_feedback(self.current_gap_mm, self.target_gap)
        applied_voltage = self.bus.write_actuator_voltage(correction_voltage)
        
        # Simulate physical gap correcting
        if applied_voltage > 0.5:
            print("[ACC ACTUATOR] Opening Gap Flaps (Relieving Cavitation Pressure)...")
            self.current_gap_mm += 0.05
        elif applied_voltage < 0.5:
            print("[ACC ACTUATOR] Closing Gap Flaps (Maximizing Torque Efficiency)...")
            self.current_gap_mm -= 0.05
            
        # 4. Serialize to Univac
        self.univac.serialize_telemetry(actual_rpm, f_hex, hex_v, hex_char, temp_c, self.current_gap_mm)
        
        return True

if __name__ == "__main__":
    tcu = TurbineControlUnit(fluid_type="hydro")
    
    # Simulate a noisy sensor read (0.5V = 1500 RPM), with 0.1V gap size
    simulated_raw_rpm = 0.52 # Includes 0.02V EMI noise
    simulated_raw_gap = 0.05 # Gap is starting too small (0.5mm)
    simulated_temp = 32.5
    
    # Run the cycle
    tcu.execute_control_cycle(simulated_raw_rpm, simulated_raw_gap, simulated_temp)
