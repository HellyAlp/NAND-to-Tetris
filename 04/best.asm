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


(MAIN_LOOP)
	@divisor
	D=M

	@dividend //calaulate the result
	D = M - D


	@WHILE_POZ_LOOP
	D;JGE

	@k
	M = M - 1	
	
	@k
	D=M
	
	@WHILE_K_POZ_LOOP
	D;JGT
	

	 
	@END
	@quotient
	D = M
	@R15
	M = D


	

(WHILE_POZ_LOOP)

	@divisor
	M=M<<
	@k
	M = M + 1
(WHILE_POZ_LOOP_END)
	@MAIN_LOOP
	0;JMP

(WHILE_K_POZ_LOOP)
	@divisor
	M=M>>
		
	@divisor
	D=M
	@dividend //calaulate the result
	D = M - D
	
	@IF_LOOP
	D;JGE
	
	@ELSE_LOOP
	D;JLT
	
	@MAIN_LOOP
	0;JMP
		
(IF_LOOP)
	@divisor
	D=M
	@dividend //calaulate the result
	M = M - D
	
	//@quotient
	//M = M<<
	@quotient
	M = M + 1
	
	@k
	M = M - 1	
	
	@k
	D=M

	

	@WHILE_K_POZ_LOOP
	D;JGT
	@MAIN_LOOP
	0;JMP

(ELSE_LOOP)
	@quotient
	M = M<<
	@k
	M = M - 1	
	
	@k
	D=M


	@WHILE_K_POZ_LOOP
	D;JGT
	
	@MAIN_LOOP
	0;JMP
	
	