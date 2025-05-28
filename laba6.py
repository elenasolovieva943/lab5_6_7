import time
import math

def F_recursive(n):
    if n == 0 or n == 1:
        return 1
    return (-1)**n * (F_recursive(n - 1) / math.factorial(n) + F_recursive(n - 2) / math.factorial(2 * n))

def F_iterative(n):
    if n == 0 or n == 1:
        return 1
    F0, F1 = 1, 1
    for i in range(2, n + 1):
        Fi = (-1)**i * (F1 / math.factorial(i) + F0 / math.factorial(2 * i))
        F0, F1 = F1, Fi
    return F1

def compare_methods(max_n):
    print(f"{'n':<5} {'Рекурсивный':<15} {'Итеративный':<15}")
    for n in range(max_n + 1):
            start = time.time()
            F_recursive(n)
            rec_time = time.time() - start

            start = time.time()
            F_iterative(n)
            iter_time = time.time() - start

            print(f"{n:<5} {rec_time:<15.8f} {iter_time:<15.8f}")

compare_methods(15)