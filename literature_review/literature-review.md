# Literature Review

## Neuromorphic Computing and FPGA-Based Spiking Neural Networks for Autonomous UAV Control

---

**Abstract** — Spiking Neural Networks (SNNs) represent a biologically inspired paradigm of computation that processes information through discrete, sparse spike events, offering substantial energy efficiency compared to conventional artificial neural networks (ANNs). This literature review surveys the fundamental concepts of SNNs, their training methodologies, neuromorphic hardware platforms, FPGA-based implementations, and their emerging application in autonomous UAV control. The review identifies a significant research gap: FPGA-based SNN implementations predominantly target perception and classification tasks, while continuous control applications — particularly those generating low-level actuator commands such as PWM signals — remain largely unexplored. This gap motivates the present thesis, which proposes a surrogate-gradient-trained, fixed-point quantized, FPGA-deployed LIF control network for autonomous UAV (fixed-wing) flight.

---

## 1. Introduction

Autonomous UAVs operating in real-world environments face severe constraints on weight, power, and computational capacity. Conventional deep neural network controllers, while effective, impose significant computational and energy burdens that limit deployment on small aerial platforms [Paredes-Vallés et al., 2024]. Spiking Neural Networks offer a promising alternative: they communicate through sparse, asynchronous binary events, closely emulating biological neural computation [Schuman et al., 2017]. This event-driven nature enables orders-of-magnitude reductions in energy consumption when implemented on suitable hardware [Merolla et al., 2014; Davies et al., 2018].

This review is organized as follows. Section 2 presents the theoretical foundations of SNNs, including neuron models and encoding schemes. Section 3 discusses SNN training methodologies. Section 4 surveys neuromorphic hardware platforms. Section 5 reviews FPGA-based SNN implementations. Section 6 examines SNN applications in UAV and robot control. Section 7 presents a gap analysis and the research positioning of this thesis.

## 2. Spiking Neural Networks: Foundations

### 2.1 Neuron Models

The fundamental processing unit of an SNN is the spiking neuron. Among the numerous models ranging from simple to biologically detailed, the **Leaky Integrate-and-Fire (LIF)** neuron is the most widely adopted in hardware implementations due to its computational efficiency and sufficiency for practical tasks [Isik, 2023]. The LIF dynamics are described by:

```
U[t+1] = β·U[t] + Σ wᵢⱼ·sᵢ[t]
sⱼ[t] = 1,  if Uⱼ[t] > θ;  0 otherwise
```

where β is the membrane leak factor (0 < β < 1), U is the membrane potential, w are synaptic weights, s are input spikes, and θ is the firing threshold. A higher β retains more previous state, increasing firing likelihood, while a lower threshold θ reduces the potential required to fire [Neftci et al., 2019]. Other models, including the Izhikevich and Hodgkin-Huxley models, offer greater biological fidelity at substantially higher computational cost [Schuman et al., 2017].

### 2.2 Spike Encoding Schemes

Since real-world signals are continuous, input data must be encoded into spiking form. Isik [2023] identifies five primary encoding formats used in FPGA-based SNN research:

- **Rate coding** — the most widely used format; input value is represented by the firing rate of a Poisson spike train. Higher input values produce higher firing rates.
- **Temporal/latency coding** — information encoded in the precise timing of spikes; larger values fire earlier.
- **Delta modulation, BSA (Binned Spike Activation)**, and other schemes offer latency or precision trade-offs.

Rate coding is preferred for hardware implementations due to its robustness and simplicity, albeit at the cost of requiring multiple timesteps to accumulate statistically meaningful firing rates [Isik, 2023; Fang et al., 2023].

## 3. SNN Training Methodologies

### 3.1 The Non-Differentiability Problem

The binary, discontinuous nature of spike generation (Heaviside step function) makes the spike output non-differentiable, blocking the direct application of backpropagation [Neftci et al., 2019]. The derivative of the step function is zero almost everywhere, causing gradients to vanish.

### 3.2 Surrogate Gradient Learning

The surrogate gradient method resolves this by using the real Heaviside function during the forward pass while substituting a smooth approximation during the backward pass [Neftci et al., 2019]. Common surrogate functions include arctangent, sigmoid, and fast-sigmoid:

```
Forward:   s = Θ(U − θ)                          (real spike)
Backward:  ∂s/∂U ≈ σ′(U − θ)                     (smooth surrogate)
```

This approach enables end-to-end training of deep SNNs without specifying hidden-layer coding schemes, reduces memory-access overhead by allowing local loss functions, and is compatible with neuromorphic hardware [Neftci et al., 2019]. Frameworks such as snnTorch and SpikingJelly operationalize this methodology; SpikingJelly demonstrates up to 11× training speedup over competing frameworks through GPU-optimized spike operations [Fang et al., 2023].

### 3.3 ANN-to-SNN Conversion

An alternative to direct training is converting a pre-trained ANN into a functionally equivalent SNN by replacing ReLU activations with IF/LIF neurons and transferring weights [Rueckauer et al., 2016]. This approach allows inheriting ANN performance without costly retraining. However, it requires many timesteps to approximate the continuous activations, trading latency for accuracy [Rueckauer et al., 2016].

