a = eval(input())

i = 0
while i <= 2:
    j = 0;
    while j <= 2:
        mul = (a + i) * (a + j)
        s = sum(map(int, str(mul)))
    
        if s == 6:
            mul = ":=)"
        
        print(a + i, "*", a + j, "=", mul, end=" ")
        j += 1
    print()
    i += 1
