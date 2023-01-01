import re

class Parser:

    # ----- Class constant ------ #
    C_ARITHMETIC = ['add', 'sub', 'neg', 'and', 'eq', 'or', 'gt', 'lt', 'not']
    C_PUSH = 'push'
    C_POP = 'pop'
    # C_LABEL =''
    # C_GOTO = 5
    # C_IF = 6
    # C_RETURN = 7
    # C_CALL = 8

    def __init__(self, file_name):
        """
        Opens the input file and get ready to parse it
        :param file_name:
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
        else:
            return self.C_ARITHMETIC

    def arg1(self):
        """
        This method returns the first argument of the current command.
        :return: string
        """
        if self.commandType() == self.C_POP or self.commandType() \
                == self.C_PUSH:
            return self.current_line[1]
        else:
            return self.current_line[0]

    def arg2(self):
        """
        This method returns the second argument of the current command.
        :return: int
        """
        return int(self.current_line[2])
