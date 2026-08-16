# Summary: Fully Neuromorphic Vision and Control for Autonomous Drone Flight

**Authors:** Federico Paredes-Vallés, Jesse Hagenaars, Julien Dupeyroux, Stein Stroobants, Yingfu Xu, Guido C. H. E. de Croon (TU Delft) | **Year:** 2023 (arXiv) / 2024 (Science Robotics) | **Type:** Research Article

## Overview

**Landmark paper** — pehli baar drone ne **fully neuromorphic** pipeline se udana seekha: event camera se raw spike data → 5-layer SNN vision → SNN control → motor commands. Sab kuch Intel Loihi neuromorphic chip par onboard.

## Key Points

- **Pipeline:** Event camera (DVS) → SNN vision (5 layers, 28.8k neurons, self-supervised ego-motion estimation) → SNN control (single decoding layer, evolutionary algorithm se trained in simulator) → motor commands
- **Training:** Vision = self-supervised on real event data; Control = evolutionary algorithm in drone simulator; **sim-to-real transfer successful**
- **Hardware:** Intel Loihi, 200 Hz execution, **only 27 µJ per inference**
- **Results:** Drone can hover, land, maneuver sideways, yaw — tracking ego-motion setpoints
- **Performance claim:** DNN data processing 64x faster, 3x less energy vs GPU
- **Limitation:** Earlier versions controlled only vertical motion; this one does 3D ego-motion + control

## Relevance to Our Project

**Ye hamara ultimate benchmark / competing work hai.** Comparison:
- Unhone event camera + vision + control full neuromorphic (Loihi) — hum control-only (FPGA)
- Unhone Loihi ASIC use kiya — hum **FPGA** (accessible, cheaper)
- Unhone 27µJ/inference pe claim — hum FPGA par resource/power efficiency show kar sakte hain
- Unka control SNN small (single decoding layer) — hamara 3-layer control SNN

## Key Takeaway

Science Robotics level par publish proof hai ki **neuromorphic drone control is real and important**. Humara contribution: similar control task ko **FPGA (custom RTL, fixed-point Q4.11)** par implement karna — ASIC ki jagah cost-effective alternative.
