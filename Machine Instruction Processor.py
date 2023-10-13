#!/usr/bin/python3
"""
CS-UY 2214
Sam Cao
Starter code for E20 simulator
sim.py
"""
from collections import namedtuple
import re
import argparse
# overfolow in pc
# slti
# Some helpful constant values that we'll be using.
Constants = namedtuple("Constants",["NUM_REGS", "MEM_SIZE", "REG_SIZE"])
constants = Constants(NUM_REGS = 8,
                      MEM_SIZE = 2**13,
                      REG_SIZE = 2**16)

def load_machine_code(machine_code, mem):
    """
    Loads an E20 machine code file into the list
    provided by mem. We assume that mem is
    large enough to hold the values in the machine
    code file.
    sig: list(str) -> list(int) -> NoneType
    """
    machine_code_re = re.compile("^ram\[(\d+)\] = 16'b(\d+);.*$")
    expectedaddr = 0
    for line in machine_code:
        match = machine_code_re.match(line)
        if not match:
            raise ValueError("Can't parse line: %s" % line)
        addr, instr = match.groups()
        addr = int(addr,10)
        instr = int(instr,2)
        if addr != expectedaddr:
            raise ValueError("Memory addresses encountered out of sequence: %s" % addr)
        if addr >= len(mem):
            raise ValueError("Program too big for memory")
        expectedaddr += 1
        mem[addr] = instr

def print_state(pc, regs, memory, memquantity):
    """
    Prints the current state of the simulator, including
    the current program counter, the current register values,
    and the first memquantity elements of memory.
    sig: int -> list(int) -> list(int) - int -> NoneType
    """
    print("Final state:")
    print("\tpc="+format(pc,"5d"))
    for reg, regval in enumerate(regs):
        print(("\t$%s=" % reg)+format(regval,"5d"))
    line = ""
    for count in range(memquantity):
        line += format(memory[count], "04x")+ " "
        if count % 8 == 7:
            print(line)
            line = ""
    if line != "":
        print(line)

