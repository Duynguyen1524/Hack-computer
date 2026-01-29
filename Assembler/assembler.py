# -*- coding: utf-8 -*-
"""
Assembler for the Hack processor.

Author: Naga Kandasamy
Date modified: October 28, 2024

Student name(s): Jean A. Garcia, Justin Nguyen
Date modified: 
"""

import os
import sys

"""The comp field is a c1 c2 c3 c4 c5 c6"""
valid_comp_patterns = {'0':'0101010', 
                       '1':'0111111',
                       '-1':'0111010',
                       'D':'0001100',
                       'A':'0110000',
                       '!D':'0001101',
                       '!A':'0110001',
                       '-D':'0001111',
                       '-A':'0110011',
                       'D+1':'0011111',
                       'A+1':'0110111',
                       'D-1':'0001110',
                       'A-1':'0110010',
                       'D+A':'0000010',
                       'D-A':'0010011',
                       'A-D':'0000111',
                       'D&A':'0000000',
                       'D|A':'0010101',
                       'M':'1110000',
                       '!M':'1110001',
                       '-M':'1110011',
                       'M+1':'1110111',
                       'M-1':'1110010',
                       'D+M':'1000010',
                       'M+D':'1000010',
                       'D-M':'1010011',
                       'M-D':'1000111',
                       'D&M':'1000000',
                       'D|M':'1010101'
                       }

"""The dest bits are d1 d2 d3"""
valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

"""The jump fields are j1 j2 j3"""
valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

"""Symbol table populated with predefined symbols and RAM locations"""
symbol_table = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }

ram_address = 16  # Base RAM address for variable allocation

"""Label dictionary."""
label_list = {}

def print_intermediate_representation(ir):
    """Prints the intermediate representation of parsed instructions."""
    for i in ir:
        print()
        for key, value in i.items():
            print(f"{key} : {value}")

def print_instruction_fields(fields):
    """Prints each field in the parsed instruction."""
    for key, value in fields.items():
        print(f"{key} : {value}")

def valid_tokens(sequence):
    """Placeholder for token validation."""
    return True

def generate_machine_code(s):
    """Generate machine code from parsed structure."""
    global ram_address

    if(s.startswith("@")):
        #A-type
        #Check if numeric
        if(s.strip("@").isnumeric()):
            return '{0:016b}'.format(int(s.strip("@")))
        else:
            if label_list.get(s.strip("@")) != None: 
                return '{0:016b}'.format(int(label_list[s.strip("@")]))
            elif symbol_table.get(s.strip("@")) != None: 
                return '{0:016b}'.format(int(symbol_table[s.strip("@")]))
            else:
                symbol_table[s.strip("@")] = ram_address
                ram_address = ram_address + 1
                return '{0:016b}'.format(int(symbol_table[s.strip("@")]))
    else:
        cmd = s.replace(" ", "")
        isJump = ";" in cmd
        if isJump:
            splitcmd = cmd.split(";")
            acval = valid_comp_patterns.get(splitcmd[0])
            jval = valid_jmp_patterns.get(splitcmd[1], '000')  # Default to '000' if not found
            if acval is None:
                raise KeyError(f"Unrecognized comp pattern: {splitcmd[0]}")
            return "111" + acval + "000" + jval
        else:
            splitcmd = cmd.split("=")
            dval = valid_dest_patterns.get(splitcmd[0], '000')
            acval = valid_comp_patterns.get(splitcmd[1])
            if acval is None:
                raise KeyError(f"Unrecognized comp pattern: {splitcmd[1]}")
            return "111" + acval + dval + "000"

def run_assembler(file_name):
    commandlist = []
    with open(file_name, 'r') as f:
        for command in f:
            if not command.strip().startswith("//") and command.strip():
                commandlist.append(command.split("//")[0].strip())

    for c in commandlist:
        if c.startswith("("):
            label_list[c.strip("() ")] = commandlist.index(c)
            commandlist.remove(c)

    machine_code = [generate_machine_code(c) for c in commandlist]
    return machine_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python assembler.py file-name.asm")
    else:
        file_name = sys.argv[1]
        output_file = os.path.splitext(file_name)[0] + '.hack'
        machine_code = run_assembler(file_name)
        if machine_code:
            print('Machine code was generated successfully');
            print('Writing machine code output to file:', output_file)
            f = open(output_file, 'w')
            for s in machine_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating machine code')