# 108-Bit Stacked Telemetry & ATX Hardware System Interface Specification
**Document Class:** System Integration Blueprint  
**System Architecture:** Revolutionary Technology (RT) 16-State Modular Architecture

---

## 1. System Overview & The ATX Structural Repair Philosophy

To minimize lifecycle downtime in commercial, micro-grid, and defense generation environments, the **Square-Tooth Generator Infrastructure** rejects proprietary hardware footprints. Instead, it utilizes standard **ATX Form Factor Specifications** for all electronics housing spaces.

### The Repair & Rebuilding Advantage:
* **Standardized Standoffs:** The generator enclosure features pre-tapped holes matching the standard 9-pin ATX motherboard grid. Any custom PCB or off-the-shelf control board matching the ATX standard can be bolted directly into the machine without drilling or bracket modifications.
* **Modular Payload Bays:** 
  * Larger processing units and power electronic inversion modules are mapped to standard **5.25" CD-ROM bay footprints**.
  * Dynamic tuning logic modules and high-speed telemetry chips match the standard **2.5" SSD and M.2 NVMe (2280) mechanical profiles**.
* **Rapid Field Swap-Outs:** If a controller chip burns out or is damaged by a fluid surge, field technicians do not need to replace the entire generator casing. They can slide out the damaged module, unseat standard PCIe or I2C bus connectors, and click a replacement module straight into the ATX bay.

---

## 2. Telemetry Architecture: The 108-Bit Stacked Word

To achieve zero rounding drift when tracking micro-vibrations, dynamic blade deflections, and high-frequency fluid pulses, the system stacks **three 36-bit UNIVAC legacy words** into a single continuous **108-bit multi-word register**.

### 108-Bit Float Bitwise Allocation Map:
```text
 MSB                                                                                  LSB

  |                                                                                    |
 [0] [1-----------------17] [18------------------------------------------------------107]

  |            |                                        |
 Sign      Biased Exponent                           Mantissa
(1 bit)       (17 bits)                             (90 bits)
```

### Word Field Breakdown:
1. **Word 1 (Bits 0–35):** `[Sign Flag (1 bit)]` + `[Biased Exponent (17 bits)]` + `[Upper Mantissa Bits 0–17 (18 bits)]`
2. **Word 2 (Bits 36–71):** `[Mid Mantissa Bits 18–53 (36 bits)]`
3. **Word 3 (Bits 72–107):** `[Lower Mantissa Bits 54–89 (36 bits)]`

*   **Exponent Bias:** Excess-65536 (\(2^{16}\)) structure mapped over 17 bits to support extreme macro/micro scale scaling bounds.
*   **Mantissa Resolution:** 90 bits of fractional payload depth provides up to **27 decimal places of fixed accuracy**.

---

## 3. Physical Mapping: 16-State [0.0V - 1.0V] Logic Transmission

The 108-bit register payload is serialized into sequential streams of base-16 hexadecimal characters (`0` through `F`). Outside engineering teams interfacing with our bus pins must calibrate their hardware to recognize non-standard **Discrete Voltage Logic Steps**.

### Physical Voltage Calibration Matrix:
The strict operational voltage window spans from **0.0V (Baseline Ground)** to **1.0V (V-Ceiling Max)**. Each hexadecimal state step translates exactly to an incremental change of **66.666667 mV**.

| Hex Token | State Index | Target Line Voltage (V) | Step Increment Delta |
| :---: | :---: | :---: | :--- |
| `0` | 0 | 0.000000 V | Baseline Ground Reference |
| `1` | 1 | 0.066667 V | \(+\Delta V\) |
| `2` | 2 | 0.133333 V | \(+2\Delta V\) |
| `3` | 3 | 0.200000 V | \(+3\Delta V\) |
| `4` | 4 | 0.266667 V | \(+4\Delta V\) |
| `5` | 5 | 0.333333 V | \(+5\Delta V\) |
| `6` | 6 | 0.400000 V | \(+6\Delta V\) |
| `7` | 7 | 0.466667 V | \(+7\Delta V\) |
| `8` | 8 | 0.533333 V | \(+8\Delta V\) |
| `9` | 9 | 0.600000 V | \(+9\Delta V\) |
| `A` | 10 | 0.666667 V | \(+10\Delta V\) |
| `B` | 11 | 0.733333 V | \(+11\Delta V\) |
| `C` | 12 | 0.800000 V | \(+12\Delta V\) |
| `D` | 13 | 0.866667 V | \(+13\Delta V\) |
| `E` | 14 | 0.933333 V | \(+14\Delta V\) |
| `F` | 15 | 1.000000 V | Max Ceiling Limit |

---

## 4. Signal Protection Protocol: Anti-Crosstalk Guard Rings

Because the margin between logic states is tightly spaced at **66.66mV**, the signal traces are susceptible to electromagnetic crosstalk. Third-party interfacing PCBs must comply with **RT Fabrication Design Rule #2**:

1. **Symmetric Isolation Routing:** Every high-speed logic line must be flanked symmetrically on both sides by a parallel **0.4mm grounded copper shield trace (Guard Ring)**.
2. **Clearance Envelope:** The distance between the core data signal line edge and the internal shield guard ring edge must be set to exactly **0.5mm**.
3. **Trace Impedance Limits:** Interfacing cards must utilize **2oz or 3oz thick outer layer copper** structures. This guarantees trace line resistance stays \(<0.05\,\Omega\), absorbing capacitive coupling hum and dropping line crosstalk attenuation below **-45 dB**.

---

## 5. Hardware Interface Register Logic Flow

When capturing sensor parameters (e.g., dynamic tip clearance or turbine axle strain), data travels across the modular stack via the following software-to-hardware pipeline:

```text
[Sensor Readout] -> [Calculated Float Value]
                         |
                         v
             [UnivacStackedSerializer] -> Packs value into 108-bit Register
                         |
                         v
             Slices payload into 3 words -> Generates Hex Strings (e.g., "A5F...")
                         |
                         v
             [dac_mcp4725.c Firmware] -> Formats to 12-bit Fast-Write I2C bytes
                         |
                         v
             [Physical MCP4725 Chip] -> Outputs precise 66.66mV stepped voltages
                         |
                         v
             [Shielded Guard Rings] -> Transmits safely down ATX backplane traces
```
