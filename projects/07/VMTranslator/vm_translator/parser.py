from command_type import CommandType
import re

class Parser:

    total_lines = []

    def __init__(self, file_path) -> None:
        try:
            with open(file_path, 'r') as file:
                self.total_lines = [line.strip() for line in file.readlines() 
                                    if line.strip() and not line.strip().startswith(r'//')]

            self.line_pointer = 0
            self.current_command = None
        except FileNotFoundError:
            print("Error: The file does not exist.")

    def hasMoreLines(self):
        if self.total_lines[self.line_pointer + 1]:
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
        if self.commandType(cur_command) == CommandType.C_ARITHMETIC:
            arg = cur_command
        elif self.commandType(cur_command) == CommandType.C_POP \
            or self.commandType(cur_command) == CommandType.C_PUSH:

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
        if self.commandType(cur_command) == CommandType.C_POP \
            or self.commandType(cur_command) == CommandType.C_PUSH:

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