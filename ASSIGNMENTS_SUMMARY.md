# Assignments Summary - Data Mining

This document summarizes each assignment folder in the workspace, the main script(s), input/output files, a short description of what the code does, how to run it, and notes about dependencies or issues.

---

## apriori
- Main: `apriori/main.py`
- Inputs: `data.csv` (transactions, rows containing items)
- Outputs: `frequent_itemsets.csv`, `association_rules.csv`
- Description: Implements the Apriori algorithm to find frequent itemsets and generate simple association rules (confidence). Interactive prompts for minimum support and minimum confidence.
- How to run: Run `python apriori/main.py` and follow prompts.
- Notes: Current script uses `pandas` for CSV I/O and dataframe manipulation. Will need conversion to `csv` if pandas removal is required.

## bayes
- Main: `bayes/main.py`
- Inputs: `data.csv` (categorical features and class column)
- Outputs: `bayes_output.csv` (predicted class for the provided new case)
- Description: Simple naive-Bayes style classifier helper — computes base probabilities and conditional feature probabilities from the dataset and evaluates a single new case entered interactively.
- How to run: Run `python bayes/main.py` and follow prompts.
- Notes: Uses `pandas`. Normalizes string features to lowercase/trim.

## gain-gini
- Main: `gain-gini/main.py`
- Inputs: `data.csv` (features and target/class column)
- Outputs: `gain_gini_output.csv`
- Description: Computes entropy, information gain and Gini split for attributes relative to a chosen target/class column. Meant to help with attribute selection for decision trees.
- How to run: Run `python gain-gini/main.py` and enter the target column when prompted.
- Notes: Uses `pandas` and `math`.

## correlation
- Main: `correlation/main.py`
- Inputs: `data.csv` (numeric columns; may include TID column that is ignored)
- Outputs: `pearson_correlation_output.csv`
- Description: Computes Pearson correlation coefficient pairwise between numeric item columns and writes results out.
- How to run: Run `python correlation/main.py`.
- Notes: Uses `pandas` and `math`. Could be refactored to pure Python + `csv`/`math` if needed.

## clustering
This folder contains multiple clustering assignments and scripts.

- k-means (tabular)
  - Main: `clustering/k-means/k-means.py`
  - Inputs: `clustering/k-means/data.csv` (numerical records)
  - Outputs: `k-means.csv` (clusters assigned), `k-means-out.csv` (step matrices)
  - Description: Implements K-means clustering (iterative), writes step-by-step matrices and final clusters.
  - How to run: Run `python clustering/k-means/k-means.py` and enter k when prompted.
  - Notes: Uses `pandas` for CSV I/O; also writes CSV by manual file write in places.

- DBSCAN / density-based
  - Main: `clustering/density/density.py`
  - Inputs: `clustering/density/data.csv`
  - Outputs: `dbscan.csv`
  - Description: DBSCAN clustering implementation with interactive prompts for eps and min_samples.
  - How to run: Run `python clustering/density/density.py`.
  - Notes: Uses `pandas` and `matplotlib` (matplotlib imported but not required for core algorithm). Needs pandas removal if requested.

- Hierarchical clustering (single, complete, average linkage)
  - Mains:
    - `clustering/heirarchial/heirarchial-1.py` (single linkage)
    - `clustering/heirarchial/heirarchial-2.py` (complete linkage)
    - `clustering/heirarchial/heirarchial-3.py` (average linkage)
  - Inputs: `clustering/heirarchial/data.csv`
  - Outputs: `heirarchial-*-steps.csv`, `heirarchial-*.csv` (final clusters)
  - Description: Each script implements a variant of hierarchical clustering and writes step matrices showing distances during merging.
  - How to run: Run the desired `heirarchial-*.py` script.
  - Notes: All three use `pandas` for loading/writing CSVs.

- k-means (image segmentation)
  - Main: `k-means-image/main.py`
  - Inputs: any image file (asked interactively)
  - Outputs: `output_kmeans.jpg`
  - Description: Performs k-means on image pixel colors to segment the image and saves a segmented image.
  - How to run: Run `python k-means-image/main.py` and provide an image path and k.
  - Notes: Uses `numpy` and `Pillow` (PIL). No pandas.

