m, n = eval(input())
print([i for i in range(m, n) if (all((i % j != 0) for j in range(2, i)) and i >= 2)])