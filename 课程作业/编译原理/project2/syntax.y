%{
    #include "lex.yy.c"
    
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdarg.h>

    #include "myhead.h"

    void yyerror();

    Node* root=NULL;
    int flag=0;

    

    void connect_to_next(int next_num, ...)
{
    if (next_num <= 0) {
        // 如果没有节点或参数数量为负，不执行任何操作
        return;
    }
    
    va_list valist;
    va_start(valist, next_num); 

    Node* temp = va_arg(valist, Node*); // 获取第一个节点
    Node* prev = temp; 
    for (int i = 1; i < next_num; i++)
    {
        temp = va_arg(valist, Node*); // 获取下一个节点
        if (prev) {
            prev->next = temp; 
        }
        prev = temp; // 更新
    }

    if (temp) {
        temp->next = NULL; 
    }
    
    va_end(valist); 
}

    bool is_in_function=false;//标记当前是否在函数体内部，如果不是，则不允许定义变量
    char *current_function_name;//标记当前所在的函数名
    bool index_error=false; //标记数组下标是否出错
    void find_compst_return(Node *Compst, char *expected_type);
    void check_nested_statements(Node *stmt, char *expected_type);
    
    
    /* 结构体操作 */
    void insert_vardec(Node *node) {
        if (!node->child->next) {
            // 如果子节点没有next成员，则不是数组类型
            add_dec(node->child->id, last_type, node->lineno);
        } else {
            // 如果子节点有next成员，则为数组类型
            if (add_dec(node->child->child->id, "array", node->lineno)) {
                add_array(node->child->child->id, last_type, node->lineno);
            }
        }
    }

    void insert_ExtDecList(Node* node) {
        // 处理当前变量声明
        insert_vardec(node->child);
        if (node->child->next) {
            // 如果存在多个变量声明（逗号分隔），递归处理余下的声明
            insert_ExtDecList(node->child->next->next);
        }
    }

    void add_struct_member_deflist(Node* node, char* struct_name)
    {
        //用于处理struct内部的成员声明
        //node为DefList
        //struct_name为结构体名
        if(!node||!node->child)
        {
            return;
        }
        Node* temp=node->child;
        //temp即Def
        Node* temp2=temp->child;
        //temp2即Specifier
        //char* type=temp2->child->id;
        char *type;
        if (strcmp(temp2->child->type,"TYPE")==0)
        {
            //不是结构体
            type=temp2->child->id;
        }
        else
        {
            //是结构体
            type=temp2->child->child->next->id;
        }
        Node *temp3=temp->child->next;
        //temp3即DecList
        while(temp3)
        {
            Node* temp4=temp3->child;
            //temp4即Dec
            Node* temp5=temp4->child;
            //temp5即VarDec
            if(temp5->child->next==NULL)
            {
                //不是数组
                add_struct_member(struct_name,temp5->child->id,type,temp5->lineno);
            }
            else
            {
                //是数组
                add_struct_member(struct_name,temp5->child->child->id,"array",temp5->lineno);
                add_array(temp5->child->child->id,type,temp5->lineno);
            }
            if(temp3->child->next)
            {
                //Dec COMMA DecList
                temp3=temp3->child->next->next;
            }
            else
            {
                //Dec
                break;
            }
        }
        if(node->child)
        {
            //Def DefList
            add_struct_member_deflist(node->child->next,struct_name);
        }
        else
        {
            //Def
            return;
        }
        return;
    }


    /* 函数参数和变量插入 */
    void insert_function_args(char *func_name, Node *node) {
        if (node == NULL) {
            // 如果节点为空，没有更多的变量需要处理，返回
            return;
        }

        // 处理当前的ParamDec节点
        Node *param = node->child;
        Node *specifier = param->child;
        Node *vardec = specifier->next;
        char *type = specifier->child->id; // 获取类型
        char *name = vardec->child->id;    // 获取变量名
        // 为简单起见，此处假设参数是非数组类型
        add_func_args(func_name, name, type, param->lineno);

        // 如果存在COMMA，说明后面还有参数，递归处理后续的VarList
        Node *nextParam = node->child->next;
        if (nextParam != NULL && strcmp(nextParam->type, "COMMA") == 0) {
            insert_function_args(func_name, nextParam->next);
        }
    }
        
    void insert_func_variables(Node *Dec) {
        // 如果不在函数内部或输入节点为空，则不需要处理
        if (!is_in_function || Dec == NULL) {
            return;
        }

        // 在函数体内部
        Node *VarDec = Dec->child;
        char *var_name;
        char *var_type;
        
        // 判断是否为数组类型
        if (VarDec->child->next) {
            // 处理数组类型的变量
            var_name = VarDec->child->child->id;
            var_type = "array";
            add_func_variables(current_function_name, var_name, var_type, VarDec->lineno);
            add_array(var_name, last_type, VarDec->lineno);
        } else {
            // 处理普通变量
            var_name = VarDec->child->id;
            var_type = last_type;
            add_func_variables(current_function_name, var_name, var_type, VarDec->lineno);
        }

        // 检查赋值语句并验证类型匹配
        Node *Assign = VarDec->next;
        if (Assign && strcmp(Assign->type, "ASSIGN") == 0) {
            Node *Exp = Assign->next;
            if (strcmp(Exp->value_type, "error") != 0 && strcmp(Exp->value_type, last_type) != 0) {
                printf("Error type 5 at line %d: Type mismatched for assignment\n", Exp->lineno);
            }
        }
    }


    /* 表达式检查 */
    void check_type(Node *exp, const char *expected_type, int error_type, int lineno) {
        if (strcmp(exp->value_type, "error") == 0) {
            // 类型已经是错误，之前的步骤中已经报错，此处不再重复。
            return;
        }
        if (expected_type != NULL && strcmp(exp->value_type, expected_type) != 0) {
            printf("Error type %d at line %d: Type mismatched for operands\n", error_type, lineno);
        }
    }

    void check_single_arithmetic_exp(Node *exp) {
        // 检查单个Exp的类型是否为int或者float
        check_type(exp, NULL, 7, exp->lineno);
        if (strcmp(exp->value_type, "int") != 0 && strcmp(exp->value_type, "float") != 0) {
            printf("Error type 7 at line %d: Type mismatched for operands, expected int or float\n", exp->lineno);
        }
    }

    void check_single_logical_exp(Node *exp) {
        // 检查单个Exp的类型是否为int
        check_type(exp, "int", 7, exp->lineno);
    }

    void check_exp_arithmetic_symbols(Node *exp1, Node *exp2) {
        // 假设算术运算只能由int或float类型的变量进行
        check_type(exp1, NULL, 7, exp1->lineno);
        check_type(exp2, NULL, 7, exp2->lineno);
        if ((strcmp(exp1->value_type, "int") != 0 && strcmp(exp1->value_type, "float") != 0) || 
            (strcmp(exp2->value_type, "int") != 0 && strcmp(exp2->value_type, "float") != 0)) {
            printf("Error type 7 at line %d: Type mismatched for operands, expected int or float\n", exp1->lineno);
        }
        if (strcmp(exp1->value_type, exp2->value_type) != 0) {
            printf("Error type 7 at line %d: Type mismatched for operands, expected same type\n", exp1->lineno);
        }
    }

    void check_exp_logical_symbols(Node *exp1, Node *exp2) {
        // 假设逻辑运算只能由int类型的变量进行
        check_type(exp1, "int", 7, exp1->lineno);
        check_type(exp2, "int", 7, exp2->lineno);
    }

    void check_exp_assign(Node *exp1, Node *exp2) {
        // 用于检查赋值语句左右两边的类型是否匹配
        check_type(exp1, NULL, 6, exp1->lineno);
        check_type(exp2, NULL, 5, exp2->lineno);
        if (exp1->rvalue) {
            printf("Error type 6 at line %d: rvalue on the left side of assignment operator\n", exp1->lineno);
            return;
        }
        if (strcmp(exp1->value_type, exp2->value_type) != 0) {
            printf("Error type 5 at line %d: Type mismatched for assignment\n", exp1->lineno);
        }
    }

    void check_Exp_with_specific_type(Node *Exp, char *expected_type) {
        // 用于检查Exp的类型是否为expected_type
        check_type(Exp, expected_type, 7, Exp->lineno);
    }

    void check_Def(Node *Def) {
        // expected_type 为定义的类型
        char *expected_type = last_type;
        Node *DecList = Def->child->next;
        
        // 循环处理定义列表中的所有声明
        while (DecList) {
            Node *Dec = DecList->child;
            Node *VarDec = Dec->child;

            // 如果存在赋值（ASSIGN），检查表达式（Exp）的类型是否匹配
            Node *Assign = VarDec->next;
            if (Assign && strcmp(Assign->type, "ASSIGN") == 0) {
                Node *Exp = Assign->next;
                if (strcmp(Exp->value_type, "error") != 0 && strcmp(Exp->value_type, expected_type) != 0) {
                    printf("Error type 5 at line %d: Type mismatched for assignment\n", Exp->lineno);
                }
            }

            // 移动到下一个声明，如果存在
            DecList = (Dec->next && strcmp(Dec->next->type, "COMMA") == 0) ? Dec->next->next : NULL;
        }
    }

    //设置节点的值为右值 
    void set_rvalue(Node *node) {
        if (node) {
            node->rvalue = 1;
        }
    }

    //设置节点的类型
    void set_EXP_value_type(Node *node, char *type) {
        if (node && type) {
            strcpy(node->value_type, type);
        }
    }


    /* 函数参数和返回类型检查 */
    void check_func_return_type(Node* Compst, char *expected_type) {
        if (!is_in_function || Compst == NULL) {
            // 如果不在函数内部或者Compst为空，则不需要处理
            return;
        }
        // 递归检查函数体中的返回语句
        find_compst_return(Compst, expected_type);
    }

    void find_compst_return(Node *Compst, char *expected_type) {
        Node *stmtlist = Compst->child->next->next;
        while (stmtlist && stmtlist->child) {
            Node *stmt = stmtlist->child;
            if (strcmp(stmt->child->type, "RETURN") == 0) {
                Node *exp = stmt->child->next;
                if (exp && strcmp(exp->value_type, expected_type) != 0 && strcmp(exp->value_type, "error") != 0) {
                    printf("Error type 8 at line %d: The return type mismatched\n", exp->lineno);
                }
            } else if (strcmp(stmt->child->type, "CompSt") == 0) {
                find_compst_return(stmt->child, expected_type);
            } else {
                // 处理可能嵌套的结构，如if-else和while语句
                check_nested_statements(stmt, expected_type);
            }
            stmtlist = stmtlist->next ? stmtlist->next->child : NULL;
        }
    }

    void check_nested_statements(Node *stmt, char *expected_type) {
        Node *head = stmt->child;
        while (head) {
            if (strcmp(head->type, "Stmt") == 0) {
                if (strcmp(head->child->type, "CompSt") == 0) {
                    find_compst_return(head->child, expected_type);
                } else if (strcmp(head->child->type, "RETURN") == 0) {
                    Node *exp = head->child->next;
                    if (exp && strcmp(exp->value_type, expected_type) != 0 && strcmp(exp->value_type, "error") != 0) {
                        printf("Error type 8 at line %d: The return type mismatched\n", exp->lineno);
                    }
                }
            }
            head = head->next;
        }
    }

    void check_func_args(char *func_name, Node *Args, int arg_index) {
        // 查找函数定义
        int func_index;
        for(func_index = 0; func_index < def_num; func_index++) {
            if(strcmp(def[func_index].name, func_name) == 0) {
                break;
            }
        }
        // 如果没有找到函数，直接返回
        if(func_index == def_num) return;

        Node *current_arg = Args->child;
        // 检查参数个数和类型是否匹配
        if(arg_index < def[func_index].arg_num) {
            if(strcmp(current_arg->value_type, def[func_index].args[arg_index].type) != 0) {
                printf("Error type 9 at line %d: Unmatched argument type for Function \"%s\"\n", current_arg->lineno, func_name);
                return;
            }
        } else {
            printf("Error type 9 at line %d: Too many arguments for Function \"%s\"\n", current_arg->lineno, func_name);
            return;
        }
        // 递归检查下一个参数，如果存在
        if(current_arg->next) {
            check_func_args(func_name, current_arg->next->next, arg_index + 1);
        } else if(arg_index + 1 < def[func_index].arg_num) {
            printf("Error type 9 at line %d: Too few arguments for Function \"%s\"\n", current_arg->lineno, func_name);
        }
    }

    void check_func_without_args(char *func_name, int lineno) {
        // 查找函数定义
        int func_index;
        for(func_index = 0; func_index < def_num; func_index++) {
            if(strcmp(def[func_index].name, func_name) == 0) {
                break;
            }
        }
        // 如果没有找到函数，直接返回
        if(func_index == def_num) return;

        if(def[func_index].arg_num != 0) {
            printf("Error type 9 at line %d: Function \"%s\" expects no arguments\n", lineno, func_name);
        }
    }


    /* 数组操作检查 */
    bool check_exp_array(Node *array_exp, Node *index_exp) {
        // 如果下标或数组表达式的类型已经是错误，不再进行检查
        if (strcmp(index_exp->value_type, "error") == 0 || strcmp(array_exp->value_type, "error") == 0) {
            return false;
        }
        // 检查是否应用了下标操作符到非数组类型的变量上
        if (strcmp(array_exp->value_type, "array") != 0) {
            printf("Error type 10 at line %d: Indexing operator ([...]) applied to non-array variable \"%s\".\n", array_exp->lineno, array_exp->id);
            return false;
        }
        // 检查下标是否为整型
        if (strcmp(index_exp->value_type, "int") != 0) {
            printf("Error type 12 at line %d: Array index is not an integer.\n", index_exp->lineno);
            index_error = true; // 确保外部标记了存在下标错误
            return true;
        }
        return true;
    }

    char* find_array_elem_type(Node *exp) {
        // 找到数组的ID节点
        Node *id = NULL;
        bool found = false;
        while (exp->child && !found) {
            exp = exp->child;
            Node *temp = exp;
            while (temp) {
                if (strcmp(temp->type, "ID") == 0) {
                    id = temp;
                    found = true;
                    break;
                }
                temp = temp->next;
            }
        }
        // 在定义中查找匹配的数组并返回其元素类型
        for (int i = 0; i < def_num; i++) {
            if (strcmp(def[i].name, id->id) == 0) {
                return def[i].elem_type;
            }
        }
        return NULL; // 如果没有找到匹配的定义，返回NULL
    }

    /* 结构体成员检查 */
    bool check_exp_structure(Node *structure_exp, Node *member_id) {
        // 如果表达式类型有错误，则不再检查
        if (strcmp(structure_exp->value_type, "error") == 0 || strcmp(member_id->value_type, "error") == 0) {
            return false;
        }

        // 检查是否为结构体
        bool is_structure_found = false;
        for (int i = 0; i < dec_num && !is_structure_found; i++) {
            if (strcmp(dec[i].name, structure_exp->value_type) == 0) {
                if (strcmp(dec[i].type, "structure") != 0) {
                    printf("Error type 13 at line %d: Illegal member access on non-structure variable \"%s\"\n", 
                        structure_exp->lineno, structure_exp->id);
                    return false;
                }
                is_structure_found = true;
            }
        }

        // 如果没有找到对应的结构体定义，则报错
        if (!is_structure_found) {
            printf("Error type 13 at line %d: Illegal member access on non-structure variable \"%s\"\n", 
                structure_exp->lineno, structure_exp->id);
            return false;
        }

        // 检查结构体内是否有该成员
        char *type = find_structure_member_type(structure_exp->value_type, member_id->id);
        if (!type) {
            printf("Error type 14 at line %d: Structure '%s' has no member named '%s'\n", 
                structure_exp->lineno, structure_exp->value_type, member_id->id);
            return false;
        }

        return true;
    }


    /* 函数调用检查 */
    bool check_if_func_exist(char *name, int lineno) {
        // 首先检查全局声明是否包含该名称
        for (int i = 0; i < dec_num; ++i) {
            if (strcmp(dec[i].name, name) == 0) {
                // 名称匹配，检查是否为函数类型
                if (strcmp(dec[i].type, "function") != 0) {
                    printf("Error type 11 at Line %d: '%s' is not a function name.\n", lineno, name);
                    return false;
                }
                return true;
            }
        }

        // 接下来检查当前函数内部是否有同名的参数或局部声明
        for (int i = 0; i < def_num; ++i) {
            if (strcmp(def[i].name, current_function_name) == 0) {
                // 检查参数
                for (int j = 0; j < def[i].arg_num; ++j) {
                    if (strcmp(def[i].args[j].name, name) == 0) {
                        printf("Error type 11 at Line %d: '%s' is a parameter, not a function.\n", lineno, name);
                        return false;
                    }
                }
                // 检查局部声明
                for (int j = 0; j < def[i].dec_num; ++j) {
                    if (strcmp(def[i].dec[j].name, name) == 0) {
                        if (strcmp(def[i].dec[j].type, "function") != 0) {
                            printf("Error type 11 at Line %d: '%s' is not a function name.\n", lineno, name);
                            return false;
                        }
                        return true;
                    }
                }
            }
        }

        // 如果前面的检查都没有返回，意味着函数未定义
        printf("Error type 2 at Line %d: Function \"%s\" is invoked without definition.\n", lineno, name);
        return false;
    }


    /* 变量检查 */
    char* check_exp_id(Node *id) {
        char *type = "error"; // 默认类型为 "error"

        // 首先在全局声明中检索
        for (int i = 0; i < dec_num; ++i) {
            if (strcmp(dec[i].name, id->id) == 0) {
                return dec[i].type; // 找到匹配，返回对应类型
            }
        }

        // 再检查是否为某个结构体定义的成员
        for (int i = 0; i < def_num; ++i) {
            for (int j = 0; j < def[i].dec_num; ++j) {
                if (strcmp(def[i].dec[j].name, id->id) == 0) {
                    return def[i].dec[j].type; // 找到匹配，返回对应类型
                }
            }
        }

        // 最后检查是否为当前函数的参数或局部变量
        for (int i = 0; i < def_num; ++i) {
            if (strcmp(def[i].name, current_function_name) == 0) {
                // 检查参数
                for (int j = 0; j < def[i].arg_num; ++j) {
                    if (strcmp(def[i].args[j].name, id->id) == 0) {
                        return def[i].args[j].type; // 找到匹配，返回对应类型
                    }
                }
                // 检查局部变量
                for (int j = 0; j < def[i].dec_num; ++j) {
                    if (strcmp(def[i].dec[j].name, id->id) == 0) {
                        return def[i].dec[j].type; // 找到匹配，返回对应类型
                    }
                }
            }
        }

        // 如果标识符未定义并且处于函数内部，则打印错误信息
        if (strcmp(type, "error") == 0 && is_in_function) {
            printf("Error type 1 at line %d: Undefined variable \"%s\".\n", id->lineno, id->id);
        }
        return type; // 如果没有找到匹配的声明，返回 "error"
    }
%}



