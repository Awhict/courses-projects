%{
    #include"syntax.tab.h"
    #include <stdlib.h> 
    #include <stdio.h> 
    #include <string.h> 

    #define MAX_ID_SIZE 256 

    int line = 1;
    typedef struct Head 
    {
        int terminal;
        char type[200];
        char id[200];
        char value_type[200];   //用于标记EXP的类型
        int rvalue;           //用于标记是否是右值
        int lineno;
        struct Head* child;
        struct Head* next;
    }Node;
    struct Head* create_Node(int terminal,char* type, char* id, Node* child,Node* next,int lineno);

    Node* create_Node(int terminal, char* type, char* id, Node* child, Node* next, int lineno) 
    {
        Node* newNode = malloc(sizeof(Node));
        if (newNode == NULL) {
            perror("Memory allocation error");
            exit(EXIT_FAILURE);
        }
        
        newNode->terminal = terminal;
        newNode->lineno = (lineno == 0 && child != NULL) ? child->lineno : lineno;
        
        if (type != NULL) {
            strncpy(newNode->type, type, sizeof(newNode->type) - 1);
            newNode->type[sizeof(newNode->type) - 1] = '\0'; 
        } else {
            newNode->type[0] = '\0';
        }
        
        if (id != NULL) {
            strncpy(newNode->id, id, sizeof(newNode->id) - 1);
            newNode->id[sizeof(newNode->id) - 1] = '\0'; 
        } else {
            newNode->id[0] = '\0';
        }
        
        newNode->child = child;
        newNode->next = next;
        newNode->rvalue = 0;
        
        return newNode;
    }
    
    void print_tree(Node* root, int depth) 
    {
        if (root == NULL) {
            return;
        }

        // 对于非空节点，进行缩进处理
        if (strcmp(root->type, "empty") != 0) {
            for (int i = 0; i < depth; i++) {
                printf("  ");
            }
        }

        // 打印终端节点（叶子节点）的信息
        if (root->terminal == 1) {
            printf("%s", root->type);

            // 对特定类型的节点，打印额外的信息
            if (strcmp(root->type, "ID") == 0 || strcmp(root->type,"TYPE") == 0 ||
                strcmp(root->type, "INT") == 0 || strcmp(root->type,"FLOAT") == 0 || 
                strcmp(root->type, "CHAR") == 0) {
                printf(": %s", root->id);
            }
            printf("\n");
        } else if (strcmp(root->type, "empty") != 0) {
            // 对于非终端且非空节点，打印节点类型和所在行号
            printf("%s (%d)\n", root->type, root->lineno);
        }

        // 递归打印子节点，增加缩进深度
        print_tree(root->child, depth + 1);

        // 递归打印兄弟节点，保持当前缩进深度
        print_tree(root->next, depth);
    }
%}

%option noyywrap

int_        [0-9]+|0x[0-9a-fA-F]+
float_      [0-9]+"."[0-9]+
id_         [a-zA-Z_][a-zA-Z0-9_]*
char_       \'.\'|\'\\x[0-9a-fA-F]{2}\'

%%
"int"                 { yylval.node=create_Node(1,"TYPE",yytext,NULL,NULL,line);return TYPE; }
"float"               { yylval.node=create_Node(1,"TYPE",yytext,NULL,NULL,line);return TYPE; }
"char"                { yylval.node=create_Node(1,"TYPE",yytext,NULL,NULL,line);return TYPE; }
"struct"              { yylval.node=create_Node(1,"STRUCT",yytext,NULL,NULL,line);return STRUCT; }
"if"                  { yylval.node=create_Node(1,"IF",yytext,NULL,NULL,line);return IF; }
"else"                { yylval.node=create_Node(1,"ELSE",yytext,NULL,NULL,line);return ELSE; }
"while"               { yylval.node=create_Node(1,"WHILE",yytext,NULL,NULL,line);return WHILE; }
"return"              { yylval.node=create_Node(1,"RETURN",yytext,NULL,NULL,line);return RETURN; }
{int_}              {yylval.node=create_Node(1,"INT",yytext,NULL,NULL,line);return INT;}
{float_}             { yylval.node=create_Node(1,"FLOAT",yytext,NULL,NULL,line);return FLOAT; }
{id_}               { yylval.node=create_Node(1,"ID",yytext,NULL,NULL,line);return ID; }
{char_}             { yylval.node=create_Node(1,"CHAR",yytext,NULL,NULL,line);return CHAR; }

