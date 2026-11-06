// T24【省选/NOI-】禁咒词库
// 算法：AC 自动机 —— 统计所有模式串在文本中的出现总次数
// 插入时令终止节点 cnt++；沿 fail 边反向传播后，扫描文本累加每个节点的 cnt。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000005;

int ch[MAXN][26], fail[MAXN], cnt[MAXN];
int tot = 0;

void insert(const string &s) {
    int u = 0;
    for (char c : s) {
        int v = c - 'a';
        if (!ch[u][v]) ch[u][v] = ++tot;
        u = ch[u][v];
    }
    cnt[u]++;
}

void build() {
    queue<int> q;
    for (int i = 0; i < 26; i++)
        if (ch[0][i]) q.push(ch[0][i]);     // fail 默认为 0
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int i = 0; i < 26; i++) {
            int v = ch[u][i];
            if (v) {
                fail[v] = ch[fail[u]][i];
                q.push(v);
            } else ch[u][i] = ch[fail[u]][i];  // 直接补全转移边（图化）
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;
        insert(s);
    }
    build();
    // 沿 fail 树自浅向深传播：cnt[u] 累加其 fail 链上祖先的模式数，
    // 这样扫描到节点 u 时 cnt[u] 即为「以当前位置结尾的禁咒个数」
    vector<int> order;
    {
        vector<vector<int>> tree(tot + 1);
        for (int i = 1; i <= tot; i++) tree[fail[i]].push_back(i);
        queue<int> q;
        q.push(0);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (int v : tree[u]) q.push(v);
        }
    }
    for (int i = 1; i < (int)order.size(); i++)
        cnt[order[i]] += cnt[fail[order[i]]];

    string T;
    cin >> T;
    long long ans = 0;
    int u = 0;
    for (char c : T) {
        u = ch[u][c - 'a'];
        ans += cnt[u];
    }
    cout << ans << "\n";
    return 0;
}