%union
{
    int     num;
    char*   str;
    struct Head* node; /*"struct" is indispensable*/
}



%right ASSIGN
%left OR
%left AND
%left LT LE GT GE NE EQ
%left PLUS MINUS
%left MUL DIV
%right NOT NEGATIVE
%nonassoc LC RC LB RB LP RP DOT

%token <node> ID INT FLOAT CHAR STRUCT RETURN IF ELSE WHILE PLUS MINUS MUL DIV AND OR LT LE GT GE NE EQ NOT ASSIGN TYPE LP RP LB RB LC RC SEMI COMMA DOT ILLEGAL ILLEGAL_ID ILLEGAL_HEX_INT ILLEGAL_CHAR

%type <node> Program ExtDefList ExtDef ExtDecList Specifier StructSpecifier VarDec FunDec VarList ParamDec CompSt StmtList Stmt DefList Def DecList Dec Exp Args
%%

Program: ExtDefList {$$=create_Node(0,"Program","",$1,NULL,0);root=$$;}

ExtDefList: ExtDef ExtDefList  {connect_to_next(2,$1,$2);$$=create_Node(0,"ExtDefList","",$1,NULL,0);}
          | /* empty */         {$$=create_Node(0,"empty","",NULL,NULL,100);}

ExtDef: Specifier ExtDecList SEMI   {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"ExtDef","",$1,NULL,0);insert_ExtDecList($2);}
      | Specifier ExtDecList error  {printf("Error type B at line %d: missing semicolon ';'\n", $1->lineno);}
      | Specifier SEMI              {connect_to_next(2,$1,$2);$$=create_Node(0,"ExtDef","",$1,NULL,0);}
      | Specifier FunDec CompSt     {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"ExtDef","",$1,NULL,0);if(is_in_function){set_func_return_type(current_function_name,$1->child->id);check_func_return_type($3,$1->child->id);}is_in_function=false;}

