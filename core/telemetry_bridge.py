import math

class TelemetryBridge:
    @staticmethod
    def calculate_hex_tooth_matrix(rpm, target_hex_frequency=1600):
        """Forces the tooth count to always align with a clean 16-base cluster."""
        if rpm <= 0:
            return 16
        
        raw_teeth = (target_hex_frequency * 60) / rpm
        # Snap directly to the closest multiple of 16 for hexadecimal alignment
        synchronized_teeth = 16 * round(raw_teeth / 16)
        
        # Ensure we always have at least a baseline cluster
        return max(16, synchronized_teeth)

    @staticmethod
    def generate_hex_sync_frequency(rpm, teeth_count):
        """Outputs the real-time physical telemetry wave speed in Hz."""
        return (rpm * teeth_count) / 60.0

class HexTelemetryBridge:
    """
    Bridges the physical Square-Tooth Generator pulses to the 
    Revolutionary Technology 16-State Hexadecimal Logic.
    Copies core analog quantization logic from the Digital-Signals repository.
    """
    def __init__(self, z_teeth, max_rpm=3000):
        self.z_teeth = z_teeth
        self.max_rpm = max_rpm
        self.max_expected_hz = (self.max_rpm * self.z_teeth) / 60.0
        
        # The absolute 16-state hex grid (0.0V to 1.0V in 0.0625V intervals)
        self.hex_grid = [x * 0.0625 for x in range(16)]
        
    def process_rotor_pulse(self, current_rpm):
        """
        Ingests the physical RPM of the Titanium shaft and chops the magnetic
        flux cuts into a strict Hexadecimal frequency and logic state.
        """
        # 1. Physical Frequency Calculation (from physics_engine.py)
        # Equation: f_hex = (N * Z_teeth) / 60
        f_hex = (current_rpm * self.z_teeth) / 60.0
        
        # 2. Map the frequency to a continuous analog voltage (0.0V - 1.0V)
        normalized_signal = min(1.0, max(0.0, f_hex / self.max_expected_hz))
        
        # 3. Hardware Quantization: Snap to the nearest RT Hex state
        snapped_voltage = round(normalized_signal / 0.0625) * 0.0625
        
        # 4. Extract the Hex Character (0-F)
        hex_state = hex(int(snapped_voltage / 0.0625))[2:].upper()
        
        return f_hex, snapped_voltage, hex_state

    def active_clearance_feedback(self, current_gap_mm, target_gap_mm):
        """
        Outputs a correction voltage to the 'Gap Flaps' / Active Clearance Control.
        If the gap is too large (losing power) or too small (cavitation screaming),
        it outputs an analog shift to the actuators.
        """
        error_mm = current_gap_mm - target_gap_mm
        
        # Calculate a correction voltage centered at Hex 8 (0.5V)
        # > 0.5V tells actuators to open gap, < 0.5V tells actuators to close gap
        correction_v = 0.5 + (error_mm * 10.0) # Scaled multiplier for actuator sensitivity
        
        # Snap to Hex Logic
        snapped_correction = max(0.0, min(1.0, round(correction_v / 0.0625) * 0.0625))
        return snapped_correction
