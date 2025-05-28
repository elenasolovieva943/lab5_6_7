import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import time

def F_recursive(n):
    if n == 0 or n == 1:
        return 1
    return (-1) ** n * (F_recursive(n - 1) / math.factorial(n) + F_recursive(n - 2) / math.factorial(2 * n))


def F_iterative(n):
    if n == 0 or n == 1:
        return 1
    F0, F1 = 1, 1
    for i in range(2, n + 1):
        Fi = (-1) ** i * (F1 / math.factorial(i) + F0 / math.factorial(2 * i))
        F0, F1 = F1, Fi
    return F1


def compare_performance():
        max_n = int(max_n_entry.get())

        headers = f"{'n':<5}  {'Рекурсивный':<20}  {'Итеративный':<20}"
        output_text.insert(tk.END, headers + "\n")

        for n in range(max_n + 1):
            rec_time = measure_time(F_recursive, n)
            iter_time = measure_time(F_iterative, n)

            result_line = f"{n:<5}  {rec_time * 1e6:<20.2f}  {iter_time * 1e6:<20.2f}"
            output_text.insert(tk.END, result_line + "\n")

            output_text.see(tk.END)
            output_text.update()

def measure_time(func, n):
        start_time = time.perf_counter()
        func(n)
        return time.perf_counter() - start_time

root = tk.Tk()
root.title("7 лаба")
root.geometry("400x300+400+200")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

control_frame = ttk.Frame(main_frame)
control_frame.pack(fill=tk.X, pady=5)

ttk.Label(control_frame, text="n:").pack(side=tk.LEFT)
max_n_entry = ttk.Entry(control_frame, width=10)
max_n_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Сравнить", command=compare_performance).pack(side=tk.LEFT)

output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=70, height=25)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()