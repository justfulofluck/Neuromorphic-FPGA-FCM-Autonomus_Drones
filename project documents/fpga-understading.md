# FPGA part

## Read RTL files to explain them well

- Read fpga/rtl/lif_neuron.sv
- Read fpga/rtl/linear_lif.sv
- Read fpga/rtl/control_snn.sv

## Then we will explain them in simple words

File Structure
fpga/
├── export/          ← Python se export kiye weights (Q4.11 hex .mem files)
│   ├── fc1_weight.mem  (384 values = 6×64)
│   ├── fc1_bias.mem    (64 values)
│   ├── fc2_weight.mem  (2048 values = 64×32)
│   ├── fc2_bias.mem    (32 values)
│   ├── fc3_weight.mem  (128 values = 32×4)
│   └── fc3_bias.mem    (4 values)
├── rtl/             ← RTL (Register Transfer Level) code — digital circuit design
│   ├── lif_neuron.sv    ← Ek LIF neuron ka circuit
│   ├── linear_lif.sv    ← Ek linear layer + neuron array
│   └── control_snn.sv   ← Top module — 3 layers ka chain + controller
├── tb/              ← Testbench code (stimulus + check)
│   └── tb_control_snn.sv
└── sim/             ← Simulation output files
    ├── tb_control_snn.vvp  ← iverilog compiled binary
    └── tb_control_snn.vcd  ← Waveform file (GTKWave mai dekh sakte)

### Weights (.mem files)

fpga/export/ ke andar 6 hex files hain:

fc1_weight.mem 6 × 64 = 384 weights Linear layer 1 (6 inputs → 64 neurons)
fc1_bias.mem 64 biases Layer 1 ke neurons ke liye
fc2_weight.mem 64 × 32 = 2048 weights Linear layer 2 (64 inputs → 32 neurons)
fc2_bias.mem 32 biases Layer 2 ke neurons ke liye
fc3_weight.mem 32 × 4 = 128 weights Linear layer 3 (32 inputs → 4 outputs)
fc3_bias.mem 4 biases Layer 3 ke outputs ke liye
Ye Q4.11 fixed-point hex values hain, jo memory-mapped registers mai load hongi.

1. lif_neuron.sv — Ek neuron ka circuit

# Python equivalent (snnTorch)

mem = beta * mem + current
spike = (mem >= threshold)
if spike: mem = 0  # reset
Hardware mai same logic:

- mem_q = previous membrane potential (registered)
- beta_mul = BETA_Q * mem_q >>> 11 → beta decay (0.8 × mem)
- mem_d = beta_mul + current_in → leak + input current
- spike_d = (mem_d >= THRESH_Q) → spike if crossed threshold
- If spike → mem_d = 0 (reset)
- Clock cycle pe: mem_q <= mem_d, spike_out <= spike_d (but only when valid_in=1)
Inputs: current_in (16-bit Q4.11), valid_in  
Outputs: spike_out (1 bit), mem_out (membrane potential)

1. linear_lif.sv — Pura linear layer
Ye do kaam karta hai:
1. MAC (Multiply-Accumulate): y_j = Σ(w_ji × x_i) + bias_j
1. LIF neurons: Har output neuron ke liye ek lif_neuron instantiate
State machine (3 states):
IDLE → MAC → DONE → IDLE

- IDLE: valid_in aane par MAC start karta hai, acc reset karta hai
- MAC: Har cycle ek input index process karta hai:
- acc[j] += weight[j*IN_FEATURES + mac_idx]* x_in[mac_idx]  
(har neuron j ke liye, current input mac_idx ka weight × input value accumulate)
- IN_FEATURES cycles lagte hain
- DONE: current[j] = (acc[j] + bias[j]) >>> 11 → LIF neurons ko feed  
valid_out = 1 bhejta hai next layer ko batane ke liye
Key point: Har neuron ka LIF apne current[i] ko check karta hai. valid_in for LIF = (state == DONE) — matlab sirf DONE state mai neuron update hota hai.

1. control_snn.sv — Top module (3 layers ka chain)
ego_in[6]  →  Layer1 (6→64)  →  64 spikes  →  Layer2 (64→32)  →  32 spikes  →  Layer3 (32→4)  →  4 spikes
Controller state machine:
WAIT → RUN_L1 → RUN_L2 → RUN_L3 → PWM_DONE → WAIT

