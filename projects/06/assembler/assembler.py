import re
from enum import Enum

class Parser:
    """  
    A Parser module that parses the input.
    """
    
    def __init__(self, filePath):
        self.commandType = None
        self.currentOffset = 0
        self.currentCommand = None
        self.lines = []
        try:
            with open(filePath, 'r') as file_stream:
                for line in file_stream:
                    line = line.strip()
                    # if the line is a comment then skip the line
                    if not line.startswith('//'):
                        self.lines.append(line.strip())
        except FileNotFoundError:
            print(f"Error: The file {filePath} was not found.")
        except IOError:
            print(f"Error: Could not read the file {filePath}")

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
        2. C_COMMAND for dest=comp;jump
        3. L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.
        """
        commandPattern = r'(?://)?.*$'
        
        command = re.search(commandPattern, self.currentCommand)
        if command:
            commandPatternA = "^@.*"
            commandPatternC = ".*=.*;.*"
            commandPatternL = "\(.*\).*"
            
            if re.match(commandPatternA, command):
                self.commandType = CommandType.A_COMMAND
            elif re.match(commandPatternC, command):
                self.commandType = CommandType.C_COMMAND
            elif re.match(commandPatternL, command):
                self.commandType = CommandType.L_COMMAND
        
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
                commandPatternL = "^\(.*\).*"
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
            commandPatternC = r'(.*)\s*=\s*(.*)\s*;\s*(.*)$'
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
            commandPatternC = r'(.*)\s*=\s*(.*)\s*;\s*(.*)$'
            match = re.search(commandPatternC, self.currentCommand)
            if match:
                return match.group(2)
    
    def jump(self) -> str:
        """
        Returns:
            str: Returns the jump mnemonic in the current C-command (8 possibilities). 
            Should be called only when commandType() is C_COMMAND.
        """
        if self.commandType == CommandType.C_COMMAND:
            commandPatternC = r'(.*)\s*=\s*(.*)\s*;\s*(.*)$'
            match = re.search(commandPatternC, self.currentCommand)
            if match:
                return match.group(3)
    


class Code:
    """
    A Code module that provides the binary codes of all the assembly mnemonics.
    """
    def dest(mnemonic: str):
        """
        Returns the binary code of the dest mnemonic. (3 bits)
        """
        pass
    
    def comp(mnemonic: str):
        """
        Returns the binary code of the comp mnemonic. (7 bits)
        """
        pass
    
    def jump(mnemonic: str):
        """
        Returns the binary code of the jump mnemonic. (3 bits)
        """
        pass


class SymbolTable:
    """
    A SymbolTable module that handles symbols.
    """
    
    def __init__(self):
        """
        Creates a new empty symbol table.
        """
        self.symbolTable = {}
        
    def addEntry(self, symbol: str, address: int):
        """
        Adds the pair (symbol, address) to the table
        """
        self.symbolTable[symbol] = address
        
    def contains(self, symbol: str):
        """
        Does the symbol table contain the given symbol?
        """
        return symbol in self.symbolTable
    
    def getAddress(self, symbol: str):
        """
        Returns the address associated with the symbol.
        """
        if self.contains(symbol):
            return self.symbolTable.get(symbol)

class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3        
        
