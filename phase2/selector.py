"""
Selection Engine Module (Phase 2)
Selects the best code candidate using the Phase 1 ML scoring engine.
"""

import os
import sys

# Ensure Phase 1 modules are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from scoring_api import evaluate
except ImportError as e:
    print(f"Error: Unable to import Phase 1 'scoring_api'. Ensure it exists in the parent directory.")
    print(e)
    # Provide a mock for development if needed
    def evaluate(code):
        return {"error": True, "message": "Phase 1 missing."}

from typing import List, Dict, Any

class CandidateSelector:
    """
    Evaluates valid candidates using the Phase 1 objective risk scoring engine.
    """
    
    def select_best(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs the evaluate() API on each valid candidate and selects the one with 
        the lowest risk score. 
        
        Args:
            candidates: List of valid candidate dictionaries containing 'code' and metadata.
            
        Returns:
            Dictionary containing the best candidate data and its evaluation score,
            or None if no candidates are provided/valid.
        """
        if not candidates:
            return None

        evaluated_candidates = []
        
        for cand in candidates:
            code = cand["code"]
            
            # Use Phase 1 API to judge the candidate
            result = evaluate(code)
            
            # Record it if scoring completes without error
            if not result.get("error"):
                evaluated_candidates.append({
                    "candidate_data": cand,
                    "score_result": result,
                    "risk_score": result.get("risk_score", 100) # Fallback to high risk
                })
            else:
                print(f"Warning: Scoring failed for a candidate: {result.get('message')}")

        if not evaluated_candidates:
            print("Warning: All candidates failed during Phase 1 evaluation.")
            return None

        # Select the candidate with the minimum risk score
        best_candidate = min(evaluated_candidates, key=lambda c: c["risk_score"])
        
        return best_candidate
