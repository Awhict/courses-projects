#ifndef MYHEAD_H_  // 防止头文件重复包含
#define MYHEAD_H_

#ifdef __cplusplus  // 允许C++调用C语言代码
extern "C" {
#endif

#include <stdbool.h>

// 定义一个结构体，用于描述变量声明
typedef struct {
    char name[100];  // 变量名
    char type[100];  // 变量类型
} declare;

// 定义一个结构体，用于描述复杂类型的定义，包括数组、结构体和函数
typedef struct {
    char name[100];          // 名称
    char elem_type[100];     // 对于数组类型，表示元素的类型
    declare dec[100];        // 存储结构体成员或函数内部变量
    char return_type[100];   // 对于函数类型，表示返回值类型
    declare args[100];       // 对于函数，存储参数列表
    int arg_num;             // 函数参数的数量
    int dec_num;             // dec数组中的元素数量
} definition;

extern declare dec[100];     // 全局变量表
extern int dec_num;          // 全局变量数目
extern definition def[100];  // 复杂类型定义数组
extern int def_num;          // 复杂类型定义数目
extern char last_type[100];  // 上一次定义的类型名称

// 函数声明
void set_last_type(char *type);
bool add_dec(char *name, char *type, int lineno);
void add_array(char *name, char *elem_type, int lineno);
bool add_func_or_struct(char *name, int lineno, char *type);
void build_func_and_struct_dec(char *name, char *dec_name, char *type);
char* find_id_type(char *name);
declare* find_func_or_struct_dec(char *name);
char* find_func_return_type(char *name);
void add_struct_member(char *struct_name, char *member_name, char *member_type, int lineno);
void add_func_args(char *func_name, char *arg_name, char *arg_type, int lineno);
void add_func_variables(char *func_name, char *variable_name, char *variable_type, int lineno);
char* find_structure_member_type(char *struct_name, char *member_name);
void set_func_return_type(char *func_name, char *return_type);

#ifdef __cplusplus
}  
#endif

#endif /* MYHEAD_H_ */
