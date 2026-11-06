// T20【NOI/NOI+/CTSC】屠龙之杆
// 算法：NTT（模 998244353，原根 3）求多项式乘积
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const ll MOD = 998244353, G = 3;

ll modPow(ll a, ll b) {
    ll r = 1;
    while (b) {
        if (b & 1) r = r * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return r;
}

void ntt(vector<ll> &a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {          // 位逆序置换
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        ll wn = modPow(G, (MOD - 1) / len);
        if (invert) wn = modPow(wn, MOD - 2);
        for (int i = 0; i < n; i += len) {
            ll w = 1;
            for (int j = 0; j < len / 2; j++) {
                ll u = a[i + j], v = a[i + j + len / 2] * w % MOD;
                a[i + j] = (u + v) % MOD;
                a[i + j + len / 2] = (u - v + MOD) % MOD;
                w = w * wn % MOD;
            }
        }
    }
    if (invert) {
        ll inv = modPow(n, MOD - 2);
        for (auto &x : a) x = x * inv % MOD;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<ll> A(n + 1), B(m + 1);
    for (auto &x : A) cin >> x;
    for (auto &x : B) cin >> x;

    int sz = 1;
    while (sz < n + m + 1) sz <<= 1;
    A.resize(sz); B.resize(sz);

    ntt(A, false);
    ntt(B, false);
    for (int i = 0; i < sz; i++) A[i] = A[i] * B[i] % MOD;
    ntt(A, true);

    for (int i = 0; i <= n + m; i++) {
        if (i) cout << " ";
        cout << A[i];
    }
    cout << "\n";
    return 0;
}
