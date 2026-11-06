# -*- coding: utf-8 -*-
"""
台球之夜题包构建器：
1. 从题集 md 中拆分每题题面 -> problems/Txx-名称/problem.md
2. 复制标程 -> problems/Txx-名称/std.cpp
3. 每题生成 10 组数据 -> problems/Txx-名称/data/{1..10}.{in,out}
   （第 1 组为题面样例；小规模点用暴力与快速参考实现对拍）
"""
import os
import re
import sys
import math
import random
import heapq
import shutil
from array import array
from fractions import Fraction
from collections import deque
from itertools import combinations, permutations, product

sys.setrecursionlimit(3000000)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 台球之夜-题包/
ROOT = os.path.dirname(BASE)                                          # text/
MD = os.path.join(ROOT, "台球之夜-洛谷风格题集.md")
SOL = os.path.join(BASE, "solutions")
OUT = os.path.join(BASE, "problems")
MOD = 1000000007

report = []

# ============ 题面拆分 ============
def split_statements():
    text = open(MD, encoding="utf-8").read()
    # 匹配形如 ## T12【普及+ / 提高】运气衰减之谜
    pat = re.compile(r"^## T(\d+)【(.+?)】(.+?)\s*$", re.M)
    matches = list(pat.finditer(text))
    meta = {}
    for i, mch in enumerate(matches):
        num = int(mch.group(1))
        diff = mch.group(2).strip()
        name = mch.group(3).strip()
        start = mch.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # 截掉尾部的分隔线与总览章节
        for stop in ("## 全题集算法覆盖总览", "## 扩展篇二算法覆盖总览", "# 扩展篇"):
            idx = body.find("\n" + stop)
            if idx != -1:
                body = body[:idx]
        body = body.rstrip()
        if body.endswith("---"):
            body = body[:-3].rstrip()
        meta[num] = (name, diff, body)
    return meta

META = split_statements()
assert len(META) == 33, f"题面拆分数量异常：{len(META)}"

def tid(num):
    return f"T{num:02d}"

def folder(num):
    return f"{tid(num)}-{META[num][0]}"

# ============ 通用写入 ============
def write_problem(num, points):
    """points: list of (input_str, output_str)"""
    d = os.path.join(OUT, folder(num))
    os.makedirs(os.path.join(d, "data"), exist_ok=True)
    name, diff, body = META[num]
    with open(os.path.join(d, "problem.md"), "w", encoding="utf-8") as f:
        f.write(f"# {tid(num)} {name}（{diff}）\n\n")
        f.write("> 系列背景：2026 年 11 月 5 日，小民和小欣饭后前往台球厅，从 23 点切磋到次日 1 点。"
                "小欣技术很好，小民运气也不差（50%~300%）。期间来了不少朋友。"
                "小欣多次焚香试图打破小民的运气，惨淡收场，最终小民结账 38 元。\n\n")
        f.write(body + "\n")
    src = os.path.join(SOL, f"{tid(num)}.cpp")
    shutil.copyfile(src, os.path.join(d, "std.cpp"))
    for i, (inp, outp) in enumerate(points, 1):
        with open(os.path.join(d, "data", f"{i}.in"), "w", encoding="utf-8") as f:
            f.write(inp)
        with open(os.path.join(d, "data", f"{i}.out"), "w", encoding="utf-8") as f:
            f.write(outp)
    open(os.path.join(d, "_DONE"), "w").close()   # 完成标记，供断点续跑
    report.append(f"{tid(num)} {name}: {len(points)} 组数据")
    print(f"[build] {folder(num)}  ({len(points)} points)")

def rnd():
    return random

# =====================================================
# 每题：solve_fast(inp)->out；部分题另有 solve_brute 对拍
# =====================================================

# ---- T01 小民买单 ----
def s01(t):
    a, b = map(int, t.split())
    return f"{50 - 2 * a - 2 * b}\n"

def g01():
    pts = [("15 4\n", s01("15 4\n"))]
    for _ in range(9):
        while True:
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            if 2 * a + 2 * b <= 50:
                break
        inp = f"{a} {b}\n"
        pts.append((inp, s01(inp)))
    return pts

# ---- T02 焚香压运 ----
def s02(t):
    lines = t.strip().split("\n")
    L = 100
    for line in lines[1:]:
        op, x = line.split()
        L = L + int(x) if op == "WIN" else L - int(x)
        L = max(50, min(300, L))
    return f"{L}\n"

def g02():
    pts = [("5\nWIN 80\nWIN 100\nINCENSE 250\nWIN 30\nINCENSE 10\n",
            s02("5\nWIN 80\nWIN 100\nINCENSE 250\nWIN 30\nINCENSE 10\n"))]
    for n in [10, 100, 1000, 5000, 10000, 10000, 10000, 10000, 10000]:
        lines = [str(n)]
        for _ in range(n):
            op = "WIN" if random.random() < 0.5 else "INCENSE"
            lines.append(f"{op} {random.randint(1, 300)}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s02(inp)))
    return pts

# ---- T03 分段复盘 ----
def s03(t):
    tk = t.split()
    n, m = int(tk[0]), int(tk[1])
    a = list(map(int, tk[2:2 + n]))
    lo, hi = max(a), sum(a)
    while lo < hi:
        mid = (lo + hi) // 2
        cnt, cur = 1, 0
        for x in a:
            if cur + x <= mid:
                cur += x
            else:
                cnt += 1
                cur = x
        if cnt <= m:
            hi = mid
        else:
            lo = mid + 1
    return f"{lo}\n"

def b03(t):  # 暴力（小规模）：枚举分段点
    tk = t.split()
    n, m = int(tk[0]), int(tk[1])
    a = list(map(int, tk[2:2 + n]))
    best = None
    for cuts in combinations(range(1, n), m - 1):
        segs = []
        prev = 0
        s = 0
        for c in list(cuts) + [n]:
            segs.append(sum(a[prev:c]))
            prev = c
        cur = max(segs)
        best = cur if best is None else min(best, cur)
    return f"{best}\n"

def g03():
    pts = [("5 2\n10 20 30 40 50\n", "90\n")]
    for n, m in [(6, 3), (10, 4), (10, 1)]:
        a = [random.randint(1, 100) for _ in range(n)]
        inp = f"{n} {m}\n" + " ".join(map(str, a)) + "\n"
        fast, slow = s03(inp), b03(inp)
        assert fast == slow, (inp, fast, slow)
        pts.append((inp, fast))
    for n, m in [(100, 7), (1000, 13), (10000, 100), (100000, 1000), (100000, 2), (100000, 99999)]:
        a = [random.randint(1, 10**9) for _ in range(n)]
        inp = f"{n} {m}\n" + " ".join(map(str, a)) + "\n"
        pts.append((inp, s03(inp)))
    return pts[:10]

# ---- T04 运气连击 ----
def s04(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    NEG = float("-inf")
    f0 = NEG
    f1 = NEG
    ans = NEG
    for i in range(n):
        nf0 = max(f0, 0) + a[i]
        nf1 = max(f1 + a[i], f0) if i >= 1 else NEG
        f0, f1 = nf0, nf1
        ans = max(ans, f0, f1)
    return f"{ans}\n"

def b04(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    best = None
    for i in range(n):
        for j in range(i, n):
            seg = a[i:j + 1]
            best = max(best if best is not None else -10**18, sum(seg))
            for k in range(len(seg)):
                if len(seg) > 1:
                    best = max(best, sum(seg) - seg[k])
    return f"{best}\n"

def g04():
    pts = [("6\n4 -10 8 7 -20 9\n", "24\n")]
    for n in [6, 10, 30]:
        a = [random.randint(-20, 20) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        fast, slow = s04(inp), b04(inp)
        assert fast == slow, (inp, fast, slow)
        pts.append((inp, fast))
    for n in [100, 1000, 10000, 100000, 200000, 200000]:
        a = [random.randint(-10**4, 10**4) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        pts.append((inp, s04(inp)))
    return pts[:10]

# ---- T05 批量焚香 ----
class Seg:
    def __init__(self, a, p):
        self.n = len(a) - 1
        self.p = p
        N = 4 * self.n + 5
        self.sum = [0] * N
        self.mul = [1] * N
        self.add = [0] * N
        self.build(1, 1, self.n, a)

    def build(self, u, l, r, a):
        if l == r:
            self.sum[u] = a[l] % self.p
            return
        m = (l + r) >> 1
        self.build(u * 2, l, m, a)
        self.build(u * 2 + 1, m + 1, r, a)
        self.sum[u] = (self.sum[u * 2] + self.sum[u * 2 + 1]) % self.p

    def apply(self, u, l, r, k, b):
        p = self.p
        self.sum[u] = (self.sum[u] * k + b * (r - l + 1)) % p
        self.mul[u] = self.mul[u] * k % p
        self.add[u] = (self.add[u] * k + b) % p

    def down(self, u, l, r):
        if self.mul[u] == 1 and self.add[u] == 0:
            return
        m = (l + r) >> 1
        self.apply(u * 2, l, m, self.mul[u], self.add[u])
        self.apply(u * 2 + 1, m + 1, r, self.mul[u], self.add[u])
        self.mul[u] = 1
        self.add[u] = 0

    def update(self, u, l, r, ql, qr, k, b):
        if ql <= l and r <= qr:
            self.apply(u, l, r, k, b)
            return
        self.down(u, l, r)
        m = (l + r) >> 1
        if ql <= m:
            self.update(u * 2, l, m, ql, qr, k, b)
        if qr > m:
            self.update(u * 2 + 1, m + 1, r, ql, qr, k, b)
        self.sum[u] = (self.sum[u * 2] + self.sum[u * 2 + 1]) % self.p

    def query(self, u, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sum[u]
        self.down(u, l, r)
        m = (l + r) >> 1
        res = 0
        if ql <= m:
            res += self.query(u * 2, l, m, ql, qr)
        if qr > m:
            res += self.query(u * 2 + 1, m + 1, r, ql, qr)
        return res % self.p

def s05(t):
    lines = t.strip().split("\n")
    n, m, p = map(int, lines[0].split())
    a = [0] + list(map(int, lines[1].split()))
    st = Seg(a, p)
    out = []
    for line in lines[2:2 + m]:
        op = list(map(int, line.split()))
        if op[0] == 1:
            _, l, r, x = op
            st.update(1, 1, n, l, r, 1, x % p)
        elif op[0] == 2:
            _, l, r, x = op
            st.update(1, 1, n, l, r, x % p, 0)
        else:
            _, l, r = op
            out.append(str(st.query(1, 1, n, l, r)))
    return "\n".join(out) + "\n"

def b05(t):
    lines = t.strip().split("\n")
    n, m, p = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    out = []
    for line in lines[2:2 + m]:
        op = list(map(int, line.split()))
        if op[0] == 1:
            _, l, r, x = op
            for i in range(l - 1, r):
                a[i] = (a[i] + x) % p
        elif op[0] == 2:
            _, l, r, x = op
            for i in range(l - 1, r):
                a[i] = a[i] * x % p
        else:
            _, l, r = op
            out.append(str(sum(a[l - 1:r]) % p))
    return "\n".join(out) + "\n"

def g05():
    sample = "5 5 1000\n1 2 3 4 5\n1 1 3 10\n2 2 4 2\n3 1 5\n1 5 5 100\n3 4 5\n"
    pts = [(sample, "74\n113\n")]
    for n, m in [(10, 10), (50, 50), (200, 200)]:
        p = random.randint(2, 10**9)
        lines = [f"{n} {m} {p}", " ".join(str(random.randint(1, 10**9)) for _ in range(n))]
        for _ in range(m):
            t = random.random()
            l = random.randint(1, n)
            r = random.randint(l, n)
            if t < 0.35:
                lines.append(f"1 {l} {r} {random.randint(-10**9, 10**9)}")
            elif t < 0.6:
                lines.append(f"2 {l} {r} {random.randint(1, 10**9)}")
            else:
                lines.append(f"3 {l} {r}")
        inp = "\n".join(lines) + "\n"
        fast, slow = s05(inp), b05(inp)
        assert fast == slow, "T05 对拍失败"
        pts.append((inp, fast))
    for n, m in [(1000, 1000), (10000, 10000), (20000, 20000), (30000, 30000)]:
        p = random.randint(2, 10**9)
        lines = [f"{n} {m} {p}", " ".join(str(random.randint(1, 10**9)) for _ in range(n))]
        for _ in range(m):
            t = random.random()
            l = random.randint(1, n)
            r = random.randint(l, min(n, l + random.randint(0, n)))
            if t < 0.35:
                lines.append(f"1 {l} {r} {random.randint(-10**9, 10**9)}")
            elif t < 0.6:
                lines.append(f"2 {l} {r} {random.randint(1, 10**9)}")
            else:
                lines.append(f"3 {l} {r}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s05(inp)))
    return pts[:10]

# ---- T06 香炉布防 ----
def s06(t):
    tk = list(map(int, t.split()))
    n = tk[0]
    INF = 10**9
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        ch[tk[i - 1]].append(i)   # tk[1] 是 f_2
    f = [[0, 0, 0] for _ in range(n + 1)]
    # f_i < i，逆序处理保证孩子先于父亲
    for u in range(n, 0, -1):
        f0 = 1
        f2 = 0
        f1 = 0
        extra = INF
        has = False
        for v in ch[u]:
            f0 += min(f[v][0], f[v][1], f[v][2])
            f2 += min(f[v][0], f[v][1])
            best = min(f[v][0], f[v][1])
            f1 += best
            if f[v][0] <= f[v][1]:
                has = True
            else:
                extra = min(extra, f[v][0] - f[v][1])
        if not ch[u]:
            f1 = INF
        elif not has:
            f1 = f1 + extra if extra < INF else INF
        f[u] = [min(f0, INF), min(f1, INF), min(f2, INF)]
    return f"{min(f[1][0], f[1][1])}\n"

def b06(t):
    tk = list(map(int, t.split()))
    n = tk[0]
    fa = [0] * (n + 1)
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        fa[i] = tk[i - 1]
        ch[fa[i]].append(i)
    for k in range(n + 1):
        for S in combinations(range(1, n + 1), k):
            cov = set()
            for u in S:
                cov.add(u)
                if fa[u]:
                    cov.add(fa[u])
                cov.update(ch[u])
            if len(cov) == n:
                return f"{k}\n"

def g06():
    pts = [("6\n1 1 2 2 3\n", "2\n")]
    for n in [6, 9, 12]:
        fa = [random.randint(1, i - 1) for i in range(2, n + 1)]
        inp = f"{n}\n" + " ".join(map(str, fa)) + "\n"
        fast, slow = s06(inp), b06(inp)
        assert fast == slow, (inp, fast, slow)
        pts.append((inp, fast))
    for n in [100, 1000, 2000, 100000, 100000, 100000]:
        fa = [random.randint(max(1, i - 50), i - 1) if n <= 2000 else random.randint(1, i - 1)
              for i in range(2, n + 1)]
        inp = f"{n}\n" + " ".join(map(str, fa)) + "\n"
        pts.append((inp, s06(inp)))
    return pts[:10]

# ---- T07 黑八的轨迹 ----
def s07(t):
    lines = t.strip().split("\n")
    W, H, x0, y0 = map(int, lines[0].split())
    vx, vy = map(int, lines[1].split())
    k = int(lines[2])
    avx, avy = abs(vx), abs(vy)
    if avx == 0:
        L = avy
    elif avy == 0:
        L = avx
    else:
        L = avx // math.gcd(avx, avy) * avy

    def cnt(pos0, vel, ln, U):
        if vel == 0:
            return 0
        if vel < 0:                    # 镜像翻转为正方向，保证计数区间端点开闭正确
            pos0 = ln - pos0
            vel = -vel
        cur = (pos0 * L + vel * U) // (ln * L)
        start = pos0 // ln
        return cur - start

    def total(U):
        return cnt(x0, vx, W, U) + cnt(y0, vy, H, U)

    hi = 1
    while total(hi) < k:
        hi *= 2
    lo = 0
    while lo < hi:
        mid = (lo + hi) // 2
        if total(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    U = lo
    xnum = x0 * L + vx * U
    ynum = y0 * L + vy * U

    def fold(num, ln):
        period = 2 * ln * L
        r = num % period
        res = r if r <= ln * L else period - r
        return res * pow(L % MOD, MOD - 2, MOD) % MOD

    return f"{fold(xnum, W)} {fold(ynum, H)}\n"

def b07(t, kmax=2000):
    """逐事件模拟（Fraction 精确），仅适用于小 k。"""
    lines = t.strip().split("\n")
    W, H, x0, y0 = map(int, lines[0].split())
    vx, vy = map(int, lines[1].split())
    k = int(lines[2])
    assert k <= kmax
    def events(pos, vel, ln):
        ts = []
        if vel == 0:
            return ts
        if vel < 0:                    # 镜像翻转为正速度：pos' = ln - pos
            pos = ln - pos
            vel = -vel
        m = 0
        while True:
            num = m * ln - pos
            m += 1
            if num <= 0:
                continue
            tt = Fraction(num, vel)
            if tt > kmax * max(ln, 1) + 10:
                break
            ts.append(tt)
        return ts
    ev = sorted(events(x0, vx, W) + events(y0, vy, H))
    # 检查同时碰两库（进袋）—— 不允许出现在数据里
    for i in range(1, k):
        assert ev[i] != ev[i - 1], "轨迹经过袋口，数据非法"
    tk = ev[k - 1]
    def fold(v, ln):
        v = v % (2 * ln)
        return v if v <= ln else 2 * ln - v
    xf = fold(x0 + vx * tk, W)
    yf = fold(y0 + vy * tk, H)
    inv = lambda fr: fr.numerator % MOD * pow(fr.denominator % MOD, MOD - 2, MOD) % MOD
    return f"{inv(xf)} {inv(yf)}\n"

def g07():
    pts = [("3 2 1 1\n1 2\n3\n", "3 1\n")]
    # 小 k，随机形状，模拟验证合法（无袋口事件）
    made = 0
    while made < 4:
        W = random.randint(2, 9)
        H = random.randint(2, 9)
        x0 = random.randint(1, W - 1)
        y0 = random.randint(1, H - 1)
        vx = random.choice([-3, -2, -1, 1, 2, 3])
        vy = random.choice([-3, -2, -1, 1, 2, 3])
        k = random.randint(1, 30)
        inp = f"{W} {H} {x0} {y0}\n{vx} {vy}\n{k}\n"
        try:
            slow = b07(inp)
        except AssertionError:
            continue
        fast = s07(inp)
        assert fast == slow, (inp, fast, slow)
        pts.append((inp, fast))
        made += 1
    # 大 k：奇偶构造保证永不进袋
    # vx=1, x0=1, W 任意>=3：x 事件在整数时刻；vy=2, y0=1, H=2：y 事件在半整数时刻
    for k in [10**3, 10**6, 10**9, 10**12, 10**18]:
        W = random.randint(3, 10**6)
        vx, x0 = 1, 1
        if random.random() < 0.5:
            vx = -1
            x0 = W - 1
        inp = f"{W} 2 {x0} 1\n{vx} 2\n{k}\n"
        pts.append((inp, s07(inp)))
    return pts[:10]

# ---- T08 朋友圈 ----
def s08(t):
    lines = t.strip().split("\n")
    n, m, q = map(int, lines[0].split())
    fa = list(range(n + 1))
    def find(x):
        while fa[x] != x:
            fa[x] = fa[fa[x]]
            x = fa[x]
        return x
    for line in lines[1:1 + m]:
        x, y = map(int, line.split())
        fa[find(x)] = find(y)
    out = []
    for line in lines[1 + m:1 + m + q]:
        x, y = map(int, line.split())
        out.append("Yes" if find(x) == find(y) else "No")
    return "\n".join(out) + "\n"

def g08():
    pts = [("6 3 3\n1 2\n2 3\n4 5\n1 3\n3 4\n4 5\n", "Yes\nNo\nYes\n")]
    for n, m, q in [(10, 5, 5), (100, 50, 50), (1000, 2000, 2000), (100000, 200000, 200000),
                    (100000, 200000, 200000), (100000, 0, 200000), (100000, 200000, 200000),
                    (100000, 200000, 200000), (100000, 99999, 200000)]:
        lines = [f"{n} {m} {q}"]
        for _ in range(m):
            lines.append(f"{random.randint(1, n)} {random.randint(1, n)}")
        for _ in range(q):
            lines.append(f"{random.randint(1, n)} {random.randint(1, n)}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s08(inp)))
    return pts[:10]

# ---- T09 回家之路 ----
def s09(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    for line in lines[1:1 + m]:
        u, v, w = map(int, line.split())
        g[u].append((v, w))
        g[v].append((u, w))
    INF = 1 << 62
    dis = [INF] * (n + 1)
    dis[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dis[u]:
            continue
        for v, w in g[u]:
            if d + w < dis[v]:
                dis[v] = d + w
                heapq.heappush(pq, (dis[v], v))
    return f"{dis[n]}\n"

def g09():
    pts = [("4 5\n1 2 3\n2 4 4\n1 3 8\n3 4 2\n1 4 20\n", "7\n")]
    for n, extra in [(5, 3), (10, 10), (100, 200), (1000, 3000), (100000, 100000),
                     (100000, 200000), (100000, 200000), (100000, 200000), (100000, 200000)]:
        lines = []
        edges = []
        for i in range(2, n + 1):   # 生成树保证连通
            u = random.randint(1, i - 1)
            w = random.randint(1, 10**4)
            edges.append((u, i, w))
        seen = {(min(u, v), max(u, v)) for u, v, _ in edges}
        while len(edges) < n - 1 + extra:
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u == v:
                continue
            e = (min(u, v), max(u, v))
            if e in seen:
                continue
            seen.add(e)
            edges.append((u, v, random.randint(1, 10**4)))
        lines.append(f"{n} {len(edges)}")
        lines += [f"{u} {v} {w}" for u, v, w in edges]
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s09(inp)))
    return pts[:10]

# ---- T10 牢大补给 ----
def s10(t):
    lines = t.strip().split("\n")
    n, V = map(int, lines[0].split())
    NEG = -10**18
    dp = [NEG] * (V + 1)
    dp[0] = 0
    for line in lines[1:1 + n]:
        c, w = map(int, line.split())
        for j in range(c, V + 1):
            if dp[j - c] > NEG:
                dp[j] = max(dp[j], dp[j - c] + w)
    return f"{dp[V]}\n"

def g10():
    pts = [("3 38\n4 5\n10 12\n15 18\n", "47\n")]
    for n, V in [(5, 20), (10, 50), (20, 100), (50, 1000), (100, 5000), (100, 10000),
                 (100, 10000), (100, 10000), (100, 10000)]:
        lines = [f"{n} {V}"]
        lines.append(f"1 {random.randint(1, 3)}")   # 保底 1 元饮品，保证恰好花完
        for _ in range(n - 1):
            lines.append(f"{random.randint(2, V)} {random.randint(1, 10**4)}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s10(inp)))
    return pts[:10]

# ---- T11 小欣的咒语 ----
def s11(t):
    T, S = t.split("\n")[:2]
    m = len(S)
    nxt = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and S[i] != S[j]:
            j = nxt[j - 1]
        if S[i] == S[j]:
            j += 1
        nxt[i] = j
    cnt = 0
    j = 0
    for c in T:
        while j > 0 and (j == m or c != S[j]):
            j = nxt[j - 1]
        if c == S[j]:
            j += 1
        if j == m:
            cnt += 1
            j = nxt[j - 1]
    return f"{cnt}\n"

def b11(t):
    T, S = t.split("\n")[:2]
    return f"{sum(1 for i in range(len(T) - len(S) + 1) if T[i:i+len(S)] == S)}\n"

def g11():
    pts = [("aaaa\naa\n", "3\n")]
    for tl, sl in [(20, 2), (200, 3), (1000, 4)]:
        S = "".join(random.choice("ab") for _ in range(sl))
        T = "".join(random.choice("ab") for _ in range(tl))
        inp = f"{T}\n{S}\n"
        fast, slow = s11(inp), b11(inp)
        assert fast == slow
        pts.append((inp, fast))
    # 大点：文本中埋入若干模式串
    for tl in [100000, 500000, 1000000, 1000000, 1000000, 1000000]:
        S = "".join(random.choice("abc") for _ in range(random.randint(2, 8)))
        buf = []
        cur = 0
        while cur < tl:
            if random.random() < 0.1:
                buf.append(S)
                cur += len(S)
            else:
                seg = "".join(random.choice("abc") for _ in range(min(50, tl - cur)))
                buf.append(seg)
                cur += len(seg)
        T = "".join(buf)[:tl]
        inp = f"{T}\n{S}\n"
        pts.append((inp, s11(inp)))
    return pts[:10]

# ---- T12 运气衰减之谜 ----
def s12(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    b = sorted(set(a))
    idx = {v: i + 1 for i, v in enumerate(b)}
    bit = [0] * (len(b) + 2)
    ans = 0
    for i, v in enumerate(a):
        r = idx[v]
        s = 0
        j = r
        while j > 0:
            s += bit[j]
            j -= j & -j
        ans += i - s
        j = r
        while j < len(bit):
            bit[j] += 1
            j += j & -j
    return f"{ans}\n"

def b12(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    return f"{sum(1 for i in range(n) for j in range(i+1, n) if a[i] > a[j])}\n"

def g12():
    pts = [("5\n3 1 2 5 4\n", "3\n")]
    for n in [5, 8, 12]:
        a = [random.randint(1, 20) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        fast, slow = s12(inp), b12(inp)
        assert fast == slow
        pts.append((inp, fast))
    for n in [100, 1000, 10000, 100000, 100000, 100000]:
        a = [random.randint(1, 10**9) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        pts.append((inp, s12(inp)))
    return pts[:10]

# ---- T13 幸运数字 ----
def s13(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    ch0 = array("i", [0])
    ch1 = array("i", [0])
    ans = 0
    def insert(x):
        u = 0
        for i in range(31, -1, -1):
            b = (x >> i) & 1
            if b == 0:
                if ch0[u] == 0:
                    ch0[u] = len(ch0)
                    ch0.append(0)
                    ch1.append(0)
                u = ch0[u]
            else:
                if ch1[u] == 0:
                    ch1[u] = len(ch0)
                    ch0.append(0)
                    ch1.append(0)
                u = ch1[u]
    def query(x):
        u = 0
        res = 0
        for i in range(31, -1, -1):
            b = (x >> i) & 1
            if b == 0 and ch1[u] or b == 1 and ch0[u]:
                res |= 1 << i
                u = ch1[u] if b == 0 else ch0[u]
            else:
                u = ch0[u] if b == 0 else ch1[u]
        return res
    insert(a[0])
    for i in range(1, n):
        ans = max(ans, query(a[i]))
        insert(a[i])
    return f"{ans}\n"

def b13(t):
    tk = t.split()
    n = int(tk[0])
    a = list(map(int, tk[1:1 + n]))
    return f"{max(a[i]^a[j] for i in range(n) for j in range(i+1, n))}\n"

def g13():
    pts = [("4\n1 2 3 4\n", "7\n")]
    for n in [4, 8, 12]:
        a = [random.randint(0, 100) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        fast, slow = s13(inp), b13(inp)
        assert fast == slow
        pts.append((inp, fast))
    for n in [100, 1000, 10000, 50000, 100000, 100000]:
        a = [random.randint(0, 2**31 - 1) for _ in range(n)]
        inp = f"{n}\n" + " ".join(map(str, a)) + "\n"
        pts.append((inp, s13(inp)))
    return pts[:10]

# ---- T14 师徒大会 ----
def s14(t):
    lines = t.strip().split("\n")
    n, q = map(int, lines[0].split())
    fa = [0] * (n + 1)
    fas = list(map(int, lines[1].split()))
    for i in range(2, n + 1):
        fa[i] = fas[i - 2]
    LOG = max(1, n.bit_length())
    dep = [0] * (n + 1)
    up = [[0] * (n + 1) for _ in range(LOG)]
    for i in range(2, n + 1):   # f_i < i，顺序递推即可
        dep[i] = dep[fa[i]] + 1
        up[0][i] = fa[i]
        for j in range(1, LOG):
            up[j][i] = up[j - 1][up[j - 1][i]]
    out = []
    for line in lines[2:2 + q]:
        x, y = map(int, line.split())
        if dep[x] < dep[y]:
            x, y = y, x
        d = dep[x] - dep[y]
        ox, oy = x, y
        for j in range(LOG - 1, -1, -1):
            if (d >> j) & 1:
                x = up[j][x]
        if x == y:
            c = x
        else:
            for j in range(LOG - 1, -1, -1):
                if up[j][x] != up[j][y]:
                    x = up[j][x]
                    y = up[j][y]
            c = up[0][x]
        out.append(str(dep[ox] + dep[oy] - 2 * dep[c]))
    return "\n".join(out) + "\n"

def b14(t):
    lines = t.strip().split("\n")
    n, q = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    fas = list(map(int, lines[1].split()))
    for i in range(2, n + 1):
        f = fas[i - 2]
        g[i].append(f)
        g[f].append(i)
    out = []
    for line in lines[2:2 + q]:
        x, y = map(int, line.split())
        dist = {x: 0}
        dq = deque([x])
        while dq:
            u = dq.popleft()
            for v in g[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    dq.append(v)
        out.append(str(dist[y]))
    return "\n".join(out) + "\n"

def g14():
    pts = [("6 2\n1 1 2 2 3\n4 6\n4 5\n", "4\n2\n")]
    for n, q in [(6, 5), (10, 10), (20, 20)]:
        fa = [random.randint(1, i - 1) for i in range(2, n + 1)]
        lines = [f"{n} {q}", " ".join(map(str, fa))]
        for _ in range(q):
            lines.append(f"{random.randint(1, n)} {random.randint(1, n)}")
        inp = "\n".join(lines) + "\n"
        fast, slow = s14(inp), b14(inp)
        assert fast == slow
        pts.append((inp, fast))
    for n, q in [(1000, 1000), (100000, 100000), (100000, 100000), (100000, 100000),
                 (100000, 100000), (100000, 100000)]:
        fa = [random.randint(1, i - 1) for i in range(2, n + 1)]
        lines = [f"{n} {q}", " ".join(map(str, fa))]
        for _ in range(q):
            lines.append(f"{random.randint(1, n)} {random.randint(1, n)}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s14(inp)))
    return pts[:10]

# ---- T15 巅峰时刻 ----
def s15(t):
    lines = t.strip().split("\n")
    n, k = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    dq = deque()
    out = []
    for i, v in enumerate(a):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and a[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(str(a[dq[0]]))
    return " ".join(out) + "\n"

def b15(t):
    lines = t.strip().split("\n")
    n, k = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    return " ".join(str(max(a[i-k+1:i+1])) for i in range(k-1, n)) + "\n"

def g15():
    pts = [("8 3\n1 3 -1 -3 5 3 6 7\n", "3 3 5 5 6 7\n")]
    for n, k in [(8, 2), (10, 5), (20, 1)]:
        a = [random.randint(-50, 50) for _ in range(n)]
        inp = f"{n} {k}\n" + " ".join(map(str, a)) + "\n"
        fast, slow = s15(inp), b15(inp)
        assert fast == slow
        pts.append((inp, fast))
    for n, k in [(1000, 10), (100000, 100), (1000000, 1000), (1000000, 1),
                 (1000000, 1000000), (1000000, 777)]:
        a = [random.randint(-10**9, 10**9) for _ in range(n)]
        inp = f"{n} {k}\n" + " ".join(map(str, a)) + "\n"
        pts.append((inp, s15(inp)))
    return pts[:10]

# ---- T16 时光复盘 ----
def s16(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    b = sorted(set(a))
    sz = len(b)
    lc = array("i", [0])
    rc = array("i", [0])
    cnt = array("i", [0])

    def new_node():
        lc.append(0)
        rc.append(0)
        cnt.append(0)
        return len(cnt) - 1

    def update(pre, l, r, pos):
        u = new_node()
        lc[u] = lc[pre]
        rc[u] = rc[pre]
        cnt[u] = cnt[pre] + 1
        if l < r:
            mid = (l + r) >> 1
            if pos <= mid:
                lc[u] = update(lc[pre], l, mid, pos)
            else:
                rc[u] = update(rc[pre], mid + 1, r, pos)
        return u

    # 递归深度 log2(1e5) ~ 17，安全
    def build(l, r):
        u = new_node()
        if l < r:
            mid = (l + r) >> 1
            lc[u] = build(l, mid)
            rc[u] = build(mid + 1, r)
        return u

    def query(uL, uR, l, r, k):
        while l < r:
            mid = (l + r) >> 1
            c = cnt[lc[uR]] - cnt[lc[uL]]
            if k <= c:
                uL, uR, r = lc[uL], lc[uR], mid
            else:
                uL, uR, l, k = rc[uL], rc[uR], mid + 1, k - c
        return l

    rt = [0] * (n + 1)
    rt[0] = build(1, sz)
    pos_map = {v: i + 1 for i, v in enumerate(b)}
    for i in range(1, n + 1):
        rt[i] = update(rt[i - 1], 1, sz, pos_map[a[i - 1]])
    out = []
    for line in lines[2:2 + m]:
        l, r, k = map(int, line.split())
        out.append(str(b[query(rt[l - 1], rt[r], 1, sz, k) - 1]))
    return "\n".join(out) + "\n"

def b16(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    out = []
    for line in lines[2:2 + m]:
        l, r, k = map(int, line.split())
        out.append(str(sorted(a[l - 1:r])[k - 1]))
    return "\n".join(out) + "\n"

def g16():
    pts = [("7 1\n1 5 2 6 3 7 4\n2 5 3\n", "5\n")]
    for n, m in [(7, 5), (10, 10), (20, 20)]:
        a = [random.randint(-50, 50) for _ in range(n)]
        lines = [f"{n} {m}", " ".join(map(str, a))]
        for _ in range(m):
            l = random.randint(1, n)
            r = random.randint(l, n)
            k = random.randint(1, r - l + 1)
            lines.append(f"{l} {r} {k}")
        inp = "\n".join(lines) + "\n"
        fast, slow = s16(inp), b16(inp)
        assert fast == slow, "T16 对拍失败"
        pts.append((inp, fast))
    for n, m in [(1000, 1000), (10000, 10000), (100000, 100000), (100000, 100000),
                 (100000, 100000), (100000, 100000)]:
        a = [random.randint(-10**9, 10**9) for _ in range(n)]
        lines = [f"{n} {m}", " ".join(map(str, a))]
        for _ in range(m):
            l = random.randint(1, n)
            r = random.randint(l, n)
            k = random.randint(1, r - l + 1)
            lines.append(f"{l} {r} {k}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s16(inp)))
    return pts[:10]

# ---- T17 球厅人流 ----
def s17(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    for line in lines[1:1 + m]:
        u, v, c = map(int, line.split())
        g[u].append([v, c, len(g[v])])
        g[v].append([u, 0, len(g[u]) - 1])
    flow = 0
    while True:
        level = [-1] * (n + 1)
        level[1] = 0
        dq = deque([1])
        while dq:
            u = dq.popleft()
            for e in g[u]:
                if e[1] > 0 and level[e[0]] < 0:
                    level[e[0]] = level[u] + 1
                    dq.append(e[0])
        if level[n] < 0:
            break
        it = [0] * (n + 1)
        # 迭代 DFS
        while True:
            # 显式栈的阻塞流
            stack = [(1, 1 << 62)]
            path = []
            pushed = 0
            # 简单起见用递归风格的显式栈找增广路
            visited_edge = it
            u = 1
            route = []
            bottleneck = 1 << 62
            dead = False
            while True:
                if u == n:
                    # 增广
                    for (uu, ei) in route:
                        g[uu][ei][1] -= bottleneck
                        rev = g[uu][ei][2]
                        g[g[uu][ei][0]][rev][1] += bottleneck
                    flow += bottleneck
                    break
                advanced = False
                while visited_edge[u] < len(g[u]):
                    e = g[u][visited_edge[u]]
                    if e[1] > 0 and level[e[0]] == level[u] + 1:
                        route.append((u, visited_edge[u]))
                        bottleneck = min(bottleneck, e[1])
                        u = e[0]
                        advanced = True
                        break
                    visited_edge[u] += 1
                if not advanced:
                    if not route:
                        dead = True
                        break
                    u, ei = route.pop()
                    bottleneck = 1 << 62
                    for (uu, eii) in route:
                        bottleneck = min(bottleneck, g[uu][eii][1])
                    visited_edge[u] += 1
            if dead:
                break
    return f"{flow}\n"

def b17(t):
    # 朴素 Ford-Fulkerson（小规模）
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    cap = {}
    for line in lines[1:1 + m]:
        u, v, c = map(int, line.split())
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
    flow = 0
    while True:
        pre = {1: None}
        dq = deque([1])
        while dq:
            u = dq.popleft()
            for (a, b), c in cap.items():
                if a == u and c > 0 and b not in pre:
                    pre[b] = a
                    dq.append(b)
        if n not in pre:
            break
        f = float("inf")
        v = n
        while v != 1:
            f = min(f, cap[(pre[v], v)])
            v = pre[v]
        v = n
        while v != 1:
            cap[(pre[v], v)] -= f
            cap[(v, pre[v])] += f
            v = pre[v]
        flow += f
    return f"{flow}\n"

def g17():
    pts = [("4 5\n1 2 40\n1 4 20\n2 4 20\n2 3 30\n3 4 10\n", "50\n")]
    for n, extra in [(5, 5), (10, 15), (30, 60)]:
        edges = [(i, i + 1, random.randint(1, 100)) for i in range(1, n)]  # 链保证连通
        seen = {(i, i + 1) for i in range(1, n)}
        while len(edges) < n - 1 + extra:
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u == v or (u, v) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v, random.randint(1, 10**9)))
        lines = [f"{n} {len(edges)}"] + [f"{u} {v} {c}" for u, v, c in edges]
        inp = "\n".join(lines) + "\n"
        fast, slow = s17(inp), b17(inp)
        assert fast == slow, "T17 对拍失败"
        pts.append((inp, fast))
    for n, extra in [(100, 300), (200, 500), (300, 800), (300, 1000), (300, 1200), (400, 1200)]:
        edges = [(i, i + 1, random.randint(1, 10**9)) for i in range(1, n)]
        seen = {(i, i + 1) for i in range(1, n)}
        tries = 0
        while len(edges) < n - 1 + extra and tries < extra * 20:
            tries += 1
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u == v or (u, v) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v, random.randint(1, 10**9)))
        lines = [f"{n} {len(edges)}"] + [f"{u} {v} {c}" for u, v, c in edges]
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s17(inp)))
    return pts[:10]

# ---- T18 巡回敬杆 ----
def s18(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    d = [list(map(int, lines[1 + i].split())) for i in range(n)]
    full = 1 << n
    INF = 1 << 62
    dp = [array("q", [INF] * n) for _ in range(full)]
    dp[1][0] = 0
    for mask in range(1, full):
        if not (mask & 1):
            continue
        row = dp[mask]
        for i in range(n):
            if not (mask >> i & 1):
                continue
            cur = row[i]
            if cur >= INF:
                continue
            di = d[i]
            for j in range(n):
                if mask >> j & 1:
                    continue
                nm = mask | (1 << j)
                nv = cur + di[j]
                if nv < dp[nm][j]:
                    dp[nm][j] = nv
    ans = min(dp[full - 1][i] + d[i][0] for i in range(n))
    return f"{ans}\n"

def b18(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    d = [list(map(int, lines[1 + i].split())) for i in range(n)]
    best = float("inf")
    for perm in permutations(range(1, n)):
        tour = (0,) + perm + (0,)
        best = min(best, sum(d[tour[i]][tour[i + 1]] for i in range(n)))
    return f"{best}\n"

def g18():
    pts = [("4\n0 1 2 3\n1 0 1 2\n2 1 0 1\n3 2 1 0\n", "6\n")]
    for n in [4, 6, 8]:
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = random.randint(1, 100)
        lines = [str(n)] + [" ".join(map(str, row)) for row in d]
        inp = "\n".join(lines) + "\n"
        fast, slow = s18(inp), b18(inp)
        assert fast == slow
        pts.append((inp, fast))
    for n in [10, 11, 12, 13, 14, 14]:
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = random.randint(0, 10**6)
        lines = [str(n)] + [" ".join(map(str, row)) for row in d]
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s18(inp)))
    return pts[:10]

# ---- T19 学球顺序 ----
def s19(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for line in lines[1:1 + m]:
        u, v = map(int, line.split())
        g[u].append(v)
        indeg[v] += 1
    pq = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(pq)
    ans = []
    while pq:
        u = heapq.heappop(pq)
        ans.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(pq, v)
    return " ".join(map(str, ans)) + "\n"

def g19():
    pts = [("4 3\n1 3\n2 3\n3 4\n", "1 2 3 4\n")]
    for n, m in [(5, 4), (10, 15), (100, 200), (1000, 3000), (100000, 200000),
                 (100000, 200000), (100000, 100000), (100000, 99999), (100000, 200000)]:
        edges = set()
        while len(edges) < m:
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u < v:
                edges.add((u, v))
        lines = [f"{n} {len(edges)}"] + [f"{u} {v}" for u, v in edges]
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s19(inp)))
    return pts[:10]

# ---- T20 屠龙之杆 ----
MOD20 = 998244353
G20 = 3

def ntt(a, invert, n):
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wn = pow(G20, (MOD20 - 1) // length, MOD20)
        if invert:
            wn = pow(wn, MOD20 - 2, MOD20)
        half = length >> 1
        for i in range(0, n, length):
            w = 1
            for jj in range(i, i + half):
                u = a[jj]
                v = a[jj + half] * w % MOD20
                a[jj] = (u + v) % MOD20
                a[jj + half] = (u - v) % MOD20
                w = w * wn % MOD20
        length <<= 1
    if invert:
        inv = pow(n, MOD20 - 2, MOD20)
        for i in range(n):
            a[i] = a[i] * inv % MOD20

def s20(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    A = list(map(int, lines[1].split()))
    B = list(map(int, lines[2].split()))
    sz = 1
    while sz < n + m + 1:
        sz <<= 1
    A += [0] * (sz - len(A))
    B += [0] * (sz - len(B))
    ntt(A, False, sz)
    ntt(B, False, sz)
    C = [A[i] * B[i] % MOD20 for i in range(sz)]
    ntt(C, True, sz)
    return " ".join(map(str, C[:n + m + 1])) + "\n"

def b20(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    A = list(map(int, lines[1].split()))
    B = list(map(int, lines[2].split()))
    C = [0] * (n + m + 1)
    for i in range(n + 1):
        for j in range(m + 1):
            C[i + j] = (C[i + j] + A[i] * B[j]) % MOD20
    return " ".join(map(str, C)) + "\n"

def g20():
    pts = [("2 1\n1 2 1\n1 1\n", "1 3 3 1\n")]
    for n, m in [(2, 2), (5, 3), (20, 20)]:
        A = [random.randint(0, MOD20 - 1) for _ in range(n + 1)]
        B = [random.randint(0, MOD20 - 1) for _ in range(m + 1)]
        inp = f"{n} {m}\n" + " ".join(map(str, A)) + "\n" + " ".join(map(str, B)) + "\n"
        fast, slow = s20(inp), b20(inp)
        assert fast == slow, "T20 对拍失败"
        pts.append((inp, fast))
    for n, m in [(100, 100), (1000, 1000), (5000, 5000), (20000, 20000), (30000, 30000), (30000, 20000)]:
        A = [random.randint(0, MOD20 - 1) for _ in range(n + 1)]
        B = [random.randint(0, MOD20 - 1) for _ in range(m + 1)]
        inp = f"{n} {m}\n" + " ".join(map(str, A)) + "\n" + " ".join(map(str, B)) + "\n"
        pts.append((inp, s20(inp)))
    return pts[:10]

# ---- T21 全面压制 ----
def s21(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    raw = [tuple(map(int, lines[1 + i].split())) for i in range(n)]
    # 去重压缩
    from collections import Counter
    cc = Counter(raw)
    items = sorted(cc.keys())
    m = len(items)
    A = [it[0] for it in items]
    Bv = [it[1] for it in items]
    C = [it[2] for it in items]
    W = [cc[it] for it in items]
    RES = [0] * m
    K = max(C)
    bit = [0] * (K + 2)
    order = list(range(m))

    sys.setrecursionlimit(3000000)

    def bit_add(i, v):
        while i <= K:
            bit[i] += v
            i += i & -i
    def bit_ask(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    tmp = [0] * m

    def cdq(l, r):  # 对 order[l..r]（按下标，a 升序）
        if l == r:
            return
        mid = (l + r) >> 1
        cdq(l, mid)
        cdq(mid + 1, r)
        i, j = l, mid + 1
        while j <= r:
            while i <= mid and Bv[order[i]] <= Bv[order[j]]:
                bit_add(C[order[i]], W[order[i]])
                i += 1
            RES[order[j]] += bit_ask(C[order[j]])
            j += 1
        for q in range(l, i):
            bit_add(C[order[q]], -W[order[q]])
        # 按 b 归并
        i, j, t = l, mid + 1, l
        while i <= mid and j <= r:
            if Bv[order[i]] <= Bv[order[j]]:
                tmp[t] = order[i]; i += 1
            else:
                tmp[t] = order[j]; j += 1
            t += 1
        while i <= mid:
            tmp[t] = order[i]; i += 1; t += 1
        while j <= r:
            tmp[t] = order[j]; j += 1; t += 1
        order[l:r + 1] = tmp[l:r + 1]

    cdq(0, m - 1)
    gans = {}
    for i in range(m):
        gans[items[i]] = RES[i] + W[i] - 1
    return "\n".join(str(gans[t_]) for t_ in raw) + "\n"

def b21(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    p = [tuple(map(int, lines[1 + i].split())) for i in range(n)]
    out = []
    for i in range(n):
        out.append(str(sum(1 for j in range(n) if j != i and
                           p[j][0] <= p[i][0] and p[j][1] <= p[i][1] and p[j][2] <= p[i][2])))
    return "\n".join(out) + "\n"

def g21():
    pts = [("3\n1 1 1\n2 2 2\n2 2 3\n", "0\n1\n2\n")]
    for n in [5, 10, 15]:
        a = [tuple(random.randint(1, 10) for _ in range(3)) for _ in range(n)]
        inp = f"{n}\n" + "\n".join(" ".join(map(str, x)) for x in a) + "\n"
        fast, slow = s21(inp), b21(inp)
        assert fast == slow, "T21 对拍失败"
        pts.append((inp, fast))
    for n in [100, 1000, 5000, 10000, 15000, 20000]:
        a = [tuple(random.randint(1, 2 * 10**5) for _ in range(3)) for _ in range(n)]
        inp = f"{n}\n" + "\n".join(" ".join(map(str, x)) for x in a) + "\n"
        pts.append((inp, s21(inp)))
    return pts[:10]

# ---- T22 球杆统计 ----
def s22(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    a = [0] + list(map(int, lines[1].split()))
    qs = []
    for i, line in enumerate(lines[2:2 + m]):
        l, r = map(int, line.split())
        qs.append((l, r, i))
    B = max(1, int(n / math.sqrt(m)) ) if m > 0 else n
    qs.sort(key=lambda q: (q[0] // B, -q[1] if (q[0] // B) % 2 else q[1]))
    cnt = [0] * (1000001)
    ans = [0] * m
    cur = 0
    l, r = 1, 0
    for ql, qr, qi in qs:
        while l > ql:
            l -= 1
            cnt[a[l]] += 1
            if cnt[a[l]] == 1:
                cur += 1
        while r < qr:
            r += 1
            cnt[a[r]] += 1
            if cnt[a[r]] == 1:
                cur += 1
        while l < ql:
            cnt[a[l]] -= 1
            if cnt[a[l]] == 0:
                cur -= 1
            l += 1
        while r > qr:
            cnt[a[r]] -= 1
            if cnt[a[r]] == 0:
                cur -= 1
            r -= 1
        ans[qi] = cur
    return "\n".join(map(str, ans)) + "\n"

def b22(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    out = []
    for line in lines[2:2 + m]:
        l, r = map(int, line.split())
        out.append(str(len(set(a[l - 1:r]))))
    return "\n".join(out) + "\n"

def g22():
    pts = [("5 3\n1 2 1 3 2\n1 5\n1 3\n2 4\n", "3\n2\n3\n")]
    for n, m in [(6, 5), (10, 10), (20, 20)]:
        a = [random.randint(1, 20) for _ in range(n)]
        lines = [f"{n} {m}", " ".join(map(str, a))]
        for _ in range(m):
            l = random.randint(1, n)
            r = random.randint(l, n)
            lines.append(f"{l} {r}")
        inp = "\n".join(lines) + "\n"
        fast, slow = s22(inp), b22(inp)
        assert fast == slow, "T22 对拍失败"
        pts.append((inp, fast))
    for n, m in [(1000, 1000), (5000, 5000), (10000, 10000), (15000, 15000),
                 (20000, 15000), (20000, 20000)]:
        a = [random.randint(1, 10**6) for _ in range(n)]
        lines = [f"{n} {m}", " ".join(map(str, a))]
        for _ in range(m):
            l = random.randint(1, n)
            r = random.randint(l, n)
            lines.append(f"{l} {r}")
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s22(inp)))
    return pts[:10]

# ---- T23 咒语的本质 ----
def s23(t):
    S = t.strip()
    link = [0]   # 1 号为根（下标 0 作为根）
    length = [0]
    nxt = [dict()]
    last = 0
    for c in S:
        # extend
        p = last
        np = len(length)
        length.append(length[p] + 1)
        nxt.append(dict())
        link.append(0)
        while p != -1 and c not in nxt[p]:
            nxt[p][c] = np
            p = link[p] if p != 0 else -1
        if p == -1:
            link[np] = 0
        else:
            q = nxt[p][c]
            if length[q] == length[p] + 1:
                link[np] = q
            else:
                nq = len(length)
                length.append(length[p] + 1)
                nxt.append(dict(nxt[q]))
                link.append(link[q])
                link[q] = link[np] = nq
                while p != -1 and nxt[p].get(c) == q:
                    nxt[p][c] = nq
                    p = link[p] if p != 0 else -1
        last = np
    return f"{sum(length[i] - length[link[i]] for i in range(1, len(length)))}\n"

def b23(t):
    S = t.strip()
    return f"{len({S[i:j] for i in range(len(S)) for j in range(i + 1, len(S) + 1)})}\n"

def g23():
    pts = [("abab\n", "7\n")]
    for ln in [10, 30, 60]:
        S = "".join(random.choice("ab") for _ in range(ln))
        inp = S + "\n"
        fast, slow = s23(inp), b23(inp)
        assert fast == slow, "T23 对拍失败"
        pts.append((inp, fast))
    pts.append(("ab" * 25000 + "\n", s23("ab" * 25000 + "\n")))
    for ln in [10000, 50000, 200000, 200000, 200000]:
        S = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(ln))
        inp = S + "\n"
        pts.append((inp, s23(inp)))
    return pts[:10]

# ---- T24 禁咒词库 ----
def s24(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    pats = lines[1:1 + n]
    T = lines[1 + n]
    nxt = [dict()]
    fail = [0]
    cnt = [0]
    for p in pats:
        u = 0
        for c in p:
            if c not in nxt[u]:
                nxt[u][c] = len(nxt)
                nxt.append(dict())
                fail.append(0)
                cnt.append(0)
            u = nxt[u][c]
        cnt[u] += 1
    dq = deque()
    for c, v in nxt[0].items():
        dq.append(v)
    while dq:
        u = dq.popleft()
        for c, v in nxt[u].items():
            f = fail[u]
            while f and c not in nxt[f]:
                f = fail[f]
            fail[v] = nxt[f].get(c, 0)
            dq.append(v)
    # 传播：BFS 正向（浅 -> 深），cnt[u] 累加其 fail 祖先的模式数
    tree = [[] for _ in range(len(nxt))]
    for i in range(1, len(nxt)):
        tree[fail[i]].append(i)
    order = []
    dq = deque([0])
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in tree[u]:
            dq.append(v)
    for u in order[1:]:
        cnt[u] += cnt[fail[u]]
    ans = 0
    u = 0
    for c in T:
        while u and c not in nxt[u]:
            u = fail[u]
        u = nxt[u].get(c, 0)
        ans += cnt[u]
    return f"{ans}\n"

def b24(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    pats = lines[1:1 + n]
    T = lines[1 + n]
    cnt = 0
    for p in pats:
        for i in range(len(T) - len(p) + 1):
            if T[i:i + len(p)] == p:
                cnt += 1
    return f"{cnt}\n"

def g24():
    pts = [("3\nab\nbc\nca\nabcab\n", "4\n")]
    for n, tl in [(3, 20), (5, 50), (10, 200)]:
        pats = ["".join(random.choice("ab") for _ in range(random.randint(1, 4))) for _ in range(n)]
        T = "".join(random.choice("ab") for _ in range(tl))
        inp = f"{n}\n" + "\n".join(pats) + f"\n{T}\n"
        fast, slow = s24(inp), b24(inp)
        assert fast == slow, "T24 对拍失败"
        pts.append((inp, fast))
    for n, tl in [(100, 10000), (1000, 100000), (10000, 200000), (30000, 200000),
                  (50000, 200000), (50000, 200000)]:
        pats = set()
        while len(pats) < n:
            pats.add("".join(random.choice("abcde") for _ in range(random.randint(1, 8))))
        pats = list(pats)
        # 文本中埋入部分模式
        buf = []
        cur = 0
        while cur < tl:
            if random.random() < 0.15:
                p = random.choice(pats)
                buf.append(p)
                cur += len(p)
            else:
                seg = "".join(random.choice("abcde") for _ in range(min(30, tl - cur)))
                buf.append(seg)
                cur += len(seg)
        T = "".join(buf)[:tl]
        inp = f"{n}\n" + "\n".join(pats) + f"\n{T}\n"
        pts.append((inp, s24(inp)))
    return pts[:10]

# ---- T25 香味分配 ----
def s25(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    c = [list(map(int, lines[1 + i].split())) for i in range(n)]
    N = 2 * n + 2
    S, T = 2 * n, 2 * n + 1
    g = [[] for _ in range(N)]
    def add(u, v, cap, cost):
        g[u].append([v, cap, cost, len(g[v])])
        g[v].append([u, 0, -cost, len(g[u]) - 1])
    for i in range(n):
        add(S, i, 1, 0)
        add(n + i, T, 1, 0)
        for j in range(n):
            add(i, n + j, 1, c[i][j])
    flow = 0
    cost = 0
    while True:
        dis = [1 << 62] * N
        dis[S] = 0
        pre = [-1] * N
        pe = [-1] * N
        inq = [False] * N
        dq = deque([S])
        inq[S] = True
        while dq:
            u = dq.popleft()
            inq[u] = False
            for i, e in enumerate(g[u]):
                if e[1] > 0 and dis[u] + e[2] < dis[e[0]]:
                    dis[e[0]] = dis[u] + e[2]
                    pre[e[0]] = u
                    pe[e[0]] = i
                    if not inq[e[0]]:
                        inq[e[0]] = True
                        dq.append(e[0])
        if pre[T] == -1:
            break
        v = T
        while v != S:
            e = g[pre[v]][pe[v]]
            e[1] -= 1
            g[v][e[3]][1] += 1
            v = pre[v]
        flow += 1
        cost += dis[T]
    return f"{cost}\n"

def b25(t):
    lines = t.strip().split("\n")
    n = int(lines[0])
    c = [list(map(int, lines[1 + i].split())) for i in range(n)]
    return f"{min(sum(c[i][p[i]] for i in range(n)) for p in permutations(range(n)))}\n"

def g25():
    pts = [("2\n1 5\n5 2\n", "3\n")]
    for n in [2, 4, 6]:
        c = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]
        inp = f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in c) + "\n"
        fast, slow = s25(inp), b25(inp)
        assert fast == slow, "T25 对拍失败"
        pts.append((inp, fast))
    for n in [10, 20, 40, 60, 80, 100]:
        c = [[random.randint(0, 1000) for _ in range(n)] for _ in range(n)]
        inp = f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in c) + "\n"
        pts.append((inp, s25(inp)))
    return pts[:10]

# ---- T26 两难之约 ----
def s26(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(2 * n + 1)]
    def id_(i, val):
        return 2 * i - 1 + val
    for line in lines[1:1 + m]:
        i, a, j, b = map(int, line.split())
        g[id_(i, a)].append(id_(j, b))
        g[id_(j, b ^ 1)].append(id_(i, a ^ 1))
    # 迭代 Tarjan
    N = 2 * n + 1
    dfn = [0] * N
    low = [0] * N
    comp = [0] * N
    ins = [False] * N
    dfc = 0
    scc = 0
    for s in range(1, N):
        if dfn[s]:
            continue
        stk = [(s, 0)]
        dfc += 1
        dfn[s] = low[s] = dfc
        st = [s]
        ins[s] = True
        while stk:
            u, i = stk[-1]
            if i < len(g[u]):
                v = g[u][i]
                stk[-1] = (u, i + 1)
                if not dfn[v]:
                    dfc += 1
                    dfn[v] = low[v] = dfc
                    st.append(v)
                    ins[v] = True
                    stk.append((v, 0))
                elif ins[v]:
                    if dfn[v] < low[u]:
                        low[u] = dfn[v]
            else:
                if low[u] == dfn[u]:
                    scc += 1
                    while True:
                        v = st.pop()
                        ins[v] = False
                        comp[v] = scc
                        if v == u:
                            break
                stk.pop()
                if stk:
                    pu = stk[-1][0]
                    if low[u] < low[pu]:
                        low[pu] = low[u]
    for i in range(1, n + 1):
        if comp[id_(i, 0)] == comp[id_(i, 1)]:
            return "IMPOSSIBLE\n"
    assign = ["1" if comp[id_(i, 1)] < comp[id_(i, 0)] else "0" for i in range(1, n + 1)]
    return "POSSIBLE\n" + " ".join(assign) + "\n"

def check26(inp, out):
    lines = inp.strip().split("\n")
    n, m = map(int, lines[0].split())
    cons = [tuple(map(int, lines[1 + i].split())) for i in range(m)]
    o = out.strip().split("\n")
    if o[0] == "IMPOSSIBLE":
        # 暴力确认无解
        for assign in product([0, 1], repeat=n):
            if all(not (assign[i - 1] == a and assign[j - 1] != b) for (i, a, j, b) in cons):
                return False
        return True
    assign = list(map(int, o[1].split()))
    return all(not (assign[i - 1] == a and assign[j - 1] != b) for (i, a, j, b) in cons)

def g26():
    sample = "2 2\n1 0 2 1\n2 1 1 0\n"
    pts = [(sample, s26(sample))]
    assert check26(sample, pts[0][1])
    # 可满足点：先随机赋值，再生成与其相容的约束
    for n, m in [(10, 15), (50, 80), (200, 300), (2000, 5000), (20000, 50000),
                 (50000, 100000), (50000, 100000)]:
        s = [random.randint(0, 1) for _ in range(n + 1)]
        lines = [f"{n} {m}"]
        made = 0
        while made < m:
            i = random.randint(1, n)
            j = random.randint(1, n)
            a = random.randint(0, 1)
            b = random.randint(0, 1)
            if s[i] == a and s[j] != b:
                continue    # 与预设解冲突，跳过
            lines.append(f"{i} {a} {j} {b}")
            made += 1
        inp = "\n".join(lines) + "\n"
        out = s26(inp)
        assert out.startswith("POSSIBLE") and check26(inp, out), "T26 数据校验失败"
        pts.append((inp, out))
    # 不可满足点：x1 被迫同时为 0 和 1
    for extra in [0, 5]:
        n = 2 + extra
        lines = [f"{n} {2 + extra}", "1 0 1 1", "1 1 1 0"]
        for _ in range(extra):
            lines.append(f"2 {random.randint(0,1)} {2 + extra} {random.randint(0,1)}")
        inp = "\n".join(lines) + "\n"
        out = s26(inp)
        assert out == "IMPOSSIBLE\n" and check26(inp, out)
        pts.append((inp, out))
    return pts[:10]

# ---- T27 树上有约 ----
def s27(t, kmax=10**7):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    for line in lines[1:n]:
        u, v, w = map(int, line.split())
        g[u].append((v, w))
        g[v].append((u, w))
    qs = [int(lines[n + i]) for i in range(m)]
    ans = [False] * m
    exist = bytearray(kmax + 1)
    vis = [False] * (n + 1)
    sz = [0] * (n + 1)
    mx = [0] * (n + 1)

    sys.setrecursionlimit(3000000)

    def get_root(u, fa, tot):
        sz[u] = 1
        mx[u] = 0
        best_root = u
        for v, w in g[u]:
            if v == fa or vis[v]:
                continue
            r = get_root(v, u, tot)
            sz[u] += sz[v]
            mx[u] = max(mx[u], sz[v])
            if mx[r] < mx[best_root] or best_root == u and False:
                pass
        # 重心需要在完整遍历后确定，改用两遍：先算 sz，再找重心
        return u

    # 为避免重写两遍逻辑，采用标准递归实现：
    def getroot(u, fa, tot, res):
        sz[u] = 1
        mx[u] = 0
        for v, w in g[u]:
            if v == fa or vis[v]:
                continue
            getroot(v, u, tot, res)
            sz[u] += sz[v]
            if sz[v] > mx[u]:
                mx[u] = sz[v]
        if tot - sz[u] > mx[u]:
            mx[u] = tot - sz[u]
        if mx[u] < mx[res[0]]:
            res[0] = u

    def getdis(u, fa, d, ds):
        ds.append(d)
        for v, w in g[u]:
            if v == fa or vis[v]:
                continue
            getdis(v, u, d + w, ds)

    def solve(u, tot):
        res = [u]
        mx[u] = tot + 1  # 占位
        getroot(u, 0, tot, res)
        rt = res[0]
        vis[rt] = True
        exist[0] = 1
        used = [0]
        for v, w in g[rt]:
            if vis[v]:
                continue
            ds = []
            getdis(v, rt, w, ds)
            for d in ds:
                if d > kmax:
                    continue
                for i in range(m):
                    if not ans[i] and qs[i] >= d and exist[qs[i] - d]:
                        ans[i] = True
            for d in ds:
                if d <= kmax and not exist[d]:
                    exist[d] = 1
                    used.append(d)
        for d in used:
            exist[d] = 0
        for v, w in g[rt]:
            if not vis[v]:
                solve(v, sz[v])
    # 初始：整棵树
    res = [1]
    mx[1] = n + 1
    getroot(1, 0, n, res)
    # solve 里会再找一次重心；直接从 res[0] 开始
    def solve2(u, tot):
        vis[u] = True
        exist[0] = 1
        used = [0]
        for v, w in g[u]:
            if vis[v]:
                continue
            ds = []
            getdis(v, u, w, ds)
            for d in ds:
                if d > kmax:
                    continue
                for i in range(m):
                    if not ans[i] and qs[i] >= d and exist[qs[i] - d]:
                        ans[i] = True
            for d in ds:
                if d <= kmax and not exist[d]:
                    exist[d] = 1
                    used.append(d)
        for d in used:
            exist[d] = 0
        for v, w in g[u]:
            if vis[v]:
                continue
            res2 = [v]
            mx[v] = 10**9
            getroot(v, u, sz[v], res2)
            solve2(res2[0], sz[v])
    solve2(res[0], n)
    return "\n".join("AYE" if a else "NAY" for a in ans) + "\n"

def b27(t):
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    g = [[] for _ in range(n + 1)]
    for line in lines[1:n]:
        u, v, w = map(int, line.split())
        g[u].append((v, w))
        g[v].append((u, w))
    dists = set()
    for s in range(1, n + 1):
        dist = {s: 0}
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v, w in g[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    dq.append(v)
        for v in dist:
            if v != s:                       # 排除自身：题目要求两个不同节点
                dists.add(dist[v])
    out = []
    for i in range(m):
        k = int(lines[n + i])
        out.append("AYE" if k in dists else "NAY")
    return "\n".join(out) + "\n"

def g27():
    pts = [("4 3\n1 2 1\n2 3 1\n3 4 1\n1\n2\n4\n", "AYE\nAYE\nNAY\n")]
    for n, m in [(6, 5), (10, 8), (15, 10)]:
        lines = [f"{n} {m}"]
        edges = []
        d_actual = set()
        for i in range(2, n + 1):
            u = random.randint(1, i - 1)
            w = random.randint(1, 10)
            edges.append((u, i, w))
        lines += [f"{u} {v} {w}" for u, v, w in edges]
        for _ in range(m):
            lines.append(str(random.randint(0, 4 * n)))
        inp = "\n".join(lines) + "\n"
        fast, slow = s27(inp), b27(inp)
        assert fast == slow, "T27 对拍失败"
        pts.append((inp, fast))
    for n, m in [(1000, 50), (3000, 50), (5000, 50), (5000, 50), (5000, 100), (5000, 100)]:
        lines = [f"{n} {m}"]
        for i in range(2, n + 1):
            u = random.randint(max(1, i - 20), i - 1)
            w = random.randint(1, 10**4)
            lines.append(f"{u} {i} {w}")
        for _ in range(m):
            lines.append(str(random.randint(0, 10**7)))
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s27(inp)))
    return pts[:10]

# ---- T28 运气排行榜 ----
def s28(t):
    # 参考实现用有序模拟（bisect），与标程 FHQ-Treap 逻辑独立
    import bisect
    lines = t.strip().split("\n")
    n = int(lines[0])
    ms = []
    out = []
    for line in lines[1:1 + n]:
        op, x = map(int, line.split())
        if op == 1:
            bisect.insort(ms, x)
        elif op == 2:
            ms.pop(bisect.bisect_left(ms, x))
        elif op == 3:
            out.append(str(bisect.bisect_left(ms, x) + 1))
        elif op == 4:
            out.append(str(ms[x - 1]))
        elif op == 5:
            out.append(str(ms[bisect.bisect_left(ms, x) - 1]))
        else:
            out.append(str(ms[bisect.bisect_right(ms, x)]))
    return "\n".join(out) + "\n"

def g28():
    pts = [("7\n1 5\n1 2\n1 8\n3 5\n4 2\n5 5\n6 5\n", "2\n5\n2\n8\n")]
    for total in [100, 1000, 10000, 50000, 50000, 50000, 50000, 50000, 50000]:
        import bisect as _b
        ms = []
        lines = [str(total)]
        made = 0
        while made < total:
            op = random.randint(1, 6)
            if not ms:
                op = 1                      # 空集合只能插入
            if op == 1:
                x = random.randint(-10**9, 10**9)
                _b.insort(ms, x)
                lines.append(f"1 {x}")
            elif op == 2:
                x = random.choice(ms)
                ms.pop(_b.bisect_left(ms, x))
                lines.append(f"2 {x}")
            elif op == 3:
                x = random.randint(-10**9, 10**9)
                lines.append(f"3 {x}")
            elif op == 4:
                lines.append(f"4 {random.randint(1, len(ms))}")
            elif op == 5:
                if ms[0] >= 10**9 - 1:
                    continue
                x = random.randint(ms[0] + 1, 10**9)   # 保证前驱存在
                lines.append(f"5 {x}")
            else:
                if ms[-1] <= -10**9 + 1:
                    continue
                x = random.randint(-10**9, ms[-1] - 1) # 保证后继存在
                lines.append(f"6 {x}")
            made += 1
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s28(inp)))
    return pts[:10]

# ---- T29 变动的师门 ----
def s29(t):
    # 参考实现：直接维护森林 + BFS 路径（数据规模小，逻辑独立）
    lines = t.strip().split("\n")
    n, m = map(int, lines[0].split())
    val = [0] + list(map(int, lines[1].split()))
    adj = [set() for _ in range(n + 1)]
    out = []
    for line in lines[2:2 + m]:
        op, x, y = map(int, line.split())
        if op == 0:
            par = {x: 0}
            dq = deque([x])
            found = False
            while dq:
                u = dq.popleft()
                if u == y:
                    found = True
                    break
                for v in adj[u]:
                    if v not in par:
                        par[v] = u
                        dq.append(v)
            if not found:
                out.append("-1")
            else:
                path = [y]
                while path[-1] != x:
                    path.append(par[path[-1]])
                xr = 0
                for u in path:
                    xr ^= val[u]
                out.append(str(xr))
        elif op == 1:
            adj[x].add(y)
            adj[y].add(x)
        elif op == 2:
            adj[x].discard(y)
            adj[y].discard(x)
        else:
            val[x] = y
    return "\n".join(out) + "\n"

def g29():
    pts = [("3 5\n1 2 3\n1 1 2\n1 2 3\n0 1 3\n2 2 3\n0 1 3\n", "0\n-1\n")]
    for n, m in [(10, 20), (100, 300), (500, 1000), (1000, 2000), (2000, 3000),
                 (3000, 3000), (3000, 3000), (3000, 3000), (3000, 3000)]:
        val = [random.randint(0, 10**9) for _ in range(n)]
        adj = [set() for _ in range(n + 1)]
        lines = [f"{n} {m}", " ".join(map(str, val))]
        made = 0
        while made < m:
            r = random.random()
            if r < 0.12:
                op = 0
            elif r < 0.5:
                op = 1
            elif r < 0.7:
                op = 2
            else:
                op = 3
            x = random.randint(1, n)
            y = random.randint(1, n)
            if op == 0:
                lines.append(f"0 {x} {y}")
            elif op == 1:
                # 仅当不连通时 link
                par = {x}
                dq = deque([x])
                conn = False
                while dq:
                    u = dq.popleft()
                    if u == y:
                        conn = True
                        break
                    for v in adj[u]:
                        if v not in par:
                            par.add(v)
                            dq.append(v)
                if x != y and not conn:
                    adj[x].add(y)
                    adj[y].add(x)
                    lines.append(f"1 {x} {y}")
                else:
                    continue
            elif op == 2:
                es = [(a, b) for a in range(1, n + 1) for b in adj[a] if a < b]
                if not es:
                    continue
                a, b = random.choice(es)
                adj[a].discard(b)
                adj[b].discard(a)
                lines.append(f"2 {a} {b}")
            else:
                lines.append(f"3 {x} {random.randint(0, 10**9)}")
            made += 1
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s29(inp)))
    return pts[:10]

# ---- T30 集齐七色球 ----
def s30(t):
    n = int(t.strip())
    E = sum(n / (n - i) for i in range(n))
    return f"{E:.2f}\n"

def g30():
    pts = [("2\n", "3.00\n")]
    for n in [1, 3, 5, 10, 50, 100, 1000, 5000, 10000]:
        inp = f"{n}\n"
        pts.append((inp, s30(inp)))
    return pts[:10]

# ---- T31 吉利台号 ----
def s31(t):
    from functools import lru_cache
    l, r = map(int, t.split())
    def count(x):
        if x < 0:
            return 0
        dig = list(map(int, str(x)))[::-1]   # dig[0] 个位
        L = len(dig)
        @lru_cache(maxsize=None)
        def dfs(pos, pre6, tight, lead):
            if pos < 0:
                return 1
            up = dig[pos] if tight else 9
            res = 0
            for d in range(up + 1):
                if d == 4:
                    continue
                if pre6 and d == 2:
                    continue
                res += dfs(pos - 1, d == 6, tight and d == up, lead and d == 0)
            return res
        return dfs(L - 1, False, True, True)
    return f"{count(r) - count(l - 1)}\n"

def b31(t):
    l, r = map(int, t.split())
    def ok(x):
        s = str(x)
        return "4" not in s and "62" not in s
    return f"{sum(1 for x in range(l, r + 1) if ok(x))}\n"

def g31():
    pts = [("1 100\n", "80\n")]
    for l, r in [(1, 1000), (50, 5000), (1, 20000)]:
        inp = f"{l} {r}\n"
        fast, slow = s31(inp), b31(inp)
        assert fast == slow, "T31 对拍失败"
        pts.append((inp, fast))
    for l, r in [(1, 10**6), (10**6, 10**9), (1, 10**12), (10**10, 10**15),
                 (1, 10**18), (10**17, 10**18)]:
        inp = f"{l} {r}\n"
        pts.append((inp, s31(inp)))
    return pts[:10]

# ---- T32 运气复利 ----
def s32(t):
    n = int(t.strip())
    if n <= 2:
        return "1\n"
    def mul(X, Y):
        return [[(X[0][0] * Y[0][0] + X[0][1] * Y[1][0]) % MOD,
                 (X[0][0] * Y[0][1] + X[0][1] * Y[1][1]) % MOD],
                [(X[1][0] * Y[0][0] + X[1][1] * Y[1][0]) % MOD,
                 (X[1][0] * Y[0][1] + X[1][1] * Y[1][1]) % MOD]]
    base = [[1, 1], [1, 0]]
    res = [[1, 0], [0, 1]]
    e = n - 2
    while e:
        if e & 1:
            res = mul(res, base)
        base = mul(base, base)
        e >>= 1
    return f"{(res[0][0] + res[0][1]) % MOD}\n"

def b32(t):
    n = int(t.strip())
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % MOD
    return f"{a}\n"

def g32():
    pts = [("10\n", "55\n")]
    for n in [1, 2, 3, 100, 10000]:
        inp = f"{n}\n"
        fast, slow = s32(inp), b32(inp)
        assert fast == slow, "T32 对拍失败"
        pts.append((inp, fast))
    for n in [10**9, 10**12, 10**15, 10**18]:
        inp = f"{n}\n"
        pts.append((inp, s32(inp)))
    return pts[:10]

# ---- T33 最后三堆球 ----
def s33(t):
    lines = t.strip().split("\n")
    T = int(lines[0])
    out = []
    idx = 1
    for _ in range(T):
        n = int(lines[idx])
        xr = 0
        for p in map(int, lines[idx + 1].split()):
            xr ^= p
        out.append("Xiaomin" if xr else "Xiaoxin")
        idx += 2
    return "\n".join(out) + "\n"

def g33():
    pts = [("2\n3\n1 2 3\n3\n1 2 4\n", "Xiaoxin\nXiaomin\n")]
    for T, n in [(3, 3), (10, 5), (50, 10), (100, 100), (100, 1000), (1, 100000),
                 (100, 10000), (100, 10000), (100, 10000)]:
        lines = [str(T)]
        for _ in range(T):
            piles = [random.randint(1, 10**9) for _ in range(n)]
            if random.random() < 0.5:
                xr = 0
                for p in piles[:-1]:
                    xr ^= p
                piles[-1] = xr if xr >= 1 else 1  # 构造异或和为 0 的局
            lines.append(str(n))
            lines.append(" ".join(map(str, piles)))
        inp = "\n".join(lines) + "\n"
        pts.append((inp, s33(inp)))
    return pts[:10]

# ============ 主流程 ============
def main():
    import time
    random.seed(20261105)
    os.makedirs(OUT, exist_ok=True)
    gens = {
        1: g01, 2: g02, 3: g03, 4: g04, 5: g05, 6: g06, 7: g07, 8: g08, 9: g09,
        10: g10, 11: g11, 12: g12, 13: g13, 14: g14, 15: g15, 16: g16, 17: g17,
        18: g18, 19: g19, 20: g20, 21: g21, 22: g22, 23: g23, 24: g24, 25: g25,
        26: g26, 27: g27, 28: g28, 29: g29, 30: g30, 31: g31, 32: g32, 33: g33,
    }
    for num in range(1, 34):
        d = os.path.join(OUT, folder(num), "_DONE")
        if os.path.exists(d):
            print(f"[skip] {folder(num)} 已完成", flush=True)
            continue
        t0 = time.time()
        write_problem(num, gens[num]())
        print(f"[time] {tid(num)} 用时 {time.time() - t0:.1f}s", flush=True)
    print("\n===== 构建完成 =====")
    for line in report:
        print(line)

if __name__ == "__main__":
    main()
