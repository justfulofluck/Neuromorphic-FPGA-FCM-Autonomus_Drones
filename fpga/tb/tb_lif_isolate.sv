`timescale 1ns / 1ps

module tb_lif_isolate;
    logic clk, rst_n;
    logic valid_in;
    logic signed [15:0] current_in;
    logic spike_out;
    logic signed [15:0] mem_out;

    lif_neuron dut (
        .clk(clk),
        .rst_n(rst_n),
        .valid_in(valid_in),
        .current_in(current_in),
        .spike_out(spike_out),
        .mem_out(mem_out)
    );

    always #5 clk = ~clk;

    initial begin
        $display("=== LIF Isolation Test ===");
        clk = 0; rst_n = 0; valid_in = 0; current_in = 0;
        @(posedge clk);
        #1 rst_n = 1;
        @(posedge clk);
        @(posedge clk);

        // Step 1: valid_in=1 with current=724
        $display("Step 1: valid_in=1, current=724");
        valid_in = 1;
        current_in = 16'sd724;  // > threshold 205
        @(posedge clk);
        #1 valid_in = 0;
        $display("  spike_out=%b, mem_out=%0d", spike_out, mem_out);

        // Step 2: another valid_in=1
        @(posedge clk);
        #1 valid_in = 1; current_in = 16'sd100;  // < threshold
        @(posedge clk);
        #1 valid_in = 0;
        $display("Step 2: valid_in=1, current=100");
        $display("  spike_out=%b, mem_out=%0d", spike_out, mem_out);

        $finish;
    end
endmodule