ExtDecList: VarDec                      {$$=create_Node(0,"ExtDecList","",$1,NULL,0);}
           | VarDec COMMA ExtDecList    {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"ExtDecList","",$1,NULL,0);}

Specifier: TYPE                         {$$=create_Node(0,"Specifier","",$1,NULL,0);set_last_type($1->id);}
          | StructSpecifier             {$$=create_Node(0,"Specifier","",$1,NULL,0);}

StructSpecifier: STRUCT ID LC DefList RC    {connect_to_next(5,$1,$2,$3,$4,$5);$$=create_Node(0,"StructSpecifier","",$1,NULL,0);if(add_dec($2->id,"structure",$2->lineno)&&add_func_or_struct($2->id,$2->lineno,"structure")){add_struct_member_deflist($4,$2->id);}}
               | STRUCT ID                  {connect_to_next(2,$1,$2);$$=create_Node(0,"StructSpecifier","",$1,NULL,0);set_last_type($2->id);}

VarDec: ID                              {$$=create_Node(0,"VarDec","",$1,NULL,0);}
       | ILLEGAL_ID error               {printf("Error type A at line %d: illegal identifier '%s'\n", $1->lineno,$1->id);}
       | VarDec LB INT RB               {connect_to_next(4,$1,$2,$3,$4);$$=create_Node(0,"VarDec","",$1,NULL,0);}

