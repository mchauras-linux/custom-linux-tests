all: $(basename $(wildcard *.c))

%: %.c
	gcc -o $@ $<

clean:
	rm -rf *.o

.PHONY: all clean

