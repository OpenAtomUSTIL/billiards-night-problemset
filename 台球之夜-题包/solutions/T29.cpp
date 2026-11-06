// T29【NOI/NOI+/CTSC】变动的师门
// 算法：Link-Cut Tree，维护路径异或和
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;

int ch[MAXN][2], fa[MAXN], rev[MAXN];
long long val[MAXN], xr[MAXN];

bool isRoot(int x) {
    return ch[fa[x]][0] != x && ch[fa[x]][1] != x;
}

void pushup(int x) {
    xr[x] = xr[ch[x][0]] ^ val[x] ^ xr[ch[x][1]];
}

void pushrev(int x) {
    swap(ch[x][0], ch[x][1]);
    rev[x] ^= 1;
}

void pushdown(int x) {
    if (rev[x]) {
        if (ch[x][0]) pushrev(ch[x][0]);
        if (ch[x][1]) pushrev(ch[x][1]);
        rev[x] = 0;
    }
}

void pushAll(int x) {           // 自顶向下释放标记
    if (!isRoot(x)) pushAll(fa[x]);
    pushdown(x);
}

void rotate(int x) {
    int y = fa[x], z = fa[y];
    int dx = (ch[y][1] == x), dy = (ch[z][1] == y);
    if (!isRoot(y)) ch[z][dy] = x;
    fa[x] = z;
    ch[y][dx] = ch[x][dx ^ 1];
    if (ch[x][dx ^ 1]) fa[ch[x][dx ^ 1]] = y;
    ch[x][dx ^ 1] = y;
    fa[y] = x;
    pushup(y);
}

void splay(int x) {
    pushAll(x);
    while (!isRoot(x)) {
        int y = fa[x];
        if (!isRoot(y)) {
            bool zigzig = (ch[y][0] == x) == (ch[fa[y]][0] == y);
            rotate(zigzig ? y : x);
        }
        rotate(x);
    }
    pushup(x);
}

void access(int x) {
    for (int y = 0; x; y = x, x = fa[x]) {
        splay(x);
        ch[x][1] = y;
        pushup(x);
    }
}

void makeRoot(int x) {
    access(x);
    splay(x);
    pushrev(x);
}

int findRoot(int x) {
    access(x);
    splay(x);
    while (ch[x][0]) { pushdown(x); x = ch[x][0]; }
    splay(x);
    return x;
}

void link(int x, int y) {
    makeRoot(x);
    fa[x] = y;
}

void cut(int x, int y) {
    makeRoot(x);
    access(y);
    splay(y);
    // 此时 x 应为 y 的左孩子且 x 无右孩子
    if (ch[y][0] == x && !ch[x][1]) {
        ch[y][0] = 0;
        fa[x] = 0;
        pushup(y);
    }
}

void split(int x, int y) {      // 把 x-y 路径拉成以 y 为根的 splay
    makeRoot(x);
    access(y);
    splay(y);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> val[i];
        xr[i] = val[i];
    }
    while (m--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 0) {
            if (findRoot(x) != findRoot(y)) cout << -1 << "\n";
            else {
                split(x, y);
                cout << xr[y] << "\n";
            }
        } else if (op == 1) {
            if (findRoot(x) != findRoot(y)) link(x, y);
        } else if (op == 2) {
            cut(x, y);
        } else if (op == 3) {
            splay(x);
            val[x] = y;
            pushup(x);
        }
    }
    return 0;
}