**Critically for this thesis**, Xu et al. [2026] demonstrate that ANN-to-SNN conversion performs poorly in **continuous control** tasks. Performance degradation stems not from instantaneous action errors but from the progressive divergence of induced state trajectories; action approximation errors exhibit positive temporal correlation that amplifies even small conversion errors. This establishes that for continuous control — precisely the domain of autonomous UAV flight — **direct surrogate-gradient training is necessary** rather than ANN-to-SNN conversion.

## 4. Neuromorphic Hardware Platforms

### 4.1 Dedicated Neuromorphic ASICs

Several full-custom neuromorphic chips have advanced the field:

- **TrueNorth (IBM, 2014)**: 5.4-billion-transistor chip with 4096 neurosynaptic cores integrating 1 million programmable neurons and 256 million synapses. Consuming only 63 mW for real-time video processing, it established the energy-efficiency potential of digital neuromorphic hardware [Merolla et al., 2014].
- **Loihi (Intel, 2018)**: A 60 mm² 14-nm digital chip with 128 neuromorphic cores, hierarchical connectivity, dendritic compartments, and — most notably — programmable on-chip learning rules (STDP and reinforcement learning traces) [Davies et al., 2018]. Loihi demonstrated over three orders of magnitude improvement in energy-delay product over conventional solvers on sparse coding problems.
- **SpiNNaker (Manchester, 2013)**: An ARM-based processor array scaled from 1 million cores (SpiNNaker1, 130 nm) toward a 10-million-core system (SpiNNaker2, 22 nm FDSOI), providing software-defined neuron simulation flexibility [Mayr et al., 2019].
- **DYNAPs and BrainScaleS-2**: Additional research platforms exploring scalable multicore asynchronous designs and accelerated mixed-signal analog simulation respectively.

While these ASICs are technically advanced, their cost and restricted availability limit accessibility for research and deployment [Isik, 2023; Schuman et al., 2017].

### 4.2 Comparison of Neuromorphic Platforms

| Platform | Year | Scale | Power / Efficiency | Learning |
|----------|------|-------|-------------------|----------|
| TrueNorth (IBM) | 2014 | 1M neurons, 256M synapses | 63 mW; 46G SOPS/W | Inference |
| Loihi (Intel) | 2018 | 130k neurons | >3000× EDP vs CPU | On-chip (STDP/RL) |
| SpiNNaker1/2 | 2013/19 | 1M–10M cores | Highly efficient | Software-defined |
| BrainScaleS-2 | 2022 | ~512 analog neurons | Accelerated | Hybrid plasticity |

## 5. FPGA-Based SNN Implementations

FPGAs have emerged as a compelling platform for SNN deployment, offering custom topology, reconfigurability, low power, and lower non-recurring engineering costs compared to ASICs [Isik, 2023; Guo et al., 2017]. The main hardware design schemes for FPGA-based SNN accelerators include:

- **Time-multiplexed architectures** that share computation resources across neurons, trading throughput for area efficiency.
- **Fully-parallel architectures** that instantiate every neuron, maximizing throughput.
- **Fixed-point quantization** of weights and activations (e.g., integer-only arithmetic) to reduce resource usage while preserving accuracy — a technique aligned with the approaches in [Guo et al., 2017; Fang et al., 2023].

Recent open-source frameworks demonstrate lightweight FPGA SNN implementations using as few as 13K LUTs, training on low-end FPGA boards via snnTorch with subsequent quantization and RTL generation [Snn-FPGA, 2025].

The survey by Isik [2023] enumerates FPGA-SNN applications across speech recognition, biomedical analysis, and self-driving vehicles. **Notably, the surveyed application instances are predominantly classification and perception tasks**; control-oriented deployments that map sensor input to actuator commands remain comparatively rare.

## 6. SNN Applications in UAV and Robot Control

Neuromorphic computing holds particular promise for small autonomous UAVs, where energy and weight budgets are severe [Paredes-Vallés et al., 2024]. Several works have progressed toward SNN-based flight control:

- **Dupeyroux et al. [2021]** demonstrated optic-flow-based landing of micro air vehicles using the Loihi processor.
- **Stagsted et al. [2020]** proposed spiking PID controllers for UAVs.
- **Stroobants et al. [2024/25]** developed a modular SNN for quadrotor attitude estimation and control, training estimation and control sub-networks separately via imitation learning and merging them. Deployed on a Crazyflie at 500 Hz, the SNN achieved an average tracking error of ~3° compared to 2.5° for the conventional flight stack, with only 15% spiking activity.
- **Paredes-Vallés et al. [2024]** (Science Robotics) demonstrated the first fully neuromorphic vision-to-control pipeline for autonomous drone flight. A five-layer SNN (28.8k neurons) processing raw event-camera data, trained via self-supervised learning, was combined with an SNN control layer trained through an evolutionary algorithm. The complete pipeline ran onboard on Intel Loihi at 200 Hz, consuming only **27 µJ per inference**, and successfully achieved hovering, landing, and sideway maneuvering with sim-to-real transfer.
- **Mengozzi et al. [2025]** showed that PPO-trained SNN policies for agile quadrotor flight achieve 2.5% higher success rate, 40% higher average flight speed, and 28.6% less time-to-target than ANN-based policies in simulation.

