import csv
import itertools
import math

DATA_PATH = "data.csv"
OUT_PATH = "dbscan.csv"


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def region_query(rows, point_idx, eps):
    p = rows[point_idx]
    neighbors = []
    for j, q in enumerate(rows):
        if dist(p, q) <= eps:
            neighbors.append(j)
    return neighbors


def dbscan(rows, eps, min_samples):
    n = len(rows)
    labels = [None] * n
    cluster_id = 0

    for i in range(n):
        if labels[i] is not None:
            continue

        neighbors = region_query(rows, i, eps)
        if len(neighbors) < min_samples:
            labels[i] = -1
            continue

        labels[i] = cluster_id
        seeds = neighbors.copy()
        k = 0
        while k < len(seeds):
            j = seeds[k]
            if labels[j] is None:
                labels[j] = cluster_id
                j_neighbors = region_query(rows, j, eps)
                if len(j_neighbors) >= min_samples:
                    for nb in j_neighbors:
                        if nb not in seeds:
                            seeds.append(nb)
            elif labels[j] == -1:
                labels[j] = cluster_id
            k += 1

        cluster_id += 1

    return labels


def main():
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_rows = [row for row in reader]
        fieldnames = reader.fieldnames or []

    if not fieldnames:
        raise SystemExit("No columns found in the CSV.")

    
    
    num_cols = []
    for col in fieldnames:
        ok = False
        all_ok = True
        for r in all_rows:
            v = r.get(col, "").strip()
            if v == "":
                continue
            ok = True
            try:
                float(v)
            except Exception:
                all_ok = False
                break
        if ok and all_ok:
            num_cols.append(col)

    if not num_cols:
        raise SystemExit("No numeric columns found in the CSV.")

    
    rows = []
    indexes = []
    for idx, r in enumerate(all_rows):
        vals = []
        skip = False
        for c in num_cols:
            v = r.get(c, "").strip()
            if v == "":
                skip = True
                break
            try:
                vals.append(float(v))
            except Exception:
                skip = True
                break
        if not skip:
            rows.append(vals)
            indexes.append(idx)

    try:
        eps = float(input("Enter neighborhood radius eps : ").strip())
    except Exception:
        eps = 0.5
    try:
        min_samples = int(input("Enter min_samples : ").strip())
    except Exception:
        min_samples = 5
    if eps <= 0:
        eps = 0.5
    if min_samples < 1:
        min_samples = 1

    labels = dbscan(rows, eps, min_samples)

    out_fieldnames = fieldnames[:]
    if "cluster" not in out_fieldnames:
        out_fieldnames.append("cluster")

    
    for r in all_rows:
        r["cluster"] = ""

    for idx, lbl in zip(indexes, labels):
        all_rows[idx]["cluster"] = str(int(lbl))

    
    with open(OUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)

    n_noise = sum(1 for l in labels if l == -1)
    cluster_ids = sorted(set(l for l in labels if l is not None and l >= 0))
    counts = {cid: labels.count(cid) for cid in cluster_ids}

    print(f"\nDBSCAN results (eps={eps}, min_samples={min_samples}):")
    print("Clusters and sizes:")
    for cid in cluster_ids:
        print(f"  Cluster {cid}: {counts[cid]} points")
    print(f"  Noise: {n_noise} points")


if __name__ == "__main__":
    main()
