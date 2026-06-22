#!/usr/bin/env python3
"""
Square-Tooth Generator Infrastructure
Automated Storm Procedure & Kinetic Deflection Safety Module
"""

import math

class StormSafetyController:
    def __init__(self, shaft_diameter_mm=50.0, shaft_length_m=1.2):
        self.d = shaft_diameter_mm / 1000.0 # Convert to meters
        self.L = shaft_length_m
        self.E_titanium = 114e9               # Grade 5 Titanium Modulus (Pa)
        self.I = (math.pi * (self.d ** 4)) / 64.0
        
    def evaluate_hydro_flood_safety(self, current_velocity_m_s, conduit_length_m):
        """Calculates Joukowsky Water Hammer boundaries to protect against casing rupture."""
        c_speed_sound = 1200.0  # Confined speed of sound in housing
        rho_water = 1000.0
        
        # Calculate instant stoppage pressure spike risk
        potential_pressure_pascal = rho_water * c_speed_sound * current_velocity_m_s
        potential_psi = potential_pressure_pascal / 6894.76
        
        # Calculate minimum safe closing time of flaps to avoid physical rupture
        min_close_time_seconds = (2.0 * conduit_length_m) / c_speed_sound
        
        if current_velocity_m_s > 6.0: # Extreme flood threshold trigger
            action = "EMERGENCY_VENT_OPEN_GAP_FLAPS"
        else:
            action = "NORMAL_TCU_REGULATION"
            
        return {
            "pressure_spike_risk_psi": round(potential_psi, 2),
            "min_safe_actuation_time_sec": round(min_close_time_seconds, 4),
            "tcu_storm_command": action
        }

    def evaluate_wind_gale_safety(self, wind_speed_m_s, thrust_force_newtons):
        """Monitors wind loads to prevent bending stress fatigue from snapping the axle."""
        # Bending Moment M = Force * Length
        bending_moment = thrust_force_newtons * self.L
        radius = self.d / 2.0
        
        # Flexural Bending Stress Equation: Sigma = M * c / I
        bending_stress_pa = (bending_moment * radius) / self.I
        bending_stress_mpa = bending_stress_pa / 1e6
        
        # Titanium safety limit threshold check
        if bending_stress_mpa > 400.0 or wind_speed_m_s > 25.0:
            action = "EXECUTE_FEATHERING_DECREASE_LIFT"
        else:
            action = "NORMAL_TCU_REGULATION"
            
        return {
            "calculated_bending_stress_mpa": round(bending_stress_mpa, 2),
            "titanium_yield_margin_percent": round(((400.0 - bending_stress_mpa) / 400.0) * 100, 2),
            "tcu_storm_command": action
        }

if __name__ == "__main__":
    safety = StormSafetyController(shaft_diameter_mm=65.0, shaft_length_m=1.5)
    
    print("=== EMERGENCY SIMULATION: HYDRO FLASH FLOOD ===")
    hydro_status = safety.evaluate_hydro_flood_safety(current_velocity_m_s=8.5, conduit_length_m=150.0)
    print(f"  Pressure Spike Risk: {hydro_status['pressure_spike_risk_psi']} PSI")
    print(f"  Min Actuation Time:  {hydro_status['min_safe_actuation_time_sec']} seconds")
    print(f"  TCU Action Command:  {hydro_status['tcu_storm_command']}")
    
    print("\n=== EMERGENCY SIMULATION: WIND GALE FORCE HURRICANE ===")
    wind_status = safety.evaluate_wind_gale_safety(wind_speed_m_s=28.0, thrust_force_newtons=4500.0)
    print(f"  Axle Bending Stress: {wind_status['calculated_bending_stress_mpa']} MPa")
    print(f"  Titanium Stress Margin: {wind_status['titanium_yield_margin_percent']}%")
    print(f"  TCU Action Command:  {wind_status['tcu_storm_command']}")
