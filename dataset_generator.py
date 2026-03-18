import csv
import os
import random
from ast_analyzer import extract_features

random.seed(42)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset.csv")

FEATURE_COLUMNS = [
    "num_functions",
    "num_loops",
    "num_if",
    "num_try_except",
    "num_return",
    "line_count",
    "max_nesting_depth",
    "cyclomatic_complexity",
    "avg_function_length",
    "recursion_flag",
    "global_variable_count",
    "label",
]

def _make_clean_snippet(index):

    variant = index % 10

    if variant == 0:
        return f

    elif variant == 1:
        return f

    elif variant == 2:
        return f

    elif variant == 3:
        return f

    elif variant == 4:
        return f

    elif variant == 5:
        return f

    elif variant == 6:
        return f

    elif variant == 7:
        return f

    elif variant == 8:
        return f

    else:
        return f

def _make_risky_snippet(index):

    variant = index % 10

    if variant == 0:
        return f

    elif variant == 1:
        return f

    elif variant == 2:
        return f

    elif variant == 3:
        return f

    elif variant == 4:
        return f

    elif variant == 5:
        return f

    elif variant == 6:
        return f

    elif variant == 7:
        return f

    elif variant == 8:
        return f

    else:
        return f

def generate_dataset(n_clean=110, n_risky=110):

    dataset = []
    skipped = 0

    print(f"Generating {n_clean} clean snippets...")

    for i in range(n_clean):
        code = _make_clean_snippet(i)
        features = extract_features(code)

        if features.get("error"):
            skipped += 1
            continue

        features["label"] = 0
        dataset.append(features)

    print(f"Generating {n_risky} risky snippets...")

    for i in range(n_risky):
        code = _make_risky_snippet(i)
        features = extract_features(code)

        if features.get("error"):
            skipped += 1
            continue

        features["label"] = 1
        dataset.append(features)

    random.shuffle(dataset)

    print(f"\nDataset ready: {len(dataset)} samples ({skipped} skipped due to errors)")
    return dataset

def save_dataset(dataset, output_path=OUTPUT_PATH):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FEATURE_COLUMNS)
        writer.writeheader()

        for row in dataset:
            filtered_row = {col: row.get(col, 0) for col in FEATURE_COLUMNS}
            writer.writerow(filtered_row)

    print(f"Dataset saved to: {output_path}")

def print_summary(dataset):

    clean_rows = [r for r in dataset if r["label"] == 0]
    risky_rows = [r for r in dataset if r["label"] == 1]

    print("\n" + "=" * 55)
    print("  DATASET SUMMARY")
    print("=" * 55)
    print(f"  Total samples   : {len(dataset)}")
    print(f"  Clean (label=0) : {len(clean_rows)}")
    print(f"  Risky (label=1) : {len(risky_rows)}")
    print("-" * 55)
    print(f"  {'Feature':<28} {'Clean Avg':>10} {'Risky Avg':>10}")
    print("-" * 55)

    for col in FEATURE_COLUMNS[:-1]:
        clean_avg = sum(r[col] for r in clean_rows) / len(clean_rows) if clean_rows else 0
        risky_avg = sum(r[col] for r in risky_rows) / len(risky_rows) if risky_rows else 0
        print(f"  {col:<28} {clean_avg:>10.2f} {risky_avg:>10.2f}")

    print("=" * 55)

if __name__ == "__main__":

    dataset = generate_dataset(n_clean=110, n_risky=110)
    print_summary(dataset)
    save_dataset(dataset)
