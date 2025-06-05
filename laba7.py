import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import time

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

def measure_time(func, n):
    start = time.perf_counter()
    try:
        result = func(n)
        duration = (time.perf_counter() - start)
        return result, duration
    except RecursionError:
        return "RecursionError", None

def compare_performance():
    output_text.delete(1.0, tk.END)
    try:
        max_n = int(max_n_entry.get())
    except ValueError:
        output_text.insert(tk.END, "n:\n")
        return

    headers = f"{'n':<3} | {'Итеративный':<22} | {'Рекурсивный':<22} | {'Время итерации':<22} | {'Время рекурсии'}"
    output_text.insert(tk.END, headers + "\n")

    for n in range(max_n + 1):
        iter_val, iter_time = measure_time(F_iterative, n)
        rec_val, rec_time = measure_time(F_recursive, n)

        iter_val_str = f"{iter_val:.14e}" if isinstance(iter_val, (int, float)) else str(iter_val)
        rec_val_str = f"{rec_val:.14e}" if isinstance(rec_val, (int, float)) else str(rec_val)

        iter_time_us = f"{iter_time * 1e6:.2f}" if iter_time is not None else "-"
        rec_time_us = f"{rec_time * 1e6:.2f}" if rec_time is not None else "-"

        line = f"{n:<3} | {iter_val_str:<22} | {rec_val_str:<22} | {iter_time_us:<22} | {rec_time_us}"
        output_text.insert(tk.END, line + "\n")
        output_text.update()

root = tk.Tk()
root.title("7 лаба")
root.geometry("900x400")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

control_frame = ttk.Frame(main_frame)
control_frame.pack(fill=tk.X, pady=5)

ttk.Label(control_frame, text="Максимальное n:").pack(side=tk.LEFT)
max_n_entry = ttk.Entry(control_frame, width=10)
max_n_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Сравнить", command=compare_performance).pack(side=tk.LEFT, padx=10)

output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=100, height=25)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
