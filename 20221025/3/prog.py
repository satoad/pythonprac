from itertools import combinations_with_replacement

sample = 'TOR'
num = eval(input())

if num > len(sample) * 2:
    text = sample * (num // len(sample))
    if num % len(sample) != 0:
        text += sample

    ans = list(sorted(set((filter(lambda x: ''.join(x).count(sample) == 2, combinations_with_replacement(text, num)))))) #cringe

    for i in range(len(ans)):
        print(*ans[i], sep='', end='')
        if i != len(ans) - 1:
            print(',', end=' ')

elif num == len(sample) * 2:
    print(sample * 2, end='')