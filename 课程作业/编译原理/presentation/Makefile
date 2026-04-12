CC = gcc
CFLAGS = -g
LEX = flex
YACC = bison

TARGET = test

all: $(TARGET)

$(TARGET): lex.yy.c syntax.tab.c
	$(CC) $(CFLAGS) -o $(TARGET) lex.yy.c syntax.tab.c -lfl

lex.yy.c: lex.l
	$(LEX) lex.l

syntax.tab.c: syntax.y
	$(YACC) -d syntax.y

clean:
	rm -f $(TARGET) lex.yy.c syntax.tab.c syntax.tab.h