"."                 { yylval.node=create_Node(1,"DOT",yytext,NULL,NULL,line);return DOT; }
";"                 { yylval.node=create_Node(1,"SEMI",yytext,NULL,NULL,line);return SEMI; }
","                 { yylval.node=create_Node(1,"COMMA",yytext,NULL,NULL,line);return COMMA; }
"="                 { yylval.node=create_Node(1,"ASSIGN",yytext,NULL,NULL,line);return ASSIGN; }
"<"                 { yylval.node=create_Node(1,"LT",yytext,NULL,NULL,line);return LT; }
">"                 { yylval.node=create_Node(1,"GT",yytext,NULL,NULL,line);return GT; }
"<="                { yylval.node=create_Node(1,"LE",yytext,NULL,NULL,line);return LE; }
">="                { yylval.node=create_Node(1,"GE",yytext,NULL,NULL,line);return GE; }
"!="                { yylval.node=create_Node(1,"NE",yytext,NULL,NULL,line);return NE; }
"=="                { yylval.node=create_Node(1,"EQ",yytext,NULL,NULL,line);return EQ; }
"+"                 { yylval.node=create_Node(1,"PLUS",yytext,NULL,NULL,line);return PLUS; }
"-"                 { yylval.node=create_Node(1,"MINUS",yytext,NULL,NULL,line);return MINUS; }
"*"                 { yylval.node=create_Node(1,"MUL",yytext,NULL,NULL,line);return MUL; }
"/"                 { yylval.node=create_Node(1,"DIV",yytext,NULL,NULL,line);return DIV; }
"&&"                { yylval.node=create_Node(1,"AND",yytext,NULL,NULL,line);return AND; }
"||"                { yylval.node=create_Node(1,"OR",yytext,NULL,NULL,line);return OR; }
"!"                 { yylval.node=create_Node(1,"NOT",yytext,NULL,NULL,line);return NOT; }
"("                 { yylval.node=create_Node(1,"LP",yytext,NULL,NULL,line);return LP; }
")"                 { yylval.node=create_Node(1,"RP",yytext,NULL,NULL,line);return RP; }
"["                 { yylval.node=create_Node(1,"LB",yytext,NULL,NULL,line);return LB; }
"]"                 { yylval.node=create_Node(1,"RB",yytext,NULL,NULL,line);return RB; }
"{"                 { yylval.node=create_Node(1,"LC",yytext,NULL,NULL,line);return LC; }
"}"                 { yylval.node=create_Node(1,"RC",yytext,NULL,NULL,line);return RC; }

"/*"([^*]|[*][^/]|[*][*]+[^*/])*"*/"  {/* ignore comments */}
[ \t\r]+            {/* ignore whitespace */}
"\n"    {line++;}

0x([0-9a-fA-F]|[g-zG-Z])+     { yylval.node=create_Node(1,"ILLEGAL_HEX_INT", yytext, NULL, NULL, line); return ILLEGAL_HEX_INT; }
[0-9]{id_}          { yylval.node=create_Node(1,"ILLEGAL_ID", yytext, NULL, NULL, line); return ILLEGAL_ID; }
'\\x.*'                        { yylval.node=create_Node(1,"ILLEGAL_CHAR", yytext, NULL, NULL, line); return ILLEGAL_CHAR; }
.                   { yylval.node = create_Node(1,"ILLEGAL", yytext, NULL, NULL, line); return ILLEGAL; }
%%
