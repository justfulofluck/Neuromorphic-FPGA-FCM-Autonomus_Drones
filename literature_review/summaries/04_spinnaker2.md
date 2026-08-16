# Summary: SpiNNaker 2: A 10 Million Core Processor System for Brain Simulation and Machine Learning

**Authors:** Christian Mayr, Sebastian Höppner, Steve Furber | **Year:** 2019 | **Type:** Paper (arXiv:1911.02385)

## Overview

SpiNNaker (Spiking Neural Network Architecture) — Manchester University ka neuromorphic platform. Ye paper SpiNNaker1 (1M cores) se SpiNNaker2 (10M cores, 22nm FDSOI) ke roadmap ka brief hai.

## Key Points

- **Architecture:** ARM processor cores ka large-scale array; har core neurons simulate karta hai, lightweight spike-optimized asynchronous protocol se communicate
- **SpiNNaker1:** 1 million ARM processors, 130nm, ~1% human brain scale, 1ms timestep (real-time biology)
- **SpiNNaker2:** 10M cores, 144 ARM M4F processors/chip, 18MB SRAM + 8GB DRAM
- **Optimizations:**
  - Numerical accelerators (exp function, random number generation) — fixed-point hardware
  - Runtime adaptive body biasing → power efficiency (10x better)
  - 50x capacity increase in same power budget
- **Philosophy:** Processor-based flexibility (software-defined neurons) vs TrueNorth/Loihi jaise streamlined approaches

## Relevance to Our Project

**SpiNNaker = expensive multi-chip system.** Humara project isse **FPGA-based cheaper alternative** ke roop me position kar sakta hai. SpiNNaker/TrueNorth/Loihi ASIC chips cost aur availability me limited hain — FPGA = accessible, reconfigurable, same SNN principles.

## Key Takeaway

Neuromorphic platforms ke do camps: (1) custom ASIC chips (Loihi, TrueNorth, SpiNNaker) — powerful but costly, (2) FPGA — flexible, affordable, research-friendly. Hum FPGA camp me hain.
