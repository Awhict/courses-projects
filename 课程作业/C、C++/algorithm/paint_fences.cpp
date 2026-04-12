#include <cstdio>
#include <algorithm>
#include <cstring>
using namespace std;

int a[5000]; // 定义一个数组存储栅栏的高度信息

/**
 * 递归函数 dfs 用于计算区间 [l, r] 内粉刷栅栏的最少次数。
 * @param l 当前处理区间的左端点索引
 * @param r 当前处理区间的右端点索引
 * @param k 当前已粉刷的最低高度
 * @return 返回粉刷区间 [l, r] 的最少粉刷次数
 */
int dfs(int l, int r, int k) {
    // 若区间无效或当前区间的栅栏高度都已小于等于 k，返回 0 次粉刷
    if (l > r || (l == r && a[l] <= k)) return 0;
    
    // 若区间只有一个栅栏且其高度大于 k，则需要一次粉刷
    if (l == r) return 1;
    
    // 找到当前区间内未粉刷部分的最小高度位置
    int mn = min_element(a + l, a + r + 1) - a;
    
    // 比较直接粉刷整个区间与粉刷至最低高度 mn 后再递归处理其两侧部分的次数
    return min(r - l + 1, dfs(l, mn - 1, a[mn]) + dfs(mn + 1, r, a[mn]) + a[mn] - k);
}

int main() {
    int n; // 栅栏数量
    while (scanf("%d", &n) != EOF) { // 输入处理，直到文件结束符 EOF
        memset(a, 0, sizeof(a)); // 初始化数组，确保无残留数据
        for (int i = 0; i < n; i++)
            scanf("%d", &a[i]); // 读入每个栅栏的高度
        printf("%d\n", dfs(0, n - 1, 0)); // 计算并输出粉刷的最少次数
        printf("----------------------\n"); // 分割线
    }
    return 0;
}
