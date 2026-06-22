# Square-Tooth Generator Infrastructure: Hardware Deployment Manual
**System Class:** Field Engineering Installation & Servicing Guide  
**Target Audience:** Field Deployment Engineers, Electrical Technicians, Mechanical Assemblers  
**Hardware Profile:** Standard ATX System Architecture (RT-16-State Logic)

---

## 1. Safety Enforcements & Pre-Installation Audit

Before opening the generator chassis casing or handling any internal electronics module trays, technicians must stringently enforce the following safety rules:

*   **Fluid Isolation Rule:** Ensure all upstream fluid isolation valves (Hydro), brake locking systems (Wind), or fuel shutoff switches (Combustion Engine) are locked out and tagged out (**LOTO**). There must be zero kinetic input to the turbine axle.
*   **Residual Discharge Hold:** If the turbine was recently active, wait at least **5 minutes** after executing the `sys_shutdown` sequence. This allows the high-voltage inverter capacitors inside the 5.25" module bays to fully discharge.
*   **Static Dissipation Protocol:** Technicians must wear an ESD wrist strap bonded directly to the generator's unpainted cast-iron frame before handling any circuit cards inside the ATX electronics bay.

---

## 2. Mechanical Mounting: The ATX Module Matrix

The electronics enclosure utilizes standardized computing industry form-factors to enable rapid field swap-outs and screw matching.

```text
       [TOP EDGE OF ATX ENCLOSURE]
┌──────────────────────────────────────────────┐
│  (H1)         (H2)          (H3)             │  <- Standard ATX 9-Pin Screw Pattern
│   O            O             O               │     Pre-threaded for structural M3 standoffs
│                                              │
│  (H4)         (H5)          (H6)             │  <- Center row alignment pins
│   O            O             O               │
│                                              │
│  (H7)         (H8)          (H9)             │  <- Bottom edge boundary
│   O            O             O               │
└──────────────────────────────────────────────┘
```

### 2.1 Mounting the Main TCU Board (ATX Motherboard Profile)
1. Verify that **9 structural brass M3 standoffs** are securely screwed into the enclosure chassis grid matching locations `H1` through `H9`.
2. Align the custom KiCad-compiled ATX motherboard with the standoff grid. Ensure no loose wiring or metal debris is trapped underneath the PCB plane.
3. Secure the motherboard using standard **M3 pan-head structural screws**. Torque each screw evenly to **0.6 N·m**. Do not over-tighten, or you will stress and micro-crack the outer 2oz/3oz copper trace guard rings.

### 2.2 Sub-Module Insertion (Drive Trays)
*   **Data Logging & Core Sensor Hubs (2.5" SSD Profile):** Slide the ruggedized 2.5" sensor sub-module tray into the designated lower drive cage. Push until the spring-loaded locking clips click into place. Secure the side plate using two standard drive screws.
*   **High-Voltage Inverters & Actuator Controllers (5.25" CD-ROM Profile):** Guide the large inverter module module into the upper 5.25" slide rails. Slide it back until the front faceplate flushes with the chassis access bezel. Bolt the four structural shoulder screws into the side mounting brackets.

---

## 3. Electrical Wiring & Interface Bus Pinouts

The backplane distribution network decouples communications into high-speed data logic paths and isolated low-voltage DC power supply rails.

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      MAIN ATX PCB INTERFACE HEADER                     │
 │                                                                        │
 │   [5.0V VCC]  [GND SHIELD]  [CH0 DATA]  [GND SHIELD]  [CH1 REDUNDANT]   │
 │     PIN 1        PIN 2        PIN 3        PIN 4          PIN 5        │
 └────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Telemetry Link Pinout Map
All sensor connections coming from the physical square-tooth encoder wheel must wire directly to the primary 5-pin terminal interface block on the motherboard:

*   **Pin 1: 5.0V VCC Supply Rail** — Clean DC voltage out to power the active silicon nodes.
*   **Pin 2: Local GND Shield** — Terminates the left-side parallel anti-crosstalk copper guard ring.
*   **Pin 3: Channel 0 Data Line (_HEX_CH0)** — Carries the high-speed 0.0V–1.0V discrete logic steps.
*   **Pin 4: Local GND Shield** — Terminates the right-side parallel anti-crosstalk copper guard ring.
*   **Pin 5: Channel 1 Data Line (_HEX_CH1)** — Carries the secondary dual-redundant safety logic stream.

### 3.2 Actuator Wiring Harness
The physical gap-tuning flaps are driven by shielded ribbon cables connected to the 5.25" inverter module bay. Ensure the ribbon cable is routed away from the turbine shaft and secured with heavy-duty zip ties to prevent mechanical entanglement or rubbing caused by casing vibrations.

---

## 4. Hardware Verification & Boot Validation Sequence

Once mounting and physical wiring are completed, the field engineer must step through this structural validation sequence before leaving the site:

1.  **Impedance Audit:** Measure the electrical resistance between **Pin 3 (Data)** and **Pin 2 (GND)** using a calibrated digital multimeter. The resistance must read greater than **100 kΩ**. If it reads near 0 Ω, abort instantly; this flags a physical short circuit where an unshielded track is touching a guard ring.
2.  **Apply Master Logic Power:** Toggle the main ATX power supply breaker. Verify that the system diagnostic LED illuminates solid green, indicating stable **5.0V and 3.3V power rails**.
3.  **Execute Initialization Routine:** Connect a field maintenance laptop to the local serial debugging port and execute the startup script module:
    ```bash
    ./sys_init
    ```
4.  **Confirm Line Stabilization:** Verify the boot console traces print `[INIT STAGE 4]: Suppressing floating line noise to absolute 0.0V baseline ground...`. Use an oscilloscope at the test points to confirm that both telemetry tracks drop cleanly to **0.000000V** with zero voltage ripple, certifying the system is `RUNTIME_READY`.

---

## 5. Field Field Replacement & Rebuilding Matrix

If a hardware node fails or reports bit corruption due to environment fatigue out in the field, execute a rapid modular swap using this routine:

```text
 [EXECUTE HALT] -> Run ./sys_shutdown via the maintenance console terminal interface.
                         |
                         v
 [ISOLATE POWER] -> Throw the main ATX backplane structural circuit breaker.
                         |
                         v
 [UNPLUG SUB-TRAY] -> Unseat standard PCIe ribbon blocks or I2C bus connectors.
                         |
                         v
 [SWAP MODULE] -> Unscrew damaged card from standoffs; click replacement into place.
                         |
                         v
 [REBOOT SYSTEM] -> Throw breaker, run ./sys_init, and verify green TCU LED indicator.

## 6. Emergency Storm Operations & Emergency Overrides

When an extreme weather profile or generator overspeed alert trips the telemetry sensors, the system locks out standard power-generation modes and executes the following recovery steps:

1. **Hydro Flash Floods:** Do NOT close input isolation gates instantly. Ensure the TCU loops trigger `EMERGENCY_VENT_OPEN_GAP_FLAPS` to bypass water around the turbine blades. This vents kinetic pressure and prevents water hammer shockwaves from breaking the casing.
2. **High-Wind Gales:** If wind spends more than 3 seconds above 25 m/s, the controller forces pitch actuators to match the zero-lift feathering boundary. If the calculated axle bending stress spikes past 400 MPa, structural chassis bypass flaps must be manually or programmatically dropped to protect the titanium integrity.
3. **Engine Runaway:** If the square-tooth generator tracking frequency indicates an RPM surge above emergency tolerances, execution loops cut fuel line solenoids instantly and apply full reverse electromagnetic braking across the stator poles.

```
