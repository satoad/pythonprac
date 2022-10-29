def fib(m, n):
    fib1, fib2 = 1, 1

    i = 0
    while i < n + m:
        if i >= m:
            yield fib1
        i += 1
        fib1, fib2 = fib2, fib1 + fib2

import sys
exec(sys.stdin.read())
