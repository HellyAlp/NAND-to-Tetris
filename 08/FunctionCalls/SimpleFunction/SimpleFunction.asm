
// function SimpleFunction.test 2
(SimpleFunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@LCL
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M+D
M=D
// not
@SP
A=M-1
D=!M
M=D
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M+D
M=D
// push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=D
// return
@LCL
D=M
@endFrame
M=D
@5
D=A
@endFrame
D=M-D
@retAddr
A=D
D=M
@retAddr
M=D
@ARG
D=M
@SP
A=M                                                                       
M=D
@SP
M=M-1
A=M
D=M
@SP
A=M+1
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@endFrame
D=M-D
@THAT
A=D
D=M
@THAT
M=D
@2
D=A
@endFrame
D=M-D
@THIS
A=D
D=M
@THIS
M=D
@3
D=A
@endFrame
D=M-D
@ARG
A=D
D=M
@ARG
M=D
@4
D=A
@endFrame
D=M-D
@LCL
A=D
D=M
@LCL
M=D
@retAddr
D=M
@i
A=D
0;JMP