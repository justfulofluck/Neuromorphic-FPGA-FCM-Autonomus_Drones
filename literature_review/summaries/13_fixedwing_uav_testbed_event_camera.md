# Summary: Development of a Fixed-Wing UAV Testbed for In-Flight Data Collection from an Event-Based Camera

**Authors:** J. Coen et al. (AERoSysLab) | **Year:** 2026 | **Type:** Conference Paper

## Overview

**Sabse pehla reported application of an event camera on a fixed-wing UAV.** Fixed-wing platforms ki aviation-specific perception (collision avoidance, aerial imaging) degraded in high-dynamic-range conditions — event camera ise solve karta hai. Platform + synchronized event/frame/IMU-GNSS data collection framework establish kiya.

## Key Points

- **Platform:** 26% scale Cub Crafters CC11-100 Sport Cub S2, outfitted with Triton2 EVS 0.9MP event camera + HD global shutter RGB frame camera + Xsens IMU/GNSS unit — SWaP (Size, Weight, Power) optimized
- **Motivation:** Event-based vision aerial me ab tak **mostly multi-rotor** pe limited tha; fixed-wing dynamics (long endurance, high altitude, high speed) alag challenges dete hain (rolling-shutter artifacts, motion blur, overexposure)
- **Key result:** Flying into the sun — frame camera overexposed (sky/objects invisible), **event camera retained feature visibility and data integrity**
- **Findings:** IMU for event motion-compensation needs ≥100 Hz update; global-shutter frame camera required for fair comparison
- **Contribution:** First foundational framework for event-camera integration on fixed-wing; enables future aviation perception research (collision avoidance, photogrammetry, localization)

## Relevance to Our Project

- Prove karta hai ki **event-driven front-end fixed-wing UAV ke liye feasible hai** (visual obstruction problems solve).
- Hamari architecture: event camera → vision → control. Iska data-collection methodology + fixed-wing platform setup hamare **future PX4/Gazebo fixed-wing SITL integration** aur real-platform deployment ke liye reference hai.
- Fixed-wing pe event-based perception ka **research gap** yahan explicitly stated — hamara FPGA SNN controller isi gap ke control side me baitha hai.

## Key Takeaway

Event camera fixed-wing pe **first-time proven** — motor bhaar ke sense me bada kaam nahi, par perception side ka foundation hai. Fixed-wing + event-driven ka union ab research frontier hai, aur humara **FPGA-SNN control** ussi frontier ka missing piece.