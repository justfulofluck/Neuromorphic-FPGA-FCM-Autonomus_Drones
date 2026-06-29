# Neuromorphic-FPGA-FCM: Autonomous Drone Flight Control

<b>Hybrid CNN+SNN</b> vision-to-control pipeline for autonomous drone flight, deployed to FPGA via SystemVerilog RTL.

<b>Architecture:</b> Event camera → Vision CNN (Conv2D) → 6-DoF ego-motion → Control SNN (3-layer LIF) → 4× PWM motor output

---

## Pipeline

```
Event Camera (64×64 simulation)
       ↓
Vision CNN (Conv2D+ReLU+BN)
  [2→32→64→128→FC256→FC6]
       ↓ 6-DoF ego-motion (vx, vy, vz, wx, wy, wz)
Control SNN (3 LinearLIF layers)
  [6→64→32→4]
       ↓ 4× spike trains (rate-coded)
PWM Decode (spike_count / time_steps)
       ↓
4× PWM → Quadcopter motors
```

---

## Training Results

### Vision CNN
| Metric | Value |
|--------|-------|
| Architecture | Conv2D 2→32→64→128 + FC 256→6 |
| Epochs | 50 |
| Optimizer | Adam, ReduceLROnPlateau |
| Weight decay | 1e-4 |
| Input | 64×64 event frames (2-channel: on/off) |
| **Test MSE** | **0.002** |

### Control SNN
| Metric | Value |
|--------|-------|
| Architecture | LinearLIF 6→64→32→4 |
| Epochs | 30 |
| beta | 0.8 (fixed) |
| threshold | 0.1 (fixed) |
| LIF reset | Subtractive |
| Time steps | 20 |
| **Spike rate** | **~0.49** |
| PWM output | Rate-coded: spikes.mean(dim=0) |

### Key Design Decisions
- Hybrid CNN+SNN (pure SNN failed after 11 attempts — zero-output local minimum, spike rate stuck at 0)
- `sigmoid` removed from `decode()` — was capping output ≥ 0.5, enabling zero-spike escape
- Synthetic events use full 6-DoF optical flow equations (grid_sample, all 6 ego-motion components)
- PWM = `ego[:4] * 0.3 + 0.5 + noise * 0.05` (correlated with motion, not random)

---

## FPGA Implementation

### Weight Export
Python weights → Q4.11 fixed-point (16-bit signed: 1 sign + 4 integer + 11 fractional, range [-16, 15.9995]):
```bash
value_q411 = round(float_val * 2048).astype(int16)
```

Exported files in `fpga/export/`:
| File | Shape |
|------|-------|
| `fc1_weight.mem` | 6×64 = 384 |
| `fc1_bias.mem` | 64 |
| `fc2_weight.mem` | 64×32 = 2048 |
| `fc2_bias.mem` | 32 |
| `fc3_weight.mem` | 32×4 = 128 |
| `fc3_bias.mem` | 4 |

### RTL Modules

| Module | File | Description |
|--------|------|-------------|
| LIF Neuron | `rtl/lif_neuron.sv` | Single LIF neuron: beta*V + I, threshold fire, subtractive reset |
| Linear Layer | `rtl/linear_lif.sv` | MAC state machine + LIF array, weight/bias loaded via $readmemh |
| Top Module | `rtl/control_snn.sv` | 3-layer chain (6→64→32→4) with sequencing controller and PWM decode |
| Testbench | `tb/tb_control_snn.sv` | 20 timesteps, spike counting, rate-coded PWM verification |

### Simulation Status
| Step | Status |
|------|--------|
| RTL compilation (iverilog) | ✅ Passes |
| Weight loading from .mem | ✅ Valid hex values |
| MAC state machine | ✅ Current values correct (724 vs threshold 205) |
| LIF neuron spike output | ❌ Under debug (timing issue between MAC done and LIF valid_in) |
| Vivado synthesis | ❌ Pending |
| FPGA board deployment | ❌ Pending |

### Run Simulation
```bash
cd fpga && ./run_simulation.sh
```

---

## Project Structure

```
.
├── neuromorphic/              # Python training pipeline
│   ├── models/
│   │   ├── control_snn.py     # 3-layer LinearLIF (6→64→32→4)
│   │   ├── vision_snn.py      # Conv2D CNN (event→6-DoF)
│   │   └── neuron.py          # LinearLIF layer (snnTorch)
│   ├── data/
│   │   ├── synthetic_events.py # 6-DoF optical flow generation
│   │   └── dataset.py         # PWM = ego*0.3 + 0.5 + noise
│   ├── config/
│   │   └── snn_config.yaml    # Hyperparameters
│   ├── training/
│   │   └── train.py           # Training loop
│   ├── inference/
│   │   └── test.py            # Inference/evaluation
│   ├── requirements.txt       # Python dependencies
│   ├── start_training.sh      # Train both vision + control
│   └── test_training.sh       # Test trained models
│
├── fpga/                      # FPGA implementation
│   ├── rtl/                   # SystemVerilog RTL
│   │   ├── lif_neuron.sv
│   │   ├── linear_lif.sv
│   │   └── control_snn.sv
│   ├── tb/                    # Testbenches
│   │   └── tb_control_snn.sv
│   ├── export/                # Q4.11 weight/bias .mem files
│   ├── sim/                   # Simulation output (.vvp, .vcd)
│   ├── run_simulation.sh      # Compile + run + GTKWave
│   └── run_sim.tcl            # Vivado simulation script
│
├── checkpoints/               # Trained model weights (.pt)
├── PX4-Autopilot/             # PX4 drone firmware (for future integration)
├── project documents/         # Design notes
└── README.md
```

---

## Dependencies

### Python (Training & Inference)

| Package | Version | Purpose |
|---------|---------|---------|
| Python | ≥ 3.10 | Runtime |
| PyTorch | ≥ 2.0.0 | Neural network framework |
| snnTorch | ≥ 0.8.0 | Spiking neural network layers (LinearLIF) |
| NumPy | ≥ 1.24.0 | Numerical computation |
| Matplotlib | ≥ 3.7.0 | Training plots |
| PyYAML | ≥ 6.0 | Configuration files |
| SciPy | ≥ 1.10.0 | Signal processing |
| tqdm | ≥ 4.65.0 | Progress bars |

```bash
pip install -r neuromorphic/requirements.txt
```

### FPGA Simulation

| Tool | Version | Purpose |
|------|---------|---------|
| iverilog | ≥ 11.0 | SystemVerilog compilation & simulation |
| GTKWave | ≥ 3.3 | VCD waveform viewer |

```bash
sudo apt install iverilog gtkwave
```

### Future: Drone Simulation

| Tool | Version | Purpose |
|------|---------|---------|
| PX4-Autopilot | ≥ 1.14 | Drone autopilot firmware |
| Gazebo (gz-sim) | ≥ 8.0 | 3D drone simulator |
| QGroundControl | ≥ 4.2 | Ground station (optional) |

---

## Quick Start

### 1. Train Models
```bash
./neuromorphic/start_training.sh
```

### 2. Test
```bash
./neuromorphic/test_training.sh
```

### 3. FPGA Simulation
```bash
cd fpga && ./run_simulation.sh
```

### 4. View Waveforms
```bash
gtkwave fpga/sim/tb_control_snn.vcd
```

