module top
 ( input wire in1,
   input wire in2,
   input wire in3,
   output out1,
   output  out2
   );

    a U1 
    ( .in1(in1),
      .in2(in2),
      .out1(n1),
      .out2(n2) );
      
    a U2
    ( .in1(in3), .in2(n4), .out1(n3), .out2(n6) );
    
    a U3
    ( .in1(n3),. in2(n6), .out1(n5), .out2( n4 ) );
    
    b U4
    ( .in1(n1), .in2(n2), .in3(n5), .out1(out1), .out2(out2) );
   
endmodule
