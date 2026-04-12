#include "safestrcpy.h"

//strcpy_s函数的实现
errno_t strcpy_s(char *_DEST, size_t _SIZE, const char *_SRC)//_SIZE为需要传入目的地址的可用长度，即_DEST的可用长度
{
    char *p;
    size_t available;

    if (!(_DEST != NULL && _SIZE > 0))//判断目标字符串是否不空且缓冲区可用空间大于0
    {
        errno = EINVAL;//提供报错信息：无效参数
        //printf("目标字符串为空且缓冲区可用空间为0！");
        return EINVAL;
    }
    if (_SRC == NULL)//判断源字符串是否为空
    {
        *_DEST = 0;//若为真，则将目标字符串的首个字符赋值为'0'
        fill_string(_DEST, _SIZE, 1);//将后续字符填充为安全字符
        errno = EINVAL;//提供报错信息：无效参数
        //printf("源字符串为空！");
        return EINVAL;
    }

    p = _DEST;
    available = _SIZE;
    while ((*p++ = *_SRC++) != 0 && --available > 0)//逐字符拷贝，直到拷贝到'0'，或者available为0即缓冲区为0
    {
    }

    if (available == 0)//若上面的循环因缓冲区为空而终止
    {
        *_DEST = 0;//重置目标字符串
        fill_string(_DEST, _SIZE, 1);
        errno = ERANGE;//提供报错信息：范围错误
        //printf("源字符串长度超过缓冲区大小！");
        return ERANGE;
    }
    fill_string(_DEST, _SIZE, _SIZE - available + 1);//将后续字符填充为安全字符
    //printf("正常拷贝成功！");
    return 0;
}

inline void fill_string(char *string, size_t size, size_t offset)
{
#ifdef _DEBUG
    if (offset < size)
    {
        //将字符串string的后续size - offset个字符填充为安全字符0xFE
        memset(string + offset, 0xFE, (size - offset) * sizeof(char));
    }
#else
    // do nothing
    ;
#endif
}
