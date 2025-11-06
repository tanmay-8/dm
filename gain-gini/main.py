import csv
import math
from collections import Counter, defaultdict


def read_data(filename):
    """Read CSV file and return list of rows (as dicts) and list of fieldnames."""
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
        fieldnames = reader.fieldnames or []
    return rows, fieldnames


def entropy(values, name=None):
    """Compute entropy for a list of categorical values."""
    total = len(values)
    if total == 0:
        return 0.0
    counts = Counter(values)
    ent = 0.0
    for c in counts.values():
        p = c / total
        if p > 0:
            ent -= p * math.log2(p)
    if name:
        print(f"Entropy of {name}: {ent:.4f}")
    return ent


def gini_index(values, name=None):
    """Compute Gini index for a list of categorical values."""
    total = len(values)
    if total == 0:
        return 0.0
    counts = Counter(values)
    gini = 1.0
    for c in counts.values():
        p = c / total
        gini -= p * p
    if name:
        print(f"Gini index of {name}: {gini:.4f}")
    return gini


def info_gain(rows, attr, target):
    """Compute information gain of splitting on attr for target."""
    target_values = [r[target] for r in rows]
    total_entropy = entropy(target_values, name=target)
    weighted_entropy = 0.0
    groups = defaultdict(list)
    for r in rows:
        groups[r[attr]].append(r)
    for val, subset in groups.items():
        weight = len(subset) / len(rows)
        subset_targets = [r[target] for r in subset]
        ent = entropy(subset_targets)
        weighted_entropy += weight * ent
        print(f"  {attr}={val}: weight={weight:.3f}, entropy={ent:.4f}")
    gain = total_entropy - weighted_entropy
    print(f"Information Gain for {attr}: {gain:.4f}")
    return gain


def gini_split(rows, attr, target):
    """Compute weighted Gini index (Gini split) for attr."""
    weighted_gini = 0.0
    groups = defaultdict(list)
    for r in rows:
        groups[r[attr]].append(r)
    for val, subset in groups.items():
        weight = len(subset) / len(rows)
        subset_targets = [r[target] for r in subset]
        g = gini_index(subset_targets)
        weighted_gini += weight * g
        print(f"  {attr}={val}: weight={weight:.3f}, gini={g:.4f}")
    print(f"Gini Split for {attr}: {weighted_gini:.4f}")
    return weighted_gini


def main():
    target = input("Enter target (class) column name: ").strip()
    rows, fieldnames = read_data('data.csv')
    if not fieldnames:
        print("No columns found in data.csv")
        return
    if target == '':
        print("No target provided. Available columns:", ", ".join(fieldnames))
        return
    if target not in fieldnames:
        print(f"Target '{target}' not found in columns: {fieldnames}")
        return

    results = []
    for col in fieldnames:
        if col == target:
            continue
        print(f"\n--- Attribute: {col} ---")
        gain = info_gain(rows, col, target)
        gini = gini_split(rows, col, target)
        results.append({"attribute": col, "gain": f"{gain:.6f}", "gini": f"{gini:.6f}"})

    # write results to CSV
    out_fields = ['attribute', 'gain', 'gini']
    with open('gain_gini_output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print("\nResults saved to gain_gini_output.csv")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
