from fractions import Fraction


def is_root(x, b, coeffs, Type):
    numerator = sum([Type(coeff) * Type(x) ** i for i, coeff in enumerate(reversed(coeffs[1:int(coeffs[0]) + 2]))])

    denominator = sum([Type(coeff) * Type(x) ** i for i, coeff in enumerate(reversed(coeffs[int(coeffs[0]) + 3:]))])

    return numerator / denominator == Type(b) if denominator else False


s, w, *pol_coeffs = input().split(',')
print(is_root(s, w, pol_coeffs, Fraction))