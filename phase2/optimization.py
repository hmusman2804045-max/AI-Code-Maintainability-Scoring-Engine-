"""
Iterative Optimization Module (Phase 2)
Implements an iterative optimization loop to continuously refine code maintainability.
It repeatedly generates, validates, and evaluates candidates until a target 
risk score is achieved or the maximum iterations are reached.
"""

import sys
import os

# Ensure the root project directory is in the path to allow imports of 'phase2' modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from typing import Dict, Any
from phase2.candidate_generator import CandidateGenerator
from phase2.validation import CodeValidator
from phase2.selector import CandidateSelector

class IterativeOptimizer:
    def __init__(self, target_score: float = 20.0, max_iterations: int = 3):
        """
        Initializes the Iterative Optimizer.
        
        Args:
            target_score (float): The desired risk score. The loop stops if a candidate achieves this.
                                  (Lower is better).
            max_iterations (int): Maximum number of refinement iterations to prevent infinite loops.
        """
        self.target_score = target_score
        self.max_iterations = max_iterations
        
        # Initialize the core Phase 2 components
        self.generator = CandidateGenerator()
        self.validator = CodeValidator()
        self.selector = CandidateSelector()

    def optimize(self, initial_code: str) -> Dict[str, Any]:
        """
        Iteratively improves the given code to achieve a better maintainability score.
        
        Args:
            initial_code (str): The raw input Python code to start optimizing.
            
        Returns:
            Dict[str, Any]: A dictionary containing the final optimized code,
                            its risk score, and detailed metadata about the iterations.
        """
        current_code = initial_code
        best_overall_candidate = None
        best_overall_score = float('inf')
        
        iteration_history = []
        
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n--- Starting Optimization Iteration {iteration}/{self.max_iterations} ---")
            
            # Step 1: Generate Candidates based on the current best code
            raw_candidates = self.generator.generate_candidates(current_code)
            
            # Step 2: Validate Candidates
            valid_candidates = []
            for cand in raw_candidates:
                if self.validator.is_valid(current_code, cand['code']):
                    valid_candidates.append(cand)
                else:
                    print(f"Candidate {cand.get('id')} failed validation checks. Skipping.")
            
            if not valid_candidates:
                print("No valid candidates generated in this iteration. Halting optimization.")
                break
                
            # Step 3: Select the Best Candidate
            best_iteration_candidate = self.selector.select_best(valid_candidates)
            
            if best_iteration_candidate is None:
                print("Failed to score candidates correctly in this iteration. Halting optimization.")
                break
                
            current_score = best_iteration_candidate.get("risk_score", float('inf'))
            print(f"Best candidate in iteration {iteration} achieved risk score: {current_score}")
            
            # Step 4: Record history and update bests
            iteration_history.append({
                "iteration": iteration,
                "best_candidate": best_iteration_candidate
            })
            
            # If this iteration's best is globally better, update overall best candidate
            if current_score < best_overall_score:
                best_overall_score = current_score
                best_overall_candidate = best_iteration_candidate
                current_code = best_iteration_candidate["candidate_data"]["code"]
            else:
                # If the score doesn't improve, we continue from the previous best code.
                print("No improvement in this iteration. Continuing with previous best code.")
            
            # Step 5: Check against target
            if best_overall_score <= self.target_score:
                print(f"Target score of {self.target_score} achieved! Stopping early.")
                break
                
        print("\n=== Optimization Process Complete ===")
        print(f"Final Best Risk Score: {best_overall_score}")
        
        return {
            "initial_code": initial_code,
            "final_code": best_overall_candidate["candidate_data"]["code"] if best_overall_candidate else initial_code,
            "final_score": best_overall_score,
            "best_candidate_details": best_overall_candidate,
            "history": iteration_history,
            "iterations_run": len(iteration_history)
        }

if __name__ == "__main__":
    import sys
    import os
    
    # Ensure project root is in system path so 'phase2' module is resolvable
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

    print("Initializing Iterative Optimizer...")
    try:
        optimizer = IterativeOptimizer(target_score=10.0, max_iterations=2)
        
        sample_code = """
def process_data(d):
    res = []
    for i in range(len(d)):
        if d[i] > 0:
            res.append(d[i])
    return res
"""
        
        print("Starting optimization on sample code...")
        result = optimizer.optimize(sample_code)
        
        print("\n=== Final Optimization Report ===")
        print("Initial Code:\n", result["initial_code"])
        print("\nFinal Optimized Code:\n", result["final_code"])
        print("\nTotal Iterations:", result["iterations_run"])
    except Exception as e:
        print(f"Error during execution: {e}")
