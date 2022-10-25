def fibonacci(m, n): 
	a = m
	b = n
	while a < max:
         yield a
         a, b = b, a+b
      