# Summary: Surrogate Gradient Learning in Spiking Neural Networks

**Authors:** Emre O. Neftci, Hesham Mostafa, Friedemann Zenke | **Year:** 2019 | **Type:** Tutorial/Review (IEEE Signal Processing Magazine)

## Overview

SNN train karne me sabse badi problem: spikes binary (0/1) hain aur non-differentiable — backpropagation directly kaam nahi karta. Ye paper **surrogate gradient method** explain karta hai jo spike step function ki jagah smooth approximation use karke gradient flow allow karta hai.

## Key Points

- **Problem:** Heaviside step function ka derivative almost everywhere 0 hai → gradient vanish → training impossible
- **Solution (Surrogate Gradient):** Forward pass me real spike (Heaviside), backward pass me smooth surrogate function ka derivative (arctan, sigmoid, fast-sigmoid)
- **Advantages:**
  - End-to-end training, koi coding scheme specify nahi karni padti
  - Memory access overhead kam (global loss ki jagah local losses)
  - Neuromorphic hardware ke liye compatible
- **Comparison:** Hebbian/STDP learning (online, biology-based) vs surrogate gradient (supervised, backprop-based)
- snnTorch aur SpikingJelly dono isi method par based hain

## Relevance to Our Project

Humara Python model (snnTorch `snn.Leaky`) surrogate gradient se hi trained hai. Ye paper humari training methodology ka theoretical foundation hai — thesis me training section likhne ke liye essential citation.

## Key Takeaway

Surrogate gradient = SNN me deep learning ki power. Humne `snn.Leaky` with default surrogate use kiya — thesis me yeh justify karna hai ki kaunsa surrogate aur kyun.
