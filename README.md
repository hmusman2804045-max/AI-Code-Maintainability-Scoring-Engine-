# AI Code Maintainability Scoring & Refactoring Engine

## Overview
The **AI Code Maintainability Scoring Engine** is a modular, machine-learning-based system designed to evaluate the structural quality of Python code and autonomously refactor it. Rather than relying on rigid rule-based linters (like PyLint or Flake8), this engine uses a supervised learning approach (Random Forest) to predict maintainability risks dynamically based on pure structural signals, and then utilizes Deep Learning (CodeT5) to actively improve the code.

This repository contains the completely unified Engine:
- **Phase 1 (The Evaluator)**: The Core Scoring Engine. It evaluates code and assigns a risk score (0–100), a risk category, and surfaces top structural risk factors.
- **Phase 2 (The Refactorer)**: The Autonomous Refactoring Agent. It generates, validates, and selects better candidates for structurally risky code to iteratively improve the risk score.

## System Architecture

The engine is built on a strictly modular architecture. 

### Evaluator (Phase 1)
1. **AST Analyzer (`ast_analyzer.py`)**: Parses Python Abstract Syntax Trees (AST) to extract 11 core structural metrics.
2. **ML Risk Model (`model_trainer.py`)**: Uses a Random Forest classifier for stateless inference of risk scores.
3. **Explanation Engine (`explanation_engine.py`)**: Converts raw feature importances into plain-English explanations.
4. **Scoring API (`scoring_api.py`)**: The central access point exposing the master `evaluate()` backend function.

### Refactorer (Phase 2)
1. **Candidate Generator (`phase2/candidate_generator.py`)**: Uses a localized Deep Learning model (`CodeT5`) to generate multiple refactored versions of the code.
2. **Code Validator (`phase2/validation.py`)**: Ensures that generated candidates compile and do not contain syntax errors.
3. **Candidate Selector (`phase2/selector.py`)**: Uses the `Scoring API` to rank candidates and selects the one that provides the best improvement in the maintainability risk score.
4. **Iterative Optimizer (`phase2/optimization.py`)**: Manages the iterative loops to continuously refine the code until a target score is reached.

## Extracted Structural Features
The Evaluator rates maintainability using the following exact signals:
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
pip install scikit-learn xgboost numpy transformers torch
```

### Usage
To analyze and refactor a Python file automatically, you can use the unified `main.py` entry point:

```bash
python main.py path/to/your/messy_code.py
```
This will:
1. Provide the initial maintainability score.
2. Interactively use Deep Learning to refactor the code.
3. Output the cleaned code and the final score improvement.
