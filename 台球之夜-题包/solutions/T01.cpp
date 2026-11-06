// T1【入门】小民买单
// 算法：基础算术。找零 = 50 - 2a - 2b
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long a, b;
    cin >> a >> b;
    cout << 50 - 2 * a - 2 * b << "\n";
    return 0;
}
