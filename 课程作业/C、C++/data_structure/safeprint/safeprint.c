#include <stdio.h>
#include <stdarg.h>
#include <string.h>


int safe_sprintf(char* buffer, size_t sizeOfBuffer, const char* format, ...) {
	if (buffer == NULL || sizeOfBuffer == 0) {
		// 参数无效
		return -1;
	}

	va_list args;
	va_start(args, format);
	size_t i = 0;  // 记录写入字符的位置

	while (*format != '\0') {
		// 处理格式化字符串中的普通字符
		if (*format != '%' && i < sizeOfBuffer - 1) {
			buffer[i++] = *format;
		}
		else if (*format == '%' && *(format + 1) == 's') 
		{

			// 处理 %s 格式符
			const char* str = va_arg(args, const char*);
			size_t len = 0;
			// 计算字符串长度
			if (str == "-1") {
				//参数不匹配
				va_end(args);
				return -1;
			}
			while (str[len] != '\0') {
				len++;
			}
			if (i + len < sizeOfBuffer) {
				// 复制字符串到缓冲区
				size_t j;
				for (j = 0; j < len; j++) {
					buffer[i + j] = str[j];
				}
				i += len;
			}
			else {
				// 缓冲区不足
				va_end(args);
				return -1;
			}


			// 判断是否能容纳整个字符串


			// 移动 format 指针到 %s 后面
			format += 1;
		}
		else if (*format == '%' && *(format + 1) == 'd')
		{
			// 处理 %d 格式符
			long int num = va_arg(args, long int);

			// 分配足够的内存来存储整数的字符串表示
			char str[200];  // 调整大小以适应你的需要
			sprintf_s(str, sizeof(str), " %d", num);

			// 检查参数是否匹配
			if (str=="-1") {
				// 参数不匹配
				va_end(args);
				return -1;
			}

			// 计算字符串长度
			size_t len = strlen(str);

			// 判断是否能容纳整个字符串
			if (i + len < sizeOfBuffer) {
				// 复制字符串到缓冲区
				size_t j;
				for (j = 0; j < len; j++) {
					buffer[i + j] = str[j];
				}
				i += len;
			}
			else {
				// 缓冲区不足
				va_end(args);
				return -1;
			}

			format += 1;
		}

		else {
			// 未知的格式化符号
			va_end(args);
			return -1;
		}

		++format;
	}

	// 在字符串末尾添加终止符
	if (i < sizeOfBuffer) {
		buffer[i] = '\0';
	}
	else {
		// 缓冲区不足
		va_end(args);
		return -1;
	}

	va_end(args);

	return i;  // 返回写入字符的数量（不包括终止符）
}

int main() {
	char buffer[20];
	printf("Normal output example:\n");
	int result = safe_sprintf(buffer, sizeof(buffer), "Hello, %s%d!", "world", 1111, "-1");		//正常输出

	if (result >= 0) {
		printf("Formatted string: %s\n", buffer);
	}
	else {
		printf("Error occurred: %d\n", result);
	}

	printf("Example of Scalable Buffer:\n");
	result = safe_sprintf(buffer, sizeof(buffer), "Helloooooooooooooooooooooooooooooooooooooooo, %s%d!", "world", 11111, "-1");	
	if (result >= 0) {
		printf("Formatted string: %s\n", buffer);
	}
	else {
		printf("Error occurred: %d\n", result);
	}

	printf("Example of viewing stack content:\n");
	result = safe_sprintf(buffer, sizeof(buffer), "Hello, %s%d%s%s%s!", "world", 11111, "-1");
	if (result >= 0) {
		printf("Formatted string: %s\n", buffer);
	}
	else {
		printf("Error occurred: %d\n", result);
	}

	printf("Memory Overwrite Example:\n");
	result = safe_sprintf(buffer, sizeof(buffer), "Hello, %s%d%s!", "world", 11111, "Memory Overwrite Memory Overwrite Memory Overwrite", "-1");
	if (result >= 0) {
		printf("Formatted string: %s\n", buffer);
	}
	else {
		printf("Error occurred: %d\n", result);
	}
	return 0;
}
