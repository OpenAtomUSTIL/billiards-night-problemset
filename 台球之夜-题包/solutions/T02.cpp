// T2【普及-】焚香压运
// 算法：模拟 + 边界截断（clamp 到 [50, 300]）
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long L = 100;
    for (int i = 0; i < n; i++) {
        string op;
        long long x;
        cin >> op >> x;
        if (op == "WIN") L += x;
        else L -= x;                 // INCENSE
        L = max(50LL, min(300LL, L)); // 截断到 [50, 300]
    }
    cout << L << "\n";
    return 0;
}
