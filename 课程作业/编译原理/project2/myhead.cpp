#include "myhead.h"
#include <cstdio>
#include <cstring>

declare dec[100];//定义的变量表
int dec_num=0;//定义的变量数目
definition def[100];//定义的array,struct,function
int def_num=0;//定义的array,struct,function数目
char last_type[100];//最后一次定义的类型

void set_last_type(char *type) {
    strcpy(last_type, type);  // 直接复制类型名称到 last_type
}

bool add_dec(char *name, char *type, int lineno) {
    // 检查变量是否已经被定义过
    for (int i = 0; i < dec_num; ++i) {
        if (strcmp(dec[i].name, name) == 0) {
            // 根据已存在变量类型区分错误类型
            const char *errorType =
                strcmp(dec[i].type, "function") == 0 ? "function" :
                strcmp(dec[i].type, "structure") == 0 ? "structure" :
                "variable";
            int errorTypeCode = strcmp(errorType, "function") == 0 ? 4 :
                                strcmp(errorType, "structure") == 0 ? 15 :
                                3;
            printf("Error type %d at Line %d: Redefined %s \"%s\".\n", errorTypeCode, lineno, errorType, name);
            return false;
        }
    }

    // 添加新的定义
    strcpy(dec[dec_num].name, name);
    strcpy(dec[dec_num].type, type);
    dec_num++;  // 增加定义计数
    return true;
}

void add_array(char *name, char *elem_type, int lineno) {
    // 检查数组是否已经被定义过
    for (int i = 0; i < def_num; ++i) {
        if (strcmp(def[i].name, name) == 0) {
            printf("Error type 3 at Line %d: Redefined variable \"%s\".\n", lineno, name);
            return;
        }
    }

    // 添加新的数组定义
    strcpy(def[def_num].name, name);
    strcpy(def[def_num].elem_type, elem_type);
    def[def_num].dec_num = 0;  // 初始化数组内部变量计数为0
    def_num++;  // 增加定义计数
}

bool add_func_or_struct(char *name, int lineno, char *type) {
    // 检查是否已经定义过同名的函数或结构体
    for (int i = 0; i < def_num; ++i) {
        if (strcmp(def[i].name, name) == 0) {
            // 错误处理，根据类型输出不同的错误信息
            int errorTypeCode = strcmp(type, "function") == 0 ? 4 : 15;
            const char *typeText = strcmp(type, "function") == 0 ? "function" : "structure";
            printf("Error type %d at Line %d: Redefined %s \"%s\".\n", errorTypeCode, lineno, typeText, name);
            return false;
        }
    }

    // 添加新的函数或结构体定义
    strcpy(def[def_num].name, name);
    if (strcmp(type, "function") == 0) {
        def[def_num].arg_num = 0; // 为函数初始化参数数量
    }
    def[def_num].dec_num = 0; // 初始化成员或局部变量数量
    def_num++; // 增加定义计数
    return true;
}

void build_func_and_struct_dec(char *name, char *dec_name, char *type) {
    // 查找并为特定的函数或结构体添加成员定义
    for (int i = 0; i < def_num; ++i) {
        if (strcmp(def[i].name, name) == 0) {
            strcpy(def[i].dec[def[i].dec_num].name, dec_name);
            strcpy(def[i].dec[def[i].dec_num].type, type);
            def[i].dec_num++; // 更新成员计数
            return;
        }
    }
}

char* find_id_type(char *name) {
    // 遍历变量表，查找匹配的变量类型
    for (int i = 0; i < dec_num; ++i) {
        if (strcmp(dec[i].name, name) == 0) {
            return dec[i].type; // 返回找到的变量类型
        }
    }
    return NULL; // 找不到时返回NULL
}

declare* find_func_or_struct_dec(char *name) {
    // 遍历定义列表，寻找匹配的函数或结构体
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, name) == 0) {
            return def[i].dec; // 找到后返回其声明数组
        }
    }
    return NULL; // 未找到返回NULL
}

char* find_func_return_type(char *name) {
    // 遍历定义列表，寻找匹配的函数
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, name) == 0) {
            return def[i].return_type; // 找到后返回其返回类型
        }
    }
    return NULL; // 未找到返回NULL
}

void add_struct_member(char *struct_name, char *member_name, char *member_type, int lineno) {
    // 遍历定义列表以查找指定的结构体
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, struct_name) == 0) {
            // 检查成员是否已经定义在结构体中
            for (int j = 0; j < def[i].dec_num; j++) {
                if (strcmp(def[i].dec[j].name, member_name) == 0) {
                    printf("Error type 15 at Line %d: Redefined field \"%s\".\n", lineno, member_name);
                    return; // 找到重复定义，报错并退出
                }
            }
            // 将新成员添加到结构体定义中
            strcpy(def[i].dec[def[i].dec_num].name, member_name);
            strcpy(def[i].dec[def[i].dec_num].type, member_type);
            def[i].dec_num++; // 更新成员数量
            return; // 成功添加后退出
        }
    }
}

void add_func_args(char *func_name, char *arg_name, char *arg_type, int lineno) {
    // 遍历定义列表以查找指定的函数
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, func_name) == 0) {
            // 检查参数是否已经定义在函数中
            for (int j = 0; j < def[i].arg_num; j++) {
                if (strcmp(def[i].args[j].name, arg_name) == 0) {
                    printf("Error type 3 at Line %d: Redefined variable \"%s\".\n", lineno, arg_name);
                    return; // 找到重复定义，报错并退出
                }
            }
            // 将新参数添加到函数定义中
            strcpy(def[i].args[def[i].arg_num].name, arg_name);
            strcpy(def[i].args[def[i].arg_num].type, arg_type);
            def[i].arg_num++; // 更新参数数量
            return; // 成功添加后退出
        }
    }
}

void add_func_variables(char *func_name, char *variable_name, char *variable_type, int lineno) {
    // 遍历已定义列表以查找指定函数
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, func_name) == 0) {
            // 在找到的函数中遍历检查是否存在同名变量
            for (int j = 0; j < def[i].dec_num; j++) {
                if (strcmp(def[i].dec[j].name, variable_name) == 0) {
                    printf("Error type 3 at Line %d: Redefined variable \"%s\".\n", lineno, variable_name);
                    return; // 发现重复定义，报错并退出
                }
            }
            // 若未发现重复定义，则添加新变量
            strcpy(def[i].dec[def[i].dec_num].name, variable_name);
            strcpy(def[i].dec[def[i].dec_num].type, variable_type);
            def[i].dec_num++; // 更新变量数量
            return; // 添加成功后退出
        }
    }
}

char* find_structure_member_type(char *struct_name, char *member_name) {
    // 遍历定义列表查找指定结构体
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, struct_name) == 0) {
            // 在找到的结构体中遍历检查是否存在指定成员
            for (int j = 0; j < def[i].dec_num; j++) {
                if (strcmp(def[i].dec[j].name, member_name) == 0) {
                    return def[i].dec[j].type; // 找到成员，返回其类型
                }
            }
            return NULL; // 指定成员不存在
        }
    }
    return NULL; // 指定结构体不存在
}

void set_func_return_type(char *name, char *type) {
    // 遍历已定义列表以查找指定函数
    for (int i = 0; i < def_num; i++) {
        if (strcmp(def[i].name, name) == 0) {
            strcpy(def[i].return_type, type); // 找到函数，设置返回类型
            return; // 设置成功后退出
        }
    }
}
