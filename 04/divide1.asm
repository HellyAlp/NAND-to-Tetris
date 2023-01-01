// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@16384
D=A
@num
M=D

@rem
M=0

@R15
D=0
@R13
D=M
@R14
D=M-D
@result
M=D

(LOOP)
@result
D=M

@END
D;JLE

@num
D=M

@END
D;JEQ

@R13
D = D & M

@dev
M=D

@LOOP1
D;JNE

@LOOP2
0;JMP


(END)
@END






 ///if num != 0
(LOOP1)
@rem
M=M+1
@LOOP2
0;JMP
 
(END)
@END


//if rem>=R14
(LOOP2)

@R14
D=M
@rem
D=M-D
@result
M=D


@LOOP3
D;JGE

@rem
M=D 

@num
D = M

@R15
M=M+D


@LOOP3
0;JMP

(END)

@END


(LOOP3)
@num
M = D>>

@rem
M = D<<

@LOOP
0;JMP

(END)
@END
