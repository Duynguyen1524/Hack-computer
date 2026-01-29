# -*- coding: utf-8 -*-
"""
Compiler backend for the Hack processor.
Translates from a stack-based intermediate representation language for the virtual machine to Hack assembly code.

Adds support for program flow and subroutines.

Author: Naga Kandasamy
Date modified: November 7, 2024


Student names(s): Jean A. Garcia, Justin Nguyen
Date modified: 
"""
import os
import sys

line_number = 1

def generate_exit_code():
    """Generate epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('(ALL_DONE)')
    s.append('@ALL_DONE')
    s.append('0;JMP')
    return s


def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    Variable is read from the specified memory segment using (base + index) addressing.
    """
    s = [] 
    strindex = str(index)

    if segment == 'constant':
        # FIXME: complete the implementation 
        s.append('@'+strindex)
        s.append('D = A')
        s.append('@SP') 
        s.append('A = M')
        s.append('M = D')
        s.append('@SP')
        s.append('M = M + 1')
        return s
    base_address = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }
    if segment in base_address:
        s.append('@' + strindex)
        s.append('D=A')
        s.append('@' + base_address[segment])
        s.append('A=M+D')
        s.append('D=M')
        s.append('@SP')
        s.append('A=M')
        s.append('M=D')
        s.append('@SP')
        s.append('M=M+1')
        return s

    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segment
    if segment == 'temp':
        s.append('@'+str(5+int(index)))
        s.append('D = M')
        s.append('@SP')
        s.append('A = M')
        s.append('M = D')
        s.append('@SP')
        s.append('M = M + 1')
        return s
    if segment == 'pointer':
        s.append('@'+str(3+int(index)))
        s.append('D = M')
        s.append('@SP')
        s.append('A = M')
        s.append('M = D')
        s.append('@SP')
        s.append('M = M + 1')
        return s
        
    if segment == 'static':
        s.append('@'+str(16+int(index)))
        s.append('D = M')
        s.append('@SP')
        s.append('A = M')
        s.append('M = D')
        s.append('@SP')
        s.append('M = M + 1')
        return s
    return s
    

def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    strindex = str(index)
    base_address = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }
    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    if segment in base_address:
        s.append('@' + strindex)
        s.append('D=A')
        s.append('@' + base_address[segment])
        s.append('D=M+D')
        s.append('@R13')
        s.append('M=D')
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M')
        s.append('@R13')
        s.append('A=M')
        s.append('M=D')
        return s

    if segment == 'temp':
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M')
        s.append('@' + str(5 + int(index)))
        s.append('M=D')
        return s

    if segment == 'pointer':
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M')
        s.append('@' + str(3 + int(index)))
        s.append('M=D')
        return s

    if segment == 'static':
        s.append('@SP')
        s.append('M=M-1')
        s.append('A=M')
        s.append('D=M')
        s.append('@' + str(16 + int(index)))
        s.append('M=D')
        return s

    return s


def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform the specified ALU operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    s.append('D=M')  # Store operand2 in D
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')
    # FIXME: complete implementation for + , - , | , and & operators
    if operation == 'add':
        s.append('M=M+D')  # operand1 + operand2
    elif operation == 'sub':
        s.append('M=M-D')  # operand1 - operand2
    elif operation == 'and':
        s.append('M=M&D')  # operand1 AND operand2
    elif operation == 'or':
        s.append('M=M|D')  # operand1 OR operand2
    
        
    
    
    
    #Push result to stack and adjust SP
    s.append('@SP')
    s.append('M = M + 1')
        
                 
    return s


