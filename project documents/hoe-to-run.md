How to run this, which has two parts: Python Traning/ inference and FPGA simulation.

1. Python Rnvoriment - traning & Inferance

# Install Python deps
pip install -r neuromorphic/requirements.txt

# Train vision CNN + control SNN
./neuromorphic/start_training.sh

# Test trained models
./neuromorphic/test_training.sh
2. FPGA Simulation
# Install tools
sudo apt install iverilog gtkwave

# Run RTL simulation
cd fpga && ./run_simulation.sh

# View waveforms
gtkwave fpga/sim/tb_control_snn.vcd
3. PX4 Integration (future)
The PX4-Autopilot/ directory is ready for fixed-wing UAV firmware integration with Gazebo + QGroundControl.
