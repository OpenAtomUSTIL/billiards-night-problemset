// T25【省选/NOI-】香味分配
// 算法：最小费用最大流（SPFA 版 SSP，n<=100 足够快）
// 建模：源->朋友（容量1费用0），朋友i->桌j（容量1费用c_ij），桌->汇（容量1费用0）
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct MCMF {
    struct Edge { int to, rev; ll cap, cost; };
    int n;
    vector<vector<Edge>> g;
    MCMF(int n) : n(n), g(n + 1) {}

    void addEdge(int u, int v, ll cap, ll cost) {
        g[u].push_back({v, (int)g[v].size(), cap, cost});
        g[v].push_back({u, (int)g[u].size() - 1, 0, -cost});
    }

    // 返回 {flow, cost}
    pair<ll, ll> minCostMaxFlow(int s, int t) {
        ll flow = 0, cost = 0;
        vector<ll> dis(n + 1);
        vector<int> pre(n + 1), pe(n + 1);
        vector<char> inq(n + 1);
        const ll INF = (1LL << 62);
        while (true) {
            fill(dis.begin(), dis.end(), INF);
            fill(inq.begin(), inq.end(), 0);
            dis[s] = 0;
            queue<int> q;
            q.push(s);
            while (!q.empty()) {
                int u = q.front(); q.pop();
                inq[u] = 0;
                for (int i = 0; i < (int)g[u].size(); i++) {
                    Edge &e = g[u][i];
                    if (e.cap > 0 && dis[u] + e.cost < dis[e.to]) {
                        dis[e.to] = dis[u] + e.cost;
                        pre[e.to] = u;
                        pe[e.to] = i;
                        if (!inq[e.to]) { inq[e.to] = 1; q.push(e.to); }
                    }
                }
            }
            if (dis[t] == INF) break;
            ll f = INF;
            for (int v = t; v != s; v = pre[v])
                f = min(f, g[pre[v]][pe[v]].cap);
            for (int v = t; v != s; v = pre[v]) {
                Edge &e = g[pre[v]][pe[v]];
                e.cap -= f;
                g[v][e.rev].cap += f;
            }
            flow += f;
            cost += f * dis[t];
        }
        return {flow, cost};
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    int S = 2 * n + 1, T = 2 * n + 2;
    MCMF mf(2 * n + 2);
    vector<vector<ll>> c(n + 1, vector<ll>(n + 1));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) cin >> c[i][j];
    for (int i = 1; i <= n; i++) {
        mf.addEdge(S, i, 1, 0);
        mf.addEdge(n + i, T, 1, 0);
        for (int j = 1; j <= n; j++)
            mf.addEdge(i, n + j, 1, c[i][j]);
    }
    auto [flow, cost] = mf.minCostMaxFlow(S, T);
    cout << cost << "\n";    // 保证有完美分配
    return 0;
}
