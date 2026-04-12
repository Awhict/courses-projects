%{
    #include "lex.yy.c"

    void yyerror();
    Node* result=NULL;
    int flag=0;
%}

%union
{
    struct Head* node; /*"struct" is indispensable*/
}

%token <node> ID INT FLOAT CHAR STRUCT RETURN IF ELSE WHILE PLUS MINUS MUL DIV AND OR LT LE GT GE NE EQ NOT ASSIGN TYPE LP RP LB RB LC RC SEMI COMMA DOT ILLEGAL ILLEGAL_ID ILLEGAL_HEX_INT ILLEGAL_CHAR
%type <node> Program ExtDefList ExtDef ExtDecList Specifier StructSpecifier VarDec FunDec VarList ParamDec CompSt StmtList Stmt DefList Def DecList Dec Exp Args
%%

Program: ExtDefList {$$=new_Node(0,"Program","",0,$1,NULL);result=$$;}

ExtDefList: ExtDef ExtDefList  {$1->brother = $2;$$=new_Node(0,"ExtDefList","",0,$1,NULL);}
          | /* empty */         {$$=new_Node(0,"empty","",100,NULL,NULL);}

ExtDef: Specifier ExtDecList SEMI   {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"ExtDef","",0,$1,NULL);}
      | Specifier ExtDecList error  {printf("Error type B at line %d: missing semicolon ';'\n", $1->line);}
      | Specifier SEMI              {$1->brother = $2;$$=new_Node(0,"ExtDef","",0,$1,NULL);}
      | Specifier FunDec CompSt     {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"ExtDef","",0,$1,NULL);}

ExtDecList: VarDec                      {$$=new_Node(0,"ExtDecList","",0,$1,NULL);}
           | VarDec COMMA ExtDecList    {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"ExtDecList","",0,$1,NULL);}

Specifier: TYPE                         {$$=new_Node(0,"Specifier","",0,$1,NULL);}
          | StructSpecifier             {$$=new_Node(0,"Specifier","",0,$1,NULL);}

StructSpecifier: STRUCT ID LC DefList RC    {$1->brother = $2;$2->brother = $3;$3->brother = $4;$4->brother = $5;$$=new_Node(0,"StructSpecifier","",0,$1,NULL);}
               | STRUCT ID                  {$1->brother = $2;$$=new_Node(0,"StructSpecifier","",0,$1,NULL);}

VarDec: ID                              {$$=new_Node(0,"VarDec","",0,$1,NULL);}
       | ILLEGAL_ID error               {printf("Error type A at line %d: illegal identifier '%s'\n", $1->line,$1->id);}
       | VarDec LB INT RB               {$1->brother = $2;$2->brother = $3;$3->brother = $4;$$=new_Node(0,"VarDec","",0,$1,NULL);}

FunDec: ID LP VarList RP                {$1->brother = $2;$2->brother = $3;$3->brother = $4;$$=new_Node(0,"FunDec","",0,$1,NULL);}
       | ID LP RP                       {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"FunDec","",0,$1,NULL);}
       | ID LP VarList error            {printf("Error type B at line %d: missing closing symbols ')'\n", $1->line);}  
       | ID LP error                    {printf("Error type B at line %d: missing closing symbols ')'\n", $1->line);} 

VarList: ParamDec COMMA VarList         {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"VarList","",0,$1,NULL);}
        | ParamDec                      {$$=new_Node(0,"VarList","",0,$1,NULL);}

ParamDec: Specifier VarDec              {$1->brother = $2;$$=new_Node(0,"ParamDec","",0,$1,NULL);}

CompSt: LC DefList StmtList RC          {$1->brother = $2;$2->brother = $3;$3->brother = $4;$$=new_Node(0,"CompSt","",0,$1,NULL);}

StmtList: Stmt StmtList                 {$1->brother = $2;$$=new_Node(0,"StmtList","",0,$1,NULL);}
         |Stmt Def StmtList error       {printf("Error type B at line %d: definition after statement\n", $2->line);}
         | /* empty */                  {$$=new_Node(0,"empty","",100,NULL,NULL);}

