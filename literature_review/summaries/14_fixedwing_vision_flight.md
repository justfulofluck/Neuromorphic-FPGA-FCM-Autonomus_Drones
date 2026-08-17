# Summary: Accurate Vision-based Flight with Fixed-Wing Drones

**Authors:** Valentin Wüest, Enrico Ajanic, Matthias Müller, Dario Floreano (EPFL LIS) | **Year:** 2022 (IROS) | **Type:** Conference Paper (Open access — Infoscience EPFL)

## Overview

**Fixed-wing drones ke liye vision-based control** — GNSS (~3 m error) perching/object-pickup jaise precise maneuvers ke liye kaafi coarse hai; RTK GNSS ko ground stations chahiye. Paper fixed-wing platform propose karta hai jo long-range me GNSS aur target-pas aate hi **vision-based control** use karta hai — accuracy me ek order-of-magnitude improvement.

## Key Points

- **Problem:** GNSS navigation error ~3.033 m → fixed-wing pe precise maneuvers (perch, pickup, gap follow) impossible
- **Method:** GNSS long-range approach → switch to vision-based control for accurate target reaching
- **Platform:** Custom fixed-wing with onboard computation; open-sourced (github.com/lis-epfl/lis-vision-flight)
- **Results (GNSS-vision vs GNSS-only):**
  - Accuracy: **0.283 m** vs 3.033 m (10× better)
  - Precision (variance across flights): **0.309 m** vs 2.095 m
  - Horizontal error < 0.5 m, vertical < 0.25 m
  - Performance **on par with RTK GNSS** (jo ground stations demand karta hai) — bina infrastructure ke
- **Robustness:** Vision control compensated 2 m GNSS offsets reliably (confidence-ellipse analysis)

## Relevance to Our Project

- Demonstrates a **complete vision→control pipeline on a fixed-wing UAV** — platform where hamara SNN controller target karta hai.
- Unka control conventional (frame camera + classical perception); hamara approach **event-driven + SNN on FPGA** — direct contrast point for thesis positioning.
- Fixed-wing control me **low-level actuator commands** ki jagah navigation-level switching use — gap: neuromorphic low-level fixed-wing actuator control (aileron/elevator/rudder/throttle) missing.

## Key Takeaway

Vision-based fixed-wing control real-world me **proven + on par with RTK GNSS** — fixed-wing platforms ab vision/neuromorphic control ke liye mature hain. Iska matlab navigation-side work exist karta hai, par **FPGA-deployed spiking control** layer abhi bhi missing — wahi hamara contribution.