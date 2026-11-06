// T7【NOI/NOI+/CTSC】黑八的轨迹
// 算法：镜像展开 + 数学计数（二分第 k 早的碰库时刻）+ 有理数取模
//
// 展开平面中球做匀速直线运动。
// 碰左右库 <=> x 到达 W 的整数倍；碰上下库 <=> y 到达 H 的整数倍。
// 设 L = lcm(|vx|, |vy|)（分量为 0 时特殊处理），所有碰库时刻乘以 L 后都是整数，
// 即「缩放时间」U = t * L。
//
// x 方向在时刻 t 前的碰库次数（vx > 0 时）：
//   cnt_x(T) = floor((x0 + vx*T) / W) - floor(x0 / W)
// 对 vx < 0 用绝对值形式即可（单调下降，取差值的绝对值）。
//
// 二分最小的整数 U 使 cnt_x + cnt_y >= k，再判定该时刻碰的是哪条库，
// 把展开坐标折返回 [0,W]x[0,H]，有理数分子分母分别对 1e9+7 取模输出。
//
// 注意：题目保证永不同时碰两条库（不进袋口），故第 k 早时刻唯一对应一条库。

#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 i128;

const ll MOD = 1000000007;

ll W, H, x0, y0, vx, vy, k;

ll gcdll(ll a, ll b) { return b ? gcdll(b, a % b) : a; }

// 向下取整除法（支持负数）
i128 floorDiv(i128 a, i128 b) {          // b > 0
    if (a >= 0) return a / b;
    return -((-a + b - 1) / b);
}

// x 方向在缩放时间 U 内（不含 t=0）的碰库次数
// 负方向先镜像（x0' = W - x0, vx' = -vx），保证边界事件计数端点正确
i128 cntX(i128 U, ll L) {
    if (vx == 0) return 0;
    ll p0 = x0, v = vx;
    if (v < 0) { p0 = W - p0; v = -v; }
    i128 posNum = (i128)p0 * L + (i128)v * U;
    i128 cur = floorDiv(posNum, (i128)W * L);
    i128 start = p0 / W;
    return cur - start;
}

i128 cntY(i128 U, ll L) {
    if (vy == 0) return 0;
    ll p0 = y0, v = vy;
    if (v < 0) { p0 = H - p0; v = -v; }
    i128 posNum = (i128)p0 * L + (i128)v * U;
    i128 cur = floorDiv(posNum, (i128)H * L);
    i128 start = p0 / H;
    return cur - start;
}

ll modPow(ll a, ll b) {
    ll r = 1;
    a %= MOD;
    while (b) {
        if (b & 1) r = r * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return r;
}

// 把展开坐标（有理数 num/L，num 为 i128）折返回桌面并对 MOD 取模
// len 为桌面该方向长度 W 或 H
ll foldMod(i128 num, ll L, ll len) {
    // 折返周期为 2*len：r = num mod (2*len*L)，落在 [0, 2*len*L)
    i128 period = (i128)2 * len * L;
    i128 r = num % period;
    if (r < 0) r += period;
    // r / L 为折前坐标；若超过 len 则镜像
    // 比较 r 与 len*L
    i128 half = (i128)len * L;
    i128 res;   // 最终坐标 * L
    if (r <= half) res = r;
    else res = period - r;                        // 2*len - r/L => (period - r)/L
    // 答案 = res / L (mod MOD)
    ll numMod = (ll)(res % MOD);
    return numMod * modPow(L % MOD, MOD - 2) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> W >> H >> x0 >> y0 >> vx >> vy >> k;

    ll avx = vx < 0 ? -vx : vx, avy = vy < 0 ? -vy : vy;
    ll L;
    if (avx == 0) L = avy;
    else if (avy == 0) L = avx;
    else L = avx / gcdll(avx, avy) * avy;

    // 二分最小整数 U：cntX + cntY >= k
    // 上界估计：每次碰库间隔不超过 max(W,H) / min(|vx|,|vy|) 量级，
    // 宽松取 hi = k * L * max(W,H) / max(1, min 非零速度) + 余量；直接用充分大的值。
    i128 lo = 0, hi = (i128)k * L * (max(W, H) + 1) + (i128)L * (max(W, H) + 1);
    // hi 可能过大但 __int128 足够；先放大 hi 直到满足
    while (cntX(hi, L) + cntY(hi, L) < (i128)k) hi *= 2;
    while (lo < hi) {
        i128 mid = lo + (hi - lo) / 2;
        if (cntX(mid, L) + cntY(mid, L) >= (i128)k) hi = mid;
        else lo = mid + 1;
    }
    i128 U = lo;

    i128 xNum = (i128)x0 * L + (i128)vx * U;      // 展开坐标 * L
    i128 yNum = (i128)y0 * L + (i128)vy * U;

    cout << foldMod(xNum, L, W) << " " << foldMod(yNum, L, H) << "\n";
    return 0;
}
