CC=gcc
FLEX=flex
BISON=bison

.PHONY: bplc clean

bplc: bin/bplc

bin/bplc: bin myhead.o syntax.tab.o
	$(CC) -o bin/bplc myhead.o syntax.tab.o -lfl -ly

myhead.o: myhead.cpp
	$(CXX) -c myhead.cpp -o myhead.o

syntax.tab.o: syntax.tab.c
	$(CC) -c syntax.tab.c -o syntax.tab.o

syntax.tab.c: syntax.y lex.yy.c
	$(BISON) -t -d syntax.y

lex.yy.c: lex.l
	$(FLEX) lex.l

bin:
	mkdir bin
	@chmod +x bin/bplc

clean:
	@rm -f lex.yy.c syntax.tab.* ./bin/* *.o

