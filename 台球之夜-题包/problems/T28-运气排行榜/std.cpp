// T28【提高+/省选-】运气排行榜
// 算法：FHQ-Treap（无旋平衡树），维护多重集
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int val, sz, cnt;          // cnt：该值重复次数
    unsigned pri;
    int l, r;
} tr[100005];
int tot = 0, root = 0;

mt19937 rng(20261105);

int newNode(int v) {
    tr[++tot] = {v, 1, 1, rng(), 0, 0};
    return tot;
}

void pushup(int u) {
    tr[u].sz = tr[u].cnt + tr[tr[u].l].sz + tr[tr[u].r].sz;
}

// 按值分裂：<= v 的进 a，> v 的进 b
void split(int u, int v, int &a, int &b) {
    if (!u) { a = b = 0; return; }
    if (tr[u].val <= v) {
        a = u;
        split(tr[u].r, v, tr[u].r, b);
    } else {
        b = u;
        split(tr[u].l, v, a, tr[u].l);
    }
    pushup(u);
}

int merge(int a, int b) {
    if (!a || !b) return a | b;
    if (tr[a].pri < tr[b].pri) {
        tr[a].r = merge(tr[a].r, b);
        pushup(a);
        return a;
    } else {
        tr[b].l = merge(a, tr[b].l);
        pushup(b);
        return b;
    }
}

void insert(int v) {
    int a, b, c;
    split(root, v, a, b);
    split(a, v - 1, a, c);
    if (c) {                    // 已存在该值
        tr[c].cnt++;
        tr[c].sz++;
    } else c = newNode(v);
    root = merge(merge(a, c), b);
}

void erase(int v) {
    int a, b, c;
    split(root, v, a, b);
    split(a, v - 1, a, c);
    if (c) {
        tr[c].cnt--;
        tr[c].sz--;
        if (tr[c].cnt == 0) c = merge(tr[c].l, tr[c].r);  // 删空则摘除
    }
    root = merge(merge(a, c), b);
}

int getRank(int v) {            // 比 v 小的数的个数 + 1
    int a, b;
    split(root, v - 1, a, b);
    int res = tr[a].sz + 1;
    root = merge(a, b);
    return res;
}

int kth(int u, int k) {
    while (u) {
        int ls = tr[tr[u].l].sz;
        if (k <= ls) u = tr[u].l;
        else if (k <= ls + tr[u].cnt) return tr[u].val;
        else { k -= ls + tr[u].cnt; u = tr[u].r; }
    }
    return -1;
}

int pre(int v) {
    int a, b;
    split(root, v - 1, a, b);
    int res = kth(a, tr[a].sz); // <= v-1 中的最大者
    root = merge(a, b);
    return res;
}

int suc(int v) {
    int a, b;
    split(root, v, a, b);
    int res = kth(b, 1);        // > v 中的最小者
    root = merge(a, b);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    while (n--) {
        int op, x;
        cin >> op >> x;
        switch (op) {
            case 1: insert(x); break;
            case 2: erase(x); break;
            case 3: cout << getRank(x) << "\n"; break;
            case 4: cout << kth(root, x) << "\n"; break;
            case 5: cout << pre(x) << "\n"; break;
            case 6: cout << suc(x) << "\n"; break;
        }
    }
    return 0;
}
