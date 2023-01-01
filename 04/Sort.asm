
// init the index
@R14
D=M
@index
M=D

// init the last
@last
M=D

@R15
D=M
@last
M=M+D
M=M-1

@last
D=M
@j
M=D

(LOOP)
	// checks if index=last
	@last
	D=M
	@index
	D=D-M
	@END
	D;JLE
	
	//compare array[last] and array[last-1]
	//@last
	//D=M
	@j
	D=M
	A=D
	D=M
	@var1
	M=D
	
	@j
	D=M
	A=D-1
	D=M
	@var2
	M=D

	@var1
	D=D-M
	@IF
	D;JGE
	
	// replace the places
	@var2
	D=M
	@j
	A=M
	M=D
	
	@var1
	D=M
	@j
	A=M-1
	M=D
	
	@IF
	0;JMP
 
(END)
@END

(IF)
	// checks if j=index
	@j
	D=M
	@index
	D=D-M
	D=D-1
	@LOOP1
	D;JGT
	
	@index
	D=M
	M=D+1
	@last
	D=M
	@j
	M=D
	@LOOP
	0;JMP
(END)
@END
	
(LOOP1)
	@j
	D=M
	M=D-1
	@LOOP
	0;JMP
(END)
@END




	
	
