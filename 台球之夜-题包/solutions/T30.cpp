// T30【省选/NOI-】集齐七色球
// 算法：期望 DP（赠券收集问题）
// E[i] = 已集齐 i 种时还需的期望摸球次数
// E[n] = 0；E[i] = i/n * E[i] + (n-i)/n * E[i+1] + 1
// 整理得 E[i] = n/(n-i) + E[i+1]，答案 E[0] = Σ n/(n-i)
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    double E = 0;
    for (int i = 0; i < n; i++)
        E += (double)n / (n - i);
    printf("%.2f\n", E);
    return 0;
}
