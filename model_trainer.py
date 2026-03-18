import os
import pickle
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from feature_pipeline import prepare_training_data, FEATURE_SCHEMA

CSV_PATH   = os.path.join(os.path.dirname(__file__), "data",   "dataset.csv")
RF_PATH    = os.path.join(os.path.dirname(__file__), "models", "rf_model.pkl")
XGB_PATH   = os.path.join(os.path.dirname(__file__), "models", "xgb_model.pkl")

RANDOM_STATE = 42

def _evaluate(model_name, model, X_test, y_test):

    y_pred   = model.predict(X_test)
    acc      = accuracy_score(y_test, y_pred)
    prec     = precision_score(y_test, y_pred)
    rec      = recall_score(y_test, y_pred)
    f1       = f1_score(y_test, y_pred)
    cm       = confusion_matrix(y_test, y_pred)

    print(f"\n{'='*55}")
    print(f"  {model_name} — Evaluation Results")
    print(f"{'='*55}")
    print(f"  Accuracy  : {acc:.4f}   ({acc*100:.1f}%)")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-Score  : {f1:.4f}")
    print(f"{'-'*55}")
    print(f"  Confusion Matrix:")
    print(f"                    Predicted Clean    Predicted Risky")
    print(f"  Actual Clean      {cm[0][0]:<18}  {cm[0][1]}")
    print(f"  Actual Risky      {cm[1][0]:<18}  {cm[1][1]}")
    print(f"{'='*55}")

    return acc

def _save_model(model, path):

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  Saved → {path}")

def train_model(csv_path=CSV_PATH, rf_path=RF_PATH, xgb_path=XGB_PATH):

    print("Loading and scaling dataset...")
    X_scaled, y = prepare_training_data(csv_path)
    print(f"  Total samples : {X_scaled.shape[0]}")
    print(f"  Features      : {X_scaled.shape[1]}")

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"\n  Train set : {len(X_train)} samples")
    print(f"  Test set  : {len(X_test)} samples")

    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )
    rf_model.fit(X_train, y_train)
    print("  Done!")

    print("\nTraining XGBoost...")
    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=RANDOM_STATE,
        verbosity=0,
    )
    xgb_model.fit(X_train, y_train)
    print("  Done!")

    print("\n\nEvaluating both models on the test set...")

    rf_acc  = _evaluate("Random Forest", rf_model,  X_test, y_test)
    xgb_acc = _evaluate("XGBoost",       xgb_model, X_test, y_test)

    print("\n  Feature Importances — Random Forest:")
    importances = rf_model.feature_importances_
    ranked = sorted(zip(FEATURE_SCHEMA, importances),
                    key=lambda x: x[1], reverse=True)
    for rank, (feature, score) in enumerate(ranked, start=1):
        bar = "█" * int(score * 50)
        print(f"  {rank:>2}. {feature:<28} {score:.4f}  {bar}")

    print("\nSaving models...")
    _save_model(rf_model,  rf_path)
    _save_model(xgb_model, xgb_path)

    print("\n" + "=" * 55)
    print("  MODEL COMPARISON SUMMARY")
    print("=" * 55)
    print(f"  Random Forest accuracy : {rf_acc*100:.1f}%")
    print(f"  XGBoost accuracy       : {xgb_acc*100:.1f}%")

    if rf_acc >= xgb_acc:
        print(f"  Winner                 : Random Forest 🏆")
    else:
        print(f"  Winner                 : XGBoost 🏆")

    print(f"\n  Both models saved to /models/ folder.")
    print(f"  Random Forest is used as the primary model in the Scoring API.")
    print("=" * 55)

    return {"rf": rf_model, "xgb": xgb_model}

def load_model(model_path=RF_PATH):

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at: {model_path}\n"
            f"Run train_model() first to create it."
        )
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

if __name__ == "__main__":
    train_model()
