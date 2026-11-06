// T6【省选/NOI-】香炉布防
// 算法：树形 DP —— 树上最小支配集（三状态）
// f[u][0]: u 放香炉；f[u][1]: u 不放但被某个直接徒弟笼罩；f[u][2]: u 不放，靠父亲笼罩
#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
int n;
vector<vector<int>> ch;
int f[100005][3];

void dfs(int u) {
    f[u][0] = 1;
    f[u][1] = 0;
    f[u][2] = 0;
    int extra = INF;            // 若没有任何孩子放香炉，强制一个孩子放的最小代价增量
    bool hasChildCenser = false;
    for (int v : ch[u]) {
        dfs(v);
        f[u][0] += min({f[v][0], f[v][1], f[v][2]});
        f[u][2] += min(f[v][0], f[v][1]);   // 孩子不能指望 u
        int best = min(f[v][0], f[v][1]);
        f[u][1] += best;
        if (f[v][0] <= f[v][1]) hasChildCenser = true; // 最优选择里孩子自己放了
        else extra = min(extra, f[v][0] - f[v][1]);    // 否则挑一个改成放
    }
    if (!ch[u].empty() && !hasChildCenser) {
        // f[u][1] 要求至少一个孩子放香炉
        f[u][1] = (extra >= INF) ? INF : f[u][1] + extra;
    }
    if (!ch[u].empty() && f[u][1] >= INF) f[u][1] = INF;
    if (ch[u].empty()) f[u][1] = INF;       // 叶子无法被徒弟笼罩
    // 三个状态都可能溢出保护
    for (int k = 0; k < 3; k++) f[u][k] = min(f[u][k], INF);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    ch.assign(n + 1, {});
    for (int i = 2; i <= n; i++) {
        int fa;
        cin >> fa;
        ch[fa].push_back(i);
    }
    dfs(1);
    cout << min(f[1][0], f[1][1]) << "\n";  // 根没有父亲，不能靠状态 2
    return 0;
}
