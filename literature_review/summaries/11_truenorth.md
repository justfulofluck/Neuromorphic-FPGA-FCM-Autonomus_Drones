# Summary: A Million Spiking-Neuron Integrated Circuit with a Scalable Communication Network and Interface

**Authors:** Paul A. Merolla, John V. Arthur, Rodrigo Alvarez-Icaza, et al. (IBM) | **Year:** 2014 | **Type:** Research Article (Science)

## Overview

**TrueNorth** — IBM ka neuromorphic chip: 5.4 billion transistors, 28nm, 4096 neurosynaptic cores, **1 million programmable neurons + 256 million synapses**. Ye field-defining paper hai — digital neuromorphic computing ka milestone.

## Key Points

- **Architecture:** 4096 neurosynaptic cores, each with local SRAM (neuron states, synapses, routing), event-driven async communication
- **Scale:** 1M neurons, 256M synapses, 4.3 cm², 428M bits on-chip memory
- **Power:** Ultra-low — video (400×240 @30fps) processing pe **63 mW** total; power density 20 mW/cm² (vs CPU 50-100 W/cm²)
- **Efficiency:** 46 billion SOPS/watt (synaptic operations per second per watt) — 10x+ more efficient than best supercomputers
- **Scalability:** Chips 2D me tile ho sakte hain — arbitrary size cortex-like sheet
- **Configurability:** Connectivity aur neural parameters fully configurable; non-plastic synapses (inference only)
- **Applications:** Real-time multi-object detection/classification (Neovision2 Tower dataset)

## Relevance to Our Project

TrueNorth ne prove kiya ki **large-scale digital SNN feasible + ultra energy-efficient hai**. Historical context ke liye essential:
- Digital (deterministic) neuron approach = hamari approach (deterministic LIF, no analog noise)
- 1M neurons vs hamare ~100 — humara control network tiny hai, isliye FPGA pe easily fit
- "Chip se FPGA" = same principles, different implementation target

## Key Takeaway

TrueNorth (2014) ne scale + power efficiency ka proof diya. Ab 10 saal baad, **FPGA-based edge deployment** (humara work) isi vision ka practical, accessible extension hai.
