// T13【提高+/省选-】幸运数字
// 算法：0-1 字典树求最大异或对
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int ch[3200005][2], tot = 0;

void insert(ll x) {
    int u = 0;
    for (int i = 31; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (!ch[u][b]) ch[u][b] = ++tot;
        u = ch[u][b];
    }
}

ll query(ll x) {
    int u = 0;
    ll res = 0;
    for (int i = 31; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (ch[u][b ^ 1]) {          // 优先走相反位，异或出 1
            res |= (1LL << i);
            u = ch[u][b ^ 1];
        } else u = ch[u][b];
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    ll ans = 0;
    insert(a[0]);
    for (int i = 1; i < n; i++) {
        ans = max(ans, query(a[i]));
        insert(a[i]);
    }
    cout << ans << "\n";
    return 0;
}
