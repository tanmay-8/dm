import csv

def read_data(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
        fieldnames = reader.fieldnames or []
    return rows, [c for c in fieldnames]

def linear_regression(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    print(f"Mean of X: {mean_x:.4f}")
    print(f"Mean of Y: {mean_y:.4f}")
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den = sum((xi - mean_x) ** 2 for xi in x)
    print(f"Numerator (Σ(xi - x̄)(yi - ȳ)): {num:.4f}")
    print(f"Denominator (Σ(xi - x̄)^2): {den:.4f}")
    slope = num / den if den != 0 else 0
    intercept = mean_y - slope * mean_x
    print(f"Slope (b1): {slope:.4f}")
    print(f"Intercept (b0): {intercept:.4f}")
    return slope, intercept

def main():
    rows, cols = read_data('data.csv')
    x_col = input("Enter independent variable (X) column name: ")
    y_col = input("Enter dependent variable (Y) column name: ")
    x = []
    y = []
    for r in rows:
        try:
            xv = float(r.get(x_col, '').strip())
            yv = float(r.get(y_col, '').strip())
        except Exception:
            continue
        x.append(xv)
        y.append(yv)
    slope, intercept = linear_regression(x, y)
    print(f"\nRegression equation: {y_col} = {intercept:.4f} + {slope:.4f}*{x_col}")
    predicted = [intercept + slope * xi for xi in x]
    fieldnames = [x_col, y_col, 'Predicted']
    with open('linear_regression_output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for xi, yi, pi in zip(x, y, predicted):
            writer.writerow({x_col: xi, y_col: yi, 'Predicted': pi})
    print("\nResults saved to linear_regression_output.csv")

if __name__ == "__main__":
    main()