def generate_unary_operation_code(operation):
    """Generate assembly code to perform the specified unary operation. 
    The operand is popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    
     # FIXME: complete implementation for bit-wise not (!) and negation (-) operatiors
    s.append('@SP')
    s.append('M=M-1')
    s.append('A=M')

    if operation == 'neg':
        s.append('M=-M')  # Negate operand
    elif operation == 'not':
        s.append('M=!M')  # NOT operand

    s.append('@SP')
    s.append('M = M + 1')  
    return s


def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    label_1 = ''
    label_2 = ''
    
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer
    s.append('A=M')
    s.append('D=M')             # D  = operand2
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer to get to operand #1
    s.append('A=M')


    if operation == 'lt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_LT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JLT')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')

    if operation == 'gt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_GT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JGT')       # if operand1 > operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')
    if operation == 'eq':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_EQ_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JEQ')       # if operand1 = operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')
        
   
    # FIXME: complete implementation for eq and gt operations
    
    return s

  

def generate_if_goto_code(label):
    """Generate code for the if-goto statement. 

    Behavior:
    
    1. Pop result of expression from stack.
    2. If result is non-zero, goto LABEL.
    
    """
    s = []
    
    # FIXME: complete implementation
    s.append('@SP')
    s.append('M=M-1')  
    s.append('A=M')
    s.append('D=M')
    s.append('@'+label)
    s.append('D;JNE')


    
    return s

def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []
    
    # FIXME
    s.append('@'+label)
    s.append('0;JMP')
    
    return s

def generate_pseudo_instruction_code(label):   
    """Generate pseudo-instruction for label."""
    s = []
    s.append('(' + label + ')')
    return s

def generate_set_code(register, value):
    """Generate assembly code for set"""
    s = []
    
    s.append('@' + value)
    s.append('D=A')
    
    if register == 'sp':
        s.append('@SP')
    
    if register == 'local':
        s.append('@LCL')
    
    if register == 'argument':
        s.append('@ARG')
        
    if register == 'this':
        s.append('@THIS')
        
    if register == 'that':
        s.append('@THAT')
        
    s.append('M=D')
    
    return s

def generate_function_call_code(function, nargs, line_number):  
    """Generate preamble for function"""
    s = []
    function_label = ('RETURN_' + function + '_' + str(line_number))

    # FIXME: Push return address to stack
    s.append('@'+str(function_label))
    s.append('D=A')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')

    
    # FIXME: Push LCL, ARG, THIS, and THAT registers to stack
    s.append('@LCL')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')

    s.append('@ARG')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')
    
    s.append('@THIS')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')

    s.append('@THAT')
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')
    
    # FIXME: Set ARG register to point to start of arguments in the current frame
    arglocal = 5 + int(nargs)
    s.append('@'+str(arglocal))
    s.append('D=A')
    s.append('@SP')
    s.append('D = M - D')
    s.append('@ARG')
    s.append('M=D')
    # FIXME: Set LCL register to current SP
    s.append('@SP')
    s.append('D = M')
    s.append('@LCL')
    s.append('M = D')
    
    # FIXME: Generate goto code to jump to function 
    s.append("@"+function)
    s.append('0;JMP')
    # FIXME: Generate the pseudo-instruction/label corresponding to the return address
    s.append("("+str(function_label)+")") 
    return s

def generate_function_body_code(f, nvars):
    """Generate code for function f.
    f: name of the function, which should be located in a separate file called f.vm
    n: number of local variables declared within the function.
    """
    s = []
    
    # FIXME: Generate the pseudo instruction -- the label
    s.append("("+f+")")
    # FIXME: Push nvars local variables into the stack, each intialized to zero
    for i in range(0, int(nvars)):
        s.append('@SP')
        s.append('A = M')
        s.append('M = 0')
        s.append('@SP')
        s.append('M = M + 1') 
    return s


def generate_function_return_code():
    """Generate assembly code for function return"""
    s = []
    
    s.append('// Copy LCL to temp register R14 (FRAME)')
    # FIXME: Copy LCL to temp register R14 (FRAME)
    s.append('@LCL')
    s.append('D=M')
    s.append('@R14')
    s.append('M = D')

    s.append('// Store return address in temp register R15 (RET)')
    # FIXME: Store return address in temp register R15 (RET)
    s.append('@5')
    s.append('A=D-A')
    s.append('D=M')
    s.append('@R15')
    s.append('M=D')
    s.append('// Pop result from the working stack and move it to beginning of ARG segment')
    # FIXME: Pop result from the working stack and move it to beginning of ARG segment
    s.append('@SP')
    s.append('M = M - 1')
    s.append('A = M')
    s.append('D = M')
    s.append('@ARG')
    s.append('A=M')
    s.append('M = D')
    # FIXME: Adjust SP = ARG + 1
    s.append('@ARG')
    s.append('D=M+1')
    s.append('@SP')
    s.append('M = D')
    
    # FIXME: Restore THAT = *(FRAME - 1)
    s.append('@R14')
    s.append('D=M-1')
    s.append('A=D')
    s.append('D = M')
    s.append('@THAT')
    s.append('M = D')
    


    # FIXME: Restore THIS = *(FRAME - 2)
    s.append('@2')
    s.append('D = A')
    s.append('@R14')
    s.append('A = M - D')
    s.append('D = M')
    s.append('@THIS')
    s.append('M = D')
    # FIXME: Restore ARG = *(FRAME - 3)
    s.append('@3')
    s.append('D = A')
    s.append('@R14')
    s.append('A = M - D')
    s.append('D = M')
    s.append('@ARG')
    s.append('M = D')
    
    # FIXME: Restore LCL = *(FRAME - 4)
    s.append('@4')
    s.append('D = A')
    s.append('@R14')
    s.append('A = M - D')
    s.append('D = M')
    s.append('@LCL')
    s.append('M = D')
    
    # FIXME: Jump to return address stored in R15 back to the caller code
    s.append('@R15')
    s.append('A = M')
    s.append('0;JMP')
    return s

def translate_vm_commands(tokens, line_number):
    """Translate a VM command into corresponding Hack assembly commands."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
    
    elif tokens[0] == 'label':
        s = generate_pseudo_instruction_code(tokens[1])
    
    elif tokens[0] == 'if-goto':
        s = generate_if_goto_code(tokens[1]) 
        
    elif tokens[0] == 'goto':
        s = generate_goto_code(tokens[1])
    
    elif tokens[0] == 'end':
        s = generate_exit_code()
        
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
        
    elif tokens[0] == 'function':
        s = generate_function_body_code(tokens[1], int(tokens[2]))
        
    elif tokens[0] == 'call':
        s = generate_function_call_code(tokens[1], tokens[2], line_number)
        
    elif tokens[0] == 'return':
        s = generate_function_return_code()
        
    else:
        print('translate_vm_commands: Unknown operation')           # Unknown operation 
    
    return s
    
