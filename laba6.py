import time
import math

def F_recursive(n):
    if n == 0 or n == 1:
        return 1
    sign = -1 if n % 2 else 1
    return sign * (F_recursive(n - 1) / math.factorial(n) + F_recursive(n - 2) / math.factorial(2 * n))

def F_iterative(n):
    if n == 0 or n == 1:
        return 1
    F0, F1 = 1, 1
    fact_i = 1
    for i in range(2, n + 1):
        fact_i *= i
        fact_2i = 1
        for j in range(2, 2 * i + 1):
            fact_2i *= j
        sign = -1 if i % 2 else 1
        Fi = sign * (F1 / fact_i + F0 / fact_2i)
        F0, F1 = F1, Fi
    return F1

def compare_methods(n_max):
    print(f"{'n':<3} | {'Время итерации':<23} | {'Время рекурсии':<23}")
    for n in range(n_max + 1):
        start = time.perf_counter()
        F_iterative(n)
        t1 = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        F_recursive(n)
        t2 = (time.perf_counter() - start) * 1000

        print(f"{n:<3} | {t1:<23.5f} | {t2:<23.5f}")

if __name__ == "__main__":
    compare_methods(15)