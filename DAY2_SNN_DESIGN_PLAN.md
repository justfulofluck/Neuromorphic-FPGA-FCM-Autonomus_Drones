# Day 2: SNN Architecture Design & Training Plan

## Project: Neuromorphic FPGA-Based Flight Controller for Autonomous Drones
**Date**: Day 2 of 10  
**Mode**: Simulation-only (no hardware)  
**Environment**: Ubuntu 22.04+, Python venv, snnTorch, morphyne, PX4/Gazebo SITL

---

## Objectives

| # | Goal | Deliverable |
|---|------|-------------|
| 1 | Design Vision SNN for ego-motion estimation | `models/vision_snn.py` |
| 2 | Design Control SNN for motor commands | `models/control_snn.py` |
| 3 | Create synthetic event data generator | `data/synthetic_events.py` |
| 4 | Build training pipelines | `training/train_vision.py`, `training/train_control.py` |
| 5 | Validate end-to-end inference | `inference/test_pipeline.py` |

---

## SNN Architectures

### Vision SNN: Event Stream → 6-DOF Ego-Motion

```
Input: Event tensor [T, 2, H, W]  (polarity × height × width)
       H=W=64 or 128, T=30 time steps
       │
       ▼
Layer 1: Conv2d LIF (32 ch, 5×5 kernel, stride 2, padding 2)
         → [T, 32, H/2, W/2]
         │
         ▼
Layer 2: Conv2d LIF (64 ch, 3×3 kernel, stride 2, padding 1)
         → [T, 64, H/4, W/4]
         │
         ▼
Layer 3: Conv2d LIF (128 ch, 3×3 kernel, stride 2, padding 1)
         → [T, 128, H/8, W/8]
         │
         ▼
Layer 4: Flatten + Linear LIF (256 units)
         → [T, 256]
         │
         ▼
Layer 5: Linear LIF (6 units)  → Ego-motion vector
         → [T, 6]  (vx, vy, vz, wx, wy, wz)
         │
         ▼
Output: Spike rate decoding over T steps → continuous 6-DOF vector
```

**Parameters**:
- Neuron: LIF with surrogate gradient (Fast Sigmoid: `1/(1+|x|)²`)
- β (membrane decay): 0.9 (τ_mem ≈ 10ms)
- Threshold: 1.0
- Reset: Subtract
- Loss: MSE + λ·spike_rate_regularization (λ=0.01)

---

### Control SNN: Ego-Motion → 4 Motor PWM

```
Input: Ego-motion [6] + optional state [attitude(3), thrust_cmd(1)]
       Total: 6-10 features
       │
       ▼
Layer 1: Linear LIF (64 units)  → [T, 64]
         │
         ▼
Layer 2: Linear LIF (32 units)  → [T, 32]
         │
         ▼
Layer 3: Linear LIF (4 units)   → [T, 4]  (Motor 0-3 PWM)
         │
         ▼
Output: Spike rate → PWM duty cycle [0, 1] per motor
```

**Parameters**:
- Neuron: LIF (Fast Sigmoid surrogate)
- β: 0.95 (faster membrane, τ_mem ≈ 20ms)
- Threshold: 1.0
- Time steps: T=10 (reactive control)
- Loss: MSE(PWM_pred, PWM_gt) + λ·spike_count (λ=0.001)

---

## File Structure

```
neuromorphic/
├── models/
│   ├── __init__.py
│   ├── vision_snn.py          # VisionSNN class (5-layer ConvLIF)
│   ├── control_snn.py         # ControlSNN class (3-layer LinearLIF)
│   └── neuron.py              # Custom LIF + surrogate gradients
├── data/
│   ├── __init__.py
│   ├── synthetic_events.py    # Event tensor generator + physics
│   ├── quad_dynamics.py       # Simple quadcopter dynamics for labels
│   └── dataset.py             # PyTorch Dataset/DataLoader
├── training/
│   ├── __init__.py
│   ├── train_vision.py        # Vision SNN training loop
│   ├── train_control.py       # Control SNN training loop
│   └── utils.py               # Metrics, logging, checkpoints
├── inference/
│   ├── __init__.py
│   └── test_pipeline.py       # End-to-end: events → vision → control → PWM
├── config/
│   └── snn_config.yaml        # Hyperparameters
└── requirements.txt           # Pinned dependencies
```

---

## Synthetic Data Generation

### Event Camera Model
```python
# Simplified event generation from ego-motion
# Events = polarity changes at pixel (x,y) when log-intensity change > threshold
# Input: ego-motion [vx,vy,vz, wx,wy,wz], scene depth map
# Output: Event tensor [T, 2, H, W] (polarity channels)
```

### Quadcopter Dynamics (for ground truth labels)
```python
# State: [pos(3), vel(3), quat(4), omega(3)]
# Control: motor_thrusts[4]
# Physics: Newton-Euler rigid body + motor model
# Generates: ego-motion labels from control inputs
```

### Dataset Format
```python
# PyTorch Dataset returns:
# {
#   'events': Tensor[T, 2, H, W],      # Event stream
#   'ego_motion_gt': Tensor[6],        # Ground truth ego-motion
#   'motor_pwm_gt': Tensor[4],         # Ground truth PWM (for control SNN)
#   'metadata': {...}                  # Timestamps, sequence info
# }
```

---

