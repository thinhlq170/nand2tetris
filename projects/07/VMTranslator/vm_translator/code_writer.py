from command_type import CommandType
from io import StringIO

class CodeWriter:

    # total_commands = []

    def __init__(self) -> None:
        pass


    def writeArithmetic(self, command: str, index):
        code_gen = StringIO()
        equality_op = command == 'eq' \
            or command == 'lt' \
            or command == 'gt'
        
        logical_2_op = command == 'and' or command == 'or'
        is_1_op = command == 'not' or command == 'neg'

        if is_1_op:
            code_gen.write(self.gen_one_op(command))

        if logical_2_op:
            code_gen.write(self.gen_logical_2_ops(command))
        
        if equality_op:
            code_gen.write(self.gen_equality(command, index))

        if command == 'add':
            code_gen.write(self.gen_add())
        elif command == 'sub':
            code_gen.write(self.gen_sub())


        return code_gen.getvalue()
    
    def writePushPop(self, command: CommandType, segment: str, index: int):
        code_gen = StringIO()
        base = ''
        match segment:
                case 'local':
                    base = 'LCL'
                case 'argument':
                    base = 'ARG'
                case 'this':
                    base = 'THIS'
                case 'that':
                    base = 'THAT'
                case 'temp':
                    base = 'TEMP'
                case 'pointer':
                    base = 'POINTER'
        if command == CommandType.C_POP:
            code_gen.write(self.pop_memory(base, index))
        elif command == CommandType.C_PUSH:
            if segment == 'constant':
                code_gen.write(self.push_constant(index))
            else:
                code_gen.write(self.push_memmory(base, index))

        return code_gen.getvalue()

    def close(self):
        pass

    def pop_memory(self, base: str, index: int) -> str:
        
        
        idx: str = str(index)
        code_gen = StringIO()
        
        if base == 'TEMP':
            '''
                access to temp + i shall be translated into asm code that access to RAM location 5 + i
            '''
            code_gen.write(r'// pop temp ' + idx)
            base = str(5 + index)
            
            code_gen.write('\n')
            code_gen.write(self.pop())
            code_gen.write('@' + base)
            code_gen.write('\n')
            code_gen.write('M=D')
            code_gen.write('\n')
        elif base == 'POINTER':
            code_gen.write(r'// pop pointer ' + idx)
            seg_base = 'THIS'
            if index == 1:
                seg_base = 'THAT'
            
            code_gen.write('\n')
            code_gen.write(self.pop())
            code_gen.write('\n')
            code_gen.write('@' + seg_base)
            code_gen.write('\n')
            code_gen.write('M=D')
            code_gen.write('\n')
                
        else:
            code_gen.write(r'// pop ' + base + r' ' + idx)
            code_gen.write('\n')
            code_gen.write('@' + idx)
            code_gen.write('\n')
            code_gen.write('D=A')
            code_gen.write('\n')
            code_gen.write('@' + base) # base address value is stored in RAM[base]
            code_gen.write('\n')
            code_gen.write('A=M')
            code_gen.write('\n')
            code_gen.write('D=D+A')
            code_gen.write('\n')
            code_gen.write('@' + base)
            code_gen.write('\n')
            code_gen.write('M=D')
            code_gen.write('\n')
            code_gen.write(self.pop())
            code_gen.write('@' + base)
            code_gen.write('\n')
            code_gen.write('A=M')
            code_gen.write('\n')
            code_gen.write('M=D')
            code_gen.write('\n')
            code_gen.write('@' + idx)
            code_gen.write('\n')
            code_gen.write('D=A')
            code_gen.write('\n')
            code_gen.write('@' + base)
            code_gen.write('\n')
            code_gen.write('A=M')
            code_gen.write('\n')
            code_gen.write('D=A-D')
            code_gen.write('\n')
            code_gen.write('@' + base)
            code_gen.write('\n')
            code_gen.write('M=D')
            code_gen.write('\n')
        


        return code_gen.getvalue()

    
    def push_memmory(self, base: str, index: int) -> str:
        idx: str = str(index)
        code_gen = StringIO()
        
        if base == 'TEMP':
            '''
                access to temp + i shall be translated into asm code that access to RAM location 5 + i
            '''
            code_gen.write(r'// push temp ' + idx)
            base = str(5 + index)
            
            code_gen.write('\n')
            code_gen.write('@' + base) # base address value is stored in RAM[base]
            code_gen.write('\n')
            code_gen.write('D=M')
            code_gen.write('\n')
            code_gen.write(self.push('M=D'))
        elif base == 'POINTER':
            code_gen.write(r'// push pointer ' + idx)
            seg_base = 'THIS'
            if index == 1:
                seg_base = 'THAT'
            
            code_gen.write('\n')
            code_gen.write('@' + seg_base)
            code_gen.write('\n')
            code_gen.write('D=M')
            code_gen.write('\n')
            code_gen.write(self.push('M=D'))
        else:
            code_gen.write(r'// push ' + base + r' ' + idx)
            code_gen.write('\n')
            code_gen.write('@' + idx)
            code_gen.write('\n')
            code_gen.write('D=A')
            code_gen.write('\n')
            code_gen.write('@' + base) # base address value is stored in RAM[base]
            code_gen.write('\n')
            code_gen.write('A=M')
            code_gen.write('\n')
            code_gen.write('D=D+A')
            code_gen.write('\n')
            code_gen.write('A=D')
            code_gen.write('\n')
            code_gen.write('D=M')
            code_gen.write('\n')
            code_gen.write(self.push('M=D'))
            code_gen.write('\n')

        
        
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
        code_gen.write(self.push('M=D'))
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

    def push(self, target_instruction: str) -> str:
        code_gen = StringIO()
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('A=M')
        code_gen.write('\n')    
        code_gen.write(target_instruction)
        code_gen.write('\n')    
        code_gen.write('@SP')    
        code_gen.write('\n')    
        code_gen.write('M=M+1')
        code_gen.write('\n')
        return code_gen.getvalue()
    
    def push_bool(self, boolean: bool) -> str:
        code_gen = StringIO()

        if boolean:
            code_gen.write(self.push('M=-1'))
        else:
            code_gen.write(self.push('M=0'))

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

        code_gen.write('// poping operand 1\n')  
        code_gen.write(self.pop())
        code_gen.write('// poping operand 2\n')
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('M=M-1')
        code_gen.write('\n')
        code_gen.write('@SP')
        code_gen.write('\n')    
        code_gen.write('A=M')
        return code_gen.getvalue()
    
    # -------------------------- arithmetic implementation --------------------------

    def gen_add(self) -> str:
        code_gen = StringIO()

        code_gen.write('// add')
        code_gen.write('\n')  
        code_gen.write('@SP')
        code_gen.write('\n')   
        code_gen.write('A=M')   
        code_gen.write('\n')   
        code_gen.write('A=A-1')
        code_gen.write('\n')
        code_gen.write('A=A-1')
        code_gen.write('\n')    
        code_gen.write('D=M')
        code_gen.write('\n')    
        code_gen.write('A=A+1') 
        code_gen.write('\n')
        code_gen.write('D=D+M') #addition
        code_gen.write('\n')
        code_gen.write('@SP')
        code_gen.write('\n')
        code_gen.write('M=M-1')
        code_gen.write('\n')
        code_gen.write('M=M-1')
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

    def gen_sub(self) -> str:
        code_gen = StringIO()
        code_gen.write('// sub')
        code_gen.write('\n')
        code_gen.write('@SP')
        code_gen.write('\n')
        code_gen.write('A=M')
        code_gen.write('\n')
        code_gen.write('A=A-1')
        code_gen.write('\n')
        code_gen.write('A=A-1')
        code_gen.write('\n')
        code_gen.write('D=M')
        code_gen.write('\n')
        code_gen.write('A=A+1')
        code_gen.write('\n')
        code_gen.write('D=D-M')
        code_gen.write('\n')
        code_gen.write('@SP')
        code_gen.write('\n')
        code_gen.write('M=M-1')
        code_gen.write('\n')
        code_gen.write('M=M-1')
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

    def gen_equality(self, operation: str, index) -> str:
        '''
            This function generates equality instructions.
            argument index (code line) is required because of marking
            for TRUE/FALSE jumping label.
        '''
        code_gen = StringIO()

        target_instruction = 'UNDEFINED_OPERATION'
        if operation == 'eq':
            target_instruction = 'D;JEQ'
            code_gen.write('// generate eq\n')
        elif operation == 'lt':
            target_instruction = 'D;JLT'
            code_gen.write('// generate lt\n')
        elif operation == 'gt':
            target_instruction = 'D;JGT'
            code_gen.write('// generate gt\n')

        code_gen.write(self.pop_2_ops())
        code_gen.write('\n')
        code_gen.write('D=M-D')
        code_gen.write('\n')
        code_gen.write('@TRUE' + str(index))
        code_gen.write('\n')
        code_gen.write(target_instruction)
        code_gen.write('\n')
        code_gen.write(self.push_bool(False))
        code_gen.write('@SKIP' + str(index))
        code_gen.write('\n')
        code_gen.write('0;JMP')
        code_gen.write('\n')
        code_gen.write('(TRUE' + str(index) + ')')
        code_gen.write('\n')
        code_gen.write(self.push_bool(True))
        code_gen.write('(SKIP' + str(index) + ')')
        code_gen.write('\n')

        return code_gen.getvalue()
    
    def gen_one_op(self, operation: str) -> str:
        '''
            This function generates asm code for one operand arithmetic such as
            not, negation.
            Default generation is for negation
        '''
        code_gen = StringIO()

        target_instruction = 'UNDEFINED_OPERATION'
        if operation == 'not':
            code_gen.write('// proceed NOT operation\n')
            target_instruction = 'M=!D'
        else:
            code_gen.write('// proceed negation\n')
            target_instruction = 'M=-D'

        
        code_gen.write(self.pop())
        code_gen.write(self.push(target_instruction))

        return code_gen.getvalue()
    
    def gen_logical_2_ops(self, operation: str) -> str:
        '''
            This function generates asm code for logical operation with 2 operands
            such as AND, OR.
        '''
        code_gen = StringIO()

        target_instruction = 'UNDEFINED_OPERATION'
        if operation == 'and':
            code_gen.write('// Proceed AND\n')
            target_instruction = 'D=D&M'
        elif operation == 'or':
            code_gen.write('// Proceed OR\n')
            target_instruction = 'D=D|M'
        
        code_gen.write(self.pop_2_ops())
        code_gen.write('\n')
        code_gen.write(target_instruction)
        code_gen.write('\n')

        code_gen.write(self.push('M=D'))

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
