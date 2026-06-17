#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RTL_DIR="$SCRIPT_DIR/rtl"
TB_DIR="$SCRIPT_DIR/tb"
SIM_DIR="$SCRIPT_DIR/sim"
VVP="$SIM_DIR/tb_control_snn.vvp"
VCD="$SIM_DIR/tb_control_snn.vcd"

mkdir -p "$SIM_DIR"

echo "=== Compiling SystemVerilog ==="
iverilog -g2012 -o "$VVP" \
    "$RTL_DIR/lif_neuron.sv" \
    "$RTL_DIR/linear_lif.sv" \
    "$RTL_DIR/control_snn.sv" \
    "$TB_DIR/tb_control_snn.sv"

echo "=== Running Simulation ==="
vvp "$VVP"

echo ""
echo "=== VCD Waveform ==="
echo "View with: gtkwave $VCD"
echo ""

if command -v gtkwave &> /dev/null; then
    echo "Launching GTKWave..."
    gtkwave "$VCD" &
fi
