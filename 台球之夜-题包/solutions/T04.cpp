// T4【普及+/提高】运气连击
// 算法：线性 DP —— 删除至多一个元素的最大子段和
// f0[i]：以 i 结尾、未删除的非空区间最大和
// f1[i]：以 i 结尾、已删除一个元素的非空区间最大和
// f1[i] = max(f1[i-1] + a[i], f0[i-1])   （此前已删 / 删除 a[i]）
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    const long long NEG = -(1LL << 60);
    vector<long long> f0(n + 1, NEG), f1(n + 1, NEG);
    long long ans = NEG;
    for (int i = 1; i <= n; i++) {
        f0[i] = max(f0[i - 1], 0LL) + a[i];      // 重新开始 or 接上
        if (i >= 2)
            f1[i] = max(f1[i - 1] + a[i], f0[i - 1]); // 删除 a[i] 需前面非空
        ans = max({ans, f0[i], f1[i]});
    }
    cout << ans << "\n";
    return 0;
}
