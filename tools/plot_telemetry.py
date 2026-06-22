#!/usr/bin/env python3
"""
Square-Tooth Generator Architecture Pipeline.
Automated Telemetry Dashboard & Storm Response Performance Data Visualization.
"""

import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np

class TelemetryDashboardGenerator:
    def __init__(self, output_dir="outputs/manufacturing"):
        self.output_dir = output_dir
        
        # Adjust path dynamically if executed from inside subfolders
        if not os.path.exists(self.output_dir) and os.path.exists(os.path.join("..", self.output_dir)):
            self.output_dir = os.path.join("..", self.output_dir)
            
        os.makedirs(self.output_dir, exist_ok=True)
        self.STEPS = 16
        self.VOLTAGE_STEP = 1.0 / (self.STEPS - 1)

    def generate_dashboard_plots(self):
        """Generates a multi-panel visual engineering dashboard chart."""
        print("=== Generating Automated Visual Telemetry Dashboard ===")
        
        # Create a 2x2 grid layout for multi-variable analysis
        fig, axs = plt.subplots(2, 2, figsize=(14, 9))
        fig.suptitle('Square-Tooth Generator Master Telemetry Dashboard\n[RT-16-State Logic & Structural Storm Responses]', 
                     fontsize=14, fontweight='bold', color='#1a1a1a')

        # -------------------------------------------------------------------------
        # PLOT 1: 16-State Stepped Voltage Logic [0.0V - 1.0V]
        # -------------------------------------------------------------------------
        states = [f"{i:X}" for i in range(self.STEPS)]
        voltages = [i * self.VOLTAGE_STEP for i in range(self.STEPS)]
        
        axs[0, 0].step(range(self.STEPS), voltages, where='mid', color='#1f77b4', linewidth=2.5, marker='o')
        axs[0, 0].set_xticks(range(self.STEPS))
        axs[0, 0].set_xticklabels(states, fontweight='bold')
        axs[0, 0].set_title('16-State Voltage Logic Steps (66.66mV Intervals)', fontsize=11, fontweight='bold')
        axs[0, 0].set_xlabel('Hexadecimal Telemetry Token')
        axs[0, 0].set_ylabel('Trace Line Potential (Volts)')
        axs[0, 0].grid(True, linestyle=':', alpha=0.6)
        axs[0, 0].set_ylim(-0.05, 1.05)

        # -------------------------------------------------------------------------
        # PLOT 2: Anti-Crosstalk Guard Ring Attenuation Envelope
        # -------------------------------------------------------------------------
        frequency_hz = np.logspace(1, 6, 100) # From 10Hz to 1MHz
        # Modeling trace noise isolation with a standard -45dB baseline drop-off
        crosstalk_db_unshielded = -10 + 15 * np.log10(frequency_hz / 1000)
        crosstalk_db_shielded = crosstalk_db_unshielded - 45.0  # Appling the RT Guard Ring suppression
        
        axs[0, 1].plot(frequency_hz, crosstalk_db_unshielded, 'r--', label='Unshielded Lane', linewidth=1.5)
        axs[0, 1].plot(frequency_hz, crosstalk_db_shielded, 'g-', label='0.5mm Guard Ring Shielded Lane', linewidth=2)
        axs[0, 1].set_xscale('log')
        axs[0, 1].set_title('Crosstalk Noise Suppression Attenuation Profile', fontsize=11, fontweight='bold')
        axs[0, 1].set_xlabel('Interference Frequency Harmonic (Hz)')
        axs[0, 1].set_ylabel('Crosstalk Isolation Energy (dB)')
        axs[0, 1].axhline(y=-45.0, color='blue', linestyle=':', label='Strict RT-16 Compliance Ceiling')
        axs[0, 1].grid(True, which="both", linestyle=':', alpha=0.5)
        axs[0, 1].legend(loc='lower left', fontsize=9)

        # -------------------------------------------------------------------------
        # PLOT 3: Real-Time PID Gap Flap Response Curve
        # -------------------------------------------------------------------------
        time_axis = np.linspace(0, 5, 200)
        # Modeling transient flood surge input and stabilizing response
        simulated_deflection = 0.05 + 0.04 * np.exp(-1.5 * time_axis) * np.sin(2 * np.pi * time_axis)
        target_clearance = np.full_like(time_axis, 0.05)
        
        axs[1, 0].plot(time_axis, simulated_deflection, color='#ff7f0e', linewidth=2, label='Current Vibrational Gap')
        axs[1, 0].plot(time_axis, target_clearance, 'r:', linewidth=1.5, label='Acoustic Sweet Spot Target (0.05mm)')
        axs[1, 0].set_title('Real-Time PID Gap Flap Actuation Response', fontsize=11, fontweight='bold')
        axs[1, 0].set_xlabel('Simulation Operational Window (Seconds)')
        axs[1, 0].set_ylabel('Blade Tip Clearance Deflection (mm)')
        axs[1, 0].grid(True, linestyle=':', alpha=0.6)
        axs[1, 0].legend(loc='upper right', fontsize=9)

        # -------------------------------------------------------------------------
        # PLOT 4: Structural Storm Bending Stresses (Titanium Limits)
        # -------------------------------------------------------------------------
        wind_gust_speeds = np.linspace(10, 45, 50)
        # Bending stress scales non-linearly with thrust forces square profile
        calculated_stress_mpa = 25 + 0.22 * (wind_gust_speeds ** 2)
        
        axs[1, 1].plot(wind_gust_speeds, calculated_stress_mpa, color='#9467bd', linewidth=2.5, label='Axle Load')
        axs[1, 1].axhline(y=400.0, color='red', linestyle='--', linewidth=2, label='Titanium Fatigue Yield Threshold')
        axs[1, 1].axvline(x=25.0, color='darkorange', linestyle=':', label='Storm Cut-Out Trigger (Feathering Mode)')
        axs[1, 1].set_title('Titanium Grade 5 Axle Storm Bending Stress Limit', fontsize=11, fontweight='bold')
        axs[1, 1].set_xlabel('Wind Velocity Speed Profiles (m/s)')
        axs[1, 1].set_ylabel('Flexural Structural Stress (MPa)')
        axs[1, 1].grid(True, linestyle=':', alpha=0.6)
        axs[1, 1].legend(loc='upper left', fontsize=9)

        # Apply structural spacing formatting layout properties
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Save output graphic layout asset directly to manufacturing tree
        target_chart_path = os.path.join(self.output_dir, "telemetry_dashboard.png")
        plt.savefig(target_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  -> [SUCCESS]: Telemetry dashboard chart successfully exported to: {target_chart_path}")

if __name__ == "__main__":
    try:
        dashboard = TelemetryDashboardGenerator()
        dashboard.generate_dashboard_plots()
        sys.exit(0)
    except Exception as err:
        print(f"[ERROR]: Graphical telemetry rendering aborted: {err}")
        sys.exit(1)
