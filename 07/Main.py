import sys
import os
from Parser import *
from CodeWriter import *


class Main:
    """
    This class is the main class. It rus the VM to Assembly program.
    """

    # ----- Class constant ------ #
    C_ARITHMETIC = ['add', 'sub', 'neg', 'and', 'eq', 'or', 'gt', 'lt', 'not']
    C_PUSH = 'push'
    C_POP = 'pop'

    def __init__(self, path):
        """
        A constructor that init all of the program
        :param path: a path to a file\folder
        """
        # parse all input files
        input_files, output_file = self.create_files(path)
        self.codeWriter = CodeWriter(output_file)
        for file in input_files:
            file_name = os.path.basename(file).split('.')[0]
            self.codeWriter.file_name = file_name
            self.parser = Parser(file)
            while self.parser.hasMoreCommands():
                self.parser.advance()
                c_type = self.parser.commandType()
                if c_type == self.C_PUSH or c_type == self.C_POP:
                    self.codeWriter.writePushPop(c_type, self.parser.arg1(),
                                                 self.parser.arg2())
                else:
                    self.codeWriter.writeArithmetic(self.parser.arg1())
        self.codeWriter.close()

    def create_files(self, path):
        """
        This function creates the output file
        :param path:
        :return: the output file
        """
        input_files = self.files_reader(path)
        if os.path.isdir(path):
            if path.endswith("/"):
                path = path[0:-1]
            folder = os.path.basename(path)
            output_file = path + "/" + folder + ".asm"
        else:
            output_file = input_files[0].split('.')[0]
            output_file = str(output_file) + ".asm"
        return input_files, output_file


    def files_reader(self, path):
        """
        A method that finds the relevant files
        :param path: path given in the program arguments
        :return: input_files list
        """
        input_files = []
        if not os.path.isdir(path):
            input_files.append(path)
            return input_files
        for dir_path, x, file_names in os.walk(path):

            for file in file_names:
                if file.endswith(".vm"):
                    input_files.append(os.path.abspath(os.path.join(dir_path,
                                                                    file)))
        return input_files


if __name__ == '__main__':
    main = Main(sys.argv[1])
