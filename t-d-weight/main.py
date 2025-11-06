import csv

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    data = [row for row in reader]

group_cols = header[1:]
rows = []

for row in data:
    class_name = row[0]
    values = list(map(int, row[1:]))
    total = sum(values)
    rows.append([class_name] + values + [total])

totals = [sum(col) for col in zip(*[r[1:] for r in rows])]
total_per_class = [r[-1] for r in rows]

out_header = header + ["TOTAL"]
for col in group_cols:
    out_header.append(f"T-weight ({col})")
    out_header.append(f"D-weight ({col})")

out_rows = []
for r in rows:
    class_name = r[0]
    values = r[1:-1]
    total = r[-1]
    new_row = [class_name] + values + [total]

    for i, col in enumerate(group_cols):
        new_row.append(values[i] / totals[i])
        new_row.append(values[i] / total)

    out_rows.append(new_row)

print("\n=== Generalized T-weight & D-weight Table ===\n")
print(out_header)
for r in out_rows:
    print(r)

with open("output_weights.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(out_header)
    writer.writerows(out_rows)
