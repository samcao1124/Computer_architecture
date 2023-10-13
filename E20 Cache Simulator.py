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
Constants = namedtuple("Constants",["NUM_REGS", "MEM_SIZE", "REG_SIZE"])
constants = Constants(NUM_REGS = 8,
                      MEM_SIZE = 2**13,
                      REG_SIZE = 2**16)

def print_cache_config(cache_name, size, assoc, blocksize, num_rows):
    """
    Prints out the correctly-formatted configuration of a cache.

    cache_name -- The name of the cache. "L1" or "L2"

    size -- The total size of the cache, measured in memory cells.
        Excludes metadata

    assoc -- The associativity of the cache. One of [1,2,4,8,16]

    blocksize -- The blocksize of the cache. One of [1,2,4,8,16,32,64])

    num_rows -- The number of rows in the given cache.

    sig: str, int, int, int, int -> NoneType
    """

    summary = "Cache %s has size %s, associativity %s, " \
        "blocksize %s, rows %s" % (cache_name,
        size, assoc, blocksize, num_rows)
    print(summary)
def print_log_entry(cache_name, status, pc, addr, row):
    """
    Prints out a correctly-formatted log entry.

    cache_name -- The name of the cache where the event
        occurred. "L1" or "L2"

    status -- The kind of cache event. "SW", "HIT", or
        "MISS"

    pc -- The program counter of the memory
        access instruction

    addr -- The memory address being accessed.

    row -- The cache row or set number where the data
        is stored.

    sig: str, str, int, int, int -> NoneType
    """
    log_entry = "{event:8s} pc:{pc:5d}\taddr:{addr:5d}\t" \
        "row:{row:4d}".format(row=row, pc=pc, addr=addr,
            event = cache_name + " " + status)
    print(log_entry)
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
        line += format(memory[count], "04x") + " "
        if count % 8 == 7:
            print(line)
            line = ""
    if line != "":
        print(line)

def cache_simulate(pc, lw, addr, L1, L1blocksize, L2, L2blocksize):
    L1_blockid = addr // L1blocksize
    L1_number_row = len(L1)
    L1_row = L1_blockid % L1_number_row
    L1_tag = L1_blockid // L1_number_row
    if L2blocksize != 0:
        L2_blockid = addr // L2blocksize
        L2_number_row = len(L2)
        L2_row = L2_blockid % L2_number_row
        L2_tag = L2_blockid // L2_number_row
    if L2blocksize == 0:
        Hit = False
        for L1_index in range(len(L1[L1_row])):  # l2 not in use and l1 hit
            if L1[L1_row][L1_index] == L1_tag:
                L1[L1_row].pop(L1_index)
                L1[L1_row].append(L1_tag)
                if lw:
                    status = "HIT"
                else:
                    status = "SW"
                print_log_entry("L1", status, pc, addr, L1_row)
                Hit = True
                break
        if not Hit:
            L1[L1_row].pop(0)
            L1[L1_row].append(L1_tag)  # l1 not hit
            if lw:
                status = "MISS"
            else:
                status = "SW"
            print_log_entry("L1", status, pc, addr, L1_row)
    else:
        Hit = False
        for L1_index in range(len(L1[L1_row])):
            if L1[L1_row][L1_index] == L1_tag:
                L1[L1_row].pop(L1_index)
                L1[L1_row].append(L1_tag)
                Hit = True
                if lw:
                    print_log_entry("L1", "HIT", pc, addr, L1_row)
                else:
                    print_log_entry("L1", "SW", pc, addr, L1_row)
                    print_log_entry("L2", "SW", pc, addr, L2_row)
        if not Hit:  # l2 in use and l1 not hit
            l2_hit = False
            L1[L1_row].pop(0)
            L1[L1_row].append(L1_tag)
            for L2_index in range(len(L2[L2_row])):  # process l2
                if L2[L2_row][L2_index] == L2_tag:
                    L2[L2_row].pop(L2_index)
                    L2[L2_row].append(L2_tag)
                    l2_hit = True
            if l2_hit:
                if lw:
                    print_log_entry("L1", 'MISS', pc, addr, L1_row)
                    print_log_entry("L2", 'HIT', pc, addr, L2_row)
                else:
                    print_log_entry("L1", 'SW', pc, addr, L1_row)
                    print_log_entry("L2", 'SW', pc, addr, L2_row)
            if not l2_hit:  # l2 not hit
                L2[L2_row].pop(0)
                L2[L2_row].append(L2_tag)
                L1[L1_row].pop(0)
                L1[L1_row].append(L1_tag)
                if lw:
                    print_log_entry("L1", 'MISS', pc, addr, L1_row)
                    print_log_entry("L2", 'MISS', pc, addr, L2_row)
                else:
                    print_log_entry("L1", 'SW', pc, addr, L1_row)
                    print_log_entry("L2", 'SW', pc, addr, L2_row)

