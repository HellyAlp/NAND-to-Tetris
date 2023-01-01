  
@R15 //result register
M=0

@quotient //counts the apperance
M = 0


@R13 // dividend register
D=M
@dividend
M=D

@R14 //divisor register
D=M
@divisor
M=D

@divisor
D=M

@dividend //calaulate the result
D = M - D

@END
D;JLT

@LOOP
D;JGE

(LOOP)
@quotient
M = M + 1

@quotient
D = M 

@R15     
M=D 

@divisor
D=M

@dividend //calaulate the result
M = M -D
D=M


	
@NEG
D;JLT

@LOOP
D;JGT

@FIN
D;JEQ

(NEG)
@quotient 
M = M -1
@quotient 
D = M

@R15
M=D
@END
0;JMP

(FIN)
@quotient 
D = M

@R15
M=D
@END
0;JMP

(END)
@END
