import csv
import itertools
import sys
from collections import defaultdict

def read_data(filename='data.csv'):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
        fieldnames = reader.fieldnames or []

    print(f"Columns in data: {fieldnames}")
    measure = input("Enter target (measure) column name: ").strip()
    if measure not in fieldnames:
        raise RuntimeError(f"Column '{measure}' not found in data.")
    dims = [c for c in fieldnames if c != measure]

    for r in rows:
        for d in dims:
            v = r.get(d, '')
            r[d] = '' if v is None else str(v)
        m = r.get(measure, '')
        try:
            r[measure] = float(m)
        except Exception:
            r[measure] = 0.0

    return rows, dims, measure

def all_subsets(seq):
    items = list(seq)
    for r in range(len(items) + 1):
        for comb in itertools.combinations(items, r):
            yield comb

def build_olap_cube(rows, dims, measure, fill_value='ALL'):
    cube_rows = []

    total = sum(r[measure] for r in rows)
    row = {d: fill_value for d in dims}
    row[measure] = float(total)
    cube_rows.append(row)

    
    for subset in (s for s in all_subsets(dims) if len(s) > 0):
        agg = defaultdict(float)
        for r in rows:
            key = tuple(r[d] for d in subset)
            agg[key] += r[measure]

        for key, val in agg.items():
            out = {}
            for d in dims:
                if d in subset:
                    out[d] = key[subset.index(d)]
                else:
                    out[d] = fill_value
            out[measure] = float(val)
            cube_rows.append(out)

    cube_rows.sort(key=lambda r: tuple(r[d] for d in dims))
    return cube_rows

def roll_up(cube_rows, dims, measure, target_dims):
    res = []
    seen = set()
    for r in cube_rows:
        ok = True
        for d in dims:
            if d not in target_dims and r[d] != 'ALL':
                ok = False
                break
        if not ok:
            continue
        key = tuple(r[d] for d in target_dims) + (r[measure],)
        if key in seen:
            continue
        seen.add(key)
        out = {d: r[d] for d in target_dims}
        out[measure] = r[measure]
        res.append(out)
    return res

def drill_down(cube_rows, dims, measure, drill_dims):
    res = []
    seen = set()
    for r in cube_rows:
        ok = all(r[d] != 'ALL' for d in drill_dims)
        if not ok:
            continue
        key = tuple(r[d] for d in drill_dims) + (r[measure],)
        if key in seen:
            continue
        seen.add(key)
        out = {d: r[d] for d in drill_dims}
        out[measure] = r[measure]
        res.append(out)
    return res

def slice_cube(cube_rows, dims, measure, slice_dim, value):
    v = str(value)
    res = [ {d: r[d] for d in dims + [measure]} for r in cube_rows if r[slice_dim] == v ]
    return res

def dice_cube(cube_rows, dims, measure, filters):
    res = []
    for r in cube_rows:
        ok = True
        for d, v in filters.items():
            if isinstance(v, (list, tuple, set)):
                if r[d] not in [str(x) for x in v]:
                    ok = False
                    break
            else:
                if r[d] != str(v):
                    ok = False
                    break
        if ok:
            res.append({d: r[d] for d in dims + [measure]})
    return res

def print_menu(dims, measure):
    print("\nChoose an operation to perform on the cube:")
    print("1. Show full cube")
    print("2. Roll-up (aggregate to target dims)")
    print("3. Drill-down (show detailed levels)")
    print("4. Slice (fix one dimension)")
    print("5. Dice (filter multiple dimensions)")
    print("6. Exit\n")
    print(f"Available dimensions: {dims}, measure: {measure}")

def interactive_cli(cube_df, dims, measure):
    import sys
    if not sys.stdin.isatty():
        print("\nInteractive mode skipped (stdin is not a TTY). Run the script in a terminal for interactive queries.")
        return
    while True:
        print_menu(dims, measure)
        choice = input("Enter choice (1-6): ").strip()
        if choice == '1':
            print("\nFull Cube:")
            print_table(cube_df, dims + [measure])
        elif choice == '2':
            td = input(f"Enter target dimensions for roll-up separated by commas (subset of {dims}): ").strip()
            target_dims = [x.strip() for x in td.split(',') if x.strip()]
            invalid = [d for d in target_dims if d not in dims]
            if invalid:
                print("Invalid dimensions:", invalid)
                continue
            res = roll_up(cube_df, dims, measure, target_dims)
            print("\nRoll-up result:")
            print_table(res, target_dims + [measure])
        elif choice == '3':
            dd = input(f"Enter dimensions for drill-down separated by commas (e.g. Month,Product): ").strip()
            drill_dims = [x.strip() for x in dd.split(',') if x.strip()]
            invalid = [d for d in drill_dims if d not in dims]
            if invalid:
                print("Invalid dimensions:", invalid)
                continue
            res = drill_down(cube_df, dims, measure, drill_dims)
            print("\nDrill-down result:")
            print_table(res, drill_dims + [measure])
        elif choice == '4':
            sd = input(f"Enter slice dimension (one of {dims}): ").strip()
            if sd not in dims:
                print("Invalid dimension.")
                continue
            val = input("Enter value to slice on (e.g. Feb): ").strip()
            res = slice_cube(cube_df, dims, measure, sd, val)
            if not res:
                print("\nNo rows found for this slice.")
            else:
                print("\nSlice result:")
                print_table(res, dims + [measure])
        elif choice == '5':
            print("Enter dice filters in format Dim=Val,Dim2=Val")
            raw = input("Filters: ").strip()
            try:
                filters = {}
                parts = [p.strip() for p in raw.split(',') if p.strip()]
                for p in parts:
                    k,v = p.split('=',1)
                    k = k.strip()
                    v = v.strip()
                    filters[k] = v
                res = dice_cube(cube_df, dims, measure, filters)
                if not res:
                    print("\nNo rows found for these dice filters.")
                else:
                    print("\nDice result:")
                    print_table(res, dims + [measure])
            except Exception as e:
                print("Error parsing filters:", e)
        elif choice == '6':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

def print_table(rows, columns):
    if not rows:
        print("(no rows)")
        return
    widths = {c: max(len(str(c)), max((len(str(r.get(c, ''))) for r in rows), default=0)) for c in columns}
    # header
    hdr = ' | '.join(str(c).ljust(widths[c]) for c in columns)
    sep = '-+-'.join('-' * widths[c] for c in columns)
    print(hdr)
    print(sep)
    for r in rows:
        line = ' | '.join(str(r.get(c, '')).ljust(widths[c]) for c in columns)
        print(line)
        
def main():
    rows, dims, measure = read_data()
    print("\nInput Data:")
    print_table(rows, dims + [measure])
    cube_rows = build_olap_cube(rows, dims, measure)
    print("\nGenerated OLAP Cube:")
    print_table(cube_rows, dims + [measure])

    with open('cube_output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=dims + [measure])
        writer.writeheader()
        for r in cube_rows:
            writer.writerow(r)
    print("\nCube saved to: cube_output.csv")
    interactive_cli(cube_rows, dims, measure)

if __name__ == "__main__":
    main()




