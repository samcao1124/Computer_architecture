# Computer_architecture
## Machine Instruction Processor

### Introduction
This repository contains a machine instruction processor that processes and executes machine instructions. 
The processor is designed to handle a set of instructions with specific edge cases and ensure the correct execution of these instructions. 
The primary goal is to pass a set of 9 test cases provided by the Autograder while addressing potential issues like modifying register 0, overflow during calculations, and dealing with program counter (PC) values that exceed 8192.

### Instructions Processing
The processing of machine instructions follows these steps:
1. Instruction Parsing: The processor begins by parsing the given machine instruction to understand its structure.
2. Opcode Extraction: The processor uses a function from the starter code to load the machine code. It then right-shifts 13 bits to extract the opcode, which is the first 3 bits of the instruction.
3. Opcode Differentiation: For instructions with opcodes starting with '000,' the processor uses a series of conditional statements to distinguish between different instructions based on the last four bits.
   Other instructions are processed separately.
4. State Printing: After processing the instructions, the processor prints out the state using the provided 'Print_state' function.

### Handling Edge Cases
The processor is equipped to handle the following edge cases:
1. Modifying Register 0: If an instruction attempts to modify register 0, the program counter (PC) will automatically increment by 1, ensuring no actual modification takes place.
2. Overflow During Calculations: To control overflow during calculations, the processor adds a 16-bit binary number '1111111111111111' to the results of arithmetic operations.
3. PC Exceeding 8192: The processor accounts for the program counter exceeding the maximum value of 8192. In such cases, the PC is reset to 0.

### Conclusion
The code in this repository has been designed to handle various machine instructions while addressing specific edge cases to ensure correct execution. 
The code is well-structured and passes all 9 test cases provided by the Autograder. 
While there may be some repeated lines of code, the ability to address each instruction's edge cases specifically is a strength of this implementation.
