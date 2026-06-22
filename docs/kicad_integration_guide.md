# Local KiCad 8.0+ Integration & Automation Setup Guide

This guide details how to link your local KiCad installation straight into the `Square-Tooth-Generator` repository pipeline. By configuring this local environment, you can run `src/build_hex_board.py` to automatically update board dimensions, footprints, and 16-state guard rings without manual clicking.

---

## Step 1: Environment Verification

Our automation script requires **KiCad 8.0 or newer**, as it relies on the modernized, thread-safe `pcbnew` Python 3 API.

### For Windows Engineers:
Windows isolates its KiCad Python environment from the system shell. Do **NOT** use your standard command prompt.
1. Open the **Windows Start Menu**.
2. Search for and launch the **KiCad Command Prompt** (this explicitly initializes KiCad's internal `python.exe` with bundled pathing variables).

### For macOS Engineers:
KiCad's Python binary is embedded inside the application bundle. Verify access by opening your terminal and executing:
```bash
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 -c "import pcbnew; print('KiCad API Linked Successfully')"
```

### For Linux Engineers:
Ensure your system python has access to the KiCad libraries (usually bundled via standard package managers):
```bash
python3 -c "import pcbnew; print('KiCad API Linked Successfully')"
```

---

## Step 2: Repository Binding & Local Execution

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com
   cd Square-Tooth-Generator
   ```

2. To generate or dynamically revise a layout matching your active turbine model parameters, execute the compilation matrix script.

   * **Windows (Inside KiCad Prompt):**
     ```cmd
     python src/build_hex_board.py
     ```
   * **macOS (Terminal):**
     ```bash
     /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 src/build_hex_board.py
     ```
   * **Linux (Terminal):**
     ```bash
     python3 src/build_hex_board.py
     ```

The console will output verification bounds, placing a freshly compiled file at `outputs/hex_telemetry_atx.kicad_pcb`.

---

## Step 3: Viewing and Verifying Local Revisions

1. Launch the main **KiCad 8.0** GUI desktop application.
2. Select **File > Open Project** and navigate to your local `Square-Tooth-Generator` folder.
3. Open the **PCB Editor** tool.
4. Open the file generated at `outputs/hex_telemetry_atx.kicad_pcb`.
5. Run an **Electrical Rules Check (ERC)** and a **Design Rules Check (DRC)**. The script automatically isolates trace nets, meaning your 16-state logic lines will read as fully shielded by the parallel `GND` guard rings with **zero clearance or crosstalk violations**.

---

## Step 4: Connecting the Local Loop to Git Actions

To ensure that your local KiCad files stay synchronized with the remote pipeline every time you push board modifications:

1. Stage both the script and the output footprint layouts:
   ```bash
   git add src/build_hex_board.py outputs/hex_telemetry_atx.kicad_pcb
   ```
2. Commit the physical updates:
   ```bash
   git commit -m "hw: revised telemetry track dimensions to optimize guard ring pathing"
   ```
3. Push to your active feature branch:
   ```bash
   git push origin feature/your-branch-name
   ```

The automated GitHub Action `.github/workflows/docker-build.yml` will catch the change, run your unit precision tests, check for link dependencies inside Docker, and verify hardware safety bounds before certifying the layout build.
