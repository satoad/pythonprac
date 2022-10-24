w = eval(input())

words = {}

while a := input():
    a = ''.join([i if i.isalpha() else ' ' for i in a])

    a = a.split()
    for i in a:
        if i in words.keys():
            words[i] += 1
        elif len(i) == w:
            words[i] = 1


max1 = 0
for i in words.keys():
    if words[i] > max1:
        max1 = words[i]


for i in words.keys():
    if words[i] == max1:
        print(i, end=' ')