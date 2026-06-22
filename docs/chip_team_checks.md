Square-Tooth Generator: Chip & Hardware Team TODOs
==================================================

**Status:** COMPLETED / INTEGRATED **Target Architecture:** Multi-Environment (Hydro, Wind, Combustion) **Material Baseline:** Titanium Grade 5 (Ti-6Al-4V)

[x] 1. Hexadecimal Digital Signal Integration (Cross-Repo Sync)
---------------------------------------------------------------

**Objective:** Replace standard analog frequency outputs with discrete pulses that natively map to the 16-state hexadecimal architecture from the `Digital-Signals-in-Hexadecimal-Code` repository.

-   **Resolution:** Implemented the **Synchronous Hex-Pulse Equation**. The tooth count ($Z_{teeth}$) is dynamically forced to multiples of 16 ($16, 32, 64$).

-   **Equation:** $f_{hex} = \frac{N \cdot Z_{teeth}}{60}$. This ensures the telemetry bridge can chop the physical frequency directly into 16-state logic intervals without floating-point software conversion.

[x] 2. Titanium Grade 5 Dynamic Shaft Sizing
--------------------------------------------

**Objective:** Calculate shaft thickness to prevent "whipping" and resonance, compensating for Titanium's lower modulus of elasticity compared to steel.

-   **Resolution:** Implemented the modified ASME Shaft Sizing Equation.

-   **Equation:** $d = \left[ \frac{16}{\pi \cdot \tau_{allow}} \sqrt{ (K_b M)^2 + (K_t T)^2 } \right]^{1/3}$

-   **Parameters Locked:** Allowable shear ($\tau_{allow}$) set to 220 MPa for Ti-6Al-4V. Shock factors ($K_b$, $K_t$) dynamically adjust based on fluid type (Hydro = 1.5, Wind = 1.2).

[x] 3. Water-Lubricated Bearing Configuration
---------------------------------------------

**Objective:** Replace AC Delco/GE metal ball bearings with a silent, fluid-wedge Tilting Pad system.

-   **Resolution:** Integrated the **Sommerfeld Number (S)** calculation. The Python engine now verifies the radial clearance ($c$) to ensure the shaft hydroplanes. Target $S$ is bound between $0.08$ and $1.0$.

[x] 4. Acoustic Resonator Tuning (The "Silent" Turbine)
-------------------------------------------------------

**Objective:** Mathematically match the physical length of the turbine to cancel out the Blade Passing Frequency (BPF).

-   **Resolution:** Implemented the Anti-Resonance Acoustic Silencer (Quarter-Wave) logic.

-   **Equations:** 1\. $f = \frac{N \cdot Z}{60}$ (Blade Passing Frequency) 2. $c = \frac{c_0}{\sqrt{1 + (K \cdot D) / (E \cdot t)}}$ (Joukowsky Confined Wave Speed) 3. $L = \frac{c}{4 \cdot f}$ (Target Turbine Length for 180° out-of-phase noise cancellation).

[x] 5. Active Clearance Control (ACC) / "Gap Flaps"
---------------------------------------------------

**Objective:** Provide a dynamic tip-gap tuning system to balance leakage (power loss) and cavitation (screaming noise).

-   **Resolution:** Implemented Active Gap Logic. The system monitors the Gap Cavitation Index ($\sigma_{gap}$). If noise exceeds threshold, the virtual "Rim Fin" increases the gap slightly. If efficiency drops, it closes the gap. For passive deployments, the engine recommends Boeing-style **Serrated Tips** with depth $h = 2\delta$.

*Note: All mathematical models have been translated into `core/physics_engine.py` for immediate deployment by the software team.*
