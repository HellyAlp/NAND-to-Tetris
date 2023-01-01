class CodeWriter:

    # ----- Class constant ------ #
    C_PUSH = 'push'
    C_POP = 'pop'
    POP_ASM = "@SP" + "\n"+"M=M-1"+"\n"+"A=M" + "\n"+"D=M" + \
              "\n"+"@SP" + \
              "\n"+"A=M-1" + "\n"
    SP_ADRESS = "@SP" + "\n" + "A=M-1" + "\n"
    PUSH_TO_SP = "@SP" + "\n" + "A=M" + "\n" + "M=D" + "\n"+"@SP" + "\n" + \
                 "M=M+1" + "\n"

    T = "M=-1"
    F = "M=0"

    def __init__(self, output_file):
        """
        Opens the output file and get ready to parse it
        :param output_file:
        """
        self.output = open(output_file, 'w')
        self.file_name = ''
        self.C_ARITHMETIC = {'add': self.binary_arithmetics, 'sub': self.binary_arithmetics, 'neg':
                                self.unary_arithmetics,  'eq': self.a_eq, 'and': self.binary_arithmetics
                            ,'or': self.binary_arithmetics, 'gt':self.a_gt,
                             'lt':self.a_lt, 'not':self.unary_arithmetics}
        self.SIGNS = {'add':'+', 'sub': '-', 'neg':'-',  'eq': 'EQ', 'and': '&','or': '|', 'gt': 'GT', 'lt': 'LT',
                      'not': '!'}
        self.C_SEGMENTS = {'argument': '@ARG', 'local': '@LCL', 'static': '@' + self.file_name,
                           'constant': '@SP', 'this': '@THIS'
                            , 'that': '@THAT', '0': '@THIS',
                           '1':'@THAT', 'temp': '@5'}
        self.loop_counter = str(1)

    def binary_arithmetics(self, sign):
        self.output.write(self.POP_ASM + "D=M"+sign+ "D" + "\n" + "M=D" + "\n")

    def unary_arithmetics(self, sign):
        self.output.write(self.SP_ADRESS + "D="+sign+"M" + "\n" + "M=D" + "\n")

    # TODO: compere_arithmetics(self, sign): (instead of a_eq, a_lt, a_gt)

    def a_eq(self, sign):
        self.output.write(self.POP_ASM)
        self.output.write("D=D-M" + "\n" + "@EQ" +
                          self.loop_counter + "\n" + "D;JEQ" + "\n" +
                          self.SP_ADRESS + self.F + "\n" +
                          "@END" +
                          self.loop_counter + "\n" + "D;JMP" + "\n" + "(EQ" +
                          self.loop_counter + ")" + "\n" +
                          self.SP_ADRESS + "\n" + self.T + "\n" +
                          "(END" +
                          self.loop_counter + ")" + "\n")
        self.loop_counter = str(int(self.loop_counter)+1)

    def a_lt(self, sign):
        self.output.write(self.POP_ASM)
        self.output.write("D=M-D" + "\n" + "@LT"+self.loop_counter + "\n" + "D;JLT" +
                          "\n" +
                          self.SP_ADRESS + "\n" + self.F + "\n" +
                          "@END" + self.loop_counter + "\n" + "D;JMP" + "\n" +
                          "(LT" + self.loop_counter + ")" +
                          "\n" +
                          self.SP_ADRESS + "\n" + self.T + "\n" +
                          "(END" +
                          self.loop_counter + ")" + "\n")
        self.loop_counter = str(int(self.loop_counter)+1)

    def a_gt(self, sign):
        self.output.write(self.POP_ASM)
        self.output.write("D=M-D" + "\n" + "@GT"+self.loop_counter + "\n" + "D;JGT" +
                          "\n" +
                          self.SP_ADRESS + "\n" + self.F + "\n" +
                          "@END" + self.loop_counter + "\n" + "D;JMP" + "\n" + "(GT"+
                          self.loop_counter + ")" +
                          "\n" +
                          self.SP_ADRESS + "\n" + self.T + "\n" +
                          "(END" +
                          self.loop_counter + ")" + "\n")
        self.loop_counter = str(int(self.loop_counter)+1)

    def writeArithmetic(self, command):
        """
        Writes to the output file the assembly code that implements the
        given arithmetic command
        :param command: string
        :return:
        """
        command = command.replace(" ", "").replace("\t", "")
        sign = self.SIGNS[command]
        self.C_ARITHMETIC[command](sign)

    def writePushPop(self, command, segment, index):
        """
        Writes to the output file the assembly code that implements the
        given command - C_PUSH or C_POP
        :param command: C_PUSH or C_POP
        :param segment: string
        :param index: index
        :return:
        """
        command = command.replace(" ", "").replace("\t", "")
        self.output.write("// " + command + " " + segment + " " + str(index) +
                          "\n")
        if segment == 'pointer':
            seg = self.C_SEGMENTS[str(index)]
            index = 0
        elif segment == 'static':
            seg = '@'+self.file_name+'.'+str(index)

        else:
            seg = self.C_SEGMENTS[segment]

        if command == self.C_PUSH:
            # constant case
            if segment == 'constant':
                self.output.write("@" + str(index) + "\n"+"D=A" + "\n" +
                                  self.PUSH_TO_SP)
            # local/argument case
            elif segment == 'local' or segment == 'argument'or segment == \
                    'this' or segment == 'that' :

                self.output.write(seg + "\n"+"D=M" + "\n"+"@" +
                                  str(index) + "\n"+"A=A+D" + "\n"+"D=M" +
                                  "\n" + self.PUSH_TO_SP)
            elif segment == 'temp':
                self.output.write(seg + "\n" + "D=A" + "\n" + "@" +
                                  str(index) + "\n" + "A=A+D" + "\n" + "D=M" +
                                  "\n" + self.PUSH_TO_SP)
            elif segment == 'pointer' or segment == 'static':
                self.output.write(seg + "\n" + "D=M" + "\n" + self.PUSH_TO_SP)


        else:
            if segment == 'local' or segment == 'argument' or segment == \
                    'this' or segment == 'that' :
                self.output.write(seg + "\n" + "D=M" + "\n"+"@" +
                                  str(index) + "\n"+"A=A+D" + "\n"+"D=A" +
                                  "\n" + "@SP" + "\n"+"A=M" + "\n"+"M=D" +
                                  "\n"+"@SP" + "\n"+"M=M-1" + "\n"+"A=M" +
                                  "\n"+"D=M" + "\n"+"@SP" + "\n"+"A=M+1" +
                                  "\n"+"A=M" + "\n"+"M=D" + "\n")
            elif segment == 'temp':
                self.output.write(seg + "\n" + "D=A" + "\n" + "@" +
                                  str(index) + "\n" + "A=A+D" + "\n" + "D=A" +
                                  "\n" + "@SP" + "\n" + "A=M" + "\n" + "M=D" +
                                  "\n" + "@SP" + "\n" + "M=M-1" + "\n" + "A=M" +
                                  "\n" + "D=M" + "\n" + "@SP" + "\n" + "A=M+1" +
                                  "\n" + "A=M" + "\n" + "M=D" + "\n")
            elif segment == 'pointer' or segment == 'static' :
                self.output.write("@SP" + "\n" + "A=M" + "\n" + "M=D" + "\n" +
                                  "@SP" + "\n" + "M=M-1" + "\n" + "A=M" + "\n" +
                                  "D=M" + "\n" + seg + "\n" + "M=D" + "\n")

    def close(self):
        """
        close the output file
        :return:
        """
        self.output.close()
