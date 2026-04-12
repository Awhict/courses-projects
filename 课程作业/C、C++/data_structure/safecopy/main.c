#include<stdio.h>
#include "safestrcpy.h"

int main()
{
    char dest[11];  // 目标缓冲区
    errno_t result;

    // 正常复制的示例
    const char *src_normal = "2022212387";
    result = strcpy_s(dest, sizeof(dest), src_normal);
    if (result == 0)
    {
        printf("正常复制成功, 目标缓冲区中为: %s\n", dest);
    }
    else
    {
        printf("正常复制失败, 错误码%d, 目标缓冲区中为: %s\n", result, dest);
    }

    // 源字符串太长导致截断的示例
    const char *src_too_long = "this is too long";
    result = strcpy_s(dest, sizeof(dest), src_too_long);
    if (result == ERANGE)
    {
        printf("字符串截断错误, 错误码%d, 目标缓冲区中为: %s\n", result, dest);
    }

    // 源字符串为空的示例
    result = strcpy_s(dest, sizeof(dest), NULL);
    if (result == EINVAL)
    {
        printf("无结尾字符串错误, 错误码%d, 目标缓冲区中为: %s\n", result, dest);
    }

    // 目标字符串为NULL的示例
    result = strcpy_s(NULL, sizeof(dest), src_normal);
    if (result == EINVAL)
    {
        printf("无界字符串复制错误, 错误码%d, 目标缓冲区中为: %s\n", result, dest);
    }

    // 缓冲区大小为1，差一错误的示例
    char small_dest[1];
    result = strcpy_s(small_dest, sizeof(small_dest), src_normal);
    if (result == ERANGE)
    {
        printf("差一错误, 错误码%d, 目标缓冲区中为: %s\n", result, dest);
    }

    return 0;
}
