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
