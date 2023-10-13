# Computer_architecture
## Machine Instruction Processor

### Introduction
This repository contains a machine instruction processor that processes and executes machine instructions. 
The processor is designed to handle a set of instructions with specific edge cases and ensure the correct execution of these instructions. 
The primary goal is to fulfill all the functionality of the E20 instructions while addressing potential issues like modifying register 0, overflow during calculations, and dealing with program counter (PC) values that exceed 8192.

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
While there may be some repeated lines of code, the ability to address each instruction's edge cases specifically is a strength of this implementation.


## E20 Cache Simulator

### Introduction
This repository contains a Python-based E20 cache simulator named E20 Cache Simulator.py. 
This simulator is designed to execute and analyze machine code programs, taking into account cache configurations, memory access, and various instructions.
The goal of this simulator is to facilitate cache-related experiments and provide insights into program execution behavior.

### Key Features
1. Cache Configuration
The simulator can be configured with cache settings, including:

   Cache size
   Associativity
   Block size
   
Two cache levels (L1 and L2) can be specified, each with its configuration parameters. The provided cache configuration is crucial for understanding cache behavior and its impact on program execution.

3. Machine Code Execution
The simulator loads a machine code file, processes the instructions, and simulates the execution of the program. It keeps track of the program counter, register values, and memory access.

4. Cache Simulation
The simulator supports cache simulation for both L1 and L2 caches. It records cache events, such as cache hits and misses, and maintains cache state. This feature allows users to evaluate the effectiveness of different cache configurations in improving program performance.

5. Edge Case Handling
The code accounts for various edge cases, including instruction execution, overflow control, and program counter boundaries. These considerations ensure the accurate and reliable execution of machine code programs.

### Output
The simulator provides detailed information about cache configuration, program execution, and cache events. 
Users can analyze this information to gain insights into the program's behavior and cache performance.

### Conclusion
The E20 Cache Simulator is a valuable tool for understanding the behavior of machine code programs in the context of different cache configurations. 
By providing cache simulation capabilities and handling edge cases, this code helps students and researchers explore the impact of caches on program performance and behavior.


