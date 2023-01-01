  
@R15 
M=0

@quotient
M = 1

@R13
D=M
@dividend
M=D

@R14
D=M
@divisor
M=D

@temp
M=1


(STARTLOOP) // if mechane bigger than mone jump to 0
@dividend // mone 
D = M
@divisor // temp mechane
D = D - M
@END
D;JLT

(DIVLOOP)
@dividend // mone 
D = M
@divisor // temp mechane
D = D - M
@MANAGEMINUS
D;JLE
@divisor
M = M<<
@temp //counter
M = M + 1
@DIVLOOP
0;JMP

(MANAGEMINUS)
@temp // counter
M = M - 1
D = M
@ENDCOUNT
D; JLE
@quotient
M = M <<
@temp
@MANAGEMINUS
0;JMP

(ENDCOUNT)
@quotient
D = M 
@R15
M = M + D
@divisor
D = M >>
@dividend
M = M - D 
@R14
D = M 
@divisor
M = D 
@quotient
M = 1
@STARTLOOP
0;JMP

(END)
0;JMP
