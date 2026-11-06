// T10【普及/提高-】牢大补给
// 算法：完全背包（恰好装满：dp[0]=0，其余为 -INF）
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, V;
    cin >> n >> V;
    const long long NEG = -(1LL << 60);
    vector<long long> dp(V + 1, NEG);
    dp[0] = 0;
    for (int i = 0; i < n; i++) {
        long long c, w;
        cin >> c >> w;
        for (int j = (int)c; j <= V; j++)   // 完全背包：正序枚举
            if (dp[j - c] != NEG)
                dp[j] = max(dp[j], dp[j - c] + w);
    }
    cout << dp[V] << "\n";
    return 0;
}
