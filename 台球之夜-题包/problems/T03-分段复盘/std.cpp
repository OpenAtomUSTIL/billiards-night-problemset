// T3【普及/提高-】分段复盘
// 算法：二分答案 + 贪心判定（数列分段）
// 二分最大段和 T，贪心从左到右累加，超 T 就开新段，统计段数是否 <= m
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<long long> a;

bool check(long long T) {          // 段和上限为 T 时至少需要几段
    int cnt = 1;
    long long cur = 0;
    for (int i = 0; i < n; i++) {
        if (cur + a[i] <= T) cur += a[i];
        else { cnt++; cur = a[i]; }
    }
    return cnt <= m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    a.resize(n);
    long long lo = 0, hi = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        lo = max(lo, a[i]);        // 每段非空，T 至少为最大单元素
        hi += a[i];
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    cout << lo << "\n";
    return 0;
}
