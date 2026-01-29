// Arithmetic Left Shift
// Date created: October 21, 2024
// Student name(s): Jean A. Garcia, Justin Nguyen
// Date modified: October 21, 2024

@16
D = M
@18
M = D // store the value to result 

(LOOP)
    @17
    D = M
    @END
    D;JEQ 
    @18
    D = M
    @18
    M = M + D
    @17
    M = M - 1
    @LOOP
    0;JMP
@END
0;JMP // Infinite loop