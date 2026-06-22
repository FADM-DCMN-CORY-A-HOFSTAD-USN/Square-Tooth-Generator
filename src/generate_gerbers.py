#!/usr/bin/env python3
"""
Square-Tooth Generator Manufacturing Matrix
Automated Gerber & Excellon Drill Fabrication File Exporter for KiCad.
"""

import sys
import os

try:
    import pcbnew
except ImportError:
    print("Error: KiCad pcbnew Python module not found. Please run this script inside the KiCad Python environment.")
    sys.exit(1)

class GerberFabricationGenerator:
    def __init__(self, pcb_path="outputs/hex_telemetry_atx.kicad_pcb", output_dir="outputs/manufacturing"):
        self.pcb_path = pcb_path
        self.output_dir = output_dir
        
        # Verify the target board layout file exists before starting
        if not os.path.exists(self.pcb_path):
            raise FileNotFoundError(f"Target PCB file not found: {self.pcb_path}. Please run build_hex_board.py first.")
            
        # Ensure the manufacturing output folder structure exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load the physical board layout into memory
        self.board = pcbnew.LoadBoard(self.pcb_path)
        
    def export_gerber_layers(self):
        """Plots all mandatory physical layer configurations to production Gerber files."""
        plot_controller = pcbnew.PLOT_CONTROLLER(self.board)
        plot_options = plot_controller.GetPlotOptions()
        
        # Establish fundamental industrial Gerber configurations
        plot_options.SetPlotDirectoryName(self.output_dir)
        plot_options.SetFormat(pcbnew.PLOT_FORMAT_GERBER)
        plot_options.SetUseGerberAttributes(True)
        plot_options.SetUseGerberX2format(False)  # Enforce widely compatible standard RS-274X format
        plot_options.SetScale(1.0)
        plot_options.SetPlotFrameRef(False)
        plot_options.SetPlotValue(True)
        plot_options.SetPlotReference(True)
        plot_options.SetExcludeEdgeLayer(False)
        plot_options.SetLineWidth(pcbnew.EDA_IU_RESCALE(0.1, pcbnew.EDA_IU_RESCALE_MM)) # Baseline trace width
        
        # Define the target layer matrix to map (Layer Name, KiCad Layer ID)
        layers_to_plot = [
            ("F_Cu", pcbnew.F_Cu),          # Front Copper (Contains signal and guard rings)
            ("B_Cu", pcbnew.B_Cu),          # Back Copper Ground Plane
            ("F_Mask", pcbnew.F_Mask),      # Front Solder Mask
            ("B_Mask", pcbnew.B_Mask),      # Back Solder Mask
            ("F_SilkS", pcbnew.F_SilkS),    # Front Silkscreen labels
            ("Edge_Cuts", pcbnew.Edge_Cuts) # Physical mechanical ATX board perimeter cuts
        ]
        
        print(f"[FABRICATOR]: Commencing Gerber plot sequence to target destination: {self.output_dir}")
        for layer_name, layer_id in layers_to_plot:
            plot_controller.SetLayer(layer_id)
            plot_controller.OpenPlotfile(layer_name, pcbnew.PLOT_FORMAT_GERBER, f"Plotting {layer_name}")
            plot_controller.PlotLayer()
            plot_controller.ClosePlotfile()
            print(f"  -> Generated Gerber Layer: {layer_name}.gbr")

    def export_excellon_drills(self):
        """Generates CNC Excellon drill tracking maps matching structural mounting holes."""
        drill_writer = pcbnew.EXCELLON_WRITER(self.board)
        
        # Configure standard metric formatting for drill hits
        metric_units = True
        drill_writer.SetOptions(
            aMirror=False,
            aMinimalHeader=False,
            aOffset=pcbnew.VECTOR2I(0, 0),
            aMerge_SubDrills=False
        )
        drill_writer.SetFormat(metric_units)
        
        # Define output destinations for holes (PTH) and non-plated holes (NPTH)
        generate_plated = True
        generate_non_plated = True
        
        print("[FABRICATOR]: Exporting CNC Excellon structural drill files...")
        drill_writer.CreateDrillandMapFilesSet(self.output_dir, generate_plated, generate_non_plated)
        print(f"  -> Generated Plated/Non-Plated Drill Configuration Files.")

if __name__ == "__main__":
    try:
        fabricator = GerberFabricationGenerator()
        fabricator.export_gerber_layers()
        fabricator.export_excellon_drills()
        print("\n[SUCCESS]: Full manufacturing-ready package successfully generated. Output ready for PCB assembly house.")
    except Exception as error:
        print(f"\n[CRITICAL FAILURE]: Manufacturing export failed: {error}")
        sys.exit(1)
