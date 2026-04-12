#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <errno.h>

#define SUCCESS 0
#define BUFFER_OVERFLOW -1
#define NULL_POINTER -2
#define INVALID_FORMAT -3

int snprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...) {
    if (!buffer || sizeOfBuffer == 0) {
        return NULL_POINTER; // 缓冲区为空或大小为0
    }

    if (!format) {
        return INVALID_FORMAT; // 格式字符串为空
    }

    va_list args;
    va_start(args, format);

    // 使用 vsnprintf 实现变参处理和缓冲区大小控制
    int written = vsnprintf(buffer, sizeOfBuffer, format, args);

    va_end(args);

    // 检查 vsnprintf 的返回值
    if (written < 0) {
        return INVALID_FORMAT; // 格式化错误
    } else if ((size_t)written >= sizeOfBuffer) {
        buffer[sizeOfBuffer - 1] = '\0'; // 确保字符串以 \0 结尾
        return BUFFER_OVERFLOW;         // 缓冲区溢出
    }

    return SUCCESS; // 格式化成功
}

int main() {
    char buffer[16];

    // 测试1：正常使用
    if (snprintf_s(buffer, sizeof(buffer), "Hello, %s!", "World") == SUCCESS) {
        printf("Test 1 Passed: %s\n", buffer);
    } else {
        printf("Test 1 Failed\n");
    }

    // 测试2：缓冲区溢出
    if (snprintf_s(buffer, sizeof(buffer), "This is a very long string %s", "Overflow") == BUFFER_OVERFLOW) {
        printf("Test 2 Passed: %s\n", buffer);
    } else {
        printf("Test 2 Failed\n");
    }

    // 测试3：格式字符串为空
    if (snprintf_s(buffer, sizeof(buffer), NULL) == INVALID_FORMAT) {
        printf("Test 3 Passed\n");
    } else {
        printf("Test 3 Failed\n");
    }

    // 测试4：缓冲区为空
    if (snprintf_s(NULL, sizeof(buffer), "Test") == NULL_POINTER) {
        printf("Test 4 Passed\n");
    } else {
        printf("Test 4 Failed\n");
    }

    // 测试5：栈内容访问尝试（检测 %n 攻击）
    const char *exploit_format = "%s%n";
    if (snprintf_s(buffer, sizeof(buffer), exploit_format, "Test") == INVALID_FORMAT) {
        printf("Test 5 Passed\n");
    } else {
        printf("Test 5 Failed\n");
    }

    return 0;
}
