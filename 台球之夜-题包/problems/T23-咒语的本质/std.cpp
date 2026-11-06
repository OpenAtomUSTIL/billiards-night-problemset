// T23【NOI/NOI+/CTSC】咒语的本质
// 算法：后缀自动机（SAM）—— 本质不同子串个数 = Σ (len[u] - len[link[u]])
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const int MAXN = 1000005;

struct SAM {
    int ch[MAXN * 2][26];
    int link[MAXN * 2], len[MAXN * 2];
    int last, tot;
    void init() {
        last = tot = 1;
        memset(ch[1], 0, sizeof ch[1]);
        link[1] = 0; len[1] = 0;
    }
    void extend(int c) {
        int p = last, np = last = ++tot;
        len[np] = len[p] + 1;
        memset(ch[np], 0, sizeof ch[np]);
        for (; p && !ch[p][c]; p = link[p]) ch[p][c] = np;
        if (!p) { link[np] = 1; return; }
        int q = ch[p][c];
        if (len[q] == len[p] + 1) { link[np] = q; return; }
        int nq = ++tot;
        len[nq] = len[p] + 1;
        memcpy(ch[nq], ch[q], sizeof ch[q]);
        link[nq] = link[q];
        link[q] = link[np] = nq;
        for (; p && ch[p][c] == q; p = link[p]) ch[p][c] = nq;
    }
} sam;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    sam.init();
    for (char c : s) sam.extend(c - 'a');
    ll ans = 0;
    for (int i = 2; i <= sam.tot; i++)
        ans += sam.len[i] - sam.len[sam.link[i]];
    cout << ans << "\n";
    return 0;
}
