from math import *

funcs = dict()

count1 = 0
count2 = 0

a = input()
while a.split()[0] != 'quit':
    count1 += 1
    if a[0] == ':':
        count2 += 1

        b = a[1:].split()

        funcs[b[0]] = 'eval(\'' + b[-1] + '\',globals(),{'

        for i in range(1, len(b) - 1):
            funcs[b[0]] += '\"' + b[i] + '\": '
            if i != len(b) - 2:
               funcs[b[0]] += ','
        funcs[b[0]] += '})'

    else:
        b = a.split()
        if b[0] in funcs.keys():
            tmp = funcs[b[0]].split()
            cmd = tmp[0]
            for i in range(1, len(b)):
                cmd += b[i] + tmp[i]

            print(eval(cmd))

    a = input()

print(eval(a[len(a.split()[0]):] + '.format(' + str(count2 + 1) + ',' + str(count1 + 1) + ')'))