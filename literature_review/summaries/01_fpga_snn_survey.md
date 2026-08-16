# Summary: A Survey of Spiking Neural Network Accelerator on FPGA

**Authors:** Murat Isik (Stanford) | **Year:** 2023 | **Type:** Survey (arXiv:2307.03910)

## Overview

Ye survey FPGA par SNN (Spiking Neural Network) deploy karne ke saare modern approaches ko cover karta hai. FPGA customized topology, reconfigurability aur low-power ke liye SNN deployment me popular ho raha hai — especially embedded aur high-performance applications me.

## Key Points

- **Spike coding formats:** Rate coding (input value → spike frequency, sabse common), temporal/latency coding, delta modulation, BSA (binned spike activation) — har format ka trade-off bataya hai
- **Neuron models:** LIF (Leaky Integrate-and-Fire) sabse widely used; Izhikevich, IF bhi covered
- **Hardware design schemes:** Time-multiplexed (resource sharing), fully-parallel, systolic arrays, memory architectures (BRAM/register), compression techniques
- **Training tools:** SNN train karne ke liye ANN→SNN conversion aur surrogate gradient approaches
- **Applications:** Image/audio classification, robotics, event-based vision, biomedical
- **Trends:** Transformer aur GNN jaisi naye architectures ka SNN version FPGA par explore ho raha hai

## Relevance to Our Project

Ye paper **sabse important reference** hai — humara project (control SNN on FPGA) bilkul isi category me hai. Iska section II (spike coding) humare rate-coded LIF approach ko justify karta hai. Humari Q4.11 fixed-point implementation ko yahan ke quantization/compression techniques se position kar sakte hain.

## Key Takeaway

FPGA-based SNN accelerators ki research mostly **classification/vision** pe focus hai — **control applications (jaise drone PWM output) relatively unexplored**, yehi hamara research gap hai.
