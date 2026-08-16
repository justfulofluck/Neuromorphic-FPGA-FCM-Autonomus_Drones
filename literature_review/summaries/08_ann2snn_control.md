# Summary: Error Amplification Limits ANN-to-SNN Conversion in Continuous Control

**Authors:** Zijie Xu, Zihan Huang, Yiting Dong, Kang Chen, Wenxuan Liu, Zhaofei Yu | **Year:** 2026 | **Type:** Paper (arXiv:2601.21778)

## Overview

Ye paper investigate karta hai ki **ANN→SNN conversion continuous control (RL) tasks me kyun fail hota hai**. Classification me conversion kaam karta hai, but continuous control (high-dimensional vector actions) me accuracy degrade ho jati hai.

## Key Points

- **Problem:** Continuous control me action space high-dimensional, precise, vector-valued → conversion errors se bahut sensitive
- **Root cause analysis:**
  1. Performance degradation state trajectories ke divergence se hota hai, instant action errors se nahi
  2. State deviations har decision step pe accumulate/amplify hote hain
  3. Action approximation errors me positive temporal correlation → chhote errors bhi amplify
- **Finding:** Converted SNN policies ke trajectories ANN policies se gradually diverge karte hain
- **Implication:** Existing conversion techniques continuous control ke liye unsuitable hain

## Relevance to Our Project

Ye paper **directly hamari architecture choice justify karta hai**:

1. Humne ANN→SNN conversion NAHI use kiya — direct surrogate-gradient training kiya, jo is error amplification se bachta hai
2. Humara task bhi continuous control hai (PWM commands) — is paper ke anusaar conversion approach iska galat method hota
3. Thesis me citation ke liye perfect — "why we trained directly instead of converting"

## Key Takeaway

Continuous control + SNN = **direct training zaroori hai, conversion nahi chalega**. Humari direct-trained Q4.11 SNN is research gap ka ek solution hai — strong novelty point.
