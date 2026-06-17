module lif_neuron #(
    parameter int BETA_Q     = 1638,   // 0.8 in Q4.11 (0.8 * 2048 = 1638)
    parameter int THRESH_Q   = 205,    // 0.1 in Q4.11 (0.1 * 2048 = 205)
    parameter bit RESET_ZERO = 1'b1    // 1 = reset to 0, 0 = subtractive reset
)(
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic                     valid_in,
    input  logic signed [15:0]       current_in,  // Q4.11
    output logic                     spike_out,
    output logic signed [15:0]       mem_out      // Q4.11
);

    logic signed [15:0] mem_q, mem_d;
    logic spike_d;

    // Combinational: LIF update
    always_comb begin
        // mem_d = beta * mem_q + current_in
        // beta = 0.8, so beta * mem = (1638/2048) * mem ≈ 0.8 * mem
        // Use shift-add for efficient multiplication: 0.8 = 1 - 0.2
        // 0.2 * mem = mem/5 ≈ (mem >> 2) + (mem >> 3) ... but simpler:
        // beta * mem = (1638 * mem) >> 11
        logic signed [31:0] beta_mul;
        beta_mul = (BETA_Q * mem_q) >>> 11;  // Q4.11 * Q4.11 = Q8.22 -> shift 11 = Q4.11

        mem_d = beta_mul + current_in;

        // Clamp to Q4.11 range [-16, +15.9995]
        if (mem_d > 16'sd32767) mem_d = 16'sd32767;
        if (mem_d < -16'sd32768) mem_d = -16'sd32768;

        // Spike generation
        spike_d = (mem_d >= THRESH_Q);

        // Reset after spike
        if (spike_d) begin
            if (RESET_ZERO)
                mem_d = '0;
            else
                mem_d = mem_d - THRESH_Q;
        end
    end

    // Sequential
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mem_q   <= '0;
            spike_out <= 1'b0;
        end else if (valid_in) begin
            mem_q     <= mem_d;
            spike_out <= spike_d;
        end else begin
            spike_out <= 1'b0;
        end
    end

    assign mem_out = mem_q;

endmodule