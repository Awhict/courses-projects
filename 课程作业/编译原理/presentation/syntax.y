%{
#include <stdio.h>
#include <stdlib.h>
#include "lex.yy.c"

int yylex();
void yyerror(char *s);
%}

%union {
    int iVal;
}

%token <iVal> NUMBER
%token IF ELSE QUESTION COLON

%%

expr: expr QUESTION expr COLON expr { 
        if ($1) 
            $$ = $3; 
        else 
            $$ = $5; 
    }
    | NUMBER { $$ = $1; }
    ;

%%
int main() {
    printf("Enter an expression:\n");
    yyparse();
    return 0;
}

void yyerror(char *s) {
    fprintf(stderr, "%s\n", s);
}
