/**
 * =========================================================================
 * SQUARE-TOOTH GENERATOR INFRASTRUCTURE MATRIX
 * MCP4725 Multi-Channel 16-State Voltage Injection Controller
 * Header Interface Configuration File for Modular System Linking
 * =========================================================================
 */

#ifndef DAC_MCP4725_H
#define DAC_MCP4725_H

#include <stdint.h>

/* Ensure compatibility if linked inside a C++ compiler project toolchain */
#ifdef __cplusplus
extern "C" {
#endif

/**
 * @struct MCP4725_Device
 * @brief Thread-safe structural handle containing physical track metrics.
 */
typedef struct {
    int i2c_bus_fd;             /**< System file descriptor handle for the active I2C bus lane (/dev/i2c-X) */
    uint8_t device_address;     /**< Hardwired physical I2C address designation on the bus matrix (e.g., 0x62) */
    float reference_voltage_v;  /**< Regulated supply voltage rails running to the chip VCC pin (Typically 5.0V) */
    float target_voltage_max_v; /**< Strict maximum ceiling for your discrete logic steps (Fixed at 1.0V) */
} MCP4725_Device;

/**
 * @enum DAC_Status
 * @brief System return codes used for deterministic error boundary checking.
 */
typedef enum {
    DAC_STATUS_SUCCESS = 0,
    DAC_STATUS_ERROR_BUS_FD = -1,
    DAC_STATUS_ERROR_I2C_SLAVE = -2,
    DAC_STATUS_ERROR_WRITE_FAILED = -3,
    DAC_STATUS_INVALID_TOKEN = -4
} DAC_Status;

/**
 * @brief Pre-calculates the absolute 12-bit register code for the DAC matrix.
 * 
 * Computes exact discrete voltage increments across your 16-state logic configurations.
 * 
 * @param device Pointer to the specific configuration channel handle structures.
 * @param hex_token A single 16-state character symbol ('0'-'9', 'A'-'F').
 * @return uint16_t Clamped 12-bit raw register integer value (0 to 4095).
 */
uint16_t calculate_12bit_dac_value(const MCP4725_Device *device, char hex_token);

/**
 * @brief Dispatches a 16-state logic update command sequence over the physical bus.
 * 
 * Packages the data using MCP4725 Fast Write requirements to ensure near-zero lag.
 * 
 * @param device Pointer to the specific destination target channel handle structures.
 * @param hex_token The single hexadecimal state character to be injected onto the lane.
 * @return DAC_Status Code representing operation outcome (0 for total success).
 */
DAC_Status write_mcp4725_step(const MCP4725_Device *device, char hex_token);

#ifdef __cplusplus
}
#endif

#endif /* DAC_MCP4725_H */