## Training Configuration (snn_config.yaml)

```yaml
# Vision SNN
vision_snn:
  input_shape: [30, 2, 64, 64]  # T, C, H, W
  conv_channels: [32, 64, 128]
  kernel_sizes: [5, 3, 3]
  strides: [2, 2, 2]
  fc_hidden: 256
  output_dim: 6
  beta: 0.9
  threshold: 1.0
  surrogate: "fast_sigmoid"
  time_steps: 30
  batch_size: 16
  lr: 0.001
  epochs: 100
  spike_reg_lambda: 0.01

# Control SNN
control_snn:
  input_dim: 10           # ego_motion(6) + attitude(3) + thrust(1)
  hidden_dims: [64, 32]
  output_dim: 4
  beta: 0.95
  threshold: 1.0
  surrogate: "fast_sigmoid"
  time_steps: 10
  batch_size: 32
  lr: 0.001
  epochs: 50
  spike_reg_lambda: 0.001

# Data
data:
  num_samples: 10000
  train_split: 0.8
  val_split: 0.1
  test_split: 0.1
  event_resolution: [64, 64]
  time_window_ms: 30
```

---

## Training Loop Structure

### Vision SNN Training
```python
# train_vision.py
for epoch in range(epochs):
    for events, ego_motion_gt in train_loader:
        # Forward pass through time
        spikes, mem = vision_snn(events)  # [T, B, 6]
        
        # Rate decoding
        ego_motion_pred = spikes.mean(dim=0)  # [B, 6]
        
        # Loss
        loss = mse(ego_motion_pred, ego_motion_gt) \
             + lambda * spikes.mean()  # Spike regularization
        
        # Backward + optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### Control SNN Training
```python
# train_control.py
# Input: ego_motion_gt (or predicted from vision) + state
# Target: motor_pwm_gt from quad dynamics
for epoch in range(epochs):
    for ego_motion, state, pwm_gt in train_loader:
        inp = torch.cat([ego_motion, state], dim=-1)
        spikes, _ = control_snn(inp.unsqueeze(0).repeat(T,1,1))
        pwm_pred = spikes.mean(dim=0)
        loss = mse(pwm_pred, pwm_gt) + lambda * spikes.sum()
        ...
```

---

## End-to-End Test Pipeline

```python
# inference/test_pipeline.py
def test_full_pipeline():
    # 1. Generate synthetic event sequence
    events, ego_motion_gt = generate_event_sequence()
    
    # 2. Vision SNN inference
    ego_motion_pred = vision_snn_infer(events)
    
    # 3. Control SNN inference
    state = get_current_state()  # attitude, thrust_cmd
    pwm_pred = control_snn_infer(ego_motion_pred, state)
    
    # 4. Validate
    print(f"Ego-motion error: {mse(ego_motion_pred, ego_motion_gt):.4f}")
    print(f"PWM output: {pwm_pred}")
    print(f"Spike rates - Vision: {vision_spike_rate:.2f}, Control: {control_spike_rate:.2f}")
```

---

## Dependencies (requirements.txt)

```text
torch>=2.0.0
snntorch>=0.7.0
morphyne>=0.1.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
scipy>=1.10.0
tqdm>=4.65.0
pyyaml>=6.0
mavsdk>=0.53.0
opencv-python>=4.8.0
```

---

## Timeline Estimate

| Task | Duration |
|------|----------|
| Synthetic data generator | 2-3 hrs |
| Vision SNN model + training | 3-4 hrs |
| Control SNN model + training | 2-3 hrs |
| End-to-end test script | 1-2 hrs |
| **Total** | **~8-12 hrs** |

---

## Integration Points (Future Days)

| Interface | Format | Consumer |
|-----------|--------|----------|
| Vision SNN output | `Tensor[6]` (ego-motion) | Control SNN input |
| Control SNN output | `Tensor[4]` (PWM 0-1) | MAVSDK → PX4 |
| Event input | `Tensor[T,2,H,W]` | Gazebo/synthetic |
| FPGA bitstream | Verilog/SystemVerilog | Verilator simulation |

---

## Open Decisions (Confirm Before Implementation)

1. **Event resolution**: 64×64 (faster) or 128×128 (more detail)?
2. **Training approach**: Supervised (MSE) or STDP/unsupervised?
3. **GPU available?** Affects batch size, time steps
4. **Export to morphyne later?** Train in snnTorch, deploy with morphyne
5. **Control SNN inputs**: Just ego-motion (6) or +attitude+thrust (10)?

---

## .gitignore

### Ignored Files & Directories

| Category | Items |
|----------|-------|
| Python | `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/` |
| Virtual env | `venv/`, `.env` |
| External submodules | `PX4-Autopilot/` |
| Checkpoints | `checkpoints/`, `*.pt`, `*.pth` |
| IDE | `.vscode/`, `.idea/`, `*.swp`, `*.swo` |
| OS | `.DS_Store`, `Thumbs.db` |
| Jupyter | `.ipynb_checkpoints/` |
| Logs | `*.log` |

---

## Next Steps (Day 3 Preview)

- Convert trained SNNs to FPGA-friendly format (quantization, weight export)
- Write SystemVerilog modules using TENNLab neuromorphic elements
- Set up Verilator + cocotb testbenches
- Create Python ↔ Verilator communication bridge

---

*Generated for Day 2 planning.*