def main():
    parser = argparse.ArgumentParser(description='Simulate E20 cache')
    parser.add_argument('filename', help=
        'The file containing machine code, typically with .bin suffix')
    parser.add_argument('--cache', help=
        'Cache configuration: size,associativity,blocksize (for one cache) '
        'or size,associativity,blocksize,size,associativity,blocksize (for two caches)')
    cmdline = parser.parse_args()
    pc = 0
    memory = [0] * 8192
    reg_val = [0] * 8
    overflow_controller = 0b1111111111111111
    L1 = []
    L2 = []
    L1blocksize = 0
    L2blocksize = 0
    if cmdline.cache is not None:
        parts = cmdline.cache.split(",")
        if len(parts) == 3:  #initialization
            [L1size, L1assoc, L1blocksize] = [int(x) for x in parts]
            L1rows = L1size // (L1assoc * L1blocksize)
            for index1 in range(L1rows):
                L1_curr_row = []
                for block in range(L1assoc):
                    L1_curr_row.append(None)
                L1.append(L1_curr_row)
            print_cache_config('L1',L1size,L1assoc,L1blocksize,L1rows)
            # TODO: execute E20 program and simulate one cache here
        elif len(parts) == 6:
            [L1size, L1assoc, L1blocksize, L2size, L2assoc, L2blocksize] = \
                [int(x) for x in parts]
            L2rows = L2size // (L2assoc * L2blocksize)
            L1rows = L1size // (L1assoc * L1blocksize)
            for index1 in range(L1rows):
                L1_curr_row = []
                for block in range(L1assoc):
                    L1_curr_row.append(None)
                L1.append(L1_curr_row)
            for index2 in range(L2rows):
                L2_curr_row = []
                L2.append(L2_curr_row)
                for block2 in range(L2assoc):
                    L2_curr_row.append(None)
            print_cache_config("L1", L1size, L1assoc, L1blocksize, L1rows)
            print_cache_config("L2", L2size, L2assoc, L2blocksize, L2rows)

            # TODO: execute E20 program and simulate two caches here
        else:
            raise Exception("Invalid cache config")

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

            cache_simulate(pc, 1,((reg_val[rg_addr] + imm_value) & 0b1111111111111) , L1, L1blocksize, L2, L2blocksize )
            pc = (pc + 1) & 0b1111111111111111  # changed

        if opcode == 0b101: #sw signed
            imm_value = instruction & 0b0000000001111111
            if (imm_value >> 6) != 1:
                imm_value = instruction & 0b0000000001111111
            else:
                imm_value = (instruction & 0b0000000001111111) | 0b1111111110000000
            rg_addr = (instruction & 0b0001110000000000) >> 10
            rg_src = (instruction & 0b0000001110000000) >> 7
            (memory[(reg_val[rg_addr] + imm_value) & 0b1111111111111]) = reg_val[rg_src]
            cache_simulate(pc, 0,((reg_val[rg_addr] + imm_value) & 0b1111111111111), L1, L1blocksize, L2,L2blocksize)
            pc = (pc + 1) & 0b1111111111111111  # changed
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
    #print_state(pc,reg_val,memory,128)

if __name__ == "__main__":
    main()
#ra0Eequ6ucie6Jei0koh6phishohm9
