#!/usr/bin/env bash
# =========================================================================
# SQUARE-TOOTH GENERATOR REPOSITORY SYSTEM PLATFORM WORKSPACE INITIALIZER
# Orchestrates multi-language paths, testing, CAD environment matrices.
# =========================================================================

set -euo pipefail

# Define text formatting escape indicators
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0;37m' # No Color

echo -e "${BLUE}=========================================================================${NC}"
echo -e "${BLUE}   SQUARE-TOOTH GENERATOR SYSTEM ARCHITECTURE REPOSITORY CONFIGURATOR   ${NC}"
echo -e "${BLUE}=========================================================================${NC}"

# 1. Structural Directory Geometry Generation
echo -e "\n${YELLOW}[STAGE 1/4]: Aligning directory geometry nodes...${NC}"
DIRS=(
    "core"
    "src"
    "tools"
    "tests"
    "docs"
    "config"
    "outputs/manufacturing"
)

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "  -> Instantiated missing system directory tree node: ${GREEN}$dir/${NC}"
    else
        echo -e "  -> Directory path already verified: ${GREEN}$dir/${NC}"
    fi
done

# 2. Dependency Toolchain Environment Verification
echo -e "\n${YELLOW}[STAGE 2/4]: Scanning local system toolchain binaries...${NC}"

check_dependency() {
    local cmd=$1
    local description=$2
    if command -v "$cmd" &> /dev/null; then
        echo -e "  -> Verified ${GREEN}$description${NC} dependency match found: $($cmd --version | head -n 1)"
        return 0
    else
        echo -e "  -> ${RED}[MISSING DEPENDENCY]:${NC} $description ($cmd) could not be resolved."
        return 1
    fi
}

DEPENDENCY_ERRORS=0
check_dependency "python3" "Python Runtime Engine" || DEPENDENCY_ERRORS=$((DEPENDENCY_ERRORS+1))
check_dependency "gcc" "GNU C Compiler Toolchain" || DEPENDENCY_ERRORS=$((DEPENDENCY_ERRORS+1))
check_dependency "make" "GNU Makefile System Engine" || DEPENDENCY_ERRORS=$((DEPENDENCY_ERRORS+1))

# Optional warning indicators for GUI components
if ! command -v openscad &> /dev/null; then
    echo -e "  -> ${YELLOW}[ADVISORY]:${NC} OpenSCAD CLI binary not mapped. Scripted CAD renderings will fall back to container pipelines."
fi

if [ "$DEPENDENCY_ERRORS" -gt 0 ]; then
    echo -e "\n${RED}[CRITICAL COMPLIANCE HALT]: Core compilation dependencies are missing.${NC}"
    echo -e "Please configure the missing compilers and execution components before re-running setup.sh."
    exit 1
fi

# 3. Setting Local Environment Routing Variables
echo -e "\n${YELLOW}[STAGE 3/4]: Writing workspace environment routing configuration file...${NC}"
ENV_FILE=".env"

cat << EOF > "$ENV_FILE"
# =========================================================================
# SQUARE-TOOTH GENERATOR SYSTEM INFRASTRUCTURE CORE VARIABLE CONFIGURATIONS
# =========================================================================
PROJECT_ROOT_PATH="$(pwd)"
PYTHONPATH="\${PROJECT_ROOT_PATH}:\${PYTHONPATH:-}"
FIRMWARE_OUTPUT_PATH="\${PROJECT_ROOT_PATH}/outputs"
KICAD_FABRICATION_DIRECTORY="\${PROJECT_ROOT_PATH}/outputs/manufacturing"
export PYTHONPATH FIRMWARE_OUTPUT_PATH KICAD_FABRICATION_DIRECTORY
EOF

echo -e "  -> Exported configuration rules cleanly to: ${GREEN}$ENV_FILE${NC}"
echo -e "  -> Sourcing freshly initialized environment maps..."
# Export pathways globally to the immediate shell layer
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

# 4. Triggering Initial Signal Pipeline Validation Matrix
echo -e "\n${YELLOW}[STAGE 4/4]: Executing validation matrix pipeline algorithms...${NC}"

if [ -f "tests/test_pipeline.py" ]; then
    echo -e "  -> Dispatching 108-bit stacked word resolution unit checks..."
    if python3 -m unittest discover -s tests; then
        echo -e "  -> ${GREEN}[SUCCESS]:${NC} System logic precision constraints successfully validated."
    else
        echo -e "  -> ${RED}[FAILURE]:${NC} Integrated mathematical precision baseline errors detected."
        exit 1
    fi
else
    echo -e "  -> ${YELLOW}[SKIPPED]:${NC} tests/test_pipeline.py module template not detected yet. Skipping checks."
fi

echo -e "\n${BLUE}=========================================================================${NC}"
echo -e "${GREEN}[COMPLETED]: Integrated multi-language repository framework successfully setup.${NC}"
echo -e "To lock pathways inside your current terminal runner session window, execute:"
echo -e "  ${YELLOW}source .env${NC}"
echo -e "${BLUE}=========================================================================${NC}"
