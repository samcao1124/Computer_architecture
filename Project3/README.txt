Name: Sam Cao
Email: jc10253@nyu.edu


I did complete the assignment, and all the test cases passed. I did not use any source from other places. 

In the given starter code, I initialize the rows for l1 and l2 according to the length of the parts is 3 or 6. Parameters are size, associitity,and block size for both l1 and l2. 
The way I build up the cache simulator is to build another function called cache simulate. This function accept parameters including:

Pc: the program counter;
Lw: a boolean to see if the current instruction is lw or sw; lw = 1 when the current instruction is lw. Lw = 0 when it is sw
Addr: the instruction’s address
L1: a list for cache L1
L2: a list for cache L2
L1blocksize: the blocksize of L1
L2blocksize: the blocksize of L2

There are conditions listed below:
1. only L1:
When L2 block size = 0, which means L2 is not involved. 
	a. When there is a hit in L1, I will pop out the value on the specific index, and append the tag into the row. 
	b. If there is a miss, I pop out the first element in the row and append the element to the row according to the LRU. It’s because the element in the front is the least used ones.

2. Both L1 AND L2 operating:
	a. If the value in the L1 in the specific index matches the value of the tag, there will be a hit.I will pop out the value on the specific index, and append the tag into the row. Then, we have to discuss the situations for L2:
		— when L2 hit:
		if the value matches the L2_tag, I pop out the value on the specific index, then append this element to the row.
		— when L2 miss:
		is there is a miss in L2, I will pop out the first value in both L1 AND L2, then append the tag in L1 and L2 accordingly. 

After dealing with the following situations, there is a print_log_entry function called to print out all the information that needed. For lw instruction, it will print out the according cache Status like “MISS” or “HIT”. For SW, the status will always be “SW”. 


Overall, I think the code solved all the cases. The weakness of my code is that there probably some repeated lines of code in my program, the strength is that the situations of the caches are considered. 


