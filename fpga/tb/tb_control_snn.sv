`timescale 1ns / 1ps

module tb_control_snn;

    localparam TIME_STEPS = 20;
    localparam MAX_WAIT   = 5000;

    logic clk, rst_n;
    logic valid_in;
    logic signed [15:0] ego_in [5:0];
    logic ready_out;
    logic signed [15:0] pwm_out [3:0];

    control_snn #(.TIME_STEPS(TIME_STEPS)) dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .valid_in (valid_in),
        .ego_in   (ego_in),
        .ready_out(ready_out),
        .pwm_out  (pwm_out)
    );

    always #5 clk = ~clk;

    logic [7:0] spike_count [3:0];
    int wait_cycles;

    initial begin
        $display("=== Control SNN Testbench ===");
        $display("TIME_STEPS=%0d", TIME_STEPS);

        clk = 0; rst_n = 0; valid_in = 0;
        spike_count[0] = 0; spike_count[1] = 0;
        spike_count[2] = 0; spike_count[3] = 0;

        ego_in[0] = 16'sd0512;
        ego_in[1] = 16'sd0000;
        ego_in[2] = 16'sd0000;
        ego_in[3] = 16'sd1024;
        ego_in[4] = 16'sd0000;
        ego_in[5] = 16'sd0000;

        @(posedge clk);
        rst_n = 1;
        @(posedge clk);

        for (int t = 0; t < TIME_STEPS; t++) begin
            @(posedge clk);
            valid_in = 1;
            @(posedge clk);
            valid_in = 0;

            wait_cycles = 0;
            while (!ready_out && wait_cycles < MAX_WAIT) begin
                @(posedge clk);
                wait_cycles++;
            end

            if (wait_cycles >= MAX_WAIT) begin
                $display("  Timestep %0d: TIMEOUT (%0d cycles)", t, wait_cycles);
                $finish;
            end

            @(posedge clk);

            for (int i = 0; i < 4; i++)
                if (pwm_out[i] > 16'sd0) spike_count[i] = spike_count[i] + 1;

            $display("  t=%0d: wait=%0d, ready=1, PWM=[%0d %0d %0d %0d]",
                t, wait_cycles,
                pwm_out[0], pwm_out[1], pwm_out[2], pwm_out[3]);
        end

        $display("");
        $display("=== PWM Output (Rate-Coded) ===");
        for (int i = 0; i < 4; i++)
            $display("PWM[%0d]: spikes=%0d, rate=%0.4f", i, spike_count[i],
                real'(spike_count[i]) / real'(TIME_STEPS));

        $display("");
        $display("Expected (from Python test):");
        $display("PWM[0] ~ 0.50");
        $display("PWM[1] ~ 0.50");
        $display("PWM[2] ~ 0.50");
        $display("PWM[3] ~ 0.45");

        $finish;
    end

endmodule