"""
Validation Layer Module (Phase 2)
Rule-based filtering to ensure DL-generated code is syntactically correct,
structurally safe, and not truncated before passing it to the ML scoring engine.
"""

import ast
from typing import List, Dict

class CodeValidator:
    def __init__(self, min_length_ratio: float = 0.5):
        """
        Initializes the rule-based code validator.
        
        Args:
            min_length_ratio (float): Minimum acceptable length of generated code 
                                      relative to the original code.
        """
        self.min_length_ratio = min_length_ratio

    def _extract_function_signature(self, code: str):
        """Extracts the first function name and its arguments from code."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Return name and argument names
                    args = [arg.arg for arg in node.args.args]
                    return node.name, args
            return None, None
        except Exception:
            return None, None

    def is_valid(self, original_code: str, candidate_code: str) -> bool:
        """
        Runs rule-based checks to validate the generated candidate.
        
        Args:
            original_code (str): The raw input code.
            candidate_code (str): The generated candidate code from DL model.
            
        Returns:
            bool: True if safe and valid, False otherwise.
        """
        # 1. Length / Completeness Check
        # Reject overly short code, as it might be truncated or hallucinated garbage
        if len(candidate_code.strip()) < len(original_code.strip()) * self.min_length_ratio:
            return False
            
        # 2. Syntax Validation using ast.parse()
        try:
            ast.parse(candidate_code)
        except SyntaxError:
            return False

        # 3. Structural Integrity (Function signature preservation)
        orig_name, orig_args = self._extract_function_signature(original_code)
        cand_name, cand_args = self._extract_function_signature(candidate_code)
        
        # If the original code had a function, ensure the candidate still has it
        if orig_name and cand_name:
            if orig_name != cand_name:
                return False
            if sorted(orig_args) != sorted(cand_args):
                return False

        # 4. Logic Preservation (Basic Heuristic)
        # E.g. Check if return statements are preserved if original had one
        orig_has_return = "return " in original_code
        cand_has_return = "return " in candidate_code
        if orig_has_return and not cand_has_return:
            return False

        return True

    def filter_valid_candidates(self, original_code: str, candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Filters a list of candidates, returning only the valid ones.
        
        Args:
            original_code: The raw input code.
            candidates: List of dictionaries containing candidate 'code'.
            
        Returns:
            A filtered list of valid candidates.
        """
        valid_candidates = []
        for cand in candidates:
            if self.is_valid(original_code, cand['code']):
                valid_candidates.append(cand)
        return valid_candidates
