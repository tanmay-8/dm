import csv
import math


def read_table(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]
    return header, rows


def try_float(s):
    try:
        return float(s)
    except Exception:
        return None


def pearson_corr(x_vals, y_vals):
    # x_vals and y_vals are lists of floats
    n = len(x_vals)
    if n == 0:
        return float('nan')
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x_vals, y_vals))
    den = math.sqrt(sum((xi - mean_x) ** 2 for xi in x_vals) * sum((yi - mean_y) ** 2 for yi in y_vals))
    return num / den if den != 0 else float('nan')


def main():
    header, rows = read_table('data.csv')
    # Determine numeric columns (exclude 'TID' if present)
    cols = [c for c in header if c != 'TID']

    pearson_results = []

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            col1 = cols[i]
            col2 = cols[j]
            x_vals = []
            y_vals = []
            # collect pairs where both are numeric
            for row in rows:
                # protect against short rows
                try:
                    a = row[header.index(col1)]
                    b = row[header.index(col2)]
                except Exception:
                    continue
                fa = try_float(a)
                fb = try_float(b)
                if fa is None or fb is None:
                    continue
                x_vals.append(fa)
                y_vals.append(fb)

            r = pearson_corr(x_vals, y_vals)
            pearson_results.append((col1, col2, r))
            print(f"Pearson correlation between {col1} and {col2}: {r}")

    # write output CSV
    with open('pearson_correlation_output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item 1', 'Item 2', 'Pearson Correlation'])
        for col1, col2, r in pearson_results:
            writer.writerow([col1, col2, f"{r}"])


if __name__ == '__main__':
    main()
