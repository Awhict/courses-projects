#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

#define N 105 // 定义数组的最大大小

typedef long long ll; // 定义 ll 为 long long 类型的别名，方便表示大整数

ll a[N][N], dp[N][N]; // 定义二维数组 a 和 dp，用于存储三角形数据和动态规划的中间结果

// 动态规划函数：计算从顶部到底部的最大路径和
ll getMaxPathSum(int n) {
    // 从三角形的底部开始向上计算
    for (int i = n; i >= 1; --i) { // 遍历每一行，从底部第 n 行到顶部第 1 行
        for (int j = 1; j <= i; ++j) { // 遍历每一行的所有元素
            // 当前元素的最大路径和等于当前值加上下一行两个可能路径的最大值
            dp[i][j] = a[i][j] + max(dp[i + 1][j], dp[i + 1][j + 1]);
        }
    }
    return dp[1][1]; // 返回从顶部开始的最大路径和
}

int main() {
    int n; // 用于存储三角形的行数
    // 使用 `while` 循环持续读取输入，直到文件结束符 EOF
    while (scanf("%d", &n) != EOF) { 
        // 初始化数组 a 和 dp，确保之前的数据不会对本次计算产生影响
        memset(a, 0, sizeof(a)); 
        memset(dp, 0, sizeof(dp)); 
        
        // 输入三角形的数据
        for (int i = 1; i <= n; ++i) { // 遍历每一行
            for (int j = 1; j <= i; ++j) { // 遍历当前行中的所有元素
                scanf("%lld", &a[i][j]); // 输入元素的值
            }
        }
        
        // 调用动态规划函数计算最大路径和，并输出结果
        printf("%lld\n", getMaxPathSum(n));
        
        printf("----------------------\n");
    }
    return 0; // 程序结束
}
