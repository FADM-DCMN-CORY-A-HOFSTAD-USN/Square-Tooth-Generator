import math

class UnivacIXSerializer:
    """
    Formats the Square-Tooth Generator telemetry for Univac-IX Mainframe ingestion.
    Outputs legacy 72-character wide Fieldata lines to bridge the advanced 
    Hexadecimal analog logic with legacy military monitoring systems.
    """
    def __init__(self, location_id="HYDRO-STATION-ALPHA"):
        self.location_id = location_id

    def serialize_telemetry(self, current_rpm, hex_hz, hex_voltage, hex_state, temp_c, gap_mm):
        """
        Prints the hardware state to standard output mimicking a Univac line-printer,
        and returns the data array for local storage.
        """
        print("\n************************************************************************")
        print("U N I V A C - I X   S Q U A R E - T O O T H   T E L E M E T R Y")
        print("************************************************************************")
        print(f"STATION ID:          {self.location_id}")
        print(f"ROTOR SPEED:         {current_rpm:.1f} RPM")
        print(f"HEX FREQUENCY:       {hex_hz:.2f} HZ")
        print(f"LOGIC OUTPUT:        HEX {hex_state} ({hex_voltage:.4f}V)")
        print(f"BEARING TEMP:        {temp_c:.1f}C")
        print(f"CAVITATION GAP:      {gap_mm:.3f} MM")
        print("STATUS:              SYNCED TO RT HEX MOTHERBOARD.")
        print("************************************************************************\n")
        
        # Return a Univac-compatible sequential data array
        return [hex_state, f"{hex_voltage:.4f}", f"{temp_c:.1f}", f"{gap_mm:.3f}"]

# ==========================================
# Integration Testing Example
# ==========================================
if __name__ == "__main__":
    from telemetry_bridge import HexTelemetryBridge
    
    # Initialize a 64-tooth generator (optimized for slow, high-torque hydro)
    bridge = HexTelemetryBridge(z_teeth=64, max_rpm=1500)
    serializer = UnivacIXSerializer(location_id="DAM-TURBINE-01")
    
    # Simulate the turbine spinning at 750 RPM
    simulated_rpm = 750.0
    f_hex, voltage, state = bridge.process_rotor_pulse(simulated_rpm)
    
    # Simulate ACC Gap tracking
    simulated_temp = 38.5
    simulated_gap = 0.52 # Slightly above the 0.50mm target
    
    # Push to Univac Console
    serializer.serialize_telemetry(simulated_rpm, f_hex, voltage, state, simulated_temp, simulated_gap)

