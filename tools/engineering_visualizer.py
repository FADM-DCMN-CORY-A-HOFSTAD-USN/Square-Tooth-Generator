import sys
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, RadioButtons

# Ensure the core directory is accessible to import your actual engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
try:
    from physics_engine import HexNativeSquareToothEngine
except ImportError:
    print("Error: Could not import physics_engine.py. Ensure you are running this from the 'tools/' directory.")
    sys.exit(1)

# ==========================================
# 1. SETUP FIGURE & LAYOUT
# ==========================================
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.05, bottom=0.35, right=0.75) # Leave room for controls
fig.canvas.manager.set_window_title('Revolutionary Technology - Square-Tooth Scaler')

# ==========================================
# 2. UI CONTROLS (SLIDERS & BUTTONS)
# ==========================================
axcolor = 'lightgoldenrodyellow'

# Sliders
ax_dia = plt.axes([0.15, 0.20, 0.5, 0.03], facecolor=axcolor)
ax_rpm = plt.axes([0.15, 0.15, 0.5, 0.03], facecolor=axcolor)
ax_pow = plt.axes([0.15, 0.10, 0.5, 0.03], facecolor=axcolor)

s_dia = Slider(ax_dia, 'Rotor Dia (mm)', 100.0, 2000.0, valinit=500.0, valstep=10)
s_rpm = Slider(ax_rpm, 'Target RPM', 100.0, 3000.0, valinit=1000.0, valstep=50)
s_pow = Slider(ax_pow, 'Power (Watts)', 1000.0, 500000.0, valinit=50000.0, valstep=1000)

# Environment Radio Buttons
ax_fluid = plt.axes([0.8, 0.10, 0.15, 0.15], facecolor=axcolor)
radio_fluid = RadioButtons(ax_fluid, ('hydro', 'wind', 'fuel'), active=0)

# Telemetry Text Readout Box
text_ax = plt.axes([0.8, 0.35, 0.15, 0.5])
text_ax.axis('off')
info_text = text_ax.text(0, 1, "", fontsize=10, verticalalignment='top', family='monospace',
                         bbox=dict(boxstyle="round", facecolor="black", edgecolor="gold", alpha=0.8), color="white")

# ==========================================
# 3. MASTER UPDATE LOOP (THE DIGITAL TWIN)
# ==========================================
def update(val):
    dia = s_dia.val
    rpm = s_rpm.val
    power = s_pow.val
    fluid = radio_fluid.value_selected

    # Initialize the EXACT physics engine used by the generator hardware
    engine = HexNativeSquareToothEngine(fluid_type=fluid, power_target_w=power, target_rpm=rpm)

    # Calculate actual physics based on inputs
    angular_vel = (rpm * 2 * math.pi) / 60.0
    torque = power / angular_vel

    # Extract dimensions from the engine
    shaft_dia = engine.size_titanium_shaft(torque)
    z_teeth, hex_hz = engine.calculate_hex_tooth_matrix()
    wall_thick = dia * 0.03
    housing_len = engine.calculate_acoustic_silencer_length(z_teeth, wall_thick, dia)
    gap, chev = engine.calculate_active_clearance_gap(dia)

    # Clear previous frame
    ax.clear()
    ax.set_title(f"RT Square-Tooth Cross-Section ({fluid.upper()})", fontsize=14, fontweight='bold')
    ax.set_xlabel("Width (mm)")
    ax.set_ylabel("Length (mm)")

    # ----------------------------------------
    # DRAWING THE 2D SCHEMATIC
    # ----------------------------------------
    housing_w = dia + (2 * gap) + (2 * wall_thick)
    
    # 1. Outer Titanium Housing
    ax.add_patch(patches.Rectangle((-housing_w/2, -housing_len/2), housing_w, housing_len, 
                                   fill=True, color='#B0C4DE', label='Acoustic Housing'))
    
    # 2. Inner Fluid Void
    void_w = dia + (2 * gap)
    ax.add_patch(patches.Rectangle((-void_w/2, -housing_len/2), void_w, housing_len, 
                                   fill=True, color='white', label='Fluid Channel'))
    
    # 3. Turbine Rotor
    rotor_len = housing_len * 0.25 # Visual thickness ratio
    ax.add_patch(patches.Rectangle((-dia/2, -rotor_len/2), dia, rotor_len, 
                                   fill=True, color='#2F4F4F', label='Square-Tooth Rotor'))
    
    # 4. Central Titanium Grade 5 Shaft
    ax.add_patch(patches.Rectangle((-shaft_dia/2, -housing_len/2 - 50), shaft_dia, housing_len + 100, 
                                   fill=True, color='#DAA520', label='Ti-6Al-4V Shaft'))

    # Axis Formatting
    # Dynamically scale the view to fit the generated dimensions
    max_dim = max(housing_w, housing_len) * 0.6
    ax.set_xlim(-max_dim, max_dim)
    ax.set_ylim(-max_dim, max_dim)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle=':', alpha=0.5)

    # ----------------------------------------
    # UPDATE UNIVAC TELEMETRY READOUT
    # ----------------------------------------
    readout = (
        f"--- DEPLOYMENT ---\n\n"
        f"Env:   {fluid.upper()}\n"
        f"RPM:   {rpm:.0f}\n"
        f"Power: {power/1000:.1f} kW\n"
        f"Torque:{torque:.0f} Nm\n\n"
        f"--- DIMENSIONS ---\n\n"
        f"Ti-Shaft Dia:\n {shaft_dia:.2f} mm\n\n"
        f"Acoustic Len:\n {housing_len:.2f} mm\n\n"
        f"Active Gap:\n {gap:.3f} mm\n\n"
        f"Chevron:\n {chev:.3f} mm\n\n"
        f"--- RT HEX BUS ---\n\n"
        f"Teeth: {z_teeth}\n"
        f"Pulse: {hex_hz:.2f} Hz\n"
    )
    info_text.set_text(readout)
    fig.canvas.draw_idle()

# Bind the update function to the controls
s_dia.on_changed(update)
s_rpm.on_changed(update)
s_pow.on_changed(update)
radio_fluid.on_clicked(update)

# Trigger the initial render
update(None)

# Launch the visualizer window
plt.show()
