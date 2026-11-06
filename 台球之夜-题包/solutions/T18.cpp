// T18【省选/NOI-】巡回敬杆
// 算法：状态压缩 DP（TSP）
// dp[mask][i]：从 0 号出发，已访问集合为 mask，当前位于 i 的最短路径
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<ll>> d(n, vector<ll>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> d[i][j];

    int full = 1 << n;
    const ll INF = (1LL << 62);
    vector<vector<ll>> dp(full, vector<ll>(n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < full; mask++) {
        if (!(mask & 1)) continue;              // 必须包含起点
        for (int i = 0; i < n; i++) {
            if (!(mask >> i & 1) || dp[mask][i] == INF) continue;
            for (int j = 0; j < n; j++) {
                if (mask >> j & 1) continue;
                int nmask = mask | (1 << j);
                dp[nmask][j] = min(dp[nmask][j], dp[mask][i] + d[i][j]);
            }
        }
    }
    ll ans = INF;
    for (int i = 0; i < n; i++)
        ans = min(ans, dp[full - 1][i] + d[i][0]); // 回到 1 号前台
    cout << ans << "\n";
    return 0;
}
