# =========================================================================
# SQUARE-TOOTH GENERATOR HARDWARE DEPLOYMENT PIPELINE
# Automated Makefile System Infrastructure with Integrated Gerber/CAD Links
# =========================================================================

# Update target binaries array inside src/Makefile:
TARGET_EXE = mcp4725_driver sys_init sys_shutdown

# Add the final linking and compilation recipes to the bottom:
sys_shutdown: sys_shutdown.o dac_mcp4725.o
	@echo "[LINKER]: Compiling system shutdown safety module: $@..."
	@$(CC) $(CFLAGS) $^ -o $@

sys_shutdown.o: sys_shutdown.c dac_mcp4725.h
	@echo "[COMPILER]: Synthesizing machine object code from shutdown source: $<..."
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# 1. Compiler and Linker Configuration Matrix
CC       = gcc
AR       = ar
ARFLAGS  = rcs

# 2. Performance and Optimization Flags
CFLAGS   = -Wall -Wextra -O3 -std=c99 -fPIC
INCLUDES = -I.

# 3. Output Targets Definition
TARGET_LIB = libmcp4725.a
TARGET_EXE = mcp4725_driver

# 4. Input File Vectors
SRCS = dac_mcp4725.c
OBJS = $(SRCS:.c=.o)

# 5. Native OS Python Environment Selector for KiCad Hook Execution
# Handles routing through native KiCad command lines where necessary
PYTHON   = python3

# =========================================================================
# Execution Recipes & Build Matrix
# =========================================================================

# Default Primary Recipe Target
all: $(TARGET_LIB) $(TARGET_EXE)
	@echo "[DEPLOYMENT]: Automated firmware compile and binding processes successfully finalized."

# Static Library Build Loop
$(TARGET_LIB): $(OBJS)
	@echo "[ARCHIVER]: Constructing unified static hardware library binary: $@..."
	@$(AR) $(ARFLAGS) $@ $^

# Executable Build Loop
$(TARGET_EXE): dac_mcp4725.o
	@echo "[LINKER]: Compiling monolithic device executable package: $@..."
	@$(CC) $(CFLAGS) $^ -o $@

# C Object Compilation Engine
%.o: %.c dac_mcp4725.h
	@echo "[COMPILER]: Synthesizing machine object code from source code file: $<..."
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# =========================================================================
# ADDED MANUFACTURING CAD/PCB EXTENSION RECIPES
# =========================================================================

# The Unified Hardware Fabrication Master Command Loop
fab: all
	@echo "\n[FAB-MATRIX]: Initiating full programmatic hardware layout revision cycle..."
	@echo "[FAB-MATRIX]: Instantiating KiCad ATX PCB board bounds and 16-state guard rings..."
	@$(PYTHON) build_hex_board.py
	@echo "\n[FAB-MATRIX]: Extracting manufacturing industrial Gerber and Excellon CNC drill patterns..."
	@$(PYTHON) generate_gerbers.py
	@echo "\n[SUCCESS]: Unified firmware binaries and physical fabrication packages are fully generated and synchronized."

# Repository Purge Protocol (Updated to wipe generated output and manufacturing trees)
clean:
	@echo "[HOUSEKEEPING]: Removing generated object modules and static library binaries..."
	@rm -f $(OBJS) $(TARGET_LIB) $(TARGET_EXE)
	@echo "[HOUSEKEEPING]: Clearing generated PCB outputs and manufacturing data payloads..."
	@rm -rf outputs/hex_telemetry_atx.kicad_pcb outputs/manufacturing/

# Explicit Target Verification Enforcement
.PHONY: all clean fab
