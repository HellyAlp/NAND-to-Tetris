import re


class Parser:
    """
    This class is the Parser class. It executes the parsing stage in
    the assembler..
    """
    # ----- Class constant ------ #
    C_ARITHMETIC = ['add', 'sub', 'neg', 'and', 'eq', 'or', 'gt', 'lt', 'not']
    ARITHMETIC = 'arithmetic'
    C_PUSH = 'push'
    C_POP = 'pop'
    C_LABELS = ['goto', 'if-goto', 'label', 'call', 'function', 'return']

    def __init__(self, file_name):
        """
        The class constructor. It opens the input file and get ready to
        parse it
        :param file_name: the file to parse
        """
        self.lines = []
        self.current_line_num = 0
        self.current_line = []
        with open(file_name, 'r')as file_input:
            for line in file_input:
                reg = re.compile('^[//]|^[\\s]*$')
                is_match = reg.match(line)
                if is_match is not None:
                    continue
                self.lines.append(line.rstrip("\n"))

    def hasMoreCommands(self):
        """
        This methods checks if there are more commands in the input file
        :return: True ir False
        """
        return self.current_line_num < len(self.lines)

    def advance(self):
        """
        This methods reads the next command from the input and makes it the
        current command
        """
        self.current_line = self.lines[self.current_line_num].split(" ")
        self.current_line_num += 1

    def commandType(self):
        """
        This method returns a constant representing the type of the current
        command.
        """
        if self.current_line[0] == self.C_POP:
            return self.C_POP
        elif self.current_line[0] == self.C_PUSH:
            return self.C_PUSH
        elif self.current_line[0] in self.C_LABELS:
            return self.current_line[0]
        else:
            return self.ARITHMETIC

    def arg1(self):
        """
        This method returns the first argument of the current command.
        :return: string
        """
        if self.commandType() == self.ARITHMETIC:
            return self.current_line[0]
        else:
            return self.current_line[1]

    def arg2(self):
        """
        This method returns the second argument of the current command.
        :return: int
        """
        return self.current_line[2]