These results establish the feasibility and energy-efficiency advantage of neuromorphic UAV control, but they rely on dedicated neuromorphic ASICs (predominantly Loihi) or software simulation. FPGA-deployed SNN controllers for low-level UAV control have not been systematically demonstrated.

## 7. Gap Analysis and Research Positioning

### 7.1 Identified Research Gaps

1. **Task domain**: FPGA-based SNN implementations overwhelmingly target classification and perception. Continuous control outputs — such as PWM actuator commands for flight controllers — are underexplored in the FPGA-SNN literature [Isik, 2023].
2. **Training methodology**: ANN-to-SNN conversion, common in SNN deployment, is demonstrably unsuitable for continuous control due to error amplification [Xu et al., 2026], yet direct-training approaches for control remain sparse.
3. **Hardware platform**: Neuromorphic UAV control has been demonstrated on Loihi and microcontrollers [Paredes-Vallés et al., 2024; Stroobants et al., 2024], but the affordable, reconfigurable FPGA alternative has not been systematically applied to this problem.

### 7.2 Positioning of This Thesis

This thesis addresses the identified gaps by proposing a **surrogate-gradient-trained, fixed-point (Q4.11) quantized, FPGA-deployed LIF control network** for autonomous UAV control. The contributions are:

- A three-layer LIF control network (6→64→32→4) mapping 6-DoF optical-flow sensory inputs to four PWM control-surface commands (aileron, elevator, rudder, throttle) through rate-coded spike accumulation.
- Direct surrogate-gradient training using snnTorch, justified by the demonstrated unsuitability of ANN-to-SNN conversion for continuous control.
- A fully custom RTL implementation (SystemVerilog) with verified simulation, providing a cost-effective, accessible alternative to dedicated neuromorphic ASICs.
- Bridging the control-domain gap in FPGA-based SNN research.

## 8. Conclusion

This literature review surveyed SNN foundations, training methods, neuromorphic hardware, FPGA implementations, and neuromorphic UAV control. It established that while SNNs trained via surrogate gradients and deployed on neuromorphic chips demonstrate compelling energy efficiency for UAV control, a clear gap exists in **FPGA-based SNN implementations for continuous control tasks**. This thesis positions itself precisely within this gap, contributing a fixed-point quantized, FPGA-deployed LIF control network for autonomous UAVs.

---

## References

1. Davies, M., et al. "Loihi: A Neuromorphic Manycore Processor with On-Chip Learning." *IEEE Micro* 38(1): 82–99, 2018.
2. Dupeyroux, J., et al. "Neuromorphic Control for Optic-Flow-Based Landing of MAVs Using the Loihi Processor." *ICRA*, 2021.
3. Fang, W., et al. "SpikingJelly: An Open-Source Machine Learning Infrastructure Platform for Spike-Based Intelligence." *Science Advances* 9, eadi1480, 2023.
4. Guo, K., et al. "A Survey of FPGA-Based Neural Network Inference Accelerator." *ACM TRETS*, 2017.
5. Isik, M. "A Survey of Spiking Neural Network Accelerator on FPGA." *arXiv:2307.03910*, 2023.
6. Mayr, C., Höppner, S., and Furber, S. "SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning." *arXiv:1911.02385*, 2019.
7. Mengozzi, S., et al. "Bio-Inspired Drone Control: A Reinforcement Learning-Trained Spiking Neural Network for Agile Navigation." *IEEE COINS*, 2025.
8. Merolla, P. A., et al. "A Million Spiking-Neuron Integrated Circuit with a Scalable Communication Network and Interface." *Science* 345(6197): 668–673, 2014.
9. Neftci, E. O., Mostafa, H., and Zenke, F. "Surrogate Gradient Learning in Spiking Neural Networks." *IEEE Signal Processing Magazine* 36(6): 51–63, 2019.
10. Paredes-Vallés, F., et al. "Fully Neuromorphic Vision and Control for Autonomous Drone Flight." *Science Robotics* 9(90): eadi0591, 2024.
11. Rueckauer, B., et al. "Theory and Tools for the Conversion of Analog to Spiking Convolutional Neural Networks." *arXiv:1612.04052*, 2016.
12. Schuman, C. D., et al. "A Survey of Neuromorphic Computing and Neural Networks in Hardware." *arXiv:1705.06963*, 2017.
13. Stroobants, S., De Wagter, C., and de Croon, G. C. H. E. "Neuromorphic Attitude Estimation and Control." *IEEE RA-L*, 2025.
14. Stagsted, R., et al. "Towards Neuromorphic Control: A Spiking Neural Network Based PID Controller for UAVs." *RSS*, 2020.
15. Xu, Z., et al. "Error Amplification Limits ANN-to-SNN Conversion in Continuous Control." *arXiv:2601.21778*, 2026.
16. "A Robust, Open-Source Framework for Spiking Neural Networks on Low-End FPGAs." *arXiv:2507.07284*, 2025.