FunDec: ID LP VarList RP                {connect_to_next(4,$1,$2,$3,$4);$$=create_Node(0,"FunDec","",$1,NULL,0);if(add_dec($1->id,"function",$1->lineno)&&add_func_or_struct($1->id,$1->lineno,"function")){insert_function_args($1->id,$3);current_function_name=$1->id;is_in_function=true;} else{is_in_function=false;}}
       | ID LP RP                       {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"FunDec","",$1,NULL,0);if(add_dec($1->id,"function",$1->lineno)&&add_func_or_struct($1->id,$1->lineno,"function")){current_function_name=$1->id;is_in_function=true;} else{is_in_function=false;}}
       | ID LP VarList error            {printf("Error type B at line %d: missing closing symbols ')'\n", $1->lineno);}  
       | ID LP error                    {printf("Error type B at line %d: missing closing symbols ')'\n", $1->lineno);} 

VarList: ParamDec COMMA VarList         {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"VarList","",$1,NULL,0);}
        | ParamDec                      {$$=create_Node(0,"VarList","",$1,NULL,0);}

ParamDec: Specifier VarDec              {connect_to_next(2,$1,$2);$$=create_Node(0,"ParamDec","",$1,NULL,0);}

CompSt: LC DefList StmtList RC          {connect_to_next(4,$1,$2,$3,$4);$$=create_Node(0,"CompSt","",$1,NULL,0);}

