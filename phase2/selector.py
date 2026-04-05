import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
try:
    from scoring_api import evaluate
except ImportError as e:
    print(f"Error: Unable to import Phase 1 'scoring_api'. Ensure it exists in the parent directory.")
    print(e)

    def evaluate(code):
        return {'error': True, 'message': 'Phase 1 missing.'}
from typing import List, Dict, Any

class CandidateSelector:

    def select_best(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not candidates:
            return None
        evaluated_candidates = []
        for cand in candidates:
            code = cand['code']
            result = evaluate(code)
            if not result.get('error'):
                evaluated_candidates.append({'candidate_data': cand, 'score_result': result, 'risk_score': result.get('risk_score', 100)})
            else:
                print(f"Warning: Scoring failed for a candidate: {result.get('message')}")
        if not evaluated_candidates:
            print('Warning: All candidates failed during Phase 1 evaluation.')
            return None
        best_candidate = min(evaluated_candidates, key=lambda c: c['risk_score'])
        return best_candidate