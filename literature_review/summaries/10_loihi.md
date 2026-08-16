# Summary: Loihi: A Neuromorphic Manycore Processor with On-Chip Learning

**Authors:** Mike Davies, Narayan Srinivasa, Tsung-Han Lin, et al. (Intel Labs) | **Year:** 2018 | **Type:** Paper (IEEE Micro)

## Overview

Intel ka **Loihi** — 60 mm², 14nm digital neuromorphic chip. 128 neuromorphic cores, 130k neurons, 130M synapses. SNN modeling me state-of-the-art advance — especially **on-chip learning** (programmable synaptic plasticity).

## Key Points

- **Architecture:** 128 neuromorphic cores (mesh), 3 embedded x86 processors, async manycore design
- **Neuron features:** Hierarchical connectivity, dendritic compartments, synaptic delays, threshold adaptation
- **On-chip learning:** Programmable synaptic learning rules (STDP-based), reinforcement traces, reward spikes — inference + learning dono on-chip
- **Efficiency:** LASSO sparse coding problem pe CPU vs Loihi — **>3000x better energy-delay product (EDP)**
- **Key metrics:** 60mm², 14nm, single chip; power consumption very low
- **Programming:** Lava framework (Intel's software stack for neuromorphic)
- **Follow-ups:** Loihi 2 (2021) — 1M neurons, custom microcode, Sigma-Delta conversion support

## Relevance to Our Project

Loihi = flagship neuromorphic ASIC. Humara FPGA implementation **Loihi ke design goals ko cheap, accessible hardware par achieve** karne ki koshish hai:
- Loihi: 130k neurons, on-chip learning, $ expensive, limited access
- Hamara FPGA: 100 neurons (control net), inference-only, $ cheap, full control over RTL
- Fixed-point (Q4.11) = Loihi ki numerical accelerator approach se aligned

## Key Takeaway

Neuromorphic ASICs (Loihi) advanced hain lekin **cost + accessibility barrier** — FPGAs iski functionality ka subset affordable tarike se provide karte hain. Humara work isi "democratization" narrative me fit hota hai.