StmtList: Stmt StmtList                 {connect_to_next(2,$1,$2);$$=create_Node(0,"StmtList","",$1,NULL,0);}
         |Stmt Def StmtList error       {printf("Error type B at line %d: definition after statement\n", $2->lineno);}
         | /* empty */                  {$$=create_Node(0,"empty","",NULL,NULL,100);}

Stmt: Exp SEMI                          {connect_to_next(2,$1,$2);$$=create_Node(0,"Stmt","",$1,NULL,0);}
    | CompSt                            {$$=create_Node(0,"Stmt","",$1,NULL,0);}
    | RETURN Exp SEMI                   {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Stmt","",$1,NULL,0);}
    | RETURN Exp error                  {printf("Error type B at line %d: missing semicolon ';'\n", $1->lineno);}     
    | IF LP Exp RP Stmt                 {connect_to_next(5,$1,$2,$3,$4,$5);$$=create_Node(0,"Stmt","",$1,NULL,0);}
    | IF LP Exp RP Stmt ELSE Stmt       {connect_to_next(7,$1,$2,$3,$4,$5,$6,$7);$$=create_Node(0,"Stmt","",$1,NULL,0);}
    | WHILE LP Exp RP Stmt              {connect_to_next(5,$1,$2,$3,$4,$5);$$=create_Node(0,"Stmt","",$1,NULL,0);}

DefList: Def DefList                    {connect_to_next(2,$1,$2);$$=create_Node(0,"DefList","",$1,NULL,0);}
        | /* empty */                   {$$=create_Node(0,"empty","",NULL,NULL,100);}

Def: Specifier DecList SEMI             {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Def","",$1,NULL,0);check_Def($$);}
    | Specifier DecList error           {printf("Error type B at line %d: missing semicolon ';'\n", $1->lineno);}

DecList: Dec                            {$$=create_Node(0,"DecList","",$1,NULL,0);}
        | Dec COMMA DecList             {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"DecList","",$1,NULL,0);}

Dec: VarDec                             {$$=create_Node(0,"Dec","",$1,NULL,0);insert_func_variables($$);}
    | VarDec ASSIGN Exp                 {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Dec","",$1,NULL,0);insert_func_variables($$);}

Exp: Exp ASSIGN Exp                     {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_assign($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp AND Exp                       {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp OR Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}    
    | Exp LT Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}    
    | Exp LE Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}    
    | Exp GT Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp GE Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp NE Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp EQ Exp                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_logical_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,"int");}
    | Exp PLUS Exp                      {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_arithmetic_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,$1->value_type);}
    | Exp MINUS Exp                     {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_arithmetic_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,$1->value_type);}
    | Exp MUL Exp                       {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_arithmetic_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,$1->value_type);}
    | Exp DIV Exp                       {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);check_exp_arithmetic_symbols($1,$3);set_rvalue($$);set_EXP_value_type($$,$1->value_type);}
    | LP Exp RP                         {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);strcpy($$->value_type,$2->value_type);$$->rvalue=$2->rvalue;}    //(b)
    | LP Exp error                      {printf("Error type B at line %d: missing closing symbols ')'\n", $1->lineno);}
    | MINUS Exp                         {connect_to_next(2,$1,$2);$$=create_Node(0,"Exp","",$1,NULL,0);check_single_arithmetic_exp($2);$$->rvalue=$2->rvalue;set_EXP_value_type($$,$2->value_type);}
    | NOT Exp                           {connect_to_next(2,$1,$2);$$=create_Node(0,"Exp","",$1,NULL,0);check_single_logical_exp($2);$$->rvalue=$2->rvalue;set_EXP_value_type($$,$2->value_type);}
    | ID LP Args RP                     {connect_to_next(4,$1,$2,$3,$4);$$=create_Node(0,"Exp","",$1,NULL,0);if(check_if_func_exist($1->id,$1->lineno)){check_func_args($1->id,$3,0);set_EXP_value_type($$,find_func_return_type($1->id));} else{set_EXP_value_type($$,"error");}}         //调用函数a(...)
    | ID LP Args error                  {printf("Error type B at line %d: missing closing symbols ')'\n", $1->lineno);}
    | ID LP RP                          {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);if(check_if_func_exist($1->id,$1->lineno)){check_func_without_args($1->id,$1->lineno);set_EXP_value_type($$,find_func_return_type($1->id));} else{set_EXP_value_type($$,"error");}}    //调用函数，无参数
    | Exp LB Exp RB                     {connect_to_next(4,$1,$2,$3,$4);$$=create_Node(0,"Exp","",$1,NULL,0);if(check_exp_array($1,$3)){if(index_error){set_EXP_value_type($$,"None");index_error=false;}else{set_EXP_value_type($$,find_array_elem_type($1));}}else{set_EXP_value_type($$,"error");}}     //数组访问a[...]
    | Exp DOT ID                        {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Exp","",$1,NULL,0);if(check_exp_structure($1,$3)){set_EXP_value_type($$,find_structure_member_type($1->value_type,$3->id));}else{strcpy($$->value_type,"None");}}    //结构体
    | ID                                {$$=create_Node(0,"Exp","",$1,NULL,0);set_EXP_value_type($$,check_exp_id($1));}
    | INT                               {$$=create_Node(0,"Exp","",$1,NULL,0);set_EXP_value_type($$,"int");$$->rvalue=1;}
    | FLOAT                             {$$=create_Node(0,"Exp","",$1,NULL,0);set_EXP_value_type($$,"float");$$->rvalue=1;}
    | CHAR                              {$$=create_Node(0,"Exp","",$1,NULL,0);set_EXP_value_type($$,"char");$$->rvalue=1;}
    | ILLEGAL error                     {printf("Error type A at line %d: unknown lexeme '%s'\n", $1->lineno,$1->id);}
    | ILLEGAL_HEX_INT error             {printf("Error type A at line %d: illegal hexadecimal integer '%s'\n", $1->lineno,$1->id);}
    | ILLEGAL_CHAR error                {printf("Error type A at line %d: illegal hex_character '%s'\n", $1->lineno,$1->id);}
    | Exp ILLEGAL Exp error             {printf("Error type A at line %d: illegal operator '%s'\n", $2->lineno,$2->id);}
    

Args: Exp COMMA Args                    {connect_to_next(3,$1,$2,$3);$$=create_Node(0,"Args","",$1,NULL,0);}
     | Exp                              {$$=create_Node(0,"Args","",$1,NULL,0);}

%%


void yyerror() {
    //printf("Syntax error at line %d: %s\n", line, s);
    //printf("Error type B at line ");
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
        //print_tree(root,0);
    }

    /*
    printf("\ntables:\n");
    //打印符号表
    for(int i=0;i<dec_num;i++)
    {
        printf("%s %s\n",dec[i].name,dec[i].type);
    }
    
    //打印定义表
    for(int i=0;i<def_num;i++)
    {
        printf("%s \n",def[i].name);
        for(int j=0;j<def[i].arg_num;j++)
        {
            printf("%s %s\n",def[i].args[j].name,def[i].args[j].type);
        }
        for(int j=0;j<def[i].dec_num;j++)
        {
            printf("%s %s\n",def[i].dec[j].name,def[i].dec[j].type);
        }
        printf("return_type:%s\n",def[i].return_type);
    }
    */
    return 0;
}
