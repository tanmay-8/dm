import csv


def read_data(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        fieldnames = [c.lower().strip() for c in (reader.fieldnames or [])]
        for r in reader:
            norm = {}
            for k, v in r.items():
                key = k.lower().strip() if k is not None else ''
                norm[key] = '' if v is None else str(v).lower().strip()
            rows.append(norm)
    return rows, fieldnames


def main():
    rows, columns = read_data('data.csv')
    print('Available columns:', ', '.join(columns))
    target_col = input('\nEnter target (class) column name: ').strip().lower()
    if target_col not in columns:
        raise SystemExit(f"Column '{target_col}' not found in data.")
    feature_cols = [c for c in columns if c != target_col]
    total_rows = len(rows)
    class_counts = {}
    for r in rows:
        key = r.get(target_col, '')
        class_counts[key] = class_counts.get(key, 0) + 1
    base_prob = {cls: count / total_rows for cls, count in class_counts.items()}
    print('\nStep 1: Base Probability (P(Class))')
    for cls, count in class_counts.items():
        print(f"P({cls}) = {count}/{total_rows} = {base_prob[cls]:.3f}")
    print('\nStep 2: Enter new case')
    new_case = {}
    for col in feature_cols:
        val = input(f'  {col}: ').strip().lower()
        new_case[col] = val
    print('\nNew Case:')
    for k, v in new_case.items():
        print(f'  {k.capitalize()} = {v}')
    print('\nStep 3: Feature Probabilities P(feature=value | class)')
    feature_probs = {}
    classes = list(class_counts.keys())
    for cls in classes:
        subset = [r for r in rows if r.get(target_col, '') == cls]
        total_in_class = len(subset)
        feature_probs[cls] = {}
        print(f'\nFor class = {cls} (Total = {total_in_class})')
        for feature, value in new_case.items():
            count_match = sum(1 for r in subset if r.get(feature, '') == value)
            prob = count_match / total_in_class if total_in_class > 0 else 0
            feature_probs[cls][feature] = prob
            print(f'P({feature}={value} | {cls}) = {count_match}/{total_in_class} = {prob:.3f}')
    print('\nStep 4: Final Probability (Base × All Features)')
    final_prob = {}
    for cls in feature_probs:
        product = 1
        for feature, prob in feature_probs[cls].items():
            product *= prob
        final_prob[cls] = base_prob[cls] * product
        print(f'P({cls}) × Π P(feature|{cls}) = {base_prob[cls]:.3f} × {product:.6f} = {final_prob[cls]:.6f}')
    print('\nStep 5: Compare Final Probabilities')
    for cls, prob in final_prob.items():
        print(f'Final probability for {cls}: {prob:.6f}')
    predicted = max(final_prob, key=final_prob.get)
    print(f"\nPredicted Class for the new case: {predicted.capitalize()}")
    output = {**new_case, 'Predicted_Class': predicted}
    out_fields = feature_cols + ['Predicted_Class']
    with open('bayes_output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerow(output)
    print("\nResult saved to 'bayes_output.csv'.")


if __name__ == '__main__':
    main()