Stmt: Exp SEMI                          {$1->brother = $2;$$=new_Node(0,"Stmt","",0,$1,NULL);}
    | CompSt                            {$$=new_Node(0,"Stmt","",0,$1,NULL);}
    | RETURN Exp SEMI                   {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Stmt","",0,$1,NULL);}
    | RETURN Exp error                  {printf("Error type B at line %d: missing semicolon ';'\n", $1->line);}     
    | IF LP Exp RP Stmt                 {$1->brother = $2;$2->brother = $3;$3->brother = $4;$4->brother = $5;$$=new_Node(0,"Stmt","",0,$1,NULL);}
    | IF LP Exp RP Stmt ELSE Stmt       {$1->brother = $2;$2->brother = $3;$3->brother = $4;$4->brother = $5;$5->brother = $6;$6->brother = $7;$$=new_Node(0,"Stmt","",0,$1,NULL);}
    | WHILE LP Exp RP Stmt              {$1->brother = $2;$2->brother = $3;$3->brother = $4;$4->brother = $5;$$=new_Node(0,"Stmt","",0,$1,NULL);}

DefList: Def DefList                    {$1->brother = $2;$$=new_Node(0,"DefList","",0,$1,NULL);}
        | /* empty */                   {$$=new_Node(0,"empty","",100,NULL,NULL);}

Def: Specifier DecList SEMI             {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Def","",0,$1,NULL);}
    | Specifier DecList error           {printf("Error type B at line %d: missing semicolon ';'\n", $1->line);}

DecList: Dec                            {$$=new_Node(0,"DecList","",0,$1,NULL);}
        | Dec COMMA DecList             {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"DecList","",0,$1,NULL);}

Dec: VarDec                             {$$=new_Node(0,"Dec","",0,$1,NULL);}
    | VarDec ASSIGN Exp                 {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Dec","",0,$1,NULL);}

Exp: Exp ASSIGN Exp                     {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp AND Exp                       {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp OR Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}    
    | Exp LT Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}    
    | Exp LE Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}    
    | Exp GT Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp GE Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp NE Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp EQ Exp                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp PLUS Exp                      {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp MINUS Exp                     {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp MUL Exp                       {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp DIV Exp                       {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | LP Exp RP                         {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | LP Exp error                      {printf("Error type B at line %d: missing closing symbols ')'\n", $1->line);}
    | MINUS Exp                         {$1->brother = $2;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | NOT Exp                           {$1->brother = $2;$$=new_Node(0,"Exp","",0,$1,NULL);}  
    | ID LP Args RP                     {$1->brother = $2;$2->brother = $3;$3->brother = $4;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | ID LP Args error                  {printf("Error type B at line %d: missing closing symbols ')'\n", $1->line);}
    | ID LP RP                          {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp LB Exp RB                     {$1->brother = $2;$2->brother = $3;$3->brother = $4;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | Exp DOT ID                        {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Exp","",0,$1,NULL);}
    | ID                                {$$=new_Node(0,"Exp","",0,$1,NULL);}
    | INT                               {$$=new_Node(0,"Exp","",0,$1,NULL);}
    | FLOAT                             {$$=new_Node(0,"Exp","",0,$1,NULL);}
    | CHAR                              {$$=new_Node(0,"Exp","",0,$1,NULL);}
    | ILLEGAL error                     {printf("Error type A at line %d: illegal character '%s'\n", $1->line,$1->id);}
    | ILLEGAL_HEX_INT error             {printf("Error type A at line %d: illegal hexadecimal integer '%s'\n", $1->line,$1->id);}
    | ILLEGAL_CHAR error                {printf("Error type A at line %d: illegal hex_character '%s'\n", $1->line,$1->id);}
    | Exp ILLEGAL Exp error             {printf("Error type A at line %d: illegal operator '%s'\n", $2->line,$2->id);}

Args: Exp COMMA Args                    {$1->brother = $2;$2->brother = $3;$$=new_Node(0,"Args","",0,$1,NULL);}
     | Exp                              {$$=new_Node(0,"Args","",0,$1,NULL);}

%%


void yyerror() {
    flag=1;
    return ;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file_path>\n", argv[0]);
        exit(-1);
    } else if (!(yyin = fopen(argv[1], "r"))) {
        perror(argv[1]);
        exit(-1);
    }
    yyparse();
    if(flag==0)
    {
        print_tree(result,0);
    }
    return 0;
}
