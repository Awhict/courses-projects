#ifndef _safestrcpy_h_
#define _safestrcpy_h_

#include<string.h>
#include<errno.h>

//声明在debug模式下会运行的fill_string函数
void fill_string(char *string, size_t size, size_t offset);

//声明strcpy_s函数
errno_t strcpy_s(char *_DEST, size_t _SIZE, const char *_SRC);

#endif