def translate_file(input_file):
    """Translate VM file to Hack assembly code"""
    global line_number
    assembly_code = []
    assembly_code.append('// ' + input_file)
    
    with open(input_file, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('\n')).split()
            
            if not tokens:
                continue                                        # Ignore blank lines  
            
            if tokens[0] == '//':
                continue                                        # Ignore comment       
            else:
                s = translate_vm_commands(tokens, line_number)
                line_number = line_number + 1        
            if s:
                
                for i in s:
                    assembly_code.append(i)
            else:
                return False
            
    # Write translated commands to .i file
    file_name_minus_extension, _ = os.path.splitext(input_file)
    output_file = file_name_minus_extension + '.i'
    out = open(output_file, 'w')
    for s in assembly_code:
        out.write('%s\n' %s)
    out.close()
    print('Assembly file generated: ', output_file)
        
    return True

def run_vm_to_asm_translator(path):
    """Main translator code"""
    files = os.listdir(path)
    
    cwd = os.getcwd()
    os.chdir(path)
    
    if 'sys.vm' in files:
        idx = files.index('sys.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing sys.vm file')
        return False
        
    if 'main.vm' in files:
        idx = files.index('main.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing main.vm file')
        return False
    
    for f in files:
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    
    os.chdir(cwd)
    
    return True

def assemble_final_file(output_file, path):
    """Assemble final output file"""
    intermediate_files = []
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    with open(output_file, 'w') as outfile:    
        idx = intermediate_files.index('sys.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        idx = intermediate_files.index('main.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        for f in intermediate_files:
            with open(f, 'r') as infile:
                for line in infile:
                    outfile.write(line)

    os.chdir(cwd)
    return True
    
def clean_intermediate_files(path):
    """Removes intermediate .i files from supplied path"""
    intermediate_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in intermediate_files:
        os.remove(f)
    
    os.chdir(cwd)
        

def clean_old_files(path):
    """Removes old files from supplied path"""
    old_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.asm') or f.endswith('.i') or f.endswith('.hack'):
            old_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in old_files:
        os.remove(f)
    
    os.chdir(cwd)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: Python vm_translator_v2.py file-name.asm path-name")
        print("file-name.asm: assembly file to be generated by the translator")
        print("path-name: directory containing .vm source files")
        print("Example: Python vm_translator_v2.py factorial-final.asm ./factorial")
    else:
        output_file = sys.argv[1]
        path = sys.argv[2]
        clean_old_files(path)
        
        status = run_vm_to_asm_translator(path)
        if status == True:
            print('Intermediate assembly files were generated successfully');
            print('Generating final assembly file: ', output_file)
            assemble_final_file(output_file, path)
            # clean_intermediate_files(path)
        else:
            print('Error generating assembly code')