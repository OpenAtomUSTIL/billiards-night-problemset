// T8【普及-】朋友圈
// 算法：并查集（路径压缩 + 按秩合并）
#include <bits/stdc++.h>
using namespace std;

int fa[100005], rk_[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) fa[i] = i;
    while (m--) {
        int x, y;
        cin >> x >> y;
        x = find(x); y = find(y);
        if (x != y) {
            if (rk_[x] < rk_[y]) swap(x, y);
            fa[y] = x;
            if (rk_[x] == rk_[y]) rk_[x]++;
        }
    }
    while (q--) {
        int x, y;
        cin >> x >> y;
        cout << (find(x) == find(y) ? "Yes" : "No") << "\n";
    }
    return 0;
}
