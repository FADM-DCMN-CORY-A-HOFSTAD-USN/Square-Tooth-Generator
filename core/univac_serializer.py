import math

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
        """Slices a continuous 108-bit binary string into three distinct 36-bit UNIVAC words."""
        word1 = binary_108[0:36]
        word2 = binary_108[36:72]
        word3 = binary_108[72:108]
        return [word1, word2, word3]

    def serialize_metric(self, metric_value: float) -> dict:
        """Main pipeline call to serialize data into binary and hexadecimal words."""
        binary_str = self.pack_float_to_108bit(metric_value)
        words_bin = self.slice_to_three_words(binary_str)
        
        # Convert each 36-bit block to a clean 9-character hexadecimal string for your chips
        words_hex = [f"{int(w, 2):09X}" for w in words_bin]
        
        return {
            "value": metric_value,
            "complete_binary": binary_str,
            "univac_words_binary": words_bin,
            "univac_words_hexadecimal": words_hex
        }

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
