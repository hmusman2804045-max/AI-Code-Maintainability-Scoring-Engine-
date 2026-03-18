# AI Code Maintainability Scoring Engine (Phase 1)

## Overview
The **AI Code Maintainability Scoring Engine** is a modular, machine-learning-based system designed to evaluate the structural quality of Python code. Rather than relying on rigid rule-based linters (like PyLint or Flake8), this engine uses a supervised learning approach (Random Forest) to predict maintainability risks dynamically based on pure structural signals.

This repository contains **Phase 1**: The Core Scoring Engine. It evaluates code and assigns a risk score (0–100), a risk category (Low / Medium / High), and surfaces the top structural risk factors in human-readable terms.

## System Architecture

The engine is built on a strictly modular and stateless architecture. This ensures that the scoring is entirely deterministic, which is a critical requirement for serving as a reward signal in future phases.

1. **AST Analyzer (`ast_analyzer.py`)**: Parses Python Abstract Syntax Trees (AST) to extract 11 core structural metrics without executing the code.
2. **Dataset Generator (`dataset_generator.py`)**: Generates balanced, labeled synthetic datasets of clean and risky Python patterns for model training.
3. **Feature Pipeline (`feature_pipeline.py`)**: Standardizes and scales feature vectors using a frozen `StandardScaler` to ensure training and inference scales remain perfectly matched.
4. **ML Risk Model (`model_trainer.py`)**: Trains and compares Random Forest and XGBoost classifiers, saving the best performer for stateless inference.
5. **Explanation Engine (`explanation_engine.py`)**: Converts raw feature importances and code thresholds into plain-English sentences to explain *why* a particular score was assigned.
6. **Scoring API (`scoring_api.py`)**: The central access point exposing the master `evaluate()` backend function.

## Extracted Structural Features
The AST Analyzer evaluates maintainability using the following exact signals:
- Maximum Nesting Depth (*Strongest Indicator*)
- Cyclomatic Complexity Approximation
- Average Function Length and Total Line Count
- Branching Density (`if`/`elif`)
- Loop Density (`for`/`while`)
- Error Handling Density (`try`/`except`)
- Number of Functions and Return Points
- Global Variable Declarations
- Recursion Detection

## Quick Start

### Installation
Ensure you have Python 3.8+ installed. Install the required dependencies:
```bash
pip install scikit-learn xgboost numpy
```

### Usage
To score any Python code string or `.py` file path, simply import and call the `evaluate` function from the Scoring API:

```python
import json
from scoring_api import evaluate

code_to_test = """
def example_function(x):
    if x > 0:
        for i in range(x):
            print(i)
    return x
"""

result = evaluate(code_to_test)
print(json.dumps(result, indent=2))
```

**Example Output:**
```json
{
  "risk_score": 12,
  "risk_level": "Low",
  "confidence": 0.12,
  "top_risk_factors": [
    "No significant structural risk factors detected."
  ]
}
```

## Future Roadmap (Phase 2)
This Phase 1 scoring engine actively serves as the deterministic reward function for **Phase 2**.

Phase 2 will introduce an autonomous refactoring agent (using Reinforcement Learning or heuristics) capable of modifying structurally risky code. The agent will repeatedly query this API, comparing `evaluate(new_code)` against `evaluate(old_code)` to use the score delta as a strict reward signal to systematically improve codebase health.
