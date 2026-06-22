#!/usr/bin/env python3
"""
Square-Tooth Generator Quality Gate.
Emergency Stress-Test Suite for 108-Bit Stacked Register Telemetry Pipelines.
Simulates disaster-scale physical inputs to assert zero overflow errors.
"""

import unittest
import math
from core.univac_serializer import UnivacStackedSerializer
from src.sys_storm import StormSafetyController

class TestStormEmergencyTelemetry(unittest.TestCase):
    def setUp(self):
        """Initializes high-precision serialization and safety systems before stress testing."""
        self.serializer = UnivacStackedSerializer()
        # Instantiate storm controller using our 65mm Grade 5 Titanium parameters
        self.safety_core = StormSafetyController(shaft_diameter_mm=65.0, shaft_length_m=1.5)

    def assert_numerical_stability(self, extreme_value: float, description: str):
        """
        Helper loop asserting that extreme values convert cleanly across the 
        108-bit multi-word architecture without bit-truncation or overflow errors.
        """
        # 1. Pack floating-point value to 108-bit hex representation
        packet = self.serializer.serialize_metric(extreme_value)
        hex_words = packet['univac_words_hexadecimal']
        
        # 2. Extract payload blocks back to floating point
        recovered_value = self.serializer.unpack_three_words_to_float(
            hex_words[0], hex_words[1], hex_words[2]
        )
        
        # 3. Assert zero structural bit drift down to tight floating-point tolerances
        self.assertAlmostEqual(
            extreme_value, 
            recovered_value, 
            places=12,
            msg=f"Disaster data drift detected during [{description}] stress test! "
                f"Sent: {extreme_value}, Recovered: {recovered_value}"
        )

    def test_hydro_flash_flood_surge(self):
        """Simulates extreme hydraulic pressure surges to verify water hammer data boundaries."""
        # Modeling a massive flash flood velocity spiking to 35.5 m/s in a long 500m conduit
        flood_velocity = 35.5
        conduit_len = 500.0
        
        # Run physical simulation to ensure numbers compile cleanly
        hydro_metrics = self.safety_core.evaluate_hydro_flood_safety(flood_velocity, conduit_len)
        self.assertEqual(hydro_metrics["tcu_storm_command"], "EMERGENCY_VENT_OPEN_GAP_FLAPS")
        
        # Assert that the resulting massive pressure spike (in PSI) preserves structural bit precision
        pressure_psi = hydro_metrics["pressure_spike_risk_psi"]
        self.assert_numerical_stability(pressure_psi, "HYDRO_FLASH_FLOOD_PRESSURE_PSI")

    def test_wind_hurricane_gale_force_thrust(self):
        """Simulates an ultra-high thrust spike from a Category 5 hurricane."""
        # Modeling a massive wind thrust vector spike hitting 85,000 Newtons against the blades
        wind_speed_gale = 45.0
        catastrophic_thrust = 85000.0
        
        wind_metrics = self.safety_core.evaluate_wind_gale_safety(wind_speed_gale, catastrophic_thrust)
        self.assertEqual(wind_metrics["tcu_storm_command"], "EXECUTE_FEATHERING_DECREASE_LIFT")
        
        # Verify that massive bending stress metrics do not saturate or overflow the register boundaries
        bending_stress_mpa = wind_metrics["calculated_bending_stress_mpa"]
        self.assert_numerical_stability(bending_stress_mpa, "WIND_HURRICANE_BENDING_STRESS_MPA")

    def test_combustion_runaway_kinetic_energy(self):
        """Simulates an engine overspeed explosion yielding extremely large kinetic numbers."""
        # Flywheel mass moment of inertia J (kg*m^2) and an extreme runaway speed of 8500 RPM
        inertia_j = 12.5
        runaway_rpm = 8500.0
        omega_runaway = runaway_rpm * (math.pi / 30.0)
        
        # Kinetic Energy: E = 0.5 * J * omega^2
        extreme_kinetic_joules = 0.5 * inertia_j * (omega_runaway ** 2)
        
        # Verify the stacked 108-bit register easily scales to massive energy numbers without clipping
        self.assert_numerical_stability(extreme_kinetic_joules, "FUEL_ENGINE_RUNAWAY_JOULES")

if __name__ == "__main__":
    unittest.main()
