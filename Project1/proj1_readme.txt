Sam Cao
Jc10253@nyu.edu


I completed the assignment.

I did search some python function on google, and the test cases all passed without any bugs. 

The way that i design my code is to divide these instructions into three groups according to the manual, except for some special cases, such as movi.


These three groups are : using three registers, two registers,and the instructions without using any registers. Moreover, I also considered about the labels. The way I deal with labels is to create a dictionary to store the pc and the label. The name of the label will be unique which means I make the name be the key. Before that, I designed a function to determine if the input is Label. 


When I read the file, I will go through the lines firsts, and then I will find all the labels incase for the situation where the later label will appear early in the code. Which the label will not recognize the code.
If input is label, it will be sharing the Same address with the instruction after it. In the Main function, I put assemble lists which divided according to the number of registers.

In order to pass some edge cases, I make sure all the opcodes and the labels are all lowercase. Moreover, in some cases, the immediate values are negative, which means I also need to convert those negative integers into 2s complement in binary. 

Overall, the code passes all the test code provided