a = list(eval(input()))

n = len(a)
for i in range(n):
	for j in range(i + 1, n):
		if a[i] **2 % 100 > a[j] **2 % 100:
			a[i], a[j] = a[j], a[i]

print(a)