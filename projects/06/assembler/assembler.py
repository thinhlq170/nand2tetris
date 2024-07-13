import re
from enum import Enum

class Parser:
    """  
    A Parser module that parses the input.
    """
    
    
    
    def __init__(self, filePath):
        self.code = Code()
        self.symbolTable = SymbolTable()
        self.commandType = None
        self.currentOffset = 0
        self.currentCommand = None
        self.lines = []
        self.result = []
        self.currentLine = 0
        try:
            with open(filePath, 'r') as file_stream:
                for line in file_stream:
                    line = line.strip()
                    # if the line is a comment then skip the line
                    if not line.startswith('//'):
                        self.lines.append(line)
        except FileNotFoundError:
            print(f"Error: The file {filePath} was not found.")
        except IOError:
            print(f"Error: Could not read the file {filePath}")
            
        self.pass1(self)
        self.pass2(self)
            
    def pass1(self):
        while (self.hasMoreCommand()):
            if (self.commandType() == CommandType.A_COMMAND) or (self.commandType() == CommandType.C_COMMAND):
                self.currentLine += 1
            
            if self.commandType() == CommandType.L_COMMAND:
                table = self.symbolTable
                symbol = self.symbol(self)
                table.addEntry(symbol, self.currentLine + 1)
            self.advance()
        
        # reset current offset to the first point in the assembly file after completing pass1    
        self.currentOffset = 0    
    
    def pass2(self):
        while (self.hasMoreCommand()):
            if self.commandType() == CommandType.C_COMMAND:
                self.currentLine += 1
                code = self.code
                dest = self.dest()
                comp = self.comp()
                jump = self.jump()
                commandPrefix = '111'
                binDest = code.dest(dest)
                binComp = code.comp(comp)
                binJump = code.jump(jump)
                binCommand = f'{commandPrefix}{binComp}{binDest}{binJump}'
                self.result.append(binCommand)
            elif self.commandType == CommandType.A_COMMAND:
                # TODO: complete pass2 for A_COMMAND
                pass
            self.advance()

    def hasMoreCommand(self) -> bool:
        """
        Are there more commands in the input?
        """
        nextOffset = self.currentOffset + 1
        return nextOffset < len(self.lines)
        
    
    def advance(self):
        """
        Reads the next command from the input and makes it the current command. 
        Should be called only if hasMoreCommands() is true. 
        Initially there is no current command.
        """
        if self.hasMoreCommand(self):
            self.currentOffset += 1
            self.currentCommand = self.lines[self.currentOffset]
            return self.currentCommand
        

    def commandType(self):
        """
        Returns the type of the current command:
        1. A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        2. C_COMMAND for dest=comp;jump. Either the dest or jump fields may be empty
        3. L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.
        """
        commandPattern = r'(?://)?.*$'
        
        command = re.search(commandPattern, self.currentCommand)
        if command:
            commandPatternA = "^@.*"
            commandPatternC = ".*=?.*;?.*"
            commandPatternL = "\(.*\).*"
            
            if re.match(commandPatternA, command):
                return CommandType.A_COMMAND
            elif re.match(commandPatternC, command):
                return CommandType.C_COMMAND
            elif re.match(commandPatternL, command):
                return CommandType.L_COMMAND
        
    def symbol(self) -> str:
        """
        Returns: 
        str: Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). 
        Should be called only when commandType() is A_COMMAND or L_COMMAND.
        """
        if self.currentCommand != "":
            if self.commandType == CommandType.A_COMMAND:
                commandPatternA = r'^@(.*)(?://)?.*$'
                match = re.search(commandPatternA, self.currentCommand)
                if match:
                    return match.group(1)
            elif self.commandType == CommandType.L_COMMAND:
                commandPatternL = r'^\(.*\).*'
                match = re.search(commandPatternL, self.currentCommand)
                if match:
                    return match.group(1)
    
    def dest(self) -> str:
        """
        C_COMMAND for dest=comp;jump
        Returns:
            str: Returns the dest mnemonic in the current C-command (8 possibilities). 
            Should be called only when commandType() is C_COMMAND.
        """
        if self.commandType == CommandType.C_COMMAND:
            commandPatternC = r'(.*)\s*=.*;?.*$'
            match = re.search(commandPatternC, self.currentCommand)
            if match:
                return match.group(1)
    
    def comp(self) -> str:
        """
        Returns:
            str:  Returns the comp mnemonic in the current C-command (28 possibilities). 
            Should be called only when commandType() is C_COMMAND.
        """
        if self.commandType == CommandType.C_COMMAND:
            commandPatternC = r'.*=?\s*(.*)\s*;?.*$'
            match = re.search(commandPatternC, self.currentCommand)
            if match:
                return match.group(1)
    
    def jump(self) -> str:
        """
        Returns:
            str: Returns the jump mnemonic in the current C-command (8 possibilities). 
            Should be called only when commandType() is C_COMMAND.
        """
        if self.commandType == CommandType.C_COMMAND:
            commandPatternC = r'.*=?.*;\s*(.*)$'
            match = re.search(commandPatternC, self.currentCommand)
            if match:
                return match.group(1)
    


