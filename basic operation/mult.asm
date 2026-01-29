@18
M = 0

(LOOP)
    @17
    D = M
    @END
    D;JEQ //check if B > 0
    @16
    D = M 
    @18
    M = D + M // C = C + A
    @17
    M = M - 1 // B =  B - 1
    @LOOP
    0;JMP // goto LOOP
(END)
@END
0;JMP // Infinite loop



