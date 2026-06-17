module control_snn #(
    parameter int TIME_STEPS = 20
)(
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic                     valid_in,
    input  logic signed [15:0]       ego_in [5:0],    // 6 inputs (Q4.11)
    output logic                     ready_out,
    output logic signed [15:0]       pwm_out [3:0]    // 4 PWM outputs (Q4.11)
);

    // Layer 1: 6 -> 64
    logic        l1_spike [63:0];
    logic signed [15:0] l1_mem [63:0];
    logic signed [15:0] l1_current [63:0];
    logic        l1_valid_out;
    logic        l1_valid_in;

    // Layer 2: 64 -> 32
    logic        l2_spike [31:0];
    logic signed [15:0] l2_mem [31:0];
    logic signed [15:0] l2_current [31:0];
    logic        l2_valid_out;
    logic        l2_valid_in;

    // Layer 3: 32 -> 4
    logic        l3_spike [3:0];
    logic signed [15:0] l3_mem [3:0];
    logic signed [15:0] l3_current [3:0];
    logic        l3_valid_out;
    logic        l3_valid_in;

    // Sequencing controller
    typedef enum logic [2:0] {WAIT, RUN_L1, RUN_L2, RUN_L3, PWM_DONE} ctrl_state_t;
    ctrl_state_t ctrl_state, ctrl_next;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            ctrl_state <= WAIT;
        else
            ctrl_state <= ctrl_next;
    end

    always_comb begin
        ctrl_next = ctrl_state;
        case (ctrl_state)
            WAIT:    if (valid_in)       ctrl_next = RUN_L1;
            RUN_L1:  if (l1_valid_out)   ctrl_next = RUN_L2;
            RUN_L2:  if (l2_valid_out)   ctrl_next = RUN_L3;
            RUN_L3:  if (l3_valid_out)   ctrl_next = PWM_DONE;
            PWM_DONE:                    ctrl_next = WAIT;
        endcase
    end

    // Edge-detect: pulse valid_in on entry to each RUN state
    logic [2:0] ctrl_d1;
    always_ff @(posedge clk) ctrl_d1 <= ctrl_state;

    assign l1_valid_in = (ctrl_state == RUN_L1) && (ctrl_d1 != RUN_L1);
    assign l2_valid_in = l1_valid_out;
    assign l3_valid_in = l2_valid_out;
    assign ready_out   = (ctrl_state == PWM_DONE);

    // Layer 1: 6 -> 64
    linear_lif #(
        .IN_FEATURES (6),
        .OUT_FEATURES(64),
        .WEIGHT_FILE ("fpga/export/fc1_weight.mem"),
        .BIAS_FILE   ("fpga/export/fc1_bias.mem")
    ) l1 (
        .clk       (clk),
        .rst_n     (rst_n),
        .valid_in  (l1_valid_in),
        .x_in      (ego_in),
        .spike_out (l1_spike),
        .mem_out   (l1_mem),
        .valid_out (l1_valid_out)
    );

    always_comb begin
        for (int i = 0; i < 64; i++)
            l1_current[i] = l1_spike[i] ? 16'sd2048 : 16'sd0;
    end

    // Layer 2: 64 -> 32
    linear_lif #(
        .IN_FEATURES (64),
        .OUT_FEATURES(32),
        .WEIGHT_FILE ("fpga/export/fc2_weight.mem"),
        .BIAS_FILE   ("fpga/export/fc2_bias.mem")
    ) l2 (
        .clk       (clk),
        .rst_n     (rst_n),
        .valid_in  (l2_valid_in),
        .x_in      (l1_current),
        .spike_out (l2_spike),
        .mem_out   (l2_mem),
        .valid_out (l2_valid_out)
    );

    always_comb begin
        for (int i = 0; i < 32; i++)
            l2_current[i] = l2_spike[i] ? 16'sd2048 : 16'sd0;
    end

    // Layer 3: 32 -> 4
    linear_lif #(
        .IN_FEATURES (32),
        .OUT_FEATURES(4),
        .WEIGHT_FILE ("fpga/export/fc3_weight.mem"),
        .BIAS_FILE   ("fpga/export/fc3_bias.mem")
    ) l3 (
        .clk       (clk),
        .rst_n     (rst_n),
        .valid_in  (l3_valid_in),
        .x_in      (l2_current),
        .spike_out (l3_spike),
        .mem_out   (l3_mem),
        .valid_out (l3_valid_out)
    );

    // Rate-coded PWM decode
    logic signed [15:0] pwm_acc [3:0];

    initial begin
        for (int i = 0; i < 4; i++) pwm_out[i] = 16'sd0;
    end

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (int i = 0; i < 4; i++)
                pwm_out[i] <= 16'sd0;
        end else if (l3_valid_out) begin
            for (int i = 0; i < 4; i++)
                if (l3_spike[i])
                    pwm_out[i] <= pwm_out[i] + 16'sd102;
        end
    end

endmodule