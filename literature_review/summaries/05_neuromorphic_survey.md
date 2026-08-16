# Summary: A Survey of Neuromorphic Computing and Neural Networks in Hardware

**Authors:** Catherine D. Schuman, Thomas E. Potok, Robert M. Patton, J. Douglas Birdwell, Mark E. Dean, Garrett S. Rose, James S. Plank | **Year:** 2017 | **Type:** Survey (arXiv:1705.06963)

## Overview

Ye **bada survey** (88 pages) — neuromorphic computing ke pura field ko cover karta hai: hardware architectures, neuron/synapse models, learning algorithms, aur applications. Neuromorphic research ka "bible" maan sakte hain.

## Key Points

- **Neuromorphic hardware architectures:**
  - Analog (subthreshold circuits — Mead ka concept) vs Digital (deterministic, jaise TrueNorth)
  - Arrays/cores, crossbars (memristor-based), FPGA implementations
- **Neuron models:** From simple (IF, LIF) to complex (Hodgkin-Huxley, Izhikevich) — complexity vs biological fidelity trade-off
- **Synaptic models:** Weights, delays, plasticity (STDP, reward-modulated)
- **Learning approaches:** Unsupervised (STDP), supervised, reinforcement learning on hardware
- **FPGA-based neuromorphic systems** as a dedicated category — reprogrammable, rapid prototyping
- **Challenges:** Scalability, non-volatile memory, lack of standard tools/frameworks

## Relevance to Our Project

Ye survey thesis ke **literature review chapter ka backbone** hai. Humari LIF neuron choice (Section: neuron models), fixed-point implementation (quantization), aur FPGA platform selection isme position ho sakti hai. Systematic background ke liye best single reference.

## Key Takeaway

Neuromorphic field mature ho raha hai but **standardization abhi nahi** — har system apne neuron model, encoding, toolchain use karta hai. Humara approach (snnTorch → Q4.11 RTL → FPGA) ek clean, practical pipeline demonstrate karta hai.
