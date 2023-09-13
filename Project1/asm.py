#!/usr/bin/python3
"""
CS-UY 2214
Sam Cao
Starter code for E20 assembler
asm.py
"""
import argparse
def print_machine_code(address, num):
    """
    print_line(address, num)
    Print a line of machine code in the required format.
    Parameters:
        address: int = RAM address of the instructions
        num: int = numeric value of machine instruction
    For example:
        >>> print_machine_code(3, 42)
        ram[3] = 16'b0000000000101010;
    """
    instruction_in_binary = format(num, '016b')
    print("ram[%s] = 16'b%s;" % (address, instruction_in_binary))
def main():
    parser = argparse.ArgumentParser(description='Assemble E20 files into machine code')
    parser.add_argument('filename', help='The file containing assembly language, typically with .s suffix')
    cmdline = parser.parse_args()
    # our final output is a list of ints values representing
    # machine code instructions
    instructions = []
    label_dict = {}
    pc = 0
    m_code = 0
    three_register_list = ["add","sub","or","and","slt","jr","nop"] #TODO: movi;unsigned
    two_register_list = ["slti","lw","sw","jeq","addi"]
    zero_register_list = ["j","jal","halt"]

    # iterate through the line in the file, construct a list
    # of numeric values representing machine code
    with open(cmdline.filename) as f:
        pc = 0
        lines = []
        for line in f: #first loop find labels
            opcode = ""
            line = line.split("#", 1)[0].strip()  # remove comments
            if line != "":
                if is_label(line): # 有label，push进dict，drop掉
                    label = line.split(":")[0]
                    label_dict[label.lower()] = pc
                    line = line.split(":")[-1].strip()
                if line != "":
                    lines.append(line)
                    opcode = line.split(" ")[0].lower()
            if opcode != "":
                pc += 1
        pc = 0
        for line in lines:
            opcode = ""
            opcode = line.split(" ")[0].lower()
            # 没有label，starts with opcode no space in front
            if opcode in three_register_list:
                m_code = opcode_change_three_reg(line,pc)
                instructions.append(m_code)
            elif opcode in two_register_list:
                m_code = opcode_change_two_reg(line, label_dict, pc, opcode)
                instructions.append(m_code)
            #TODO movi
            elif opcode == "movi":
                line = line.split(",")
                reg = find_dig(line[0])
                if line[1].strip().lower() in label_dict:
                    imm_value = label_dict[line[1].strip()]
                else:
                    imm_value = int(line[1])
                m_code = (1<<13) | (reg<<7) | imm_value
                print_value_in_machin_code(m_code,pc)
                instructions.append(m_code)
            elif opcode in zero_register_list:
                m_code = opcode_change_zero_reg(line, label_dict, pc,opcode)
                instructions.append(m_code)
            elif opcode == '.fill':
                dot_fill(line,pc)
            if opcode != "":
                pc += 1

    # print out each instruction in the required format
    # for address, instruction in enumerate(instructions):
    #     print_machine_code(address, instruction)

def is_label(line): # TODO mutilple label
    if ':' not in line:
        return False
    return True

def string_to_binary(string):
    return int(bin(int(string)), 2)

# done
def opcode_change_three_reg(line,pc):  # for instructions which is 000 and three registers
    value = 0# to return
    op_elem = line.split("$")
    op_elem[0] = op_elem[0].strip()
    if op_elem[0] == "jr":
        regSrcA = int(op_elem[1])
        regSrcB = 0
        regDst = 0
    else:
        regSrcA = find_dig(op_elem[2])
        regSrcB = find_dig(op_elem[3])
        regDst = find_dig(op_elem[1])
    value |= (regDst << 4)
    value |= (regSrcA << 10)
    value |= (regSrcB << 7)
    if op_elem[0] == "add" or op_elem[0] == "nop":
        value |= 0
    if op_elem[0] == "sub":
        value |= 1
    if op_elem[0] == "or":
        value |= 2
    if op_elem[0] == "and":
        value |= 3
    if op_elem[0] == "slt":
        value |= 4
    if op_elem[0] == "jr":
        value |= 8
    print_value_in_machin_code(value,pc)
    return value

