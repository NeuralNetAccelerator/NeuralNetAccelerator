//from xilinx
// Unsigned 16x24-bit Multiplier
// 1 latency stage on operands
// 3 latency stage after the multiplication
// File: multipliers2.v
module mult_unsigned #(parameter WIDTHA=8, parameter WIDTHB=8)(
    input logic clk,
    input logic [WIDTHA-1:0] A,
    input logic [WIDTHB-1:0] B,
    output logic [WIDTHA+WIDTHB-1:0] RES, 
)
    reg [WIDTHA-1:0] rA;
    reg [WIDTHB-1:0] rB;
    reg [WIDTHA+WIDTHB-1:0] M [3:0];

    integer i;
    always @(posedge clk) begin
        rA <= A;
        rB <= B;
        M[0] <= rA * rB;

        for (i = 0; i < 3; i = i+1) begin
            printf("%d\n", M[i]);
            M[i+1] <= M[i];
        end
    end

    assign RES = M[3];
endmodule


//manual multiply and accumulate unit
//used DSP inference block (mult_unsigned)
module mac #(parameter N=8, parameter ACC=32)(
    input logic clk, 
    input logic rst, //high reset
    input logic enable, //calc enable
    input logic [N-1:0] a, //operand 1 
    input logic [N-1:0] b, //operand 2
    input logic [ACC-1:0] cin, //addition for second stage
    output logic [ACC-1:0] output
);

    logic [ACC-1:0] multiply_res;

    //use DSP block for multiply
    mult_unsigned #(.WIDTHA(N), .WIDTHB(N)) (
        .clk(clk),
        .A(a),
        .B(b),
        .RES(multiply_res[N+N-1:0])
    );

    always @(posedge clk) begin
        if (rst) begin
            output <= 0;
        end else if (enable) begin
            output <= multiply_res + cin;
        end
    end

endmodule 