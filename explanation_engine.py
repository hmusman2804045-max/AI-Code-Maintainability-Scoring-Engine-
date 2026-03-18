from feature_pipeline import FEATURE_SCHEMA

FEATURE_DESCRIPTIONS = {
    "num_functions":        "Many small functions defined (count: {value})",
    "num_loops":            "High loop count detected (count: {value})",
    "num_if":               "Excessive branching / if-statements (count: {value})",
    "num_try_except":       "Heavy error handling blocks (count: {value})",
    "num_return":           "High number of return statements (count: {value})",
    "line_count":           "Large codebase size (lines: {value})",
    "max_nesting_depth":    "Deep nesting detected (depth: {value})",
    "cyclomatic_complexity":"High cyclomatic complexity (score: {value})",
    "avg_function_length":  "Large function size (avg: {value} lines)",
    "recursion_flag":       "Recursion detected in code",
    "global_variable_count":"Global variables used (count: {value})",
}

RISK_THRESHOLDS = {
    "num_functions":         5,
    "num_loops":             3,
    "num_if":                5,
    "num_try_except":        2,
    "num_return":            4,
    "line_count":           40,
    "max_nesting_depth":     3,
    "cyclomatic_complexity": 5,
    "avg_function_length":  15,
    "recursion_flag":        0,
    "global_variable_count": 1,
}

def explain(model, feature_dict, top_n=3):

    importances = model.feature_importances_

    importance_map = dict(zip(FEATURE_SCHEMA, importances))

    risky_features = []

    for feature_name in FEATURE_SCHEMA:
        raw_value  = float(feature_dict.get(feature_name, 0))
        threshold  = RISK_THRESHOLDS.get(feature_name, 0)
        importance = importance_map.get(feature_name, 0)

        if raw_value > threshold:
            risky_features.append((feature_name, importance))

    risky_features.sort(key=lambda x: x[1], reverse=True)

    top_features = risky_features[:top_n]

    explanations = []

    for feature_name, _ in top_features:
        raw_value   = feature_dict.get(feature_name, 0)
        template    = FEATURE_DESCRIPTIONS[feature_name]

        if "{value}" in template:
            sentence = template.format(value=raw_value)
        else:
            sentence = template

        explanations.append(sentence)

    if not explanations:
        explanations.append("No significant structural risk factors detected.")

    return explanations

if __name__ == "__main__":

    from model_trainer import load_model

    model = load_model()

    risky_features = {
        "num_functions":         2,
        "num_loops":             4,
        "num_if":                9,
        "num_try_except":        1,
        "num_return":            1,
        "line_count":            35,
        "max_nesting_depth":     7,
        "cyclomatic_complexity": 15,
        "avg_function_length":   34.0,
        "recursion_flag":        0,
        "global_variable_count": 0,
    }

    clean_features = {
        "num_functions":         2,
        "num_loops":             1,
        "num_if":                2,
        "num_try_except":        0,
        "num_return":            2,
        "line_count":            10,
        "max_nesting_depth":     2,
        "cyclomatic_complexity": 3,
        "avg_function_length":   4.0,
        "recursion_flag":        0,
        "global_variable_count": 0,
    }

    print("=" * 55)
    print("  EXPLANATION ENGINE — TEST")
    print("=" * 55)

    print("\n🔴 Risky Code — Top Risk Factors:")
    risky_explanations = explain(model, risky_features, top_n=3)
    for i, reason in enumerate(risky_explanations, start=1):
        print(f"  {i}. {reason}")

    print("\n🟢 Clean Code — Top Risk Factors:")
    clean_explanations = explain(model, clean_features, top_n=3)
    for i, reason in enumerate(clean_explanations, start=1):
        print(f"  {i}. {reason}")

    print("=" * 55)
