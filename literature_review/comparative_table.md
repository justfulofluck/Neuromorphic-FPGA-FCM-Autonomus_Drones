# Comparative Table — Existing Work vs Our Approach

Har entry: **paper → hardware → task → key metrics → SNN method**. Ye table thesis ke Literature Review me sabse strong figure banega — isi se research gap clear hota hai.

## 1. Neuromorphic Hardware Platforms (ASIC)

| Platform | Year | Tech | Scale | Power / Efficiency | Learning | Access |
|----------|------|------|-------|-------------------|----------|--------|
| **TrueNorth** (IBM) | 2014 | 28nm, 5.4B tr. | 1M neurons, 256M synapses | 63 mW @ video; 46G SOPS/W | Inference only | Limited (research) |
| **Loihi** (Intel) | 2018 | 14nm, 60mm² | 128 cores, 130k neurons | ~1 W; >3000x EDP vs CPU | On-chip (STDP, RL) | Limited (Intel labs) |
| **SpiNNaker1** (Manchester) | 2013 | 130nm | 1M ARM cores | ~3.96 GIPS @ 1W/core | Software-defined | Modular boards |
| **SpiNNaker2** (TU Dresden) | 2019 | 22nm FDSOI | 10M cores (planned) | 10x power efficiency | Software + HW accel | In development |
| **DYNAPs** | 2018 | 65nm | 1024 neurons/chip | Low, async | STDP | Research |
| **BrainScaleS-2** | 2022 | 65nm mixed-signal | ~512 analog neurons | Accelerated | Hybrid plasticity | Research |

**Key gap:** In sabme custom ASIC cost + availability ka barrier — FPGA approach in sabka affordable alternative hai.

## 2. FPGA-Based SNN Implementations

| Work | Year | FPGA | Task | Network | Method | Key Metric |
|------|------|------|------|---------|--------|-----------|
| **Pearson et al.** | 2007 | Xilinx | Real-time signal/control | Small SNN | Direct RTL | Model-validated FPGA |
| **Isik (Survey)** | 2023 | Various | Survey (rate coding, LIF, time-mux) | MLP/CNN/LSTM/SNN | Review | Trends + gaps |
| **Robust open-source SNN on low-end FPGA** | 2025 | Low-end (13K LUT) | MNIST 784-128-10 | IF neurons | snnTorch → quantize → RTL | 520 µs / 100 timesteps |
| **SpikingJelly deployment** | 2023 | Various (Lava/NIR/Lynxi) | Vision, classification | Deep SNN | Surrogate gradient | Framework toolchain |
| **Ours (proposed)** | 2025 | **FPGA (Vivado)** | **UAV control (PWM)** | **3-layer LIF, 6→64→32→4, Q4.11** | **Surrogate gradient (snnTorch)** | 20 timesteps, RTL verified |

**Key gap highlighted:** Existing FPGA-SNN works zyada tar **classification/vision** hain — **control output (continuous regression)** par FPGA-SNN ka kaam kam hai. Hum isi gap me hain.

## 3. SNN-Based UAV / Control Systems

| Work | Year | Hardware | Task | SNN Architecture | Training | Result |
|------|------|----------|------|-----------------|----------|--------|
| **Dupeyroux et al.** (optic-flow landing) | 2021 | Loihi | MAV landing | SNN optic-flow | Evolutionary | Real drone landing |
| **Stagsted et al.** (SNN PID) | 2020 | Loihi | UAV PID control | Spiking PID | — | Concept demo |
| **Stroobants et al.** | 2024/25 | Teensy (→Loihi ready) | Quadrotor attitude est. + control | CUBA-LIF, modular (est + ctrl) | Imitation learning | 500 Hz, ~3° tracking error |
| **Paredes-Vallés et al.** | 2024 | **Loihi** (onboard) | Full vision-to-control flight | 5-layer vision + control | Self-supervised + evolutionary | 200 Hz, **27 µJ/inference**, real flight |
| **Xu et al.** (ANN→SNN control) | 2026 | Simulation | Continuous control analysis | Converted SNN | Conversion | Shows conversion fails in continuous control |
| **Mengozzi et al.** | 2025 | Simulation | Quadrotor agile flight | PPO-trained SNN | RL (PPO) | +2.5% success, +40% speed |
| **Ours** | 2025 | **FPGA** | **UAV control (4 PWM: aileron/elevator/rudder/throttle)** | **3-layer LIF, Q4.11, inference-only** | **Surrogate gradient** | RTL sim verified |

## 4. Our Positioning Summary

| Dimension | Existing (dominant) | Ours |
|-----------|--------------------|------|
| **Hardware** | Loihi / TrueNorth / SpiNNaker (ASIC) | FPGA (accessible, reconfigurable) |
| **Task** | Classification / vision / estimation | Control output (PWM, regression) |
| **Training** | Conversion OR evolutionary / RL | Direct surrogate-gradient (deterministic) |
| **Neuron** | CUBA-LIF (2 state) | Simple LIF (1 state), Q4.11 fixed-point |
| **Deployment** | Neuromorphic chip + custom SDK | Custom RTL, full design control |
| **Cost/access** | High, restricted | Low, open toolchain (iverilog/Vivado) |

## 5. Research Gap (Final Statement)

> FPGA par SNN implementation zyada tar **perception/classification** tasks ke liye hai; **SNN-based continuous control** (PWM/actuator commands) — especially **FPGA-deployed** — kafi kam explore hua hai. Neuromorphic UAV/drone control (TU Delft) Loihi jaise ASIC chips pe hai, jo cost/access me limited hain. **Ye thesis ek surrogate-gradient trained, Q4.11 quantized, FPGA-deployed LIF control SNN propose karta hai jo UAV control output (4 PWM: aileron/elevator/rudder/throttle) ko rate-coded spikes se generate karta hai — control domain me FPGA-SNN ka ek naya use-case.**