class UnivacStackedSerializer:
    def __init__(self):
        # 108 bits total: 1 Sign, 17 Exponent, 90 Mantissa
        self.TOTAL_BITS = 108
        self.MANTISSA_BITS = 90
        self.EXPONENT_BITS = 17
        self.EXP_BIAS = 65536  # Excess-65536 bias for 17-bit signed exponent

    def pack_float_to_108bit(self, value: float) -> str:
        """Converts a Python float into a 108-bit binary string string."""
        if value == 0.0:
            return "0" * self.TOTAL_BITS
        
        # 1. Determine Sign bit
        sign_bit = "1" if value < 0 else "0"
        abs_value = abs(value)
        
        # 2. Extract fractional part and base-2 exponent
        mantissa_frac, exponent = math.frexp(abs_value)
        # frexp scales mantissa between [0.5, 1.0). Shift it to an integer across 90 bits.
        int_mantissa = int(mantissa_frac * (2 ** self.MANTISSA_BITS))
        
        # 3. Apply Bias to Exponent
        biased_exponent = exponent + self.EXP_BIAS
        
        # 4. Format into exact binary width allocations
        exp_binary = f"{biased_exponent:0{self.EXPONENT_BITS}b}"
        mantissa_binary = f"{int_mantissa:0{self.MANTISSA_BITS}b}"
        
        return sign_bit + exp_binary + mantissa_binary

    def slice_to_three_words(self, binary_108: str) -> list:
        """Slices a continuous 108-bit binary string into three 36-bit UNIVAC words."""
        return [binary_108[0:36], binary_108[36:72], binary_108[72:108]]

    def serialize_metric(self, metric_value: float) -> dict:
        """Main pipeline call to serialize data into binary and hexadecimal words."""
        binary_str = self.pack_float_to_108bit(metric_value)
        words_bin = self.slice_to_three_words(binary_str)
        words_hex = [f"{int(w, 2):09X}" for w in words_bin]
        return {
            "value": metric_value,
            "complete_binary": binary_str,
            "univac_words_binary": words_bin,
            "univac_words_hexadecimal": words_hex
        }

    # =========================================================================
    # ADDED UNPACKER / DESERIALIZER FUNCTION CODES
    # =========================================================================
    
    def unpack_three_words_to_float(self, hex_word1: str, hex_word2: str, hex_word3: str) -> float:
        """
        Reads three 36-bit hex strings, converts them back to a continuous binary string,
        and reconstructs the original high-precision physical measurement.
        """
        # 1. Convert 9-character Hex blocks back to 36-bit binary padded strings
        bin_word1 = f"{int(hex_word1, 16):036b}"
        bin_word2 = f"{int(hex_word2, 16):036b}"
        bin_word3 = f"{int(hex_word3, 16):036b}"
        
        # Reconstruct full 108-bit register
        full_binary = bin_word1 + bin_word2 + bin_word3
        
        # Check for zero value condition
        if int(full_binary, 2) == 0:
            return 0.0
            
        # 2. Extract specific segments using structural offsets
        sign_bit = int(full_binary[0])
        exponent_bits = full_binary[1:18]
        mantissa_bits = full_binary[18:108]
        
        # 3. Decode segments back to integers
        biased_exponent = int(exponent_bits, 2)
        int_mantissa = int(mantissa_bits, 2)
        
        # 4. Remove Exponent Bias and shift the fraction back to base [0.5, 1.0)
        unbiased_exponent = biased_exponent - self.EXP_BIAS
        mantissa_frac = int_mantissa / (2 ** self.MANTISSA_BITS)
        
        # 5. Compute original absolute value using inverse fractional scaling
        reconstructed_value = math.ldexp(mantissa_frac, unbiased_exponent)
        
        # Apply sign inversion if bit flag is active
        if sign_bit == 1:
            reconstructed_value = -reconstructed_value
            
        return reconstructed_value

# Example Testing Verification Loop
if __name__ == "__main__":
    serializer = UnivacStackedSerializer()
    
    # Testing a highly precise physical value (e.g., Titanium Deflection limit)
    sample_deflection = 0.049876543210987654321
    packet = serializer.serialize_metric(sample_deflection)
    
    print(f"Target Metric: {packet['value']}")
    print("\nStacked 3-Word Result (Hexadecimal Output for Registers):")
    for idx, hex_word in enumerate(packet['univac_words_hexadecimal'], start=1):
        print(f"  UNIVAC Word {idx}: 0x{hex_word}")

        # 1. Simulate an extremely precise sensor entry (e.g. Dynamic Gap Flap deflection in mm)
    original_measurement = 0.049876543210987654321
    print(f"[SENSOR INPUT]:   {original_measurement:.21f}")
    
    # 2. Pack data into telemetry hex package
    packed_packet = serializer.serialize_metric(original_measurement)
    h_words = packed_packet['univac_words_hexadecimal']
    print(f"[HEX PIPELINE]:   Word1: 0x{h_words[0]} | Word2: 0x{h_words[1]} | Word3: 0x{h_words[2]}")
    
    # 3. Simulate hardware loop receiving hex payload and unpacking it
    recovered_measurement = serializer.unpack_three_words_to_float(h_words[0], h_words[1], h_words[2])
    print(f"[TUNING DECODER]: {recovered_measurement:.21f}")
    
    # 4. Validate absolute zero bit drift assertion
    assert math.isclose(original_measurement, recovered_measurement, rel_tol=1e-20)
    print("\n[STATUS]: Deserialization execution completed. Bit integrity preserved with zero drift.")
