#!/bin/bash
# FPGA Simulation Runner
# Usage: ./run_fpga_sim.sh [gtkwave]
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RTL_DIR="$SCRIPT_DIR/fpga/rtl"
TB_DIR="$SCRIPT_DIR/fpga/tb"
SIM_DIR="$SCRIPT_DIR/fpga/sim"
VVP="$SIM_DIR/tb_control_snn.vvp"

echo "================================"
echo " FPGA Simulation"
echo "================================"

# Step 1: Compile
echo ""
echo "[1/2] Compiling SystemVerilog..."
iverilog -g2012 -o "$VVP" \
    "$RTL_DIR/lif_neuron.sv" \
    "$RTL_DIR/linear_lif.sv" \
    "$RTL_DIR/control_snn.sv" \
    "$TB_DIR/tb_control_snn.sv"

echo "       Compiled: $VVP"

# Step 2: Run
echo ""
echo "[2/2] Running simulation..."
echo ""
vvp "$VVP"

echo ""
echo "================================"
echo " Done"
echo "================================"
