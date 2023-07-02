
a = [[0 for _ in range(3)] for _ in range(4)]
b = [i for i in range(3)]
c = [1, 2, 3]
print(a[1])
print(b)
print(c[1])


def rooty(n, att):
    res = 0
    for i in range(att, 101):
        k = i / 100 * att
        for j in range(i+1-att, i):
            k *= j/(100-(i-j))
        res += k
    print(res)


for i in range(1, 11):
    rooty(100, i)
