# Literature Review — FPGA-Based Event-Driven Neuromorphic Flight Controller for Autonomous UAVs

MTech project ka literature review. Papers `papers/` folder me organized hain, summaries `summaries/` me, aur **submission-ready document `literature-review.md`** me.

## 📄 Submission Document

**`literature-review.md`** — ek complete literature review paper (prose, 8 sections + references). Yehi final submission ke liye hai.

## Paper Index

| # | File | Paper | Year | Area |
|---|------|-------|------|------|
| 01 | `papers/01_fpga_snn_survey.pdf` | A Survey of Spiking Neural Network Accelerator on FPGA (Isik) | 2023 | FPGA-SNN accelerators |
| 02 | `papers/02_surrogate_gradient.pdf` | Surrogate Gradient Learning in Spiking Neural Networks (Neftci et al.) | 2019 | SNN training |
| 03 | `papers/03_ann2snn_conversion.pdf` | Theory and Tools for the Conversion of Analog to Spiking CNNs (Rueckauer et al.) | 2016 | ANN→SNN conversion |
| 04 | `papers/04_spinnaker2.pdf` | SpiNNaker 2: A 10 Million Core Processor System (Mayr et al.) | 2019 | Neuromorphic hardware |
| 05 | `papers/05_neuromorphic_survey.pdf` | A Survey of Neuromorphic Computing and Neural Networks in Hardware (Schuman et al.) | 2017 | Neuromorphic computing survey |
| 06 | `papers/06_spikingjelly.pdf` | SpikingJelly: An open-source ML infrastructure for spike-based intelligence (Fang et al.) | 2023 | SNN frameworks |
| 07 | `papers/07_neuromorphic_attitude.pdf` | Neuromorphic Attitude Estimation and Control (Stroobants et al., TU Delft) | 2024 | SNN UAV control |
| 08 | `papers/08_ann2snn_control.pdf` | Error Amplification Limits ANN-to-SNN Conversion in Continuous Control | 2026 | ANN→SNN control |
| 09 | `papers/09_neuromorphic_drone_flight.pdf` | Fully Neuromorphic Vision and Control for Autonomous Drone Flight (Paredes-Vallés et al., TU Delft) | 2023/24 | SNN UAV control |
| 10 | `papers/10_loihi.pdf` | Loihi: A Neuromorphic Manycore Processor with On-Chip Learning (Davies et al.) | 2018 | Neuromorphic hardware |
| 11 | `papers/11_truenorth.pdf` | A Million Spiking-Neuron Integrated Circuit (Merolla et al., IBM TrueNorth) | 2014 | Neuromorphic hardware |
| 12 | *(PDF paywalled — cited only)* | High-Speed Altitude Regulation with Neuromorphic Camera and Lightweight Embedded Computation (Jeger et al., EPFL) | 2026 | Fixed-wing event-driven control |
| 13 | `papers/13_fixedwing_uav_testbed_event_camera.pdf` | Development of a Fixed-Wing UAV Testbed for In-Flight Data Collection from an Event-Based Camera (Coen et al.) | 2026 | Fixed-wing event camera (first) |
| 14 | `papers/14_fixedwing_vision_flight.pdf` | Accurate Vision-based Flight with Fixed-Wing Drones (Wüest et al., EPFL) | 2022 | Fixed-wing vision control |
| 15 | `papers/15_winged_drone_neuromorphic_landing.pdf` | Neuromorphic Vision for Autonomous Flight and Landing on a Winged Drone (Marchei, Polito/EPFL) | 2024 | Fixed-wing neuromorphic landing |

## Topic → Paper Mapping (LR structure ke liye)

- **SNN theory / neuron models**: 01 (Sec II), 05, 02
- **SNN training (surrogate gradient)**: 02, 06
- **ANN→SNN conversion**: 03, 08
- **Neuromorphic chips (ASIC)**: 10 (Loihi), 11 (TrueNorth), 04 (SpiNNaker2)
- **FPGA implementations**: 01, 06 (deployment), 05
- **UAV control with SNN**: 07, 09, 08
- **Fixed-wing UAV (event-driven / vision) control**: 15, 12, 13, 14
- **Frameworks/tools**: 06 (SpikingJelly)

## Summaries

Har paper ka detailed summary `summaries/` me hai (01_*.md to 15_*.md) — Overview, Key Points, Relevance to Our Project, aur Key Takeaway ke saath.

## Comparative Table

`comparative_table.md` — ASIC platforms, FPGA-SNN works, UAV control systems ka comparison + research gap statement. Thesis LR ka key figure.

## Next Steps

- [x] Har paper ka 1-paragraph summary `summaries/` me
- [x] Comparative table (year, hardware, method, power/accuracy)
- [ ] Gap analysis / research positioning
