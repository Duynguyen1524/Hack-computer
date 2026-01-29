// Bubble Sort
// Date created: October 21, 2024
// Student name(s): Jean A. Garcia, Justin Nguyen
// Date modified: October 21, 2024

@17
D = M
@22
M = D - 1
(WHILE)
    @18
    M = 0
    @19
    M = 0
    @20
    M = 0
    @21
    M = 0

(LOOP)

    @19
    D = M
    @22
    D = M - D

@ELOOP
    D;JEQ

    @16
    D = M
    @19
    D = D + M
    @21
    M = D 
    A = M

    D = M
    A = A + 1
    D = D - M
    @19
    M = M + 1 
    @SWAP
    D;JGT
    @LOOP
    0;JMP
(ELOOP)
    @18
    D = M
    @WHILE
    D;JGT
@END
    0;JMP

(SWAP)
    @18
    M = M + 1 
    @21 
    A = M
    D = M
    @20 
    M = D
    @21  
    A = M + 1
    D = M
    @21 
    A = M
    M = D
    @20 
    D = M
    @21
    A = M + 1
    M = D
    @LOOP
    0;JMP 

(END)
@END
0;JMP
