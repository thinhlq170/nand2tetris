from command_type import CommandType

class Command:
    def __init__(self, command_type: CommandType, arg1: str, arg2: int) -> None:
        self.command_type = command_type
        self.arg1 = arg1
        self.arg2 = arg2