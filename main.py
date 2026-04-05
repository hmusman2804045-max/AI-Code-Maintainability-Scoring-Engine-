import argparse
import sys
import os

from scoring_api import evaluate
from phase2.optimization import IterativeOptimizer

def display_results(initial_code, result):
    print("\n" + "="*60)
    print(" 🚀 AI CODE MAINTAINABILITY ENGINE (Unified Pipeline) 🚀")
    print("="*60)
    
    print("\n📝 [ORIGINAL CODE]\n")
    print(initial_code.strip())
    
    # Phase 1: Evaluate initial code directly
    print("\n🔍 [PHASE 1: INITIAL SCORING]")
    initial_score_result = evaluate(initial_code)
    print(f"Risk Score:  {initial_score_result['risk_score']}")
    print(f"Risk Level:  {initial_score_result['risk_level']}")
    if initial_score_result['top_risk_factors']:
        print("Details:")
        for factor in initial_score_result['top_risk_factors']:
            print(f"  - {factor}")

    # Phase 2: Show Optimization Results
    print("\n🛠️  [PHASE 2: AUTONOMOUS REFACTORING]")
    if result['iterations_run'] == 0:
        print("No optimization was performed (perhaps the code was already optimal!).")
    else:
        print(f"Completed {result['iterations_run']} refinement iteration(s).")
        print("\n✨ [REFACTORED CODE]\n")
        print(result['final_code'].strip())
        
        print("\n📊 [FINAL METRICS]")
        print(f"Original Score: {initial_score_result['risk_score']}")
        print(f"Final Score:    {result['final_score']}")
        
        if result['final_score'] < initial_score_result['risk_score']:
            print(f"🎉 Success! Maintainability improved by {initial_score_result['risk_score'] - result['final_score']} points.")
        else:
            print("⚠️ Code was refactored, but no net improvement in risk score was achieved.")
            
    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="AI Code Maintainability Scoring & Refactoring Engine")
    parser.add_argument("file", nargs="?", help="Path to the Python file to analyze and refactor.")
    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        with open(args.file, "r") as f:
            code = f.read()
    else:
        # Default fallback example
        code = '''
def process_data(data_list):
    results = []
    for i in range(len(data_list)):
        if data_list[i] > 0:
            if data_list[i] % 2 == 0:
                results.append(data_list[i])
    return results
'''
    print("Initializing Unified Maintainability Engine...")
    try:
        # Initializing IterativeOptimizer directly uses Phase 2 generator and Phase 1 scoring (via selector)
        optimizer = IterativeOptimizer(target_score=10.0, max_iterations=2)
        
        print("Analyzing and Refactoring code...")
        result = optimizer.optimize(code)
        
        display_results(code, result)
        
    except Exception as e:
        print(f"\nError during engine execution: {e}")

if __name__ == "__main__":
    main()
