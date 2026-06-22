import unittest
import math
from core.univac_serializer import UnivacStackedSerializer

class TestUnivacSignalPipeline(unittest.TestCase):
    def setUp(self):
        """Initializes the 108-bit stacked serializer engine before each test."""
        self.serializer = UnivacStackedSerializer()

    def assert_round_trip_integrity(self, original_value: float, decimal_precision_places: int = 15):
        """
        Helper method to run a value through the entire serialization 
        and deserialization pipeline to verify zero data corruption.
        """
        # 1. Pack floating-point value to 108-bit hex representation
        packet = self.serializer.serialize_metric(original_value)
        hex_words = packet['univac_words_hexadecimal']
        
        # 2. Unpack the three 36-bit hex blocks back to floating point
        recovered_value = self.serializer.unpack_three_words_to_float(
            hex_words[0], hex_words[1], hex_words[2]
        )
        
        # 3. Assert exact match within floating-point tolerances
        self.assertAlmostEqual(
            original_value, 
            recovered_value, 
            places=decimal_precision_places,
            msg=f"Precision drop detected! Sent: {original_value}, Got: {recovered_value}"
        )

    def test_sub_atomic_vibrational_noise(self):
        """Verifies precision integrity for nanoscale/sub-atomic shaft micro-vibrations."""
        # e.g., 0.0000000000123456789 mm of mechanical flutter
        micro_vibration = 1.2345678912345e-11
        # Expecting high decimal precision retention at sub-atomic scale
        self.assert_round_trip_integrity(micro_vibration, decimal_precision_places=24)

    def test_municipal_scale_power_surges(self):
        """Verifies accuracy when tracking massive municipal grid-scale gigawatt power values."""
        # e.g., 1,500,250,750.123456789 Watts of power throughput
        municipal_power = 1500250750.123456789
        self.assert_round_trip_integrity(municipal_power, decimal_precision_places=7)

    def test_absolute_zero_edge_case(self):
        """Ensures the serialization pipeline handles stagnant/stopped states cleanly without zero divisions."""
        self.assert_round_trip_integrity(0.0, decimal_precision_places=15)

    def test_negative_values_flow_reversal(self):
        """Tests sign bit operation when tracking negative values (e.g., fluid counter-flow or dynamic drag)."""
        negative_torque = -8742.987654321098
        self.assert_round_trip_integrity(negative_torque, decimal_precision_places=12)

if __name__ == "__main__":
    unittest.main()
