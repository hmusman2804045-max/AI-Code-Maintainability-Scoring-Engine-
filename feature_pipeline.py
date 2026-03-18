import os
import csv
import pickle

from sklearn.preprocessing import StandardScaler

import numpy as np

FEATURE_SCHEMA = [
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
]

SCHEMA_VERSION = "v1.0"

SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "scaler.pkl")

def build_feature_vector(feature_dict):

    vector = []

    for feature_name in FEATURE_SCHEMA:
        value = feature_dict.get(feature_name, 0)
        vector.append(float(value))

    return vector

def load_dataset(csv_path):

    X = []
    y = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            vector = build_feature_vector(row)
            label  = int(row["label"])

            X.append(vector)
            y.append(label)

    X = np.array(X)
    y = np.array(y)

    return X, y

def fit_and_save_scaler(X, scaler_path=SCALER_PATH):

    scaler = StandardScaler()
    scaler.fit(X)

    os.makedirs(
        os.path.dirname(scaler_path),
        exist_ok=True
    )

    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    print(f"Scaler saved to: {scaler_path}")

    return scaler

def load_scaler(scaler_path=SCALER_PATH):

    if not os.path.exists(scaler_path):
        raise FileNotFoundError(
            f"Scaler not found at {scaler_path}. "
            f"Run fit_and_save_scaler() first during training."
        )

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return scaler

def scale_features(X, scaler):

    X = np.array(X)

    if X.ndim == 1:
        X = X.reshape(1, -1)

    X_scaled = scaler.transform(X)

    return X_scaled

def prepare_training_data(csv_path, scaler_path=SCALER_PATH):

    print("Loading dataset...")
    X, y = load_dataset(csv_path)
    print(f"  Loaded {X.shape[0]} samples, {X.shape[1]} features each")

    print("Fitting and saving scaler...")
    scaler = fit_and_save_scaler(X, scaler_path)

    print("Scaling features...")
    X_scaled = scale_features(X, scaler)

    print("Training data ready!")
    return X_scaled, y

def prepare_inference_vector(feature_dict, scaler_path=SCALER_PATH):

    vector = build_feature_vector(feature_dict)
    scaler = load_scaler(scaler_path)
    X_scaled = scale_features(vector, scaler)

    return X_scaled

if __name__ == "__main__":

    import os

    CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset.csv")

    X_scaled, y = prepare_training_data(CSV_PATH)

    print("\n" + "=" * 50)
    print("  FEATURE PIPELINE — TRAINING RESULTS")
    print("=" * 50)
    print(f"  X_scaled shape : {X_scaled.shape}")
    print(f"  y shape        : {y.shape}")
    print(f"  Label counts   : Clean={sum(y==0)}, Risky={sum(y==1)}")
    print(f"  Schema version : {SCHEMA_VERSION}")
    print(f"  Feature order  : {FEATURE_SCHEMA}")
    print("=" * 50)

    print("\n  Scaled Feature Means (should be ~0.0 after StandardScaling):")
    for name, mean_val in zip(FEATURE_SCHEMA, X_scaled.mean(axis=0)):
        print(f"    {name:<28} : {mean_val:+.4f}")

    print("\n  Scaled Feature Std Devs (should be ~1.0 after StandardScaling):")
    for name, std_val in zip(FEATURE_SCHEMA, X_scaled.std(axis=0)):
        print(f"    {name:<28} : {std_val:.4f}")

    print("=" * 50)

    print("\n  Simulating inference on a sample feature dict...")

    sample_features = {
        "num_functions": 2,
        "num_loops": 5,
        "num_if": 8,
        "num_try_except": 2,
        "num_return": 3,
        "line_count": 80,
        "max_nesting_depth": 6,
        "cyclomatic_complexity": 9,
        "avg_function_length": 35.0,
        "recursion_flag": 1,
        "global_variable_count": 2,
    }

    inference_vector = prepare_inference_vector(sample_features)
    print(f"  Inference vector shape : {inference_vector.shape}")
    print(f"  Scaled values         : {inference_vector.round(3)}")
    print("=" * 50)
