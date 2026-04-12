%{
    #include"lex.yy.c"
    void yyerror(const char* s);
    int result;
%}
%token LP RP LB RB LC RC
%%
String: %empty    { /* 空字符串也是合法的 */ }
      | Group String { /* 递归检查匹配的括号组 */ }
      ;

Group: LP String RP {}
     | LB String RB {}
     | LC String RC {}
     ;
%%

void yyerror(const char* s){
    result = 0;
}

int validParentheses(char *expr){
    result = 1;
    yy_scan_string(expr);
    yyparse();
    return result;
}