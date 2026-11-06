// T15【提高+/省选-】巅峰时刻
// 算法：单调队列求滑动窗口最大值，O(n)
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    deque<int> dq;                     // 存下标，对应值单调递减
    for (int i = 0; i < n; i++) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) {
            if (i > k - 1) cout << " ";
            cout << a[dq.front()];
        }
    }
    cout << "\n";
    return 0;
}