## linear-regression
- Main: `linear-regression/main.py`
- Inputs: `data.csv` (columns with numeric X and Y)
- Outputs: `linear_regression_output.csv`
- Description: Computes simple linear regression (slope and intercept), prints detailed intermediate sums, and writes predicted values to CSV.
- How to run: Run `python linear-regression/main.py` and enter column names when prompted.
- Notes: Uses `pandas` for CSV I/O and column selection.

## normalization
- Main: `normalization/normalization.py`
- Inputs: `data.csv`
- Outputs: `out_decimal.csv`, `out_zscore.csv`, or `out_minmax.csv` depending on choice
- Description: Provides three normalization methods (decimal scaling, z-score, min-max). Interactive choice; computes statistics and outputs normalized CSV.
- How to run: Run `python normalization/normalization.py` and follow menu prompts.
- Notes: Uses built-in `csv` and `math` (already pandas-free).

## olap
- Main: `olap/olap.py`
- Inputs: `data.csv` (multidimensional table with a measure column)
- Outputs: `cube_output.csv`
- Description: Builds an OLAP cube (all aggregations across subsets of dimensions), supports roll-up, drill-down, slice, dice via an interactive CLI.
- How to run: Run `python olap/olap.py` and follow prompts to select measure and operations.
- Notes: Uses `pandas` heavily for grouping/aggregation and interactive display.

## fiveNoSummary
- Main: `fiveNoSummary/main.py`
- Inputs: `data.csv` (single-column numeric values)
- Outputs: (none written) shows boxplot and computes five-number summary
- Description: Computes five-number summary and shows boxplot (matplotlib).
- How to run: Run `python fiveNoSummary/main.py`.
- Notes: Uses `csv` and `matplotlib`.

## t-d-weight
- Main: `t-d-weight/main.py`
- Inputs: `data.csv` (first column class name, remaining columns numeric group values)
- Outputs: `output_weights.csv`
- Description: Computes generalized T-weight and D-weight per group column and per class; writes the results to CSV.
- How to run: Run `python t-d-weight/main.py`.
- Notes: Uses built-in `csv` only.

---

## Dependencies (observed)
- pandas — used by many scripts: `apriori`, `bayes`, `gain-gini`, `clustering/*` (k-means tabular, density, heirarchial), `olap`, `correlation`, `linear-regression`.
- numpy, Pillow — used by `k-means-image` (image segmentation).
- matplotlib — used by `fiveNoSummary` and optionally `clustering/density`.
- math, csv, itertools, collections — standard library usage across scripts.

## Notes & Next Steps
1. If you want the workspace converted to not use `pandas`, I can:
   - Replace the CSV reading/writing and simple DataFrame operations with `csv` + Python lists/dicts for each script that uses pandas. This is straightforward for scripts that primarily load, iterate, and write CSVs (e.g., `apriori`, `correlation`, `linear-regression`, `clustering/*`). For `olap` and scripts that rely on grouping/aggregation or DataFrame conveniences, conversions need careful handling (but are doable).

2. I can create `ASSIGNMENTS_SUMMARY.md` (this file) in the repo root (already created). If you'd like a different format (CSV, JSON, or a README), tell me.

3. I can proceed to automatically refactor each pandas-using script to use the `csv` module instead — one by one, and run quick syntax checks after each change. Recommend doing it per-assignment to avoid regressions.

If you'd like, I can now:
- Option A: Start converting the highest-priority assignments (you choose which) from `pandas` to `csv`.
- Option B: Produce a shorter checklist with exact run commands per assignment (so you can test them locally).
- Option C: Run quick automated static checks (syntax) on the current Python files to list errors.

Tell me which next step you'd like (or say “convert all” and I’ll begin converting files in order: `apriori`, `correlation`, `linear-regression`, `gain-gini`, `clustering/*`, `bayes`, `olap`).
