



Each folder, sequential and linear, includes:

bmp_steg_tool.c => our code
bmplib.c 		=> open source bmp i/o functions
bmplib.h 		=> open source bmp i/o functions header
example.bmp	=> the original photo
Makefile		=> A makefile that should compile the program on 				starship.
test.txt 		=> The constitution in plaintext for encrypting.

Program Usage

usage: bmp_steg_tool  [-e efile | -d dfile] [-m messageFile] [-o ouput_file]  [image_file]

If the -e "encrypt" flag is on we take the image from efile.
	If no file is specified, take from console. 

If the -d "decrypt" flag is on, we take the image from dfile
	or from the console.

If the -m "messageFile" flag is on and we are encrypting, 
	we read the message to be encrypted from the given file
	else, we prompt the user for a message.

If we are decryptiing and the oflag is provided
	we put the message into the output file

If we are encrypting and the oflag is provided
	we put the picture in the output file



Compiling Instructions:

Sequential version - navigate to the Sequential Folder
			     Type "make" in the command line.
	
encrypting example:

./bmpsteg -e -m test.txt -o output.bmp example.bmp

decrypting example:
	
./bmpsteg -d output.bmp


Parallel Version - navigate to the Sequential Folder
			     Type "make" in the command line.

encrypting example:

mpirun -np 8 bmpsteg -e -m test.txt -o output.bmp example.bmp

decrypting example:
	
mpirun -np 8 bmpsteg -d example.bmp

*** The number after the flag "-np" specifies the number of processors***






