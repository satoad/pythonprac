import sys

a = sys.stdin.buffer.read()
sys.stdout.buffer.write(a[0:1])

for i in sorted([a[1:][i * (len(a) - 1) // a[0]:(i+1) * (len(a) - 1) // a[0]] for i in range(0, a[0])]):
    sys.stdout.buffer.write(i)