def opcode_change_two_reg(line,label_dict,pc,opcode):  # two register
    value = 0  # to return
    if opcode == "slti":
        op_elem = line.split(",")
        regSrc = find_dig(op_elem[1])
        regDst = find_dig(op_elem[0])
        op_elem[2] = op_elem[2].strip()
        if op_elem[2].lower() in label_dict:
            imm = label_dict[op_elem[2]]
        else:
            imm = int(op_elem[2])
        value |= (regSrc << 10)
        value |= (regDst << 7)
        value |= (7 << 13)
        value |= negative_to_2complement(imm)
        print_value_in_machin_code(value, pc)
    if opcode == "lw":
        op_elem = line.split(",")
        regDst = find_dig(op_elem[0])
        imm = op_elem[1].split("(")[0]
        reg_addr = find_dig(op_elem[1].split("(")[1])
        if imm.strip().lower() in label_dict:
            imm_val = label_dict[imm.strip()]
        else:
            imm_val = int(imm)
        value |= (reg_addr << 10)
        value |= (regDst << 7)
        value |= negative_to_2complement(imm_val)
        value |= (4 << 13)
        print_value_in_machin_code(value, pc)
    if opcode == "sw":
        op_elem = line.split(",")
        regSrc = find_dig(op_elem[0])
        imm = op_elem[1].split("(")[0]
        reg_addr = find_dig(op_elem[1].split("(")[1])
        if imm.lower() in label_dict:
            imm_val = label_dict[imm]
        else:
            imm_val = int(imm)

        value |= (reg_addr << 10)
        value |= (regSrc << 7)
        value |= negative_to_2complement(imm_val)
        value |= (5 << 13)
        print_value_in_machin_code(value,pc)

    if opcode == "jeq":  # label
        op_elem = line.split(",")
        regA = find_dig(op_elem[0])
        regB = find_dig(op_elem[1])
        op_elem[2] = op_elem[2].strip()
        if op_elem[2].lower() in label_dict:
            imm = label_dict[op_elem[2]] - pc - 1
        else:
            imm = int(op_elem[2]) - pc - 1
        #TODO:在这儿把 可能是负的的imm value换成unsigned 7bit
        value |= (regA << 10)
        value |= (regB << 7)
        value |= (6 << 13)
        value |= negative_to_2complement(imm)
        print_value_in_machin_code(value, pc)

    if opcode == "addi":  # label
        op_elem = line.split(",")
        regSrc = find_dig(op_elem[1])
        regDst = find_dig(op_elem[0])
        op_elem[2] = op_elem[2].strip()
        if op_elem[2].lower() in label_dict:
            imm = label_dict[op_elem[2]]
        else:
            imm = int(op_elem[2])
        value |= (regSrc << 10)
        value |= (regDst << 7)
        value |= (1 << 13)
        value |= negative_to_2complement(imm)
        print_value_in_machin_code(value, pc)
    return value

def opcode_change_zero_reg(line,label_dict,pc,opcode):  # 0 registers
    value = 0  # to return
    op_elem = line.split(" ")
    if opcode == "j":
        value |= (2 << 13)
        imm_value = op_elem[1].strip()#it's a string right now
        if imm_value.lower() in label_dict:
            value |= label_dict[op_elem[1]]
        else:
            value |= negative_to_2complement_13_bit(int(imm_value))
        print_value_in_machin_code(value,pc)
    elif opcode == "jal":
        value |= (3 << 13)
        imm_value = op_elem[1]
        if imm_value.lower() in label_dict:
            value |= label_dict[op_elem[1]]
        else:
            value |= negative_to_2complement_13_bit(int(imm_value))
        print_value_in_machin_code(value,pc)
    elif op_elem[0] == "halt":
        value |= 2 << 13
        value |= pc
        print_value_in_machin_code(value,pc)
    return value

def dot_fill(line,pc):
    value = 0
    value = int(line.split(" ")[1])
    print_value_in_machin_code(value,pc)
    return value

def find_dig(str):
    for digits in str:
        if digits.isdigit():
            return int(digits)

def int_in_binary_as_string(my_int):
    int_in_binary = format(my_int, '016b')
    return int_in_binary

def negative_to_2complement(input_int):
    if input_int >= 0:
        return input_int
    else:
        return input_int + 0b1111111 + 1

def negative_to_2complement_13_bit(input_int):
    if input_int >= 0:
        return input_int
    else:
        return input_int + 0b1111111111111 + 1

def print_value_in_machin_code(value,pc):
    print("ram[%s] = 16'b%s;"%(pc,int_in_binary_as_string(value)))

if __name__ == "__main__":
    main()

# ra0Eequ6ucie6Jei0koh6phishohm9
