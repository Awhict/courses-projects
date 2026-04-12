%{
#include"syntax.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

typedef struct Head
{
    int is_end;
    char type[100];
    char id[100];
    int line;
    struct Head *child;
    struct Head *brother;
} Node;
struct Head *new_Node(int is_end, char *type, char *id,int line, Node *child, Node *brother);

Node* new_Node(int is_end,char* type, char* id, int line, Node* child,Node* brother)
{
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) 
    {
        perror("Memory allocation error");
        exit(EXIT_FAILURE);
    }
    newNode->is_end = is_end;
    if(line==0)
    {
        newNode->line=child->line;
    }
    else
    {
        newNode->line=line;
    }
    strcpy(newNode->type,type);
    if (id)
    {
        strcpy(newNode->id,id);
    }
    else
    {
        newNode->id[0]='\0';
    }
    newNode->child = child;
    newNode->brother = brother;
    return newNode;
}

void print_tree(Node* result,int line)
{
    if(result==NULL)
    {
        return;
    }
    if(strcmp(result->type,"empty")!=0)
    {
        for(int i=0;i<line;i++)
        {
            printf("  ");
        }
    }
    
    if(result->is_end==1)
    {
        printf("%s",result->type);
        if(strcmp(result->type,"ID")==0||strcmp(result->type,"TYPE")==0||strcmp(result->type,"INT")==0||
        strcmp(result->type,"FLOAT")==0||strcmp(result->type,"CHAR")==0)
        {
            printf(": %s",result->id);
        }
        printf("\n");
    }
    else if(strcmp(result->type,"empty")!=0)
    {
        printf("%s (%d)\n",result->type,result->line);
    }
    print_tree(result->child,line+1);
    print_tree(result->brother,line);
}
int line = 1;
%}
%option noyywrap

word_int        [0-9]+|0x[0-9a-fA-F]+
word_float      [0-9]+"."[0-9]+
word_id         [a-zA-Z_][a-zA-Z0-9_]*
word_char       \'.\'|\'\\x[0-9a-fA-F]{2}\'

%%
"int"                   { yylval.node=new_Node(1,"TYPE",yytext,line,NULL,NULL);return TYPE; }
"float"                 { yylval.node=new_Node(1,"TYPE",yytext,line,NULL,NULL);return TYPE; }
"char"                  { yylval.node=new_Node(1,"TYPE",yytext,line,NULL,NULL);return TYPE; }
"struct"                { yylval.node=new_Node(1,"STRUCT",yytext,line,NULL,NULL);return STRUCT; }
"if"                    { yylval.node=new_Node(1,"IF",yytext,line,NULL,NULL);return IF; }
"else"                  { yylval.node=new_Node(1,"ELSE",yytext,line,NULL,NULL);return ELSE; }
"while"                 { yylval.node=new_Node(1,"WHILE",yytext,line,NULL,NULL);return WHILE; }
"return"                { yylval.node=new_Node(1,"RETURN",yytext,line,NULL,NULL);return RETURN; }
{word_int}              {yylval.node=new_Node(1,"INT",yytext,line,NULL,NULL);return INT;}
{word_id}               { yylval.node=new_Node(1,"ID",yytext,line,NULL,NULL);return ID; }
{word_char}             { yylval.node=new_Node(1,"CHAR",yytext,line,NULL,NULL);return CHAR; }
{word_float}            { yylval.node=new_Node(1,"FLOAT",yytext,line,NULL,NULL);return FLOAT; }

"."                     { yylval.node=new_Node(1,"DOT",yytext,line,NULL,NULL);return DOT; }
";"                     { yylval.node=new_Node(1,"SEMI",yytext,line,NULL,NULL);return SEMI; }
","                     { yylval.node=new_Node(1,"COMMA",yytext,line,NULL,NULL);return COMMA; }
"="                     { yylval.node=new_Node(1,"ASSIGN",yytext,line,NULL,NULL);return ASSIGN; }
"<"                     { yylval.node=new_Node(1,"LT",yytext,line,NULL,NULL);return LT; }
">"                     { yylval.node=new_Node(1,"GT",yytext,line,NULL,NULL);return GT; }
"<="                    { yylval.node=new_Node(1,"LE",yytext,line,NULL,NULL);return LE; }
">="                    { yylval.node=new_Node(1,"GE",yytext,line,NULL,NULL);return GE; }
"!="                    { yylval.node=new_Node(1,"NE",yytext,line,NULL,NULL);return NE; }
"=="                    { yylval.node=new_Node(1,"EQ",yytext,line,NULL,NULL);return EQ; }
"+"                     { yylval.node=new_Node(1,"PLUS",yytext,line,NULL,NULL);return PLUS; }
"-"                     { yylval.node=new_Node(1,"MINUS",yytext,line,NULL,NULL);return MINUS; }
"*"                     { yylval.node=new_Node(1,"MUL",yytext,line,NULL,NULL);return MUL; }
"/"                     { yylval.node=new_Node(1,"DIV",yytext,line,NULL,NULL);return DIV; }
"&&"                    { yylval.node=new_Node(1,"AND",yytext,line,NULL,NULL);return AND; }
"||"                    { yylval.node=new_Node(1,"OR",yytext,line,NULL,NULL);return OR; }
"!"                     { yylval.node=new_Node(1,"NOT",yytext,line,NULL,NULL);return NOT; }
"("                     { yylval.node=new_Node(1,"LP",yytext,line,NULL,NULL);return LP; }
")"                     { yylval.node=new_Node(1,"RP",yytext,line,NULL,NULL);return RP; }
"["                     { yylval.node=new_Node(1,"LB",yytext,line,NULL,NULL);return LB; }
"]"                     { yylval.node=new_Node(1,"RB",yytext,line,NULL,NULL);return RB; }
"{"                     { yylval.node=new_Node(1,"LC",yytext,line,NULL,NULL);return LC; }
"}"                     { yylval.node=new_Node(1,"RC",yytext,line,NULL,NULL);return RC; }

"//".*$                 { /* ignore comments */ }
"/*"([^*]|[*][^/]|[*][*]+[^*/])*"*/"    { for (size_t i = 0; i < strlen(yytext); i++) if (yytext[i] == '\n') line++; }
[ \t\r]+                { /* ignore whitespace */ }
"\n"    {line++;}

0x([0-9a-fA-F]|[g-zG-Z])+     { yylval.node=new_Node(1,"ILLEGAL_HEX_INT",yytext,line,NULL,NULL); return ILLEGAL_HEX_INT; }
[0-9]{word_id}          { yylval.node=new_Node(1,"ILLEGAL_ID",yytext,line,NULL,NULL); return ILLEGAL_ID; }
'\\x.*'                 { yylval.node=new_Node(1,"ILLEGAL_CHAR",yytext,line,NULL,NULL); return ILLEGAL_CHAR; }
.                       { yylval.node = new_Node(1,"ILLEGAL",yytext,line,NULL,NULL); return ILLEGAL; }
%%
