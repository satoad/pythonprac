a = []
a.append(eval(input()))

n = len(a[0])

for i in range(n - 1):
    a.append(eval(input()))
    

b = []
for i in range(n):
    b.append(eval(input()))

c = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
    for j in range(n):
        for g in range(n):
            c[i][j] += a[i][g] * b[g][j]
        print(c[i][j], end='')

        if j != n - 1:
            print(',', end='')
    print()