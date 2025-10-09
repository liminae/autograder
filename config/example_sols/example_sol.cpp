#include <iostream>
using namespace std;

int main() {
    int e, b, m, r, x, y, z;
    cin >> e >> b >> m >> r >> x >> y >> z;

    if (b * x < 0) {
        e -= b * x;
    }
    if (m * y < 0) {
        e -= m * y;
    }
    if (r * z < 0) {
        e -= r * z;
    }

    cout << e << "\n";
    return 0;
}
