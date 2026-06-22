# =========================================================================
# SQUARE-TOOTH GENERATOR HARDWARE DEPLOYMENT PIPELINE
# Automated Makefile System Infrastructure for Firmware & Driver Modules
# =========================================================================

# 1. Compiler and Linker Configuration Matrix
CC       = gcc
AR       = ar
ARFLAGS  = rcs

# 2. Performance and Optimization Flags
# -O3 maximizes loop optimizations for raw speed in turbine real-time adjustments
# -Wall -Wextra enforce rigorous compiler warning protocols
CFLAGS   = -Wall -Wextra -O3 -std=c99 -fPIC
INCLUDES = -I.

# 3. Output Targets Definition
TARGET_LIB = libmcp4725.a
TARGET_EXE = mcp4725_driver

# 4. Input File Vectors
SRCS = dac_mcp4725.c
OBJS = $(SRCS:.c=.o)

# 5. Default Primary Recipe Target
all: $(TARGET_LIB) $(TARGET_EXE)
	@echo "[DEPLOYMENT]: Automated firmware compile and binding processes successfully finalized."

# 6. Static Library Build Loop (For clean link abstraction into telemetry systems)
$(TARGET_LIB): $(OBJS)
	@echo "[ARCHIVER]: Constructing unified static hardware library binary: $@..."
	@$(AR) $(ARFLAGS) $@ $^

# 7. Executable Build Loop (For direct hardware testing on system buses)
$(TARGET_EXE): dac_mcp4725.o
	@echo "[LINKER]: Compiling monolithic device executable package: $@..."
	@$(CC) $(CFLAGS) $^ -o $@

# 8. C Object Compilation Engine (Implicit rule template tracking changes)
%.o: %.c dac_mcp4725.h
	@echo "[COMPILER]: Synthesizing machine object code from source code file: $<..."
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# 9. Repository Purge Protocol (For resetting localized build trees)
clean:
	@echo "[HOUSEKEEPING]: Removing generated object modules and static library binaries..."
	@rm -f $(OBJS) $(TARGET_LIB) $(TARGET_EXE)

# 10. Explicit Target Verification Enforcement
.PHONY: all clean
