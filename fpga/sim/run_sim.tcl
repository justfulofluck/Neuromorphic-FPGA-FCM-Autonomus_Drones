# Vivado Simulation Script for Control SNN
# Run: vivado -mode batch -source fpga/sim/run_sim.tcl

# Create project
create_project -force control_snn_sim ./vivado_proj -part xc7z020clg400-1

# Add RTL sources
add_files -norecurse \
    ../rtl/lif_neuron.sv \
    ../rtl/linear_lif.sv \
    ../rtl/control_snn.sv

# Add testbench
add_files -fileset sim_1 ../tb/tb_control_snn.sv

# Set top module
set_property top tb_control_snn [get_filesets sim_1]

# Compile
launch_simulation -simset sim_1 -mode behavioral

# Run simulation
run 10000 ns

# Close
close_sim
close_project