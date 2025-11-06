import csv
import math


def normalize_decimal(value, factor):
    return value / (10 ** factor)


def normalize_zscore(value, mean, stddev):
    if stddev == 0:
        return 0
    return (value - mean) / stddev

def normalize_minmax(value, old_min, old_max, new_min, new_max):
    if old_max == old_min:
        return new_min
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

input_file = "data.csv"

try:
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader if len(row) == len(header)]
except FileNotFoundError:
    print("Error: Could not open input file.")
    exit(1)

cols = len(header)
numeric = [[] for _ in range(cols)]

for row in rows:
    for i in range(cols):
        try:
            numeric[i].append(float(row[i]))
        except ValueError:
            pass

print("Choose normalization method:")
print("1. Decimal Scaling\n2. Z-Score Normalization\n3. Min-Max Normalization")
choice = int(input("Enter choice: "))

new_min, new_max = 0, 1
if choice == 3:
    new_min = float(input("Enter new Min: "))
    new_max = float(input("Enter new Max: "))

if choice == 1:
    output_file = "out_decimal.csv"
elif choice == 2:
    output_file = "out_zscore.csv"
elif choice == 3:
    output_file = "out_minmax.csv"
else:
    print("Invalid option!")
    exit(1)

min_val = [float('inf')] * cols
max_val = [float('-inf')] * cols
mean = [0] * cols
stddev = [0] * cols
scale_factor = [0] * cols

for i in range(cols):
    if not numeric[i]:
        continue
    min_val[i] = min(numeric[i])
    max_val[i] = max(numeric[i])
    mean[i] = sum(numeric[i]) / len(numeric[i])
    stddev[i] = math.sqrt(
        sum((v - mean[i]) ** 2 for v in numeric[i]) / len(numeric[i]))
    max_abs = max(abs(v) for v in numeric[i])
    while max_abs / (10 ** scale_factor[i]) >= 1:
        scale_factor[i] += 1

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows:
        new_row = []
        for i in range(cols):
            try:
                val = float(row[i])
                if choice == 1:
                    norm = normalize_decimal(val, scale_factor[i])
                elif choice == 2:
                    norm = normalize_zscore(val, mean[i], stddev[i])
                elif choice == 3:
                    norm = normalize_minmax(
                        val, min_val[i], max_val[i], new_min, new_max)
                new_row.append(round(norm, 4))
            except ValueError:
                new_row.append(row[i])
        writer.writerow(new_row)

print(f"Normalization complete. Output written to {output_file}")
