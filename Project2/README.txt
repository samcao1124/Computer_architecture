Name: Sam Cao
Email: jc10253@nyu.edu

I did complete the assignment, and all the test cases passed. I did not use any source from other places. 

I firstly finds out that I need to process the given machine instruction. Then, with using the given function in the starter code, 'load the machine code', I right shifted 13 bits to get the opcode which is the first 3 bits. In the first bunch of instructions, they all started with 000, the way I figure these out is to have if statements for the last four bits. For the other instructions, I did those separately. After finish processing these data, the last step was to print out all the state by using the given function 'Print_state'.

After this step, the 9 cases that are provided by the Autograder are passed.
Considering about the edge cases which are including:
1. Modifying register 0
2. Overflow during calculations
3. When the pc go over 8192

To solve the first case, If the instructions are trying to modify register0, the pc will automatically add 1 and doing nothing.

For second case, I put an add 16bits 1111111111111111 number to control the overflow.

For the last case, I initialize the maximum index to 8191, if the pc go over 8192, it will return to 0.

Overall, I think the code solved all the cases. The weakness of my code is that there probably some repeated lines of code in my program, the strength is that I can talk very specifically to each instructions about their corresponding edge cases.



