from typing import Callable

def root_find(f: Callable[[float], float], fprime, guess, tol):
    """Given the function `f` and derivative `fprime`, find the input `x` such that `f(x)=0`"""
    diff = tol
    xp1 = guess

    iterate = lambda x: x - (f(x) / (fprime(x)))

    while diff >= tol:
        x = xp1
        xp1 = iterate(x)
        diff = abs(xp1 - x)
    
    return xp1