class Code:
    """
    A Code module that provides the binary codes of all the assembly mnemonics.
    """
    def dest(mnemonic: str):
        """
        Returns the binary code of the dest mnemonic. (3 bits)
        """
        try:
            if mnemonic == 'null' or mnemonic is None:
                return '000'
            elif mnemonic == 'M':
                return '001'
            elif mnemonic == 'D':
                return '010'
            elif mnemonic == 'MD':
                return '011'
            elif mnemonic == 'A':
                return '100'
            elif mnemonic == 'AM':
                return '101'
            elif mnemonic == 'AD':
                return '110'
            elif mnemonic == 'AMD':
                return '111'
            else:
                raise InvalidCommandException
        except InvalidCommandException:
            print("Exception occured: Invalid 'dest' Command")
            
    
    def comp(mnemonic: str):
        """
        Returns the binary code of the comp mnemonic. (7 bits)
        """
        try:
            if mnemonic == '0':
                return '0101010'
            elif mnemonic == '1':
                return '0111111'
            elif mnemonic == '-1':
                return '0111010'
            elif mnemonic == 'D':
                return '0001100'
            elif mnemonic == 'A':
                return '0110000'
            elif mnemonic == 'M':
                return '1110000'
            elif mnemonic == '!D':
                return '0001101'
            elif mnemonic == '!A':
                return '0110001'
            elif mnemonic == '!M':
                return '1110001'
            elif mnemonic == '-D':
                return '0001111'
            elif mnemonic == '-A':
                return '0110011'
            elif mnemonic == '-M':
                return '1110011'
            elif mnemonic == 'D+1':
                return '0011111'
            elif mnemonic == 'A+1':
                return '0110111'
            elif mnemonic == 'M+1':
                return '1110111'
            elif mnemonic == 'D-1':
                return '0001110'
            elif mnemonic == 'A-1':
                return '0110010'
            elif mnemonic == 'M-1':
                return '1110010'
            elif mnemonic == 'D+A':
                return '0000010'
            elif mnemonic == 'D+M':
                return '1000010'
            elif mnemonic == 'D-A':
                return '0010011'
            elif mnemonic == 'D-M':
                return '1010011'
            elif mnemonic == 'A-D':
                return '0000111'
            elif mnemonic == 'M-D':
                return '1000111'
            elif mnemonic == 'D&A':
                return '0000000'
            elif mnemonic == 'D&M':
                return '1000000'
            elif mnemonic == 'D|A':
                return '0010101'
            elif mnemonic == 'D|M':
                return '1010101'
            else:
                raise InvalidCommandException
        except InvalidCommandException:
            print("Exception occured: Invalid 'comp' Command")
    
    def jump(mnemonic: str):
        """
        Returns the binary code of the jump mnemonic. (3 bits)
        """
        
        try:
            if mnemonic == 'null' or mnemonic is None:
                return '000'
            elif mnemonic == 'JGT':
                return '001'
            elif mnemonic == 'JEQ':
                return '010'
            elif mnemonic == 'JGE':
                return '011'
            elif mnemonic == 'JLT':
                return '100'
            elif mnemonic == 'JNE':
                return '101'
            elif mnemonic == 'JLE':
                return '110'
            elif mnemonic == 'JMP':
                return '111'
            else:
                raise InvalidCommandException
        except InvalidCommandException:
            print("Exception occured: Invalid 'jump' Command")


class SymbolTable:
    """
    A SymbolTable module that handles symbols.
    """
    
    def __init__(self):
        """
        Creates a new empty symbol table.
        """
        self.table = {}
        for i in range(0, 16):
            self.addEntry('R' + str(i), i)
            
        self.addEntry('SP', 0)
        self.addEntry('LCL', 1)
        self.addEntry('ARG', 2)
        self.addEntry('THIS', 3)
        self.addEntry('THAT', 4)
        self.addEntry('SCREEN', 16384)
        self.addEntry('KBD', 24576)
        
        
    def addEntry(self, symbol: str, address: int):
        """
        Adds the pair (symbol, address) to the table
        """
        self.table[symbol] = address
        
    def contains(self, symbol: str):
        """
        Does the symbol table contain the given symbol?
        """
        return symbol in self.table
    
    def getAddress(self, symbol: str):
        """
        Returns the address associated with the symbol.
        """
        if self.contains(symbol):
            return self.table.get(symbol)

class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
    
class InvalidCommandException(Exception):
    "The command is not supported!"
    pass    
        
