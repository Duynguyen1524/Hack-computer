@18
M = 0
@17
D = M
@POSITIVE
D;JGT
@17
D = M
@NEGATIVE
D;JLT

(POSITIVE)
    @17
    D = M
    @END
    D;JEQ //check if B > 0
    @16
    D = M 
    @18
    M = D + M // C= C + A
    @17
    M = M - 1 // B =  B - 1
    @POSITIVE
    0;JMP // goto LOOP

(NEGATIVE)
    @17
    D = M
    @END
    D;JEQ //check if B > 0
    @16
    D = M  
    @18
    M = M - D // C= C - A
    @17
    M = M + 1 // B =  B + 1
    @NEGATIVE
    0;JMP // goto LOOP
(END)
@END
0;JMP // Infinite loop