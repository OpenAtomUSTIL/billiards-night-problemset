// T27【NOI/NOI+/CTSC】树上有约
// 算法：点分治 —— 离线回答「是否存在距离恰好为 k 的点对」
// 经典套路：以重心为界，统计「跨重心」路径，
// 用 exist[d] 记录已处理子树中出现过的（到重心的）距离。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 10005;
const int MAXK = 10000005;

int n, m;
vector<pair<int, int>> g[MAXN];   // (to, w)
int qs[105];                      // 询问的 k
bool ans[105];
bool exist[MAXK];                 // 距离 d 是否出现过
int stk[MAXN], top;               // 暂存当前子树的距离，便于清空
int sz[MAXN], maxSon[MAXN], root, sum;
bool vis[MAXN];
vector<int> alld;                 // 当前重心下所有子树距离全集（用于清空 exist）

void getRoot(int u, int fa) {
    sz[u] = 1;
    maxSon[u] = 0;
    for (auto [v, w] : g[u]) {
        if (v == fa || vis[v]) continue;
        getRoot(v, u);
        sz[u] += sz[v];
        maxSon[u] = max(maxSon[u], sz[v]);
    }
    maxSon[u] = max(maxSon[u], sum - sz[u]);
    if (maxSon[u] < maxSon[root]) root = u;
}

void getDis(int u, int fa, int d, vector<int> &ds) {
    ds.push_back(d);
    for (auto [v, w] : g[u]) {
        if (v == fa || vis[v]) continue;
        getDis(v, u, d + w, ds);
    }
}

void solve(int u) {
    vis[u] = true;
    exist[0] = true;
    alld.clear();
    alld.push_back(0);
    for (auto [v, w] : g[u]) {
        if (vis[v]) continue;
        vector<int> ds;
        getDis(v, u, w, ds);
        // 先用已有 exist 回答询问（保证点对跨子树，不重复）
        for (int d : ds) {
            if (d > 10000000) continue;
            for (int i = 0; i < m; i++) {
                if (ans[i]) continue;
                if (qs[i] >= d && qs[i] - d <= 10000000 && exist[qs[i] - d])
                    ans[i] = true;
            }
        }
        // 再把本子树距离加入 exist
        for (int d : ds) {
            if (d <= 10000000 && !exist[d]) {
                exist[d] = true;
                alld.push_back(d);
            }
        }
    }
    // 清空 exist
    for (int d : alld) exist[d] = false;

    for (auto [v, w] : g[u]) {
        if (vis[v]) continue;
        sum = sz[v];
        root = 0;
        getRoot(v, u);
        solve(root);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    for (int i = 1; i < n; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    for (int i = 0; i < m; i++) cin >> qs[i];
    sum = n;
    root = 0;
    maxSon[0] = n + 1;
    getRoot(1, 0);
    solve(root);
    for (int i = 0; i < m; i++)
        cout << (ans[i] ? "AYE" : "NAY") << "\n";
    return 0;
}
