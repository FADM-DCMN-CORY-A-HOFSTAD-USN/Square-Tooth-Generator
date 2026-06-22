# Square-Tooth Generator Infrastructure: Command Instruction Document
**System Class:** Developer CLI Reference & Lifecycle Command Index  
**Automation Scope:** Multi-Language Compilers, CAD Renderers, and Testing Environments  
**Target Shells:** Bash, Zsh, and KiCad Python Console  

---

## 1. Project Initialization & Environment Provisioning

Before executing any physical math simulations, your developer workstation workspace must be provisioned with localized environment routing variables and directory trees.

```bash
# Grant execution permissions to the automated interactive repository initializer
chmod +x setup.sh

# Run the project workspace initialization script to check tools and generate file geometries
./setup.sh

# Source the newly generated project profile variables into your active shell runner session
source .env
```

*   **Variables Configured Globally:** `$PROJECT_ROOT_PATH`, `$PYTHONPATH`, `$FIRMWARE_OUTPUT_PATH`, and `$KICAD_FABRICATION_DIRECTORY`.

---

## 2. Integrated Software Simulation & Hardware Orchestration

Instead of manually invoking Python modules, C compilers, and layout exporters sequentially, run the master end-to-end hardware validation timeline with a single shell command.

```bash
# Grant execution permissions to the master hardware orchestration system
chmod +x tools/simulate_system.sh

# Execute the entire four-stage design-to-factory verification loop
./tools/simulate_system.sh
```

### What This Command Executes Under the Hood:
1.  **Stage 1:** Fires up 108-bit multi-word tracking register simulations and loops the TCU PID algorithm.
2.  **Stage 2:** Validates the discrete 66.66mV logic voltage channels against line attenuation equations.
3.  **Stage 3:** Invokes `gcc` with maximum optimizations (`-O3`) to build the C driver.
4.  **Stage 4:** Generates the programmatic KiCad ATX PCB board bounds and prints an inventory of exported Gerber layers.

---

## 3. High-Precision Mathematical Unit Testing

To ensure that changes to the generator parameters do not cause truncation drift or bit rounding errors across different turbine scales, run the standard Python regression test suite.

```bash
# Run all unit tests within the /tests directory using native python discovery
python3 -m unittest discover -s tests

# Run the 108-bit stacked register precision validation test module explicitly
python3 -m unittest tests/test_pipeline.py
```

---

## 4. Firmware Driver Compilation & Static Linking (`src/Makefile`)

The lower-level embedded firmware stack utilizes a deterministic GNU Make pipeline to isolate your code modifications. Navigate into the `/src` folder before executing these recipes.

```bash
# Change directory into the firmware compilation workspace
cd src

# Compile the standalone C testing executable (mcp4725_driver) and the static library (libmcp4725.a)
make

# Master Command: Recompile firmware, draw the PCB board, and bundle manufacturing-ready Gerbers
make fab

# Purge localized intermediate object files (.o), binaries, and older Gerber folder trees
make clean
```

---

## 5. Programmatic PCB Design & Gerber Manufacturing Export

If your layout engineers are modifying layout paths, board dimensions, or guard ring clearances, they can run the KiCad Python automation scripts directly from their terminal environments.

```bash
# Formally build the ATX Motherboard shape, place standoffs, and inject the bilateral 0.5mm guard rings
python3 src/build_hex_board.py

# Extract all layer traces to industrial Gerber files (RS-274X) and compute CNC drill tracking maps
python3 src/generate_gerbers.py

# Onboarding Gate: Verify a third-party vendor board submission contains the mandatory guard ring envelopes
python3 tools/verify_interfacing_netlist.py path/to/submitted_board.kicad_pcb
```

---

## 6. Deterministic Multi-Stage Docker Toolchain

To ensure every member of your team compiles identical binary firmware blocks with zero environment or dependency drift, compile via isolated Docker containers.

```bash
# Build the multi-stage compilation image container matrix and verify compiler warnings
docker build -t square_tooth_firmware:latest .

# Run the compiled executable target inside the secure, isolated container runtime
docker run --rm square_tooth_firmware:latest

# Extract the freshly compiled production static library (.a) to your host local folder
docker create --name extract_temp square_tooth_firmware:latest
docker cp extract_temp:/firmware/libmcp4725.a ./outputs/libmcp4725.a
docker rm extract_temp
```

---

## 7. Automated Production Release Packaging

Once your simulation runs pass and the code is certified for physical manufacturing, package all deployment dependencies into a semantic version-stamped hardware distribution archive.

```bash
# Grant execution permissions to the automated deployment assembly packager
chmod +x tools/package_release.sh

# Bundle certified Gerbers, drill maps, static .a libraries, headers, and docs under version v1.0.0
./tools/package_release.sh v1.0.0
```

*   **Output Destination:** Creates a timestamped tarball inside `outputs/distribution/` containing an integrated `manifest.json` file for the factory intake system.
