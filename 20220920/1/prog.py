a = eval(input())

if a % 25 == 0:
    if a % 2 == 0:
        print("A + B - ", end='')
    else:
        print("A - B + ", end='')
else:
    print("A - B - ", end='')
    
if a % 8 == 0:
    print("C +")
else:
    print("C -")
