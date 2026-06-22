#!/usr/bin/env python3
"""
Square-Tooth Generator Architecture Matrix
16-State Hexadecimal Stepped Voltage Logic Controller [0.0V - 1.0V]
"""

import sys

class HexVoltageController:
    def __init__(self, trace_resistance_ohms=0.04, guard_shield_attenuation_db=-45.0):
        """
        Initializes the physical logic voltage step controller.
        
        :param trace_resistance_ohms: Physical impedance of the 2oz copper trace
        :param guard_shield_attenuation_db: Simulated noise isolation from guard ring
        """
        self.MIN_VOLTAGE = 0.0
        self.MAX_VOLTAGE = 1.0
        self.STATES = 16
        
        # Calculate precise stepping delta (15 intervals between 16 discrete states)
        self.VOLTAGE_STEP = (self.MAX_VOLTAGE - self.MIN_VOLTAGE) / (self.STATES - 1)
        
        # Line Characteristics
        self.trace_resistance = trace_resistance_ohms
        self.noise_attenuation = guard_shield_attenuation_db

        # Map Hex characters natively to their respective stepped voltage indices
        self.HEX_MAP = {f"{i:X}": i for i in range(16)}
        self.REVERSE_HEX_MAP = {i: f"{i:X}" for i in range(16)}

    def hex_char_to_voltage(self, hex_char: str) -> float:
        """Translates a single Hex state into its exact physical target voltage."""
        char_upper = hex_char.upper()
        if char_upper not in self.HEX_MAP:
            raise ValueError(f"Invalid 16-state token: '{hex_char}'. Must be 0-F.")
            
        state_index = self.HEX_MAP[char_upper]
        return state_index * self.VOLTAGE_STEP

    def voltage_to_hex_char(self, target_voltage: float) -> str:
        """
        Performs the physical analog-to-digital conversion (ADC) operation.
        Snaps an incoming line voltage back to the nearest discrete 16-state step.
        """
        # Clamp voltage to safe structural window
        clamped_v = max(self.MIN_VOLTAGE, min(self.MAX_VOLTAGE, target_voltage))
        
        # Find closest integer state step index
        state_index = round(clamped_v / self.VOLTAGE_STEP)
        return self.REVERSE_HEX_MAP[state_index]

    def simulate_transmission_lane(self, hex_string: str, load_current_ma=12.0) -> dict:
        """
        Simulates parsing a full telemetry stream down the shielded guard lanes.
        Accounts for real-world voltage drops (V = I * R) across the trace.
        """
        voltage_waveform = []
        received_hex_array = []
        voltage_drop = (load_current_ma / 1000.0) * self.trace_resistance
        
        for char in hex_string:
            # 1. DAC: Generate initial source voltage
            v_source = self.hex_char_to_voltage(char)
            
            # 2. Channel: Apply drop over the trace length
            v_received = v_source - voltage_drop if v_source > 0 else 0.0
            voltage_waveform.append(round(v_received, 6))
            
            # 3. ADC: Recover token at destination chip pin
            recovered_char = self.voltage_to_hex_char(v_received)
            received_hex_array.append(recovered_char)

        received_string = "".join(received_hex_array)
        success = (hex_string == received_string)
        
        return {
            "source_stream": hex_string,
            "transmitted_voltages_v": voltage_waveform,
            "destination_stream": received_string,
            "transmission_successful": success,
            "voltage_drop_detected_v": round(voltage_drop, 6)
        }

if __name__ == "__main__":
    controller = HexVoltageController()
    
    print("=== 16-State Voltage Calibration Reference Table ===")
    for token in range(16):
        char = f"{token:X}"
        volts = controller.hex_char_to_voltage(char)
        print(f"  Token [0x{char}] -> Target Level: {volts:.6f} V")

    # Simulate sending a 9-character hex telemetry packet from the 108-bit stacked register
    sample_packet = "A5F0C3B9E"
    print(f"\n[PIPELINE INJECTION]: Sending Stream: '{sample_packet}'")
    
    results = controller.simulate_transmission_lane(sample_packet)
    print(f"[LINE VOLTAGES]:      Waveform (V):   {results['transmitted_voltages_v']}")
    print(f"[HARDWARE DECODER]:   Received Stream: '{results['destination_stream']}'")
    print(f"[STATUS]:             Signal Validated: {results['transmission_successful']}")
