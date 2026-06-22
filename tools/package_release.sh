#!/usr/bin/env bash
# =========================================================================
# SQUARE-TOOTH GENERATOR HARDWARE DEPLOYMENT UTILITY
# Compiles certified firmware libraries, Gerbers, and docs into a release tarball.
# =========================================================================

set -euo pipefail

# Append this verification gate into your tools/package_release.sh script loop:

echo -e "${YELLOW}[PACKAGER]: Invoking silicon and board-space validation gate...${NC}"
if python3 "${PROJECT_ROOT_PATH}/tools/check_todo_compliance.py"; then
    echo -e "${GREEN}[PASSED]: Hardware checklist fully completed. Continuing build.${NC}"
else
    echo -e "${RED}[CRITICAL GATE BLOCK]: Factory deployment aborted due to unchecked hardware milestones.${NC}"
    exit 3
fi

# Text formatting escape variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0;37m'

# Source environmental variables to ensure path consistency
if [ -f "./.env" ]; then
    source ./.env
elif [ -f "../.env" ]; then
    source ../.env
else
    echo -e "${RED}[CRITICAL ERROR]: Project profile (.env) map missing. Run ./setup.sh first.${NC}"
    exit 1
fi

# Request semantic version input flag descriptor if not supplied as an argument
if [ "${1:-}" != "" ]; then
    VERSION_TAG="$1"
else
    echo -e "${BLUE}=== Hardware Assembly Release Packager ===${NC}"
    echo -n "Enter Semantic Version Tag (e.g., v1.0.0, v2.1.4-rc1): "
    read -r VERSION_TAG
fi

# Clean up input strings to prevent directory traversal vulnerabilities
VERSION_TAG=$(echo "$VERSION_TAG" | tr -cd 'a-zA-Z0-9._-')
if [ -z "$VERSION_TAG" ]; then
    echo -e "${RED}[ERROR]: Invalid or empty version identifier specified.${NC}"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RELEASE_NAME="square_tooth_release_${VERSION_TAG}_${TIMESTAMP}"
STAGING_DIR="${PROJECT_ROOT_PATH}/outputs/staging_${RELEASE_NAME}"
DIST_DIR="${PROJECT_ROOT_PATH}/outputs/distribution"

echo -e "\n${YELLOW}[PACKAGER]: Initializing clean staging footprint...${NC}"
rm -rf "${STAGING_DIR}"
mkdir -p "${STAGING_DIR}/hardware/gerbers"
mkdir -p "${STAGING_DIR}/firmware/include"
mkdir -p "${STAGING_DIR}/firmware/lib"
mkdir -p "${STAGING_DIR}/documentation"
mkdir -p "${DIST_DIR}"

# 1. Verification of Required Release Artifact Assets
echo -e "${YELLOW}[PACKAGER]: Inspecting artifact pools for compliance...${NC}"

ASSERT_FILE_EXISTS() {
    if [ ! -f "$1" ]; then
        echo -e "${RED}[CRITICAL MISSING ARTIFACT]: $1 could not be resolved.${NC}"
        echo -e "Please run './tools/simulate_system.sh' or 'make fab' to populate output folders."
        rm -rf "${STAGING_DIR}"
        exit 1
    fi
}

# Verify Firmware Assets
ASSERT_FILE_EXISTS "${PROJECT_ROOT_PATH}/src/libmcp4725.a"
ASSERT_FILE_EXISTS "${PROJECT_ROOT_PATH}/src/dac_mcp4725.h"

# Verify Gerber Assets (Core Layers Mapping)
ASSERT_FILE_EXISTS "${KICAD_FABRICATION_DIRECTORY}/hex_telemetry_atx-F_Cu.gbr"
ASSERT_FILE_EXISTS "${KICAD_FABRICATION_DIRECTORY}/hex_telemetry_atx-B_Cu.gbr"
ASSERT_FILE_EXISTS "${KICAD_FABRICATION_DIRECTORY}/hex_telemetry_atx-Edge_Cuts.gbr"

# 2. Populate Staging Target Directories
echo -e "${YELLOW}[PACKAGER]: Staging assets into standardized layout...${NC}"

# Copy Hardware Manufacturing Files
cp -r "${KICAD_FABRICATION_DIRECTORY}"/* "${STAGING_DIR}/hardware/gerbers/"

# Copy Firmware Assets
cp "${PROJECT_ROOT_PATH}/src/libmcp4725.a" "${STAGING_DIR}/firmware/lib/"
cp "${PROJECT_ROOT_PATH}/src/dac_mcp4725.h" "${STAGING_DIR}/firmware/include/"

# Copy Documentation System Files
if [ -d "${PROJECT_ROOT_PATH}/docs" ]; then
    cp "${PROJECT_ROOT_PATH}/docs"/*.md "${STAGING_DIR}/documentation/"
fi
if [ -f "${PROJECT_ROOT_PATH}/README.md" ]; then
    cp "${PROJECT_ROOT_PATH}/README.md" "${STAGING_DIR}/documentation/"
fi

# Inject a dynamic BOM / Manifest descriptor info file into the root of the staging build
cat << EOF > "${STAGING_DIR}/manifest.json"
{
  "release_identity": "${RELEASE_NAME}",
  "version": "${VERSION_TAG}",
  "build_timestamp": "${TIMESTAMP}",
  "architecture_compliance": "RT-16-STATE-0.0V-1.0V",
  "chassis_form_factor": "ATX_STANDARD"
}
EOF

# 3. Compress Staging Environment into Production Tarball Output
echo -e "${YELLOW}[PACKAGER]: Compressing delivery package...${NC}"
TARBALL_PATH="${DIST_DIR}/${RELEASE_NAME}.tar.gz"

cd "${PROJECT_ROOT_PATH}/outputs"
tar -czf "${TARBALL_PATH}" -C "${STAGING_DIR}" .
cd "${PROJECT_ROOT_PATH}"

# 4. Final Cleanup Operations
rm -rf "${STAGING_DIR}"

echo -e "\n${BLUE}=========================================================================${NC}"
echo -e "${GREEN}[SUCCESS]: Secure Production Assembly Archive Export Complete!${NC}"
echo -e "Target Delivery Payload Location:"
echo -e "  ${YELLOW}${TARBALL_PATH}${NC}"
echo -e "${BLUE}=========================================================================${NC}"
