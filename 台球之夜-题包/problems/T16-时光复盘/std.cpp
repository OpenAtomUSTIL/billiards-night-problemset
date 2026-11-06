// T16【省选/NOI-】时光复盘
// 算法：可持久化线段树（主席树）求区间第 k 小
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int rt[MAXN], lc[MAXN * 22], rc[MAXN * 22], cnt[MAXN * 22], tot = 0;

int build(int l, int r) {
    int u = ++tot;
    cnt[u] = 0;
    if (l < r) {
        int mid = (l + r) >> 1;
        lc[u] = build(l, mid);
        rc[u] = build(mid + 1, r);
    }
    return u;
}

int update(int pre, int l, int r, int pos) {
    int u = ++tot;
    lc[u] = lc[pre]; rc[u] = rc[pre]; cnt[u] = cnt[pre] + 1;
    if (l < r) {
        int mid = (l + r) >> 1;
        if (pos <= mid) lc[u] = update(lc[pre], l, mid, pos);
        else rc[u] = update(rc[pre], mid + 1, r, pos);
    }
    return u;
}

// 在 rtR 与 rtL-1 两棵树的差上二分第 k 小
int query(int uL, int uR, int l, int r, int k) {
    if (l == r) return l;
    int mid = (l + r) >> 1;
    int leftCnt = cnt[lc[uR]] - cnt[lc[uL]];
    if (k <= leftCnt) return query(lc[uL], lc[uR], l, mid, k);
    return query(rc[uL], rc[uR], mid + 1, r, k - leftCnt);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(n);
    for (int i = 0; i < n; i++) { cin >> a[i]; b[i] = a[i]; }
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    int sz = b.size();

    rt[0] = build(1, sz);
    for (int i = 1; i <= n; i++) {
        int pos = lower_bound(b.begin(), b.end(), a[i - 1]) - b.begin() + 1;
        rt[i] = update(rt[i - 1], 1, sz, pos);
    }
    while (m--) {
        int l, r, k;
        cin >> l >> r >> k;
        int pos = query(rt[l - 1], rt[r], 1, sz, k);
        cout << b[pos - 1] << "\n";
    }
    return 0;
}
