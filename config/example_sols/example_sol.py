e = int(input())
b, m, r = map(int, input().split())
x, y, z = map(int, input().split())

if b * x < 0:
    e -= b * x
if m * y < 0:
    e -= m * y
if r * z < 0:
    e -= r * z

print(e)
