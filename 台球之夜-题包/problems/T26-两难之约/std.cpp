// T26【省选/NOI-】两难之约
// 算法：2-SAT —— Tarjan 强连通分量（迭代实现，防爆栈）
// 变量 i 拆点：2*i 表示 x_i = 0（假），2*i+1 表示 x_i = 1（真）
// 约束 (i,a,j,b)：「x_i = a」-> 「x_j = b」，同时逆否「x_j = !b」->「x_i = !a」
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<vector<int>> g;
vector<int> dfn, low, comp, st;
vector<char> ins;
int dfc = 0, sccCnt = 0;

void tarjan(int s) {
    // 迭代 Tarjan
    vector<pair<int, int>> stk;   // (节点, 下一条边)
    stk.push_back({s, 0});
    dfn[s] = low[s] = ++dfc;
    st.push_back(s);
    ins[s] = 1;
    while (!stk.empty()) {
        int u = stk.back().first;
        int &i = stk.back().second;
        if (i < (int)g[u].size()) {
            int v = g[u][i++];
            if (!dfn[v]) {
                dfn[v] = low[v] = ++dfc;
                st.push_back(v);
                ins[v] = 1;
                stk.push_back({v, 0});
            } else if (ins[v]) low[u] = min(low[u], dfn[v]);
        } else {
            if (low[u] == dfn[u]) {
                sccCnt++;
                while (true) {
                    int v = st.back(); st.pop_back();
                    ins[v] = 0;
                    comp[v] = sccCnt;
                    if (v == u) break;
                }
            }
            stk.pop_back();
            if (!stk.empty())
                low[stk.back().first] = min(low[stk.back().first], low[u]);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    int N = 2 * n + 1;             // 节点编号 1..2n，0 号弃用
    g.assign(2 * n + 2, {});
    auto id = [&](int i, int val) { return 2 * i - 1 + val; }; // (i,0)->2i-1, (i,1)->2i
    for (int k = 0; k < m; k++) {
        int i, a, j, b;
        cin >> i >> a >> j >> b;
        g[id(i, a)].push_back(id(j, b));
        g[id(j, b ^ 1)].push_back(id(i, a ^ 1));
    }
    dfn.assign(2 * n + 2, 0);
    low.assign(2 * n + 2, 0);
    comp.assign(2 * n + 2, 0);
    ins.assign(2 * n + 2, 0);
    for (int v = 1; v <= 2 * n; v++)
        if (!dfn[v]) tarjan(v);
    for (int i = 1; i <= n; i++) {
        if (comp[id(i, 0)] == comp[id(i, 1)]) {
            cout << "IMPOSSIBLE\n";
            return 0;
        }
    }
    cout << "POSSIBLE\n";
    // Tarjan 的缩点编号是逆拓扑序：comp 越小越靠后
    // 取 x_i = (comp[id(i,1)] < comp[id(i,0)]) ? 1 : 0
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << " ";
        cout << (comp[id(i, 1)] < comp[id(i, 0)] ? 1 : 0);
    }
    cout << "\n";
    return 0;
}
