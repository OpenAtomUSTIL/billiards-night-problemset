// T12【普及+/提高】运气衰减之谜
// 算法：离散化 + 树状数组求逆序对
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int n;
vector<int> bit;
void add(int i, int v) { for (; i <= (int)bit.size() - 1; i += i & -i) bit[i] += v; }
int ask(int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    vector<ll> a(n), b(n);
    for (int i = 0; i < n; i++) { cin >> a[i]; b[i] = a[i]; }
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    bit.assign(b.size() + 2, 0);

    ll ans = 0;
    for (int i = 0; i < n; i++) {
        int r = lower_bound(b.begin(), b.end(), a[i]) - b.begin() + 1;
        // 之前出现过的数中比 a[i] 大的个数 = 已插入总数 - <=a[i] 的个数
        ans += i - ask(r);
        add(r, 1);
    }
    cout << ans << "\n";
    return 0;
}
