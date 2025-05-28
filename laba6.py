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
    for i in range(2, n + 1):
        sign = -1 if i % 2 else 1
        Fi = sign * (F1 / math.factorial(i) + F0 / math.factorial(2 * i))
        F0, F1 = F1, Fi
    return F1

def compare_methods(n_max):
    print(f"{'n':<3} | {'Итерационное':<22} | {'Рекурсия':<32} | {'Время итерации':<19} | {'Время рекурсии':<19}")
    print("-" * 110)
    for n in range(n_max + 1):
            start = time.perf_counter()
            fi = F_iterative(n)
            t1 = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            fr = F_recursive(n)
            t2 = (time.perf_counter() - start) * 1000

            print(f"{n:<3} | {fi:<22.14e} | {fr:<32.14e} | {t1:<19.5f} | {t2:<19.5f}")

if __name__ == "__main__":
    compare_methods(15)