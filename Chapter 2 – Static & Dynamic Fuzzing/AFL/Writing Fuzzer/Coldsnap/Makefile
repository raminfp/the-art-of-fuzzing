CC = gcc
CFLAGS = -g

default: run

compile:
	@$(CC) $(CFLAGS) target.c -o target

run: compile
	@chmod +x coldsnap.py
	@./coldsnap.py
	
clean:
	rm -f target
