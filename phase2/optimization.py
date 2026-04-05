import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from typing import Dict, Any
from phase2.candidate_generator import CandidateGenerator
from phase2.validation import CodeValidator
from phase2.selector import CandidateSelector

class IterativeOptimizer:

    def __init__(self, target_score: float=20.0, max_iterations: int=3):
        self.target_score = target_score
        self.max_iterations = max_iterations
        self.generator = CandidateGenerator()
        self.validator = CodeValidator()
        self.selector = CandidateSelector()

    def optimize(self, initial_code: str) -> Dict[str, Any]:
        current_code = initial_code
        best_overall_candidate = None
        best_overall_score = float('inf')
        iteration_history = []
        for iteration in range(1, self.max_iterations + 1):
            print(f'\n--- Starting Optimization Iteration {iteration}/{self.max_iterations} ---')
            raw_candidates = self.generator.generate_candidates(current_code)
            valid_candidates = []
            for cand in raw_candidates:
                if self.validator.is_valid(current_code, cand['code']):
                    valid_candidates.append(cand)
                else:
                    print(f"Candidate {cand.get('id')} failed validation checks. Skipping.")
            if not valid_candidates:
                print('No valid candidates generated in this iteration. Halting optimization.')
                break
            best_iteration_candidate = self.selector.select_best(valid_candidates)
            if best_iteration_candidate is None:
                print('Failed to score candidates correctly in this iteration. Halting optimization.')
                break
            current_score = best_iteration_candidate.get('risk_score', float('inf'))
            print(f'Best candidate in iteration {iteration} achieved risk score: {current_score}')
            iteration_history.append({'iteration': iteration, 'best_candidate': best_iteration_candidate})
            if current_score < best_overall_score:
                best_overall_score = current_score
                best_overall_candidate = best_iteration_candidate
                current_code = best_iteration_candidate['candidate_data']['code']
            else:
                print('No improvement in this iteration. Continuing with previous best code.')
            if best_overall_score <= self.target_score:
                print(f'Target score of {self.target_score} achieved! Stopping early.')
                break
        print('\n=== Optimization Process Complete ===')
        print(f'Final Best Risk Score: {best_overall_score}')
        return {'initial_code': initial_code, 'final_code': best_overall_candidate['candidate_data']['code'] if best_overall_candidate else initial_code, 'final_score': best_overall_score, 'best_candidate_details': best_overall_candidate, 'history': iteration_history, 'iterations_run': len(iteration_history)}
if __name__ == '__main__':
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    print('Initializing Iterative Optimizer...')
    try:
        optimizer = IterativeOptimizer(target_score=10.0, max_iterations=2)
        sample_code = '\ndef process_data(d):\n    res = []\n    for i in range(len(d)):\n        if d[i] > 0:\n            res.append(d[i])\n    return res\n'
        print('Starting optimization on sample code...')
        result = optimizer.optimize(sample_code)
        print('\n=== Final Optimization Report ===')
        print('Initial Code:\n', result['initial_code'])
        print('\nFinal Optimized Code:\n', result['final_code'])
        print('\nTotal Iterations:', result['iterations_run'])
    except Exception as e:
        print(f'Error during execution: {e}')