# =========================================================================
# SQUARE-TOOTH GENERATOR HARDWARE INFRASTRUCTURE MATRIX
# Multi-Stage Deterministic Cross-Compilation Toolchain Environment
# =========================================================================

# -------------------------------------------------------------------------
# STAGE 1: Isolated Construction & Compilation Workspace
# -------------------------------------------------------------------------
FROM debian:bookworm-slim AS build-matrix

# Prevent interactive configuration prompts during apt installation steps
ENV DEBIAN_FRONTEND=noninteractive

# Install strict system-level build tools and GNU compilation headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc6-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

# Establish the source mounting workspace within the execution container
WORKDIR /build

# Copy the entire src directory contents to keep dependencies clean
COPY src/ ./src/

# Change context directory and invoke your automated Makefile pipeline
WORKDIR /build/src
RUN make clean && make

# -------------------------------------------------------------------------
# STAGE 2: Lightweight Production Extraction Payload Environment
# -------------------------------------------------------------------------
FROM debian:bookworm-slim AS production-payload

WORKDIR /firmware

# Copy only the compiled binary results from Stage 1 to isolate bloat
COPY --from=build-matrix /build/src/mcp4725_driver .
COPY --from=build-matrix /build/src/libmcp4725.a .

# Set execution vector default loop to print safe firmware driver validation
CMD ["./mcp4725_driver"]
