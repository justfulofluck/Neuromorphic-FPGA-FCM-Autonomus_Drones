# Summary: SpikingJelly: An Open-Source Machine Learning Infrastructure Platform for Spike-Based Intelligence

**Authors:** Wei Fang, Yanqi Chen, Jianhao Ding, Ding Chen, Zhaofei Yu, Huihui Zhou, Timothée Masquelier, Yonghong Tian, et al. | **Year:** 2023 | **Type:** Framework paper (arXiv:2310.16620 / Science Advances)

## Overview

SpikingJelly — Peking University ka PyTorch-based full-stack SNN framework. Neuromorphic datasets process karna, deep SNN banana, GPU par efficient simulate karna, aur neuromorphic chips par deploy karna — sab ek platform me.

## Key Points

- **Full-stack:** Dataset preprocessing → network construction → training → deployment (Lava, NIR exchange, Lynxi chips)
- **High-performance simulation:** GPU par optimized spike operations; Spiking ResNet-18 training me Norse/snnTorch se up to 11x faster
- **Neuron models:** LIF, IF, and others with surrogate gradient support
- **Encoders:** Latency encoder, Poisson encoder (rate coding)
- **Datasets:** CIFAR10-DVS, N-MNIST, SHD, Spiking Heidelberg datasets etc.
- **Interchange:** NIR (Neuromorphic Intermediate Representation) standard — models ko different platforms ke beech port karna

## Relevance to Our Project

Humne **snnTorch** use kiya, SpikingJelly nahi — dono same surrogate-gradient philosophy par hain. Ye paper useful hai:
1. Framework comparison section ke liye (snnTorch vs SpikingJelly vs Norse)
2. Surrogate gradient + encoding techniques ka technical reference
3. Quantization/deployment modules — future FPGA integration me help kar sakta hai

## Key Takeaway

Modern SNN frameworks ne training ko mature bana diya hai. Research ab **training se hardware deployment** ki taraf shift ho rahi hai — humara FPGA pipeline isi direction ka kaam hai.
