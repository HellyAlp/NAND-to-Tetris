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

@k
M = 0

(START)
	@divisor
	D = M
	
	@SET_K
	D;JEQ
	
	@dividend
	D = M - D
	
	@WHILE_POZ
	D;JGE
	
	@SET_K
	D;JLT

(WHILE_POZ)
	@divisor
	M=M<<
	@k
	M = M + 1
	
	@START
	0;JMP

(SET_K)
	@k
	M = M - 1
	
	@k
	D = M
	
	@WHILE_K_POZ
	D;JGE
	
	@END_SET_K
	0;JMP

	
(WHILE_K_POZ)
	@divisor
	M=M>>
	
	@divisor
	D = M
	
	@dividend
	D = M - D
	
	@IF
	D;JGE
	
	@ELSE
	D;JLT



(IF)
	@divisor
	D = M
	@dividend
	M = M - D
	
	@quotient
	M = M<<
	
	@quotient
	M = M +1
	
	@SET_K
	0;JMP


(ELSE)
	@quotient
	M = M<<
	
	@SET_K
	0;JMP
	
	
(END_SET_K)
	@quotient
	D = M
	@R15
	M = D
	
	