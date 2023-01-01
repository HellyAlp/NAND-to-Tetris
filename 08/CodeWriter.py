class CodeWriter:
    """
    This class is the CodeWriter class. It executes the translation from vm to
    asm for all the command type/
    """

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
    SYS_INIT = 'Sys.init'


    # ----- Class constructor ------ #
    def __init__(self, output_file):
        """
        Opens the output file and initialize the dictionaries for each
        command type
        :param output_file:
        """
        self.output = open(output_file, 'w')
        self.file_name = ''
        self.C_ARITHMETIC = {'add': self.binary_arithmetics,
                             'sub': self.binary_arithmetics,
                             'neg': self.unary_arithmetics,
                             'eq': self.compere_arithmetics,
                             'and': self.binary_arithmetics,
                             'or': self.binary_arithmetics,
                             'gt': self.compere_arithmetics,
                             'lt': self.compere_arithmetics,
                             'not': self.unary_arithmetics}

        self.C_LABELS = {'label': self.writeLabel,
                         'goto': self.writeGoto,
                         'if-goto': self.writeIf,
                         'call': self.writeCall,
                         'function': self.writefunction,
                         'return': self.writeReturn}

        self.SIGNS = {'add': '+', 'sub': '-', 'neg': '-',
                      'eq': ['@FALSE', 'EQ', '@FALSE'], 'and': '&',
                      'or': '|', 'gt': ['@FALSE', 'GT', '@TRUE'],
                      'lt': ['@TRUE', 'LT', '@FALSE'], 'not': '!'}

        self.C_SEGMENTS = {'argument': '@ARG', 'local': '@LCL',
                           'static': '@' + self.file_name,
                           'constant': '@SP', 'this': '@THIS',
                           'that': '@THAT', '0': '@THIS',
                           '1': '@THAT', 'temp': '@5'}

        self.loop_counter = str(1)
        self.function_name = ""
        self.fun_count = 0
        self.writeInit() # sys.init for each file

    def binary_arithmetics(self, sign):
        """
        This method writes the code for the binary arithmetics - add, sub, and,
        or
        :param sign: the aritmetic sing
        """
        self.output.write(self.POP_ASM + "D=M"+sign+ "D" + "\n" + "M=D" + "\n")

    def unary_arithmetics(self, sign):
        """
        This method writes the code for the unnary arithmetics - neg, not
        :param sign: the aritmetic sing
        """
        self.output.write(self.SP_ADRESS + "D=" + sign + "M\n" + "M=D\n")

    def compere_arithmetics(self, sign):
        """
        This method writes the code for the compare arithmetics - eq, lt, gt
        :param sign: the aritmetic sing
        """
        self.output.write(
            "@SP\n" + "M=M-1\n" + "A=M\n" + "D=M\n" + "@FIRSTNEG" +
            self.loop_counter + "\n" + "D;JLT\n" + "@SP\n" + "A=M-1\n" +
            "D=M\n" + sign[0] + self.loop_counter + "\n" + "D;JLT\n" +
            "(SUB" + self.loop_counter + ")\n" + "@SP\n" + "A=M\n" + "D=M\n" +
            "@SP\n" + "A=M-1\n" + "D=M-D\n" + "@TRUE" + self.loop_counter +
            "\n" + "D;J" + sign[1] + "\n" + "@FALSE" + self.loop_counter + "\n"
            + "0;JMP\n" + "(FIRSTNEG" + self.loop_counter + ")" + "\n" +
            "@SP\n" + "A=M-1\n" + "D=M\n" + sign[2] + self.loop_counter + "\n"
            + "D;JGT\n" + "@SUB" + self.loop_counter + "\n" + "0;JMP\n" +
            "(FALSE" + self.loop_counter + ")\n" + "@SP\n" + "A=M-1\n" +
            "M=0\n" + "@END" + self.loop_counter + "\n" + "0;JMP\n" + "(TRUE"
            + self.loop_counter + ")" + "\n" + "@SP\n" + "A=M-1\n" + "M=-1\n"
            + "@END" + self.loop_counter + "\n" + "0;JMP\n"
            + "(END" + self.loop_counter + ")" + "\n")
        self.loop_counter = str(int(self.loop_counter) + 1)

    def writeArithmetic(self, command):
        """
        Writes to the output file the assembly code that implements the
        given arithmetic command
        :param command: string
        :return:
        """
        command = command.replace(" ", "").replace("\t", "")
        sign = self.SIGNS[command]
        self.output.write("// " + command + "\n")
        self.C_ARITHMETIC[command](sign)

    def write_push_helper(self, segment, index, seg):
        """
        This method been called by the writePushPop, and used to write code
        when the push command appears.
        """
        # constant case
        if segment == 'constant':
            self.output.write("@" + str(index) + "\n" + "D=A\n" +
                              self.PUSH_TO_SP)
        # local/argument case
        elif segment == 'local' or segment == 'argument' or segment == \
                'this' or segment == 'that':
            if index == 0:
                self.output.write(seg + "\n" + "D=M\n" + self.PUSH_TO_SP)
            else: # jump to segment + index
                self.output.write(seg + "\n" + "D=M\n" + "@" + str(index) +
                                  "\n" + "A=A+D\n" + "D=M\n" + self.PUSH_TO_SP)
        elif segment == 'temp':
            self.output.write(seg + "\n" + "D=A\n" + "@" + str(index) + "\n" +
                              "A=A+D\n" + "D=M\n" + self.PUSH_TO_SP)
        elif segment == 'pointer' or segment == 'static':
            self.output.write(seg + "\n" + "D=M\n" + self.PUSH_TO_SP)

    def write_pop_helper(self, segment, index, seg):
        """
        This method been called by the writePushPop, and used to write code
        when the pop command appears.
        """
        if segment == 'local' or segment == 'argument' or segment == \
                'this' or segment == 'that':
            self.output.write("@ARG\n" + "D=M\n")
            if index != 0:
                self.output.write(seg + "\n" + "D=M\n" + "@" +
                                  str(index) + "\n" + "A=A+D\n" + "D=A\n")
            self.output.write("@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M-1\n"
                              + "A=M\n" + "D=M\n" + "@SP\n" + "A=M+1\n" +
                              "A=M\n" + "M=D\n")
        elif segment == 'temp':
            self.output.write(seg + "\n" + "D=A\n" + "@" + str(index) + "\n" +
                              "A=A+D\n" + "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n"
                              + "@SP\n" + "M=M-1\n" + "A=M\n" + "D=M\n" +
                              "@SP\n" + "A=M+1\n" + "A=M\n" + "M=D\n")
        elif segment == 'pointer' or segment == 'static':
            self.output.write("@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M-1\n"
                              + "A=M\n" + "D=M\n" + seg + "\n" + "M=D\n")

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
        # segment type
        if segment == 'pointer':
            seg = self.C_SEGMENTS[str(index)]
            index = 0
        elif segment == 'static':
            seg = '@'+self.file_name+'.'+str(index)
        else:
            seg = self.C_SEGMENTS[segment]

        # command type
        if command == self.C_PUSH:
            self.write_push_helper(segment, index, seg)
        else:
            self.write_pop_helper(segment, index, seg)

    def close(self):
        """
        close the output file
        :return:
        """
        self.output.close()

    def setFileName(self, filename):
        """
        Informs the codeWriter that the translation of new VM file has
        started (called by the main program of the VMtranslator)
        :param filename:
        :return:
        """
        self.file_name = filename

    def writeInit(self):
        """
        Writes the assembly code that effects the
        VM initialization, also called bootstrap code.
        This code must be placed at the beginning of
        the output file.
        """
        self.output.write("@256\n"+"D=A\n"+"@SP\n"+"M=D\n")
        self.writeCall(self.SYS_INIT, '0')

    def writeLabel(self, label):
        """
        Writes the assembly code that is the
        translation of the given label command.
        :param label:
        :return:
        """
        self.output.write("// " + "Label "+label+"\n")
        self.output.write("(" + self.function_name +
                          "$" +label+")\n")

    def writeGoto(self, label):
        """
        Writes the assembly code that is the
        translation of the given goto command.
        :param label:
        :return:
        """
        self.output.write("// " + "goto"+" "+label+"\n")
        self.output.write("@"+self.function_name + "$" + label + "\n" +
                          "D=M\n" + "A=D\n" + "@" + self.function_name +
                          "$" + label + "\n" + "0;JMP\n")

    def writeIf(self, label):
        """
        Writes the assembly code that is the
        translation of the given if-goto command.
        :param label:
        :return:
        """
        self.output.write("// " + "if-goto " + label + "\n")
        self.output.write("@SP\n"
                          + "M=M-1\n" + "A=M\n" + "D=M\n" + "@" +
                          self.function_name + "$" + label + "\n" + "D;JNE\n")

    def writefunction(self, function_name, num_vars):
        """
        Writes the assembly code that is the trans. of
        the given function command.
        :param function_name:
        :param num_vars:
        :return:
        """
        self.function_name = function_name
        self.output.write("// " + 'function' + " " + function_name + " " +
                          str(num_vars) +
                          "\n")
        self.output.write("(" + function_name + ")" + "\n")
        for i in range(int(num_vars)):
            self.output.write("@0" + "\n" + "D=A" + "\n" + self.PUSH_TO_SP)

    def writeCall(self, function_name, num_args):
        """
        Writes the assembly code that is the
        translation of the given call command.
        """
        self.output.write("// " + "call "+function_name+" " + num_args+"\n")

        # push returnAdderss
        return_add = "returnAddress"+"."+str(self.fun_count)
        self.write_push_helper('constant', return_add,
                               self.C_SEGMENTS['constant'])
        self.fun_count += 1

        # push LCL
        self.write_push_helper('local', 0, self.C_SEGMENTS['local'])

        #push ARG
        self.write_push_helper('argument', 0, self.C_SEGMENTS['argument'])

        # push THIS
        self.write_push_helper('this', 0, self.C_SEGMENTS['this'])

        # push THAT
        self.write_push_helper('that', 0, self.C_SEGMENTS['that'])

        # ARG = SP-5-narg
        self.output.write("@" + num_args + "\n" + "D=A\n" + "@5\n" +
                          "D=A+D\n" + "@SP\n" + "D = M-D\n" + "@ARG\n" +
                          "M =D\n")

        #LCL=SP
        self.output.write("@SP\n" + "D=M\n" + "@LCL\n" + "M=D\n")

        #goto function name
        self.output.write("@"+function_name + "\n" + "0;JMP\n")

        # (returnAddress)
        self.output.write("(" + return_add + ")\n")

    def writeReturn(self):
        """
        Writes the assembly code that is the
        translation of the given return command.
        """
        self.output.write("// " + "return\n")
        self.output.write("@LCL\n" + "D=M\n" + "@endFrame\n" + "M=D\n")
        self.restore_stack("5", "retAddr")
        self.write_pop_helper('argument', 0, self.C_SEGMENTS['argument'])
        self.output.write("@ARG\n" + "D=M\n" + "@SP\n" + "M=D+1\n")
        self.restore_stack("1", "THAT")
        self.restore_stack("2", "THIS")
        self.restore_stack("3", "ARG")
        self.restore_stack("4", "LCL")
        self.output.write(
            "@retAddr" + "\n" + "D=M" + "\n" + "@i\n" + "A=D\n" + "0;JMP\n")

    def restore_stack(self, i, seg):
        """
        seg = *(endFrame - i)
        """
        self.output.write("@" + i + "\n" +
                          "D=A\n" + "@endFrame\n" + "D=M-D\n" + "@" + seg +
                          "\n" + "A=D\n" + "D=M\n" + "@" + seg + "\n" +
                          "M=D\n")

    def writeLabelOptions(self, c_type, param, param1):
        param1 = str(param1).replace(" ", "").replace("\t", "")
        param = param.replace(" ", "").replace("\t", "")
        c_type = c_type.replace(" ", "").replace("\t", "")
        if param1 == self.SYS_INIT:
             self.writeInit()
        elif c_type == 'label' or c_type == 'goto' or c_type == 'if-goto':
            self.C_LABELS[c_type](param)
        elif c_type == 'function' or c_type == 'call':
            self.C_LABELS[c_type](param, param1)
        elif c_type == 'return':
            self.C_LABELS[c_type]()
