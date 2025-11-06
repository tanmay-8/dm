import random
import csv

path = "data.csv"
out_path = "k-means.csv"
random.seed(42)

# Read CSV and detect numeric columns
with open(path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    all_rows = [row for row in reader]

# determine numeric column indexes: consider a column numeric if all non-empty values parse as float
num_cols_idx = []
for ci, col in enumerate(header):
    is_num = True
    for r in all_rows:
        try:
            val = r[ci]
        except Exception:
            val = ''
        if str(val).strip() == '':
            continue
        try:
            float(val)
        except Exception:
            is_num = False
            break
    if is_num:
        num_cols_idx.append(ci)

num_cols = [header[i] for i in num_cols_idx]
if not num_cols:
    raise SystemExit("No numeric columns found in the CSV.")

# build numeric rows and keep original indexes (row positions in the CSV data)
rows = []
indexes = []
for idx, r in enumerate(all_rows):
    try:
        vals = [float(r[i]) for i in num_cols_idx]
    except Exception:
        continue
    rows.append(vals)
    indexes.append(idx)

try:
    k = int(input("Enter number of clusters k: ").strip())
except Exception:
    k = 3
if k < 1:
    k = 1
if k > len(rows):
    k = len(rows)


def euclid(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

def write_step_matrix(step_name, rows_data, centers, csv_path):
    labels = [f"p{i+1}" for i in range(len(rows_data))]
    matrix = []
    for i in range(len(rows_data)):
        row_vals = []
        for j in range(len(rows_data)):
            if i == j:
                row_vals.append(0.0)
            elif i > j:
                row_vals.append(euclid(rows_data[i], rows_data[j]))
            else:
                row_vals.append("")
        matrix.append(row_vals)

    with open(csv_path, "a", newline="") as f:
        f.write(f"Step:,{step_name}\n")
        f.write("," + ",".join(labels) + "\n")
        for i in range(len(rows_data)):
            values = [
                (f"{v:.4f}" if isinstance(v, float) else str(v)) for v in matrix[i]
            ]
            f.write(labels[i] + "," + ",".join(values) + "\n")

        for ci, c in enumerate(centers):
            dists = [f"{euclid(c, rows_data[j]):.4f}" for j in range(
                len(rows_data))]
            f.write(f"c{ci+1}," + ",".join(dists) + "\n")
        f.write("\n")


def mean_point(points):
    n = len(points)
    dim = len(points[0])
    return [sum(p[i] for p in points) / n for i in range(dim)]


centroids = [list(rows[i]) for i in random.sample(range(len(rows)), k)]
print("Initial centers:")
for idx, c in enumerate(centroids):
    print(f" Center {idx}: " + ", ".join(f"{x:.4f}" for x in c))

steps_csv_path = "k-means-out.csv"
open(steps_csv_path, "w").close()
write_step_matrix("init", rows, centroids, steps_csv_path)

max_iters = 1000
for step in range(max_iters):
    clusters = [[] for _ in range(k)]
    labels = []
    all_dists = []
    for row_idx, x in enumerate(rows):
        dists = [euclid(x, c) for c in centroids]
        idx = dists.index(min(dists))
        labels.append(idx)
        clusters[idx].append(x)
        all_dists.append(dists)

    write_step_matrix(f"iter_{step}", rows, centroids, steps_csv_path)

    new_centroids = []
    changed = False
    for i in range(k):
        if clusters[i]:
            new_c = mean_point(clusters[i])
        else:
            new_c = list(rows[random.randrange(len(rows))])
        new_centroids.append(new_c)
        if not changed:
            for a, b in zip(new_c, centroids[i]):
                if abs(a - b) > 1e-8:
                    changed = True
                    break

    centroids = new_centroids
    if not changed:
        break

counts = [labels.count(i) for i in range(k)]

# write output CSV: original rows with appended cluster column
cluster_map = {orig_idx: lbl for orig_idx, lbl in zip(indexes, labels)}
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header + ['cluster'])
    for i, row in enumerate(all_rows):
        out_row = list(row)
        # pad row to header length if necessary
        if len(out_row) < len(header):
            out_row += [''] * (len(header) - len(out_row))
        cluster_val = ''
        if i in cluster_map:
            cluster_val = int(cluster_map[i])
        out_row.append(cluster_val)
        writer.writerow(out_row)

print("\nFinal cluster sizes:", counts)
print("Final centroids:")
for i, c in enumerate(centroids):
    print(f" C{i}: " + ", ".join(f"{x:.4f}" for x in c))
