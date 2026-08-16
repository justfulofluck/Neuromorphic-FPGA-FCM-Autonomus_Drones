# Summary: Neuromorphic Attitude Estimation and Control

**Authors:** S. Stroobants, C. De Wagter, G. C. H. E. de Croon (TU Delft, Micro Air Vehicle Lab) | **Year:** 2024/2025 | **Type:** Paper (IEEE RA-L, arXiv:2411.13945)

## Overview

**Sabse directly relevant paper** — TU Delft ne Crazyflie micro-drone par fully-spiking SNN se end-to-end attitude estimation + control deploy kiya. SNN raw sensor input se directly motor commands map karta hai — humari problem ke bilkul same!

## Key Points

- **System:** Modular SNN = (a) attitude estimation sub-network (2 layers, recurrent) + (b) attitude control sub-network (1 layer, recurrent) — dono ko train karke merge kiya
- **Training:** Imitation learning (flight dataset of sensory-motor pairs) + data augmentation (excitation flying, time-shifted targets)
- **Neuron model:** CUBA-LIF (current-based LIF) — Loihi's default model
- **Deployment:** Crazyflie drone par 500 Hz pe control commands; currently Teensy microcontroller pe runs
- **Performance:** Average tracking error ~3° (vs 2.5° for regular flight stack); spiking activity 15% (energy-efficient)
- **Key insights:**
  - Leak & threshold parameters ko integrators ki tarah constrain karna → faster convergence
  - k-step advance action prediction → SNN inherent delays mitigate
  - Energy order-of-magnitude me PID controller ke barabar

## Relevance to Our Project

**Ye paper literally hamara "competing work" + inspiration hai.** Same architecture: sensor input → SNN → motor/PWM commands. Comparison points:
- Unhone CUBA-LIF (2 state vars) use kiya, hum simple LIF (1 state var)
- Unhone Loihi/Teensy use kiya, hum FPGA
- Unhone attitude estimation + control dono, hum control focus

## Key Takeaway

SNN-based drone control **feasible hai aur real hardware par kaam karta hai**. Humara differentiation: **FPGA-based LIF controller + PWM output**, unka Loihi/Teensy. Ye paper prove karta hai ki hamara research direction valid hai.
