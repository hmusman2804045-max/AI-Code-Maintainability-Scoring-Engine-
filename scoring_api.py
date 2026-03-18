from ast_analyzer import extract_features
from feature_pipeline import prepare_inference_vector
from model_trainer import load_model
from explanation_engine import explain

try:
    _MODEL = load_model()
except FileNotFoundError:
    _MODEL = None

def _get_risk_level(score):

    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    else:
        return "High"

def evaluate(source):

    if _MODEL is None:
        return {
            "error": True,
            "message": "Model not found. Run train_model() first."
        }

    raw_features = extract_features(source)

    if raw_features.get("error"):
        return raw_features

    X_scaled = prepare_inference_vector(raw_features)

    probability = _MODEL.predict_proba(X_scaled)[0][1]

    risk_score = int(probability * 100)

    risk_level = _get_risk_level(risk_score)

    explanations = explain(_MODEL, raw_features, top_n=3)

    result = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "confidence": round(probability, 2),
        "top_risk_factors": explanations
    }

    return result

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("  SCORING API DEMO")
    print("=" * 60)

    clean_code =
    print("\n🟢 Testing Clean Code...")
    clean_result = evaluate(clean_code)
    print(json.dumps(clean_result, indent=2))

    risky_code =
    print("\n🔴 Testing Risky Code...")
    risky_result = evaluate(risky_code)
    print(json.dumps(risky_result, indent=2))
    print("=" * 60)