def main():
    parser = argparse.ArgumentParser(description='Simulate E20 machine')
    parser.add_argument('filename', help='The file containing machine code, typically with .bin suffix')
    cmdline = parser.parse_args()
    pc = 0
    memory = [0] * 8192
    reg_val = [0] * 8
    overflow_controller = 0b1111111111111111

    with open(cmdline.filename) as file:
    # TODO: your code here. Load file and parse using load_machine_code
        load_machine_code(file,memory)
    # TODO: your code here. Do simulation.
    while True:
        instruction = memory[pc & 8191]
        opcode = instruction >> 13
        if opcode == 0b000:
            last_four_bits = instruction & 0b1111
            rg_A = (instruction & 0b0001110000000000) >> 10
            rg_B = (instruction & 0b0000001110000000) >> 7
            rg_dst = (instruction & 0b0000000001110000) >> 4
            if last_four_bits == 0b0000: #add
                if rg_dst == 0b000:
                    pc = (pc + 1) & 0b1111111111111111

                elif rg_dst == 0b000 and rg_A == 0b000 and rg_B == 0b000: #nop
                    pc = (pc + 1) & 0b1111111111111111
                else:
                    reg_val[rg_dst] = ((reg_val[rg_A] +reg_val[rg_B]) & overflow_controller)
                    pc = (pc + 1) & 0b1111111111111111
            elif last_four_bits == 0b0001:# sub
                if rg_dst == 0b000:
                    pc = (pc + 1) & 0b1111111111111111
                else:
                    reg_val[rg_dst] = (reg_val[rg_A] - reg_val[rg_B]) & overflow_controller
                    pc = (pc + 1) & 0b1111111111111111
            elif last_four_bits == 0b0010:#or
                if rg_dst == 0b000:
                    pc = (pc + 1) & 0b1111111111111111
                else:
                    reg_val[rg_dst] = reg_val[rg_A] | reg_val[rg_B]
                    pc = (pc + 1) & 0b1111111111111111
            elif last_four_bits == 0b0011 :#and
                if rg_dst == 0b000:
                    pc = (pc + 1) & 0b1111111111111111
                else:
                    reg_val[rg_dst] = reg_val[rg_A] & reg_val[rg_B]
                    pc = (pc + 1) & 0b1111111111111111
            elif last_four_bits == 0b0100 :#slt # TODO rg0
                if rg_dst == 0b000:
                    pc = (pc + 1) & 0b1111111111111111
                elif reg_val[rg_A] < reg_val[rg_B]:
                    reg_val[rg_dst] = 0b001
                    pc = (pc + 1) & 0b1111111111111111
                else:
                    reg_val[rg_dst] = 0b000
                    pc = (pc + 1) & 0b1111111111111111
            elif last_four_bits == 0b1000 :#jr # TODO is this halt?
                if reg_val[rg_A] != pc:
                    pc = reg_val[rg_A]
                else:
                    break

        if opcode == 0b111: #slti
            imm_value = instruction & 0b0000000001111111
            if (imm_value >> 6) != 1:
                imm_value = instruction & 0b0000000001111111
            else:
                imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_src = (instruction & 0b0001110000000000) >> 10
            rg_dst = (instruction & 0b0000001110000000) >> 7
            if rg_dst == 0b000:
                pc = (pc + 1) & 0b1111111111111111
            elif (reg_val[rg_src] & 0b1111111111111111) < (imm_value):
                reg_val[rg_dst] = 0b001
                pc = (pc + 1) & 0b1111111111111111
            else:
                reg_val[rg_dst] = 0b000
                pc = (pc + 1) & 0b1111111111111111
        if opcode == 0b100: #lw signed
            pc = (pc + 1) & 0b1111111111111111 #changed
            imm_value = instruction & 0b0000000001111111
            if (imm_value >> 6) != 1:
                imm_value = instruction & 0b0000000001111111
            else:
                imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_addr = (instruction & 0b0001110000000000) >> 10
            rg_dst = (instruction & 0b0000001110000000) >> 7
            if rg_dst != 0b000:
                reg_val[rg_dst] = memory[(reg_val[rg_addr] + imm_value) & 0b1111111111111]
            else:
                pc = (pc + 1) & 0b1111111111111111 #changed
        if opcode == 0b101: #sw signed
            pc = (pc + 1) & 0b1111111111111111 #changed
            imm_value = instruction & 0b0000000001111111
            if (imm_value >> 6) != 1:
                imm_value = instruction & 0b0000000001111111
            else:
                imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_addr = (instruction & 0b0001110000000000) >> 10
            rg_src = (instruction & 0b0000001110000000) >> 7
            (memory[(reg_val[rg_addr] + imm_value) & 0b1111111111111]) = reg_val[rg_src]
        if opcode == 0b110: #jeq signed
            rel_imm_value = instruction & 0b0000000001111111
            if (rel_imm_value >> 6) != 1:
                rel_imm_value = instruction & 0b0000000001111111
            else:
                rel_imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_A = (instruction & 0b0001110000000000) >> 10
            rg_B = (instruction & 0b0000001110000000) >> 7
            if reg_val[rg_A] == reg_val[rg_B]:
                pc = (pc + 1 + rel_imm_value) & 0b1111111111111111
            else:
                pc = (pc + 1) & 0b1111111111111111
        if opcode == 0b001: #addi
            pc = (pc + 1) & 0b1111111111111111
            imm_value = instruction & 0b0000000001111111
            if (imm_value >> 6) != 1:
                imm_value = instruction & 0b0000000001111111
            else:
                imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_src = (instruction & 0b0001110000000000) >> 10
            rg_dst = (instruction & 0b0000001110000000) >> 7
            if rg_dst != 0b000:
                if rg_src != 0b000:
                    reg_val[rg_dst] = (reg_val[rg_src] + imm_value) & overflow_controller
                else:  # movi
                    reg_val[rg_dst] = imm_value
            else:
                pc = (pc + 1) & 0b1111111111111111
        if opcode == 0b010: #jump
            imm_value = instruction & 0b0001111111111111
            if pc == imm_value: #halt
                break
            else:
                pc = imm_value
        if opcode == 0b011: #jal
            imm_value = instruction & 0b0001111111111111
            reg_val[7] = pc+1
            if imm_value != pc :
                pc = imm_value & 0b1111111111111111
            else:
                break

# TODO: your code here. print the final state of the simulator before ending, using print_state
    print_state(pc,reg_val,memory,128)

if __name__ == "__main__":
    main()
#ra0Eequ6ucie6Jei0koh6phishohm9