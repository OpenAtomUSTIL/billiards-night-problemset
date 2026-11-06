// T22【省选/NOI-】球杆统计
// 算法：莫队 —— 区间不同元素个数
#include <bits/stdc++.h>
using namespace std;

struct Query { int l, r, idx, blk; };

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    int B = max(1, (int)(n / sqrt(m + 1)));
    vector<Query> qs(m);
    for (int i = 0; i < m; i++) {
        cin >> qs[i].l >> qs[i].r;
        qs[i].idx = i;
        qs[i].blk = qs[i].l / B;
    }
    sort(qs.begin(), qs.end(), [](const Query &x, const Query &y) {
        if (x.blk != y.blk) return x.blk < y.blk;
        return (x.blk & 1) ? x.r > y.r : x.r < y.r;   // 奇偶块优化
    });

    vector<int> cnt(1000005, 0), ans(m);
    int cur = 0;
    auto addPos = [&](int i) { if (++cnt[a[i]] == 1) cur++; };
    auto delPos = [&](int i) { if (--cnt[a[i]] == 0) cur--; };

    int l = 1, r = 0;
    for (auto &q : qs) {
        while (l > q.l) addPos(--l);
        while (r < q.r) addPos(++r);
        while (l < q.l) delPos(l++);
        while (r > q.r) delPos(r--);
        ans[q.idx] = cur;
    }
    for (int i = 0; i < m; i++) cout << ans[i] << "\n";
    return 0;
}
