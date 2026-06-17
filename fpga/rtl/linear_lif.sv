module linear_lif #(
    parameter int IN_FEATURES  = 6,
    parameter int OUT_FEATURES = 64,
    parameter int WEIGHT_INT_WIDTH = 16,
    parameter string WEIGHT_FILE  = "",
    parameter string BIAS_FILE     = "",
    parameter int BETA_Q        = 1638,
    parameter int THRESH_Q      = 205
)(
    input  logic                      clk,
    input  logic                      rst_n,
    input  logic                      valid_in,
    input  logic signed [15:0]        x_in   [IN_FEATURES-1:0],  // Q4.11
    output logic                      spike_out [OUT_FEATURES-1:0],
    output logic signed [15:0]        mem_out [OUT_FEATURES-1:0],
    output logic                      valid_out
);

    // Weight and bias storage (flat arrays)
    logic signed [WEIGHT_INT_WIDTH-1:0] weight_mem [0:OUT_FEATURES*IN_FEATURES-1];
    logic signed [WEIGHT_INT_WIDTH-1:0] bias_mem   [0:OUT_FEATURES-1];

    // Load weights/biases from .mem files
    initial begin
        if (WEIGHT_FILE != "") begin
            $readmemh(WEIGHT_FILE, weight_mem);
            $display("Loaded weights from %s: %0d values", WEIGHT_FILE, $size(weight_mem));
            $display("  First 5 weights: %h %h %h %h %h", 
                weight_mem[0], weight_mem[1], weight_mem[2], weight_mem[3], weight_mem[4]);
        end
        if (BIAS_FILE != "") begin
            $readmemh(BIAS_FILE, bias_mem);
            $display("Loaded bias from %s: %0d values", BIAS_FILE, $size(bias_mem));
            if (OUT_FEATURES >= 5)
                $display("  First 5 bias: %h %h %h %h %h", 
                    bias_mem[0], bias_mem[1], bias_mem[2], bias_mem[3], bias_mem[4]);
            else
                $display("  First %0d bias: %h ...", OUT_FEATURES, bias_mem[0]);
        end
    end

    // MAC state machine
    typedef enum logic [1:0] {IDLE, MAC, DONE} state_t;
    state_t state;

    logic [$clog2(IN_FEATURES):0] mac_idx;
    logic signed [31:0] acc [OUT_FEATURES-1:0];
    logic signed [15:0] current [OUT_FEATURES-1:0];

    // LIF neuron instances
    genvar i;
    generate
        for (i = 0; i < OUT_FEATURES; i++) begin : lif_gen
            lif_neuron #(
                .BETA_Q    (1638),
                .THRESH_Q  (205),
                .RESET_ZERO(0)
            ) lif_inst (
                .clk        (clk),
                .rst_n      (rst_n),
                .current_in (current[i]),
                .valid_in   (state == DONE),
                .spike_out  (spike_out[i]),
                .mem_out    (mem_out[i])
            );
        end
    endgenerate

    // Combinational: current from acc + bias
    always_comb begin
        for (int j = 0; j < OUT_FEATURES; j++)
            current[j] = (acc[j] + bias_mem[j]) >>> 11;
    end

    // MAC state machine
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            mac_idx <= '0;
            valid_out <= 1'b0;
            for (int j = 0; j < OUT_FEATURES; j++) begin
                acc[j] <= '0;
            end
        end else begin
            valid_out <= 1'b0;
            case (state)
                IDLE: begin
                    if (valid_in) begin
                        state <= MAC;
                        mac_idx <= '0;
                        for (int j = 0; j < OUT_FEATURES; j++)
                            acc[j] <= '0;
                        $display("  Layer %0d: MAC start, IN_FEATURES=%0d", OUT_FEATURES, IN_FEATURES);
                    end
                end
                MAC: begin
                    for (int j = 0; j < OUT_FEATURES; j++) begin
                        acc[j] <= acc[j] + weight_mem[j*IN_FEATURES + mac_idx] * x_in[mac_idx];
                    end
                    mac_idx <= mac_idx + 1;
                    if (mac_idx == IN_FEATURES - 1)
                        state <= DONE;
                end
                DONE: begin
                    $display("  Layer %0d: MAC done, current[0]=%0d", OUT_FEATURES, current[0]);
                    valid_out <= 1'b1;
                    state <= IDLE;
                end
            endcase
        end
    end

endmodule