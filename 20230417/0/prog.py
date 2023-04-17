def sqroots(coeffs:str) -> str:
    coeffs = coeffs.split()
    a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
    d = b ** 2 - 4 * a * c
    
    if d < 0:
        raise AttributeError
    elif d == 0:
        return (-b/(2 * a), -b/(2 * a))
    else:
        root1 = (-b + d**0.5) / (2 * a)
        root2 = (-b - d**0.5) / (2 * a)
        return (min(root1, root2), max(root1, root2))
