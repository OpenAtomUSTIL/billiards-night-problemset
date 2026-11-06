// T5【提高+/省选-】批量焚香
// 算法：线段树 + 懒惰标记（区间加、区间乘、区间求和），经典「线段树 2」
// 标记合成：先乘后加。mul 标记会把已有 add 标记一起乘掉。
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int n, m;
ll P;  // 题面中的模数 p

struct SegTree {
    vector<ll> sum, mul, add;
    SegTree(int n) : sum(4 * n + 5), mul(4 * n + 5, 1), add(4 * n + 5, 0) {}

    void pushup(int p) { sum[p] = (sum[p << 1] + sum[p << 1 | 1]) % P; }

    void apply(int p, int l, int r, ll k, ll b) {
        // 本节点整体：先乘 k 再加 b
        sum[p] = (sum[p] * k % P + b % P * (r - l + 1) % P) % P;
        mul[p] = mul[p] * k % P;
        add[p] = (add[p] * k % P + b) % P;
    }

    void pushdown(int p, int l, int r) {
        if (mul[p] == 1 && add[p] == 0) return;
        int mid = (l + r) >> 1;
        apply(p << 1, l, mid, mul[p], add[p]);
        apply(p << 1 | 1, mid + 1, r, mul[p], add[p]);
        mul[p] = 1; add[p] = 0;
    }

    void build(int p, int l, int r, const vector<ll> &a) {
        if (l == r) { sum[p] = a[l] % P; return; }
        int mid = (l + r) >> 1;
        build(p << 1, l, mid, a);
        build(p << 1 | 1, mid + 1, r, a);
        pushup(p);
    }

    // type=1: 区间加 b（k=1）；type=2: 区间乘 k（b=0）
    void update(int p, int l, int r, int ql, int qr, ll k, ll b) {
        if (ql <= l && r <= qr) { apply(p, l, r, k, b); return; }
        pushdown(p, l, r);
        int mid = (l + r) >> 1;
        if (ql <= mid) update(p << 1, l, mid, ql, qr, k, b);
        if (qr > mid) update(p << 1 | 1, mid + 1, r, ql, qr, k, b);
        pushup(p);
    }

    ll query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return sum[p];
        pushdown(p, l, r);
        int mid = (l + r) >> 1;
        ll res = 0;
        if (ql <= mid) res = (res + query(p << 1, l, mid, ql, qr)) % P;
        if (qr > mid) res = (res + query(p << 1 | 1, mid + 1, r, ql, qr)) % P;
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m >> P;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    SegTree st(n);
    st.build(1, 1, n, a);
    while (m--) {
        int op, l, r;
        cin >> op >> l >> r;
        if (op == 1) {           // 区间加 x
            ll x; cin >> x;
            x = (x % P + P) % P; // x 可为负
            st.update(1, 1, n, l, r, 1, x);
        } else if (op == 2) {    // 区间乘 x
            ll x; cin >> x;
            st.update(1, 1, n, l, r, x % P, 0);
        } else {                 // 区间求和
            cout << st.query(1, 1, n, l, r) << "\n";
        }
    }
    return 0;
}
