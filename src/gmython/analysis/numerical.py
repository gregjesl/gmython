from typing import Callable
from .algebra import Vector3

def root_find(f: Callable[[float], float], fprime: Callable[[float], float], guess: float, tol: float = 1e-9):
    """Given the function `f` and derivative `fprime`, find the input `x` such that `f(x)=0`"""
    diff = tol
    xp1 = guess

    iterate = lambda x: x - (f(x) / (fprime(x)))

    while diff >= tol:
        x = xp1
        xp1 = iterate(x)
        diff = abs(xp1 - x)
    
    return xp1

def _rk4_step(f: Callable[[float, Vector3], Vector3], t: float, delta: float, x: Vector3):
    k1: Vector3 = f(t, x)
    k2: Vector3 = f(t + (delta / 2.0), x + (k1 * (delta / 2.0)))
    k3: Vector3 = f(t + (delta / 2.0), x + (k2 * (delta / 2.0)))
    k4: Vector3 = f(t + delta, x + (k3 * delta))
    return x + ((k1 + (k2 * 2.0) + (k3 * 2.0) + k4) * (delta / 6.0))

def rk4_propagate(f: Callable[[float, Vector3], Vector3], t0: float, delta: float, x0: Vector3, steps: int):
    """Propagate a system using the Runge-Kutta 4 algorithm"""
    if steps < 0:
        raise ValueError("Number of steps must be positive")

    # Initialize the results
    results = [Vector3.zeros() for _ in range(steps + 1)]
    results[0] = x0

    # Run the steps
    for i in range(steps):
        t = t0 + (delta * i)
        results[i + 1] = (_rk4_step(f, t, delta, results[i]))

    # Return the results
    return results