- WAIT: External valid_in pulse ka wait
- RUN_L1: Layer 1 ko valid_in bhejta hai
- RUN_L2: Sirf tab layer 2 ko valid_in bhejta hai jab layer 1 complete (l1_valid_out)
- RUN_L3: Sirf tab layer 3 ko valid_in bhejta hai jab layer 2 complete
- PWM_DONE: ready_out = 1 → testbench ko signal ki output ready hai
Spike to current conversion:
spike = 1 → current = 2048 (Q4.11 = 1.0)
spike = 0 → current = 0
Neuron spike kare ya nahi — next layer ke liye current ban jata hai.
PWM decode: 20 timesteps tak har spike count karta hai:
pwm_out[i] += 102  (102 = 2048/20, Q4.11 mai 0.05 per spike)

1. tb_control_snn.sv — Testbench (jo humein spike count batata hai)
Kaam:
1. Clock generate karta hai (10ns period)
1. Reset apply karta hai
1. 6 ego inputs set karta hai (vx=0.5, wx=0.5, rest=0)
1. 20 timesteps ke liye loop:

- valid_in pulse bhejta hai (1 cycle)
- ready_out ka wait karta hai (max 5000 cycles)
- PWM read karta hai, spike count update

5. Final spike rates display karta hai

Flow diagram (visual):
Testbench           control_snn                linear_lif (×3)
─────────           ────────────               ────────────────
valid_in ──► WAIT ──► l1.valid_in ──► IDLE ──► MAC (N cycles) ──► DONE
                    │                            │
                    │                      current → LIF neurons
                    │                            │
                    │                      valid_out ──┐
                    │                                │
                    ├── RUN_L2 ◄──────────────────────┘
                    │      │
                    │      └──► l2.valid_in ──► same process
                    │              │
                    │        valid_out ──┐
                    │                    │
                    ├── RUN_L3 ◄─────────┘
                    │      │
                    │      └──► l3.valid_in (BUG: should be l2_valid_out)
                    │              │
                    │         valid_out → PWM decode
                    │
ready_out ◄── PWM_DONE

### RTL files

lif_neuron.sv — Single neuron module

Inputs clk, rst_n, valid_in, current_in[15:0]
Outputs spike_out, mem_out[15:0]
Behaviour
Membrane update: mem_d = β×mem_q + current_in
Spike if mem_d ≥ threshold
Reset after spike (configurable: to 0 or subtract threshold)
Fixed-point arithmetic: Q4.11 format (16 bits total: 4 integer + 11 fractional)
Quantization
β = 0.8 = 1638/2048 → shift by 11: (1638 × mem) >> 11
Threshold = 0.1 = 205/2048
linear_lif.sv — Single linear layer + neuron array

Inputs clk, rst_n, valid_in, data_in[N-1:0]
Outputs spike_out, data_out[M-1:0]
Internals
Implements weight matrix W[M×N] + bias B[M]
Each output neuron i: y_i = Σ_j(W_ij × x_j) + B_i
Feeds into M LIF neurons in parallel
Custom FIFO buffer (16-deep × 128-wide) to handle rate conversion (spikes → continuous values)
Output: vector of spike rates (continuous [0,1])
control_snn.sv — Top-level control module

3-layer cascade: Linear(64) → Linear(32) → Linear(4)
Each layer has: linear_lif module + output FIFO
Inputs: ego-motion vector [6] + throttle command [1] = 7 inputs
Outputs: 4 PWM duty cycles [0,1]
Clock cycle handling
clk = 25 MHz (40 ns period)
Each layer takes ~3 cycles (pipeline stages)
Overall inference: ~9-12 cycles per input vector
Weights loaded via interface (simulated via FPGA_LOAD_WEIGHTS parameter)
Verification files
tb_control_snn.sv — Testbench

DUT: control_snn
Stimulus Random ego-motion + throttle values (normalised to [-1,1], then scaled to Q4.11)
Clock generation at 25 MHz
Parameter loading simulation (FPGA_LOAD_WEIGHTS = 1)
Checks
Output format: 4 PWM values [0,1]
Internal values (for debugging):
mem_out[15:0] spike_count (for each layer)
Threshold crossing detection
Output file
tb_control_snn.vvp iverilog compiled binary
.vcd file — GTKWave waveform dump (can visualize spikes, membrane voltages, outputs)

Simulation workflow
Compile:
cd neuromorphic/ && source venv/bin/activate
cd ../fpga/rtl
ic_sim.sh
Output
Console prints:
Layers processed
Output values (hex + decimal)
Spike counts per layer
Final output: PWM values in [0,1]
View waveforms (optional):
gtkwave ../sim/tb_control_snn.vcd
