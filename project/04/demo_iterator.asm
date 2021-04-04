//demo iterator

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT //if i > n goto STOP
	
	@sum
	D=M
	@i
	D=D+M
	@sum
	M=D //sum = sum + i
	@i
	M=M+1
	@LOOP
	0;JMP
	
(STOP)
	@sum
	D=M
	@R1
	M=D //RAM[1] = sum
	
(END)
	@END
	0;JMP
	
	