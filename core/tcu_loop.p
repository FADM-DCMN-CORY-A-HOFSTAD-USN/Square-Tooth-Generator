import time
import math
from core.univac_serializer import UnivacStackedSerializer

class TurbineControlUnitLoop:
    def __init__(self, target_gap_mm=0.05, kp=12.5, ki=3.1, kd=0.5):
        """
        Initializes the dynamic Turbine Control Unit (TCU).
        
        :param target_gap_mm: Optimized blade tip clearance zone (Typically 0.05mm)
        :param kp: Proportional gain (Immediate error response)
        :param ki: Integral gain (Eliminates steady-state structural drift)
        :param kd: Derivative gain (Dampens transient fluid surges)
        """
        self.serializer = UnivacStackedSerializer()
        self.target_gap = target_gap_mm
        
        # PID Controller Parameters
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # State Tracking Registers
        self.integral_error = 0.0
        self.last_error = 0.0
        self.last_timestamp = None

    def process_telemetry_and_tune(self, word1_hex: str, word2_hex: str, word3_hex: str) -> dict:
        """
        Decodes incoming high-precision hexadecimal signals, evaluates current 
        vibrational gap deflection, and calculates the correction step for the gap flaps.
        """
        current_time = time.time()
        if self.last_timestamp is None:
            self.last_timestamp = current_time
            dt = 0.001  # Safe baseline default step delta
        else:
            dt = current_time - self.last_timestamp
            if dt <= 0:
                dt = 0.001
        
        self.last_timestamp = current_time

        # 1. Unpack the high-precision physical telemetry metric (current gap in mm)
        current_gap = self.serializer.unpack_three_words_to_float(word1_hex, word2_hex, word3_hex)
        
        # 2. Compute deviation from the optimal acoustic clearance zone
        error = current_gap - self.target_gap
        
        # 3. Process PID algorithm
        self.integral_error += error * dt
        derivative_error = (error - self.last_error) / dt
        self.last_error = error
        
        # Total actuation correction output
        flap_adjustment_signal = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        
        # 4. Define real-time tuning action vector
        if abs(error) < 0.0001:
            action = "STABLE_SWEET_SPOT_HOLD"
        elif error > 0:
            action = "ACTUATE_FLAPS_CLOSE_GAP"  # Mitigate fluid leakage efficiency losses
        else:
            action = "ACTUATE_FLAPS_OPEN_GAP"   # Mitigate extreme cavitation shear noise

        return {
            "decoded_gap_measurement_mm": round(current_gap, 9),
            "deviation_error_mm": round(error, 9),
            "flap_actuation_signal_ma": round(flap_adjustment_signal, 4),
            "tcu_command_vector": action
        }
