import pandas as pd

path = "data.csv"
out_path = "heirarchial-single.csv"
matrix_path = "heirarchial-single-steps.csv"

df = pd.read_csv(path)
num_cols = list(df.select_dtypes(include="number").columns)
if not num_cols:
    raise SystemExit("No numeric columns found in the CSV.")

df_num = df[num_cols].dropna()
rows = df_num.values.tolist()
indexes = df_num.index.tolist()

def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

def write_step_matrix(step_name, clusters_data, csv_path):
    labels = ["|".join(f"p{i+1}" for i in sorted(cluster)) for cluster in clusters_data]
    n = len(clusters_data)
    matrix = []
    for i in range(n):
        row_vals = []
        for j in range(n):
            if i == j:
                row_vals.append(0.0)
            elif i > j:
                min_d = float("inf")
                for a in clusters_data[i]:
                    for b in clusters_data[j]:
                        d = dist(rows[a], rows[b])
                        if d < min_d:
                            min_d = d
                row_vals.append(min_d)
            else:
                row_vals.append("")
        matrix.append(row_vals)
    with open(csv_path, "a", newline="") as f:
        f.write(f"Grouping:,{step_name}\n")
        f.write("," + ",".join(labels) + "\n")
        for i in range(n):
            values = [(f"{v:.4f}" if isinstance(v, float) else str(v)) for v in matrix[i]]
            f.write(labels[i] + "," + ",".join(values) + "\n")
        f.write("\n")


clusters = [[i] for i in range(len(rows))]
open(matrix_path, "w").close()
write_step_matrix("initial", clusters, matrix_path)
labels_print = [f"p{i+1}" for i in range(len(rows))]
print("Grouping: initial")
for gi, g in enumerate(clusters):
    print(f"group{gi+1}: " + "|".join(labels_print[idx] for idx in g))
print()


def cluster_distance(c1, c2):
    m = float("inf")
    for i in c1:
        for j in c2:
            d = dist(rows[i], rows[j])
            if d < m:
                m = d
    return m


step_idx = 1
while len(clusters) > 1:
    best_i, best_j, best_d = None, None, float("inf")
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            d = cluster_distance(clusters[i], clusters[j])
            if d < best_d:
                best_d = d
                best_i, best_j = i, j
    merged = clusters[best_i] + clusters[best_j]
    new_clusters = []
    for t, c in enumerate(clusters):
        if t != best_i and t != best_j:
            new_clusters.append(c)
    new_clusters.append(merged)
    clusters = new_clusters
    write_step_matrix(f"grouping_{step_idx}", clusters, matrix_path)
    print(f"Grouping: grouping_{step_idx} (distance merged: {best_d:.4f})")
    for gi, g in enumerate(clusters):
        print(f"group{gi+1}: " + "|".join(labels_print[idx] for idx in g))
    print()
    step_idx += 1

labels = [None] * len(rows)
for cid, c in enumerate(clusters):
    for idx in c:
        labels[idx] = cid

df_out = df.copy()
df_out["cluster"] = pd.NA
for idx, lbl in zip(indexes, labels):
    df_out.at[idx, "cluster"] = int(lbl)
df_out.to_csv(out_path, index=False)

print("Final clusters:")
for gi, g in enumerate(clusters):
    print(f"cluster{gi}: " + "|".join(labels_print[idx] for idx in g))
