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
	@j
	M=0 // j = 0
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
	@FILL
	D;JGT // if KBD is true goto FILL
	@CLEAR
	D;JEQ // if KBD is false goto CLEAR
	@KBDCHECK
	0;JMP
	
(FILL)
	@i
	D=M
	@256 // screen width
	D=D-A
	@START
	D;JGT
	@addrS
	A=M
	M=-1 // RAM[addrS] = -1
	@i
	M=M+1 // i = i + 1
	@32
	D=A
	@addrS
	M=M+D // addrS = addrS + 32
	@FILL
	0;JMP
	
(CLEAR)
	@j
	D=M
	@256 // screen width
	D=D-A
	@START
	D;JGT
	@addrS
	A=M
	M=0 // RAM[addrS] = 0
	@j
	M=M+1 // j = j + 1
	@32
	D=A
	@addrS
	M=M+D // addrS = addrS + 32 go next row backward
	@CLEAR
	0;JMP