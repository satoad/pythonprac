sum = 0
while sum <= 21:
    a = eval(input())
    
    if a <= 0:
        print(a)
        break
        
    sum += a
else:
    print(sum)
