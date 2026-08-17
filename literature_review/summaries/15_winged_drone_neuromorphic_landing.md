# Summary: Neuromorphic Vision for Autonomous Flight and Landing on a Winged Drone

**Authors:** Alessandro Marchei (Politecnico di Torino, MSc thesis) — Supervisors: Prof. Marcello Chiaberge (Polito), Prof. Dario Floreano, Dr. Charbel Toumieh, Simon Jeger (EPFL LIS) | **Year:** October 2024 | **Type:** Master's Thesis (Open access — webthesis.biblio.polito.it)

## Overview

**Event-based (neuromorphic) vision for fixed-wing autonomous landing.** Event camera fixed-wing pe real-time optical flow → altitude estimation + autonomous landing. Ye thesis hi Jeger et al. 2026 (*Advanced Intelligent Systems*) journal paper ka source work hai.

## Key Points

- **Platform:** Bixler 3 fixed-wing drone, Pixhawk 4 flight controller, **DVXplorer Micro event camera** (640×480, 45° downward tilt — ahead+ground patch, non-trivial configuration)
- **Pipeline:** Raw event stream → **sparse Lucas-Kanade optical flow** (chosen over learning-based for accuracy/compute balance) → **gyroscopic derotation** → **adaptive slicing** (event-rate-dependent temporal window) → altitude estimation → control
- **Challenge:** Fixed-wing high speed → up to **40 million events per second (MEPS)** — real-time processing on lightweight embedded hardware me bara constraint
- **Control:** TECS (Total Energy Control System) controller for altitude regulation
- **Results:** Robust altitude estimation + landing in **full daylight AND low-light (30 lux)** conditions; NC matches conventional camera at 100k lux, **beats it in low light** where frame camera fails
- **Method sensitivity:** Event time resolution + sensor sensitivity trade-offs analyzed

## Relevance to Our Project

**Hamare architecture ka closest real-world analog:**
- Unkay: Event camera → optical flow → altitude/landing control (**conventional CV + embedded CPU**)
- Hamara: Event camera → 6-DoF → **SNN control network → PWM (FPGA)**
- Woh **fixed-wing UAV** pe end-to-end event-driven flight control prove karta hai — hamara target same platform
- Diff: unka processing CPU/Raspberry-Pi class hai; hamara **FPGA + spiking** hai → energy/latency argument thesis me
- Fixed-wing me event-rate scalability (20–40 MEPS) — hamare Q4.11 fixed-point + time-window design ke liye design constraint reference

## Key Takeaway

Fixed-wing + event camera + real-time control **already flying in real world** (landing + altitude, low-light me bhi). Yeh hamare thesis assumption validate karta hai ki event-driven fixed-wing control feasible hai — abhi missing piece: **neuromorphic (spiking) + FPGA control layer**, jo hum provide karte hain.