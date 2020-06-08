

def factorial(n: int):
    r = n
    for i in range(1, n, 1)[::-1]:
        r *= i
    return r


def permutations_with_replacement(n: int, r: int):
    return n**r


def permutations_without_replacement(n: int, r: int):
    return int(factorial(n) / factorial(n-r))


def combinations_without_replacement(n: int, r: int):
    return int(factorial(n) / (factorial(r) * factorial(n-r)))
