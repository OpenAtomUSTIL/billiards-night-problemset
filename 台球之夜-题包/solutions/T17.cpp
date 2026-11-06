// T17【省选/NOI-】球厅人流
// 算法：Dinic 最大流（当前弧优化）
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct Dinic {
    struct Edge { int to, rev; ll cap; };
    int n, s, t;
    vector<vector<Edge>> g;
    vector<int> level, it;
    Dinic(int n, int s, int t) : n(n), s(s), t(t), g(n + 1), level(n + 1), it(n + 1) {}

    void addEdge(int u, int v, ll c) {
        g[u].push_back({v, (int)g[v].size(), c});
        g[v].push_back({u, (int)g[u].size() - 1, 0});
    }

    bool bfs() {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto &e : g[u])
                if (e.cap > 0 && level[e.to] < 0) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
        }
        return level[t] >= 0;
    }

    ll dfs(int u, ll f) {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)g[u].size(); i++) {
            Edge &e = g[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                ll d = dfs(e.to, min(f, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    g[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    ll maxFlow() {
        ll flow = 0;
        while (bfs()) {
            fill(it.begin(), it.end(), 0);
            ll f;
            while ((f = dfs(s, LLONG_MAX)) > 0) flow += f;
        }
        return flow;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    Dinic din(n, 1, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        ll c;
        cin >> u >> v >> c;
        din.addEdge(u, v, c);
    }
    cout << din.maxFlow() << "\n";
    return 0;
}
