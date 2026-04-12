#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

typedef long long ll; // 定义 ll 为 long long 类型的别名，方便表示大整数

ll a[1001] = {}, b[1001] = {}; // 定义时间数组a与编号数组b

// 冒泡排序函数
void bubblesort(ll a[], ll b[], int n) {
    int t; // 临时变量t
    for (int i = 1; i <= n - 1; i++) {
        for (int j = 1; j <= n - i; j++) {
            if (a[j] > a[j + 1]) { // 如果前一个人的时间比后一个人的时间长
                t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; // 交换
                t = b[j]; b[j] = b[j + 1]; b[j + 1] = t; // 同理
            }
        }
    }
}

int main() {
    int n; // 用于存储排队人数
    // 使用 `while` 循环持续读取输入，直到文件结束符 EOF
    while (scanf("%d", &n) != EOF) { 
        // 初始化数组 a 和 b，确保之前的数据不会对本次计算产生影响
        memset(a, 0, sizeof(a)); 
        memset(b, 0, sizeof(b));

        int i, j;
        double sum = 0;
        for (i = 1; i <= n; i++) {
            scanf("%lld", &a[i]); // a数组记录时间
            b[i] = i; // b数组记录编号
        }

        // 调用冒泡排序函数
        bubblesort(a, b, n);

        double num = 0;
        for (i = 1; i <= n; i++) {
            num = 0;
            for (j = i - 1; j >= 1; j--) {
                num += a[j]; // 累加等待时间
            }
            sum += num;
        }
        // 输出使得平均等待时间最小的编号顺序
        // for(i = 1; i <= n; i++)
        // {
        //     printf("%lld", b[i]);
        // }

        // 输出平均等待时间
        printf("%.1f\n", sum / n);

        printf("----------------------\n");
    }
    return 0;
}
