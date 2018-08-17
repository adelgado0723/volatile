C = gcc
HDRS = bmplib.h
OBJS = bstsort.o bmp_steg_tool.o

bmpsteg : bmplib.o bmp_steg_tool.o
	$(C) -o bmpsteg bmplib.c bmp_steg_tool.c

bmplib.o : bmplib.c
	$(C) -c -g bmplib.c

bmp_steg_tool.o : bmp_steg_tool.c 
	$(C) -c -g bmp_steg_tool.c
clean:
	rm -f bmptool *.o core *~
$(OBJS) : $(HDRS)
