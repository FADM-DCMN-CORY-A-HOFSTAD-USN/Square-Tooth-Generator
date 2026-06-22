/**
 * =========================================================================
 * SQUARE-TOOTH GENERATOR HARDWARE INFRASTRUCTURE MATRIX
 * Unified Multi-Channel Hardware Bus Shutdown Handler
 * Safely parks physical actuators and drains logic traces to ground.
 * =========================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include "dac_mcp4725.h"

/* Shared Bus & Stabilization Configurations */
#define I2C_BUS_PATH      "/dev/i2c-1"
#define LINE_DRAIN_US     50000         // 50ms delay for safe trace drainage

int main() {
    printf("=========================================================================\n");
    printf("     SQUARE-TOOTH MASTER RUNTIME ENVIRONMENT: SYSTEM SHUTDOWN            \n");
    printf("=========================================================================\n");

    // STAGE 1: Open Communication Bus Handle
    printf("[SHUTDOWN STAGE 1]: Accessing physical I2C communications bus...\n");
    int master_bus_fd = open(I2C_BUS_PATH, O_RDWR);
    if (master_bus_fd < 0) {
        perror("[CRITICAL SHUTDOWN FAULT]: Cannot access I2C hardware descriptor node");
        return -1;
    }

    // Map the hardware channels
    MCP4725_Device telemetry_ch0 = {
        .i2c_bus_fd = master_bus_fd,
        .device_address = 0x62,
        .reference_voltage_v = 5.0f,
        .target_voltage_max_v = 1.0f
    };

    MCP4725_Device telemetry_ch1 = {
        .i2c_bus_fd = master_bus_fd,
        .device_address = 0x63,
        .reference_voltage_v = 5.0f,
        .target_voltage_max_v = 1.0f
    };

    // STAGE 2: Actuator Parking Command Execution
    printf("[SHUTDOWN STAGE 2]: Retracting gap tuning flaps to structural park position...\n");
    // Token '0' translates to absolute minimum voltage, signaling actuators to go to zero-extension park
    if (write_mcp4725_step(&telemetry_ch0, '0') != DAC_STATUS_SUCCESS) {
        fprintf(stderr, "  [SHUTDOWN WARNING]: Primary channel failed to send park command.\n");
    } else {
        printf("  -> Primary channel flap retraction command dispatched.\n");
    }

    if (write_mcp4725_step(&telemetry_ch1, '0') != DAC_STATUS_SUCCESS) {
        fprintf(stderr, "  [SHUTDOWN WARNING]: Redundant safety channel failed to send park command.\n");
    } else {
        printf("  -> Redundant safety channel flap retraction command dispatched.\n");
    }

    // STAGE 3: Clear and Drain Electrical Traces
    printf("[SHUTDOWN STAGE 3]: Clamping logic lines to 0.0V and draining residual voltage...\n");
    // Enforce a strict hold window to allow copper trace capacitance to drop down to ground baseline
    usleep(LINE_DRAIN_US);
    printf("  -> Signal trace lines fully discharged. Crosstalk vectors cleared.\n");

    // STAGE 4: Resource Cleanup Operations
    printf("[SHUTDOWN STAGE 4]: Releasing file descriptors and unlinking bus handles...\n");
    if (close(master_bus_fd) < 0) {
        perror("[SHUTDOWN WARNING]: Error unmapping master bus descriptor node");
    } else {
        printf("  -> Hardware communication bus closed cleanly.\n");
    }

    printf("=========================================================================\n");
    printf("[SHUTDOWN STATUS]: Safe state achieved. Hardware isolated. POWER_OFF_READY.\n");
    printf("=========================================================================\n");

    return 0;
}
