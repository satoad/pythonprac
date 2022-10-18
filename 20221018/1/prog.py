a = input().lower()
b = {}

for i in a:
    if i.isalpha():
        b[i] = 1

print(len(b))