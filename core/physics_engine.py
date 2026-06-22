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

class HexNativeSquareToothEngine:
    """
    Unified Parametric Engine for the Square-Tooth Generator.
    Dynamically scales turbine geometry for Hydro, Wind, and Fuel environments.
    Outputs native parameters synchronized with the RT Hexadecimal 16-State Architecture.
    """
    
    def __init__(self, fluid_type="hydro", power_target_w=50000, target_rpm=1500, baseline_head_or_hz=10.0):
        self.fluid_type = fluid_type.lower()
        self.power_target_w = power_target_w
        self.rpm = target_rpm
        self.head_hz = baseline_head_or_hz
        
        # 1. Dynamic Density Selection (kg/m^3)
        if self.fluid_type == "hydro":
            self.rho = 1000.0
            self.shock_factor_b = 1.5
            self.shock_factor_t = 1.5
        elif self.fluid_type == "wind":
            self.rho = 1.225
            self.shock_factor_b = 2.0 # High centrifugal bending
            self.shock_factor_t = 1.2
        elif self.fluid_type in ["fuel", "combustion"]:
            self.rho = 0.001
            self.shock_factor_b = 1.1
            self.shock_factor_t = 2.5 # High torsional combustion pulses
        else:
            raise ValueError("Unknown fluid_type. Use 'hydro', 'wind', or 'fuel'.")

    def calculate_hex_tooth_matrix(self):
        """
        Forces the rotor geometry to adhere to the Hexadecimal Architecture.
        Maps the physical teeth directly to 16-state intervals.
        """
        # Slower RPMs require more teeth to maintain high-resolution telemetry
        if self.rpm < 500:
            z_teeth = 64
        elif self.rpm < 1500:
            z_teeth = 32
        else:
            z_teeth = 16
            
        hex_frequency_hz = (self.rpm * z_teeth) / 60.0
        return z_teeth, hex_frequency_hz

    def size_titanium_shaft(self, applied_torque_nm):
        """
        Calculates the exact Titanium Grade 5 shaft diameter required to prevent
        sagging and "shaft whip". 
        """
        tau_allow_titanium = 220e6 # 220 MPa safe shear limit for Ti-6Al-4V
        
        # Estimate bending moment based on environmental shock
        bending_moment = applied_torque_nm * 0.3 
        
        inside_sqrt = (self.shock_factor_b * bending_moment)**2 + (self.shock_factor_t * applied_torque_nm)**2
        shaft_diameter_m = ((16.0 / (math.pi * tau_allow_titanium)) * math.sqrt(inside_sqrt)) ** (1.0/3.0)
        
        return shaft_diameter_m * 1000.0 # Return in mm

    def calculate_acoustic_silencer_length(self, z_teeth, housing_thickness_mm, housing_diameter_mm):
        """
        Calculates the Quarter-Wave Acoustic dampening length to completely silence 
        the Blade Passing Frequency (BPF) inside the turbine.
        """
        # 1. Blade Passing Frequency (BPF)
        bpf_hz = (self.rpm * z_teeth) / 60.0
        
        # 2. Joukowsky Confined Wave Speed (Adjusted speed of sound in metal pipe)
        c_water_open = 1480.0 # m/s
        bulk_modulus_water = 2.2e9 # Pa
        elasticity_titanium = 114e9 # Pa
        
        # Joukowsky calculation
        stiffness_ratio = (bulk_modulus_water * (housing_diameter_mm / 1000.0)) / (elasticity_titanium * (housing_thickness_mm / 1000.0))
        c_confined = c_water_open / math.sqrt(1.0 + stiffness_ratio)
        
        # 3. Quarter-Wave Anti-Resonance Length
        silencer_length_m = c_confined / (4.0 * bpf_hz)
        return silencer_length_m * 1000.0 # Return in mm

    def calculate_active_clearance_gap(self, rotor_diameter_mm):
        """
        Calculates the baseline safe Tip-Gap to prevent cavitation screaming while
        maintaining power. Advises on the "Boeing" Serrated tip depth.
        """
        # Golden rule: Gap should be less than 0.1% of diameter for silent operation
        max_baseline_gap_mm = rotor_diameter_mm * 0.001
        
        # Serrated tip (Chevron) depth calculation
        chevron_depth_mm = max_baseline_gap_mm * 2.0
        
        return max_baseline_gap_mm, chevron_depth_mm

    def generate_system_blueprint(self):
        """Executes the full pipeline and returns the manufacturing specification."""
        print(f"--- GENERATING RT SQUARE-TOOTH BLUEPRINT ({self.fluid_type.upper()}) ---")
        
        # Approximated Torque (Power = Torque * Angular Velocity)
        angular_vel = (self.rpm * 2 * math.pi) / 60.0
        torque = self.power_target_w / angular_vel
        
        teeth, hex_hz = self.calculate_hex_tooth_matrix()
        shaft_mm = self.size_titanium_shaft(torque)
        
        # Assume a 500mm housing with 15mm thick Titanium walls
        silencer_mm = self.calculate_acoustic_silencer_length(teeth, 15.0, 500.0)
        gap_mm, chevron_mm = self.calculate_active_clearance_gap(500.0)
        
        blueprint = {
            "Hexadecimal Target Frequency (Hz)": round(hex_hz, 2),
            "Optimal Tooth Count": teeth,
            "Titanium Shaft Diameter (mm)": round(shaft_mm, 2),
            "Acoustic Housing Length (mm)": round(silencer_mm, 2),
            "Max Target Tip Gap (mm)": round(gap_mm, 3),
            "Passive Chevron Depth (mm)": round(chevron_mm, 3)
        }
        
        for key, value in blueprint.items():
            print(f"{key}: {value}")
            
        return blueprint

# Example Execution for a Municipal Hydro Deployment
if __name__ == "__main__":
    engine = HexNativeSquareToothEngine(fluid_type="hydro", power_target_w=150000, target_rpm=600)
    engine.generate_system_blueprint()
