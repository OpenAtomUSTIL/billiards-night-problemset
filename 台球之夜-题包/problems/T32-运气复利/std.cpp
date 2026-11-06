// T32【提高+/省选-】运气复利
// 算法：矩阵快速幂求斐波那契第 n 项（F1 = F2 = 1）
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const ll MOD = 1000000007;

struct Mat {
    ll a[2][2];
};

Mat mul(const Mat &x, const Mat &y) {
    Mat z = {};
    for (int i = 0; i < 2; i++)
        for (int k = 0; k < 2; k++)
            if (x.a[i][k])
                for (int j = 0; j < 2; j++)
                    z.a[i][j] = (z.a[i][j] + x.a[i][k] * y.a[k][j]) % MOD;
    return z;
}

Mat matPow(Mat base, ll e) {
    Mat res = {{{1, 0}, {0, 1}}};        // 单位矩阵
    while (e) {
        if (e & 1) res = mul(res, base);
        base = mul(base, base);
        e >>= 1;
    }
    return res;
}

int main() {
    ll n;
    scanf("%lld", &n);
    if (n <= 2) {
        printf("1\n");
        return 0;
    }
    // |F_n  |   |1 1|^(n-2)   |F_2|
    // |F_n-1| = |1 0|       * |F_1|
    Mat base = {{{1, 1}, {1, 0}}};
    Mat r = matPow(base, n - 2);
    printf("%lld\n", (r.a[0][0] + r.a[0][1]) % MOD);
    return 0;
}
