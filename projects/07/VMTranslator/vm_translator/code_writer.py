from command_type import CommandType
from io import StringIO

class CodeWriter:

    # total_commands = []

    def __init__(self) -> None:
        pass


    def writeArithmetic(self, command: str):
        code_gen = StringIO()
        match command:
            case 'add':
                code_gen.write(self.add())
            case 'eq':
                code_gen.write(self.equal())

        return code_gen.getvalue()
    
    def writePushPop(self, command: CommandType, segment: str, index: int):
        code_gen = StringIO()
        base = ''
        match segment:
                case 'local':
                    base = 'LCL'
                case 'argument':
                    base = 'ARG'
                case 'this' | 'pointer':
                    base = 'THIS'
                case 'that':
                    base = 'THAT'
                case 'temp':
                    base = 'TEMP'
        if command == CommandType.C_POP:
            code_gen.write(self.pop(base, index))
        elif command == CommandType.C_PUSH:
            if segment == 'constant':
                code_gen.write(self.push_constant(index))
            else:
                code_gen.write(self.push_memmory(base, index))

        return code_gen.getvalue()

    def close(self):
        pass

    def pop(self, base: str, index: int) -> str:
        idx: str = str(index)
        code_gen = StringIO()
        code_gen.write(r'// pop ' + base + r' ' + idx)
        
        code_gen.write(r'// assign new address is "base" plus ' + idx + ' ' + r'to R13 as a temporary')
        code_gen.write('@' + idx)
        code_gen.write('D=A')
        code_gen.write('@' + base) # base address value is stored in RAM[base]
        code_gen.write('D=D+M')
        code_gen.write('@R13')
        code_gen.write('M=D')

        code_gen.write(r'// pop the stack and assign the value to the new address')
        code_gen.write(self.pop())
        code_gen.write('@R13')
        code_gen.write('A=M')
        code_gen.write('M=D')


        return code_gen.getvalue()

    
    def push_memmory(self, base: str, index: int) -> str:
        idx: str = str(index)
        code_gen = StringIO()

        code_gen.write(r'// push ' + base + ' ' + idx)
        code_gen.write('\n')
        code_gen.write('@' + idx)
        code_gen.write('\n')
        code_gen.write('D=A')
        code_gen.write('\n')
        code_gen.write('@' + base) # base address value is stored in RAM[base]
        code_gen.write('\n')
        code_gen.write('D=D+M')
        code_gen.write('\n')
        code_gen.write('A=D')
        code_gen.write('\n')
        code_gen.write('D=M')
        code_gen.write('\n')
        code_gen.write(self.push())
        
        code_gen.write(r'// push ' + base + r' ' + idx)

        return code_gen.getvalue()

    def push_constant(self, index: int) -> str:
        idx: str = str(index)
        code_gen = StringIO()
        code_gen.write(r'// push constant ' + idx)
        code_gen.write('\n')
        code_gen.write('@' + idx)
        code_gen.write('\n')    
        code_gen.write('D=A')
        code_gen.write('\n')    
        code_gen.write(self.push())
        return code_gen.getvalue()
          

    def initialize_SP(self) -> str:
        '''
        This function sets stack pointer to beginning of the stack address
        which has value is 256
        '''
        code_gen = StringIO()
        code_gen.write('@256 // base address of the stack')
        code_gen.write('\n')
        code_gen.write('D=A')
        code_gen.write('\n')
        code_gen.write('@SP')
        code_gen.write('\n')
        code_gen.write('M=D')
        code_gen.write('\n')
        return code_gen.getvalue()

    def push(self) -> str:
        code_gen = StringIO()
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('A=M')
        code_gen.write('\n')    
        code_gen.write('M=D')
        code_gen.write('\n')    
        code_gen.write('@SP')    
        code_gen.write('\n')    
        code_gen.write('M=M+1')
        code_gen.write('\n')
        return code_gen.getvalue()
    
    def push_bool(self, boolean: bool) -> str:
        code_gen = StringIO()
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('A=M')
        code_gen.write('\n')
        if boolean:
            code_gen.write('M=-1')
        else:
            code_gen.write('M=0')
        code_gen.write('\n')    
        code_gen.write('@SP')    
        code_gen.write('\n')    
        code_gen.write('M=M+1')
        return code_gen.getvalue()

    def pop(self) -> str:
        code_gen = StringIO()

        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('M=M-1') # <=> AM=M-1
        code_gen.write('\n')    
        code_gen.write('A=M')
        code_gen.write('\n')    
        code_gen.write('D=M')
        code_gen.write('\n')

        return code_gen.getvalue()
    
    
    
    def pop_2_ops(self) -> str:
        code_gen = StringIO()

        code_gen.write('// adding operation')
        code_gen.write('\n')  
        code_gen.write('// poping operand 1\n')  
        code_gen.write(self.pop())
        code_gen.write('// poping operand 2\n')
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('M=M-1')
        code_gen.write('\n')    
        code_gen.write('A=M')
        return code_gen.getvalue()
    
    # -------------------------- arithmetic implementation --------------------------

    def add(self) -> str:
        code_gen = StringIO()

        code_gen.write('// adding operation')
        code_gen.write('\n')  
        code_gen.write('// poping operand 1\n')  
        code_gen.write(self.pop())
        code_gen.write('// poping operand 2\n')
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('M=M-1')
        code_gen.write('\n')    
        code_gen.write('A=M')
        code_gen.write('\n')    
        code_gen.write('D=D+M') #addition
        code_gen.write('\n')
        code_gen.write(self.push())

        return code_gen.getvalue()

    def sub(self) -> str:
        code_gen = StringIO()
        code_gen.write(self.pop_2_ops())
        code_gen.write('\n')
        code_gen.write('D=D-M')
        code_gen.write('\n')
        code_gen.write(self.push())

        return code_gen.getvalue()

    def equal(self) -> str:
        code_gen = StringIO()

        code_gen.write('// Check equality\n')

        code_gen.write(self.pop_2_ops())
        code_gen.write('\n')
        code_gen.write('D=D-M')
        code_gen.write('\n')
        code_gen.write('@TRUE')
        code_gen.write('\n')
        code_gen.write('D;JEQ')
        code_gen.write('\n')
        code_gen.write(self.push_bool(False))
        code_gen.write('\n')
        code_gen.write('@SKIP')
        code_gen.write('\n')
        code_gen.write('0;JMP')
        code_gen.write('\n')
        code_gen.write('(TRUE)')
        code_gen.write('\n')
        code_gen.write(self.push_bool(True))
        code_gen.write('\n')
        code_gen.write('(SKIP)')
        code_gen.write('\n')

        return code_gen.getvalue()
    
    def end(self) -> str:
        code_gen = StringIO()

        code_gen.write('(END)')
        code_gen.write('\n')   
        code_gen.write('@END')
        code_gen.write('\n')    
        code_gen.write('0;JMP')
        code_gen.write('\n')

        return code_gen.getvalue()
