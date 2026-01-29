@18
M = 0// Q = 0 
@19
M = 0 //set R to 0
@16
D = M
@19 
M = D //R = A

(LOOP)
    @19
    D = M
    @17
    D= D - M // R - B
    @END
    D;JLT //check if R - B  < 0 then Jump to End
    @18
    M = M + 1 // Q = Q +1 
    @17
    D = M // store B into D
    @19
    M = M - D // R = R - B
    @LOOP
    0;JMP // goto LOOP
(END)
@END
0;JMP // Infinite loop



