// T14【提高+/省选-】师徒大会
// 算法：倍增 LCA + 树上距离
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005, LOG = 17;
int dep[MAXN], up[MAXN][LOG];
vector<int> g[MAXN];

void dfs(int u, int fa) {
    up[u][0] = fa;
    for (int j = 1; j < LOG; j++) up[u][j] = up[up[u][j - 1]][j - 1];
    for (int v : g[u])
        if (v != fa) { dep[v] = dep[u] + 1; dfs(v, u); }
}

int lca(int x, int y) {
    if (dep[x] < dep[y]) swap(x, y);
    int d = dep[x] - dep[y];
    for (int j = LOG - 1; j >= 0; j--)
        if (d >> j & 1) x = up[x][j];
    if (x == y) return x;
    for (int j = LOG - 1; j >= 0; j--)
        if (up[x][j] != up[y][j]) { x = up[x][j]; y = up[y][j]; }
    return up[x][0];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    for (int i = 2; i <= n; i++) {
        int f;
        cin >> f;
        g[f].push_back(i);
        g[i].push_back(f);
    }
    dfs(1, 0);
    while (q--) {
        int x, y;
        cin >> x >> y;
        int c = lca(x, y);
        cout << dep[x] + dep[y] - 2 * dep[c] << "\n";
    }
    return 0;
}
