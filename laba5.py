from itertools import combinations

# Список всех рабочих: 8 мужчин и 12 женщин
all_workers = [f"M{i}" for i in range(1, 9)] + [f"W{j}" for j in range(1, 13)]
men = [w for w in all_workers if w.startswith("M")]
women = [w for w in all_workers if w.startswith("W")]

# Алгоритмический способ
def manual_schedule(workers):
    valid_schedules = []
    n = len(workers)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    for m in range(l+1, n):
                        shift1 = [workers[x] for x in [i, j, k, l, m]]
                        shift2 = [w for w in workers if w not in shift1]
                        valid_schedules.append((shift1, shift2))
    return valid_schedules

# Через itertools
def itertools_schedule(workers):
    shift_size = 5
    all_schedules = []
    for shift1 in combinations(workers, shift_size):
        shift2 = tuple(w for w in workers if w not in shift1)
        if len(shift2) == shift_size:
            all_schedules.append((shift1, shift2))
    return all_schedules

#С ограничением и целевой функцией
def optimal_schedule(men_list, women_list):
    best_schedules = []
    best_score = float('inf')

    for m_count in range(4, 9):
        for men_group in combinations(men_list, m_count):
            for women_group in combinations(women_list, 10 - m_count):
                team = list(men_group + women_group)

                for shift1 in combinations(team, 5):
                    shift2 = tuple(w for w in team if w not in shift1)
                    if len(shift2) != 5:
                        continue

                    if all(w.startswith('M') for w in shift1) or all(w.startswith('W') for w in shift1):
                        continue
                    if all(w.startswith('M') for w in shift2) or all(w.startswith('W') for w in shift2):
                        continue

                    men1 = sum(1 for w in shift1 if w.startswith("M"))
                    men2 = sum(1 for w in shift2 if w.startswith("M"))
                    score = abs(men1 - men2)

                    if score < best_score:
                        best_schedules = [(shift1, shift2)]
                        best_score = score
                    elif score == best_score:
                        best_schedules.append((shift1, shift2))

    return best_schedules

total_manual = 0
total_itertools = 0

for group in combinations(all_workers, 10):
    if sum(1 for w in group if w.startswith("M")) < 4:
        continue
    team = list(group)
    total_manual += len(manual_schedule(team))
    total_itertools += len(itertools_schedule(team))
total_optimized = len(optimal_schedule(men, women))

print(f"Алгоритмический способ: {total_manual} смен")
print(f"Через функции Python: {total_itertools} смен")
print(f"С ограничением и целевой функцией: {total_optimized} смен")