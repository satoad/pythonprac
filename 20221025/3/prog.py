from itertools import combinations

sample = 'TOR'
num = eval(input())

text = sample * (num//len(sample))
if num % len(sample) != 0:
    text += sample

for i in sorted(filter(lambda x: ''.join(x).count(sample) >= 2, combinations(text, num))):
    print(*i, sep='', end=', ')