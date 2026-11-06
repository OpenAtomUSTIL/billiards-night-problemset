// T21【省选/NOI-】全面压制
// 算法：CDQ 分治求三维偏序
// 对每局 i 求 f(i) = #{j != i : a_j<=a_i, b_j<=b_i, c_j<=c_i}
// 完全相同的三元组缩成一个带权点（cnt），组内成员互相支配，
// 故该组每人的答案 = 其他组贡献加权和 res + (cnt - 1)。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;

struct Node {
    int a, b, c, cnt, res;
};

Node p[MAXN], tmp[MAXN];
int bit[MAXN * 2];
int K;

void add(int i, int v) { for (; i <= K; i += i & -i) bit[i] += v; }
int ask(int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }

// p[l..r] 按 a 有序（外层），分治内部维护按 b 归并
void cdq(int l, int r) {
    if (l == r) return;
    int mid = (l + r) >> 1;
    cdq(l, mid);
    cdq(mid + 1, r);
    // 统计左半（a 更小或相等）对右半的贡献
    int i = l, j = mid + 1;
    while (j <= r) {
        while (i <= mid && p[i].b <= p[j].b) {
            add(p[i].c, p[i].cnt);
            i++;
        }
        p[j].res += ask(p[j].c);
        j++;
    }
    for (int q = l; q < i; q++) add(p[q].c, -p[q].cnt);  // 只清除真正插入过的
    // 按 b 归并，保持左右两半各自按 b 有序，供上层使用
    i = l; j = mid + 1;
    int t = l;
    while (i <= mid && j <= r) tmp[t++] = (p[i].b <= p[j].b) ? p[i++] : p[j++];
    while (i <= mid) tmp[t++] = p[i++];
    while (j <= r) tmp[t++] = p[j++];
    for (int q = l; q <= r; q++) p[q] = tmp[q];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<array<int, 3>> raw(n);
    for (int i = 0; i < n; i++) cin >> raw[i][0] >> raw[i][1] >> raw[i][2];

    // 按 (a,b,c) 排序并去重压缩
    vector<array<int, 3>> s = raw;
    sort(s.begin(), s.end());
    int m = 0;
    K = 0;
    for (int i = 0; i < n; ) {
        int j = i;
        while (j < n && s[j] == s[i]) j++;
        m++;
        p[m] = {s[i][0], s[i][1], s[i][2], j - i, 0};
        K = max(K, s[i][2]);
        i = j;
    }

    cdq(1, m);

    // 建立三元组 -> 组内答案的映射
    map<array<int, 3>, int> groupAns;
    for (int i = 1; i <= m; i++)
        groupAns[{p[i].a, p[i].b, p[i].c}] = p[i].res + p[i].cnt - 1;

    for (int i = 0; i < n; i++)
        cout << groupAns[raw[i]] << "\n";
    return 0;
}
