// T11【普及+/提高】小欣的咒语
// 算法：KMP 字符串匹配（允许重叠计数）
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string T, S;
    cin >> T >> S;
    int n = T.size(), m = S.size();

    vector<int> nxt(m);
    for (int i = 1, j = 0; i < m; i++) {
        while (j > 0 && S[i] != S[j]) j = nxt[j - 1];
        if (S[i] == S[j]) j++;
        nxt[i] = j;
    }

    long long cnt = 0;
    for (int i = 0, j = 0; i < n; i++) {
        while (j > 0 && (j == m || T[i] != S[j])) j = nxt[j - 1];
        if (T[i] == S[j]) j++;
        if (j == m) {                        // 匹配成功
            cnt++;
            j = nxt[j - 1];                  // 允许重叠：退到最长公共前后缀继续
        }
    }
    cout << cnt << "\n";
    return 0;
}
