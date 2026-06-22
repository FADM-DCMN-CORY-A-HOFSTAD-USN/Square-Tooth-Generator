import math

class SquareToothPhysics:
    def __init__(self, profile_data):
        self.rho = profile_data["fluid_density_rho"]
        self.kb = profile_data["bending_shock_kb"]
        self.kt = profile_data["torsional_shock_kt"]
        self.tau_allow = profile_data["allowable_shear_mpa"] * 1e6
        self.E_titanium = 114e9  # Grade 5 Titanium Modulus of Elasticity in Pascals

    def calculate_shaft_diameter(self, power_w, rpm, bending_moment=0.0):
        """Calculates the minimum safe Titanium shaft diameter based on torque shock."""
        omega = rpm * (math.pi / 30.0)
        torque = power_w / omega if omega > 0 else 0
        
        # Combined stress equation
        inside_sqrt = (self.kb * bending_moment)**2 + (self.kt * torque)**2
        diameter = ((16.0 / (math.pi * self.tau_allow)) * math.sqrt(inside_sqrt))**(1/3)
        return diameter

    def calculate_stiffness_diameter(self, force_n, span_m, target_deflection_mm=0.05):
        """Ensures the flexible titanium axle does not bend past tolerances."""
        target_m = target_deflection_mm / 1000.0
        numerator = 4.0 * force_n * (span_m**3)
        denominator = 3.0 * math.pi * self.E_titanium * target_m
        return (numerator / denominator)**(1/4)
