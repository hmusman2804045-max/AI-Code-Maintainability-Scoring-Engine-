import ast
from typing import List, Dict

class CodeValidator:

    def __init__(self, min_length_ratio: float=0.5):
        self.min_length_ratio = min_length_ratio

    def _extract_function_signature(self, code: str):
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    return (node.name, args)
            return (None, None)
        except Exception:
            return (None, None)

    def is_valid(self, original_code: str, candidate_code: str) -> bool:
        if len(candidate_code.strip()) < len(original_code.strip()) * self.min_length_ratio:
            return False
        try:
            ast.parse(candidate_code)
        except SyntaxError:
            return False
        orig_name, orig_args = self._extract_function_signature(original_code)
        cand_name, cand_args = self._extract_function_signature(candidate_code)
        if orig_name and cand_name:
            if orig_name != cand_name:
                return False
            if sorted(orig_args) != sorted(cand_args):
                return False
        orig_has_return = 'return ' in original_code
        cand_has_return = 'return ' in candidate_code
        if orig_has_return and (not cand_has_return):
            return False
        return True

    def filter_valid_candidates(self, original_code: str, candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
        valid_candidates = []
        for cand in candidates:
            if self.is_valid(original_code, cand['code']):
                valid_candidates.append(cand)
        return valid_candidates