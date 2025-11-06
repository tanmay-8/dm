import csv


def read_csv_rows(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = [r for r in reader]
    return rows


def parse_data(rows):
    transactions = []
    for row in rows:
        transaction = []
        for item in row:
            if item is not None and str(item).strip() != '':
                transaction.append(str(item).strip())
        transactions.append(transaction)
    return transactions

def apriori(transactions, min_support):
    if not (0 < min_support <= 1):
        raise ValueError("min_support must be between 0 and 1")

    n = len(transactions)
    min_cnt = max(1, (int)(min_support*n))

    item_cnt = {}
    for t in transactions:
        for it in t:
            if it not in item_cnt:
                item_cnt[it] = 1
            else:
                item_cnt[it] += 1

    l1 = [frozenset([it]) for it, cnt in item_cnt.items() if cnt >= min_cnt]
    supports = {}
    freq_itemsets = []
    for it in l1:
        cnt = item_cnt[list(it)[0]]
        support = cnt/n
        supports[it] = support
        freq_itemsets.append((it, cnt, support))

    k = 2
    lk_1 = l1
    while len(lk_1) > 0:
        candidates = set()
        for i in range(len(lk_1)):
            for j in range(i+1, len(lk_1)):
                combined = lk_1[i] | lk_1[j]
                if len(combined) == k:
                    candidates.add(combined)

        candidates = list(candidates)
        pruned_candidates = []
        for c in candidates:
            flag = True
            for it in c:
                subset = c - frozenset([it])
                if subset not in lk_1:
                    flag = False
                    break

            if flag:
                pruned_candidates.append(c)

        candidates = pruned_candidates

        counts = {}
        for t in transactions:
            tset = frozenset(t)
            for c in candidates:
                if c.issubset(tset):
                    if c not in counts:
                        counts[c] = 1
                    else:
                        counts[c] += 1

        lk = [c for c in candidates if c in counts and counts[c] >= min_cnt]
        for it in lk:
            support = counts[it]/n
            supports[it] = support
            freq_itemsets.append((it, counts[it], support))

        lk_1 = lk
        k += 1

    return freq_itemsets, supports

def get_association_rules(freq_itemsets, min_confidence, transactions):
    rules = []
    n = len(transactions)
    for itemset, count, support in freq_itemsets:
        if len(itemset) > 1:
            items = list(itemset)
            for r in range(1, len(items)):
                from itertools import combinations
                for combo in combinations(items, r):
                    antecedent = frozenset(combo)
                    consequent = itemset - antecedent
                    if not consequent:
                        continue
                    antecedent_count = sum(1 for t in transactions if antecedent.issubset(frozenset(t)))
                    if antecedent_count == 0:
                        continue
                    confidence = count / antecedent_count
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent, confidence))
    return rules


def main():
    rows = read_csv_rows('data.csv')
    transactions = parse_data(rows)

    print("Parsed Transactions: ")
    for transaction in transactions[0:5]:
        print(transaction)
    print("...")

    min_support = float(input("Enter minimum support (0-1): "))
    freq_itemsets, supports = apriori(transactions, min_support)

    print("\nFrequent Itemsets:")
    for itemset, count, support in freq_itemsets:
        print(
            f"Itemset: {set(itemset)}, Count: {count}, Support: {support:.4f}")

    # write frequent itemsets to CSV
    with open('frequent_itemsets.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['itemset', 'count', 'support'])
        for itemset, count, support in freq_itemsets:
            itemset_str = '{' + ','.join(sorted(list(itemset))) + '}'
            writer.writerow([itemset_str, count, f"{support:.6f}"])

    if not freq_itemsets:
        print("No frequent itemsets found with the given minimum support.")
    else:
        print(f"Total frequent itemsets found: {len(freq_itemsets)}\n")

    min_confidence = float(input("Enter minimum confidence (0-1): "))
    rules = get_association_rules(freq_itemsets, min_confidence, transactions)
    print("\nAssociation Rules:")
    for antecedent, consequent, confidence in rules:
        print(f"Rule: {set(antecedent)} -> {set(consequent)}, "
              f"Confidence: {confidence:.4f}")

    # write association rules to CSV
    with open('association_rules.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['antecedent', 'consequent', 'confidence'])
        for antecedent, consequent, confidence in rules:
            ant_str = '{' + ','.join(sorted(list(antecedent))) + '}'
            cons_str = '{' + ','.join(sorted(list(consequent))) + '}'
            writer.writerow([ant_str, cons_str, f"{confidence:.6f}"])
    if not rules:
        print("No association rules found with the given minimum confidence.")
    else:
        print(f"Total rules found: {len(rules)}")


if __name__ == "__main__":
    main()
