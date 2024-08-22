from command_type import CommandType
import re
import os
from command import Command
from code_writer import CodeWriter

class Parser:

    total_lines = []
    

    def __init__(self, file_path) -> None:
        try:
            with open(file_path, 'r') as file:
                self.line_pointer = -1
                self.current_command = None
                self.total_commands: list[Command] = []

                self.total_lines = [line.strip() for line in file.readlines() 
                                    if line.strip() and not line.strip().startswith(r'//')]
                while (True):
                    if (self.hasMoreLines()):
                        self.advance()
                        cur_command = self.current_command
                        command_type = self.commandType()
                        arg1: str = ''
                        arg2: int = -1
                        if command_type == CommandType.C_PUSH \
                            or command_type == CommandType.C_POP:
                            arg1 = self.arg1()
                            arg2 = self.arg2()
                        elif command_type == CommandType.C_ARITHMETIC:
                            arg1 = self.arg1()
                        
                        self.total_commands.append(Command(command_type, arg1, arg2))
                    else:
                        break


            dir_path = os.path.dirname(file_path)
            output_path = dir_path + r'/out.asm'
            writer = CodeWriter()
            with open(output_path, 'w') as file:
                stack_pointer = writer.initialize_SP()
                file.write(stack_pointer)
                for command in self.total_commands:
                    code_gen = ''
                    if command.command_type == CommandType.C_ARITHMETIC:
                        code_gen = writer.writeArithmetic(arg1)
                    else:
                        code_gen = writer.writePushPop(command.command_type, command.arg1, command.arg2)
                    file.write(code_gen)
                
                file.write(writer.end())

            
        except FileNotFoundError:
            print("Error: The file does not exist.")

    def hasMoreLines(self):
        if self.line_pointer + 1 < len(self.total_lines):
            return True
        return False

    def advance(self):
        """This function reads the next command from the input
        and makes it the current command.
        This routine should be called only if hasMoreLines is true.
        Initially there is no current command.
        """

        if (self.hasMoreLines()):
            self.line_pointer += 1
            self.current_command = self.total_lines[self.line_pointer]

    def commandType(self) -> CommandType:
        """This function returns a constant representing the type of
        the current command.

        Returns:
            CommandType: an enumeration of command type
        """

        command_type = CommandType.C_UNDEFINED
        cur_command = self.current_command

        is_arithmetic = cur_command == 'add' \
            or cur_command == 'sub' \
            or cur_command == 'neg' \
            or cur_command == 'eq' \
            or cur_command == 'gt' \
            or cur_command == 'lt' \
            or cur_command == 'and' \
            or cur_command == 'or' \
            or cur_command == 'not'

        if self.is_push_command(cur_command):
            command_type = CommandType.C_PUSH
        elif self.is_pop_command(cur_command):
            command_type = CommandType.C_POP
        elif is_arithmetic:
            command_type = CommandType.C_ARITHMETIC
        
        return command_type

    def arg1(self) -> str:
        """Gets the first argument of the current command.
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
        Should not be called if the current command is C_RETURN

        Returns:
            str: the first argument of the current command.
        """
        arg = ''
        cur_command = self.current_command
        if self.commandType() == CommandType.C_ARITHMETIC:
            arg = cur_command
        elif self.commandType() == CommandType.C_POP \
            or self.commandType() == CommandType.C_PUSH:

            arg = cur_command.split(' ')[1]
        return arg

    def arg2(self) -> int:
        """Gets the second argument of the current command.
        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL

        Returns:
            int: Returns the second argument of the current command.
        """
        cur_command = self.current_command
        arg = -1
        if self.commandType() == CommandType.C_POP \
            or self.commandType() == CommandType.C_PUSH:

            arg = int(cur_command.split(' ')[2])
        return arg

    def is_pop_command(self, text):
        pattern = r'^pop\s+.*\s+\d+'
        match = re.match(pattern, text)
        if match:
            return True
        return False
    
    def is_push_command(self, text):
        pattern = r'^push\s+.*\s+\d+'
        match = re.match(pattern, text)

        if match:
            return True
        return False