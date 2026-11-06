// T31【省选/NOI-】吉利台号
// 算法：数位 DP —— 统计 [0,x] 中不含数字 4 且不含连续子串 62 的整数个数
// 状态：dp[pos][pre6][lead][tight] 记忆化搜索（tight/lead 不记忆）
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

ll dp[20][2];                   // dp[余位][前一位是否为6]（仅在非 tight 非 lead 时记忆）
int dig[20];

ll dfs(int pos, bool pre6, bool tight, bool lead) {
    if (pos == 0) return 1;     // 全部填完，合法
    if (!tight && !lead && dp[pos][pre6] != -1) return dp[pos][pre6];
    int up = tight ? dig[pos] : 9;
    ll res = 0;
    for (int d = 0; d <= up; d++) {
        if (d == 4) continue;                    // 禁数字 4
        if (pre6 && d == 2) continue;            // 禁连续 62
        res += dfs(pos - 1, d == 6, tight && d == up, lead && d == 0);
    }
    if (!tight && !lead) dp[pos][pre6] = res;
    return res;
}

ll count(ll x) {                // [0, x] 中的合法整数个数
    if (x < 0) return 0;
    int len = 0;
    while (x) {
        dig[++len] = x % 10;
        x /= 10;
    }
    memset(dp, -1, sizeof dp);
    return dfs(len, false, true, true);
}

int main() {
    ll l, r;
    scanf("%lld %lld", &l, &r);
    printf("%lld\n", count(r) - count(l - 1));
    return 0;
}
