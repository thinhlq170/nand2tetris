// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
	@i
	M=0 // i = 0
	@SCREEN
	D=A
	@addrS
	M=D // addrS = SCREEN
	@KBD
	D=A
	@addrK
	M=D // addrK = KBD
	
(KBDCHECK)
	@KBD
	D=M
	@BLACK
	D;JGT // if KBD is true goto FILL
	@WHITE
	D;JEQ // if KBD is false goto CLEAR
	@KBDCHECK
	0;JMP
	
(BLACK)
	@R0
	M=-1
	@FILL
	0;JMP
	
(WHITE)
	@R0
	M=0
	@FILL
	0;JMP
	
(FILL)
	@i
	D=M
	@8192 // full screen
	D=D-A
	@START
	D;JEQ
	@R0
	D=M
	@addrS
	A=M
	M=D // fill
	@i
	M=M+1 // i = i + 1
	@addrS
	M=M+1 // addrS = addrS + 1
	@CLEAR
	0;JMP