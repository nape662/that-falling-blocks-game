
a = [[0 for _ in range(3)] for _ in range(4)]
b = [i for i in range(3)]
c = [1, 2, 3]
print(a[1])
print(b)
print(c[1])

def rooty():
    res = 0
    for i in range(10, 101):
        k = i
        print("{} = i".format(i))
        for j in range(i-9, i):
            print(j, end = " ")
            k *= j/(100-(i-j))
        print(k)
        res += k
    print(res)

rooty()

