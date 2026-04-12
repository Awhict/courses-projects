CC=gcc
FLEX=flex
BISON=bison


.lex: lex.l
	$(FLEX) lex.l
.syntax: syntax.y
	$(BISON) -t -d syntax.y
bplc: .lex .syntax
	@mkdir bin
	$(CC) syntax.tab.c -lfl -ly -o bin/bplc.out
	@chmod +x bin/bplc.out
clean:
	@rm -f lex.yy.c syntax.tab.*
.PHONY: bplc
