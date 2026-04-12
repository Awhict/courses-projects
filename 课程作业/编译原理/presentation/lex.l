%{
#include "syntax.tab.h"
%}

%%
"if"               { return IF; }
"else"           { return ELSE; }
"?"               { return QUESTION; }
":"                { return COLON; }
[0-9]+          { yylval.iVal = atoi(yytext); return NUMBER; }
[ \t\n]+        { /* ignore whitespace */ }
.                   { return yytext[0]; }
%%

