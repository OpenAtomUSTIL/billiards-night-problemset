// T33【省选/NOI-】最后三堆球
// 算法：Nim 博弈 —— 先手必胜当且仅当各堆异或和非零
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        long long xr = 0, a;
        for (int i = 0; i < n; i++) {
            cin >> a;
            xr ^= a;
        }
        cout << (xr ? "Xiaomin" : "Xiaoxin") << "\n";
    }
    return 0;
}
