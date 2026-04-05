"""
Candidate Generator Module (Phase 2)
Responsible for producing a diverse set of 3-5 code improvement candidates
using the DL Code Generator.
"""

from typing import List, Dict
from phase2.dl_generator import DLCodeGenerator

class CandidateGenerator:
    def __init__(self, dl_generator: DLCodeGenerator = None):
        """
        Initializes the candidate generator.
        
        Args:
            dl_generator: An existing instance of DLCodeGenerator, or None to create a new one.
        """
        self.dl_generator = dl_generator if dl_generator else DLCodeGenerator()
        
        # Define 3-5 variations using different prompts and temperatures for diversity
        self.strategies = [
            {
                "prompt": "Improve the readability and clarity of this code",
                "temperature": 0.5  # Lower temp = more predictable
            },
            {
                "prompt": "Reduce nesting and simplify the logic",
                "temperature": 0.7  # Medium temp = balanced
            },
            {
                "prompt": "Refactor this code for strict maintainability and best practices",
                "temperature": 0.85 # Higher temp = more creative/diverse
            }
        ]

    def generate_candidates(self, code: str) -> List[Dict[str, str]]:
        """
        Generates 3 variations of the input code based on predefined strategies.
        
        Args:
            code (str): The raw Python code to improve.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing the candidate code and strategy metadata.
        """
        candidates = []
        
        for i, strategy in enumerate(self.strategies):
            prompt = strategy["prompt"]
            temperature = strategy["temperature"]
            
            print(f"Generating candidate {i + 1}/{len(self.strategies)} (Temp: {temperature})...")
            generated_code = self.dl_generator.generate(
                code=code, 
                prompt=prompt, 
                temperature=temperature
            )
            
            candidates.append({
                "id": f"candidate_{i+1}",
                "code": generated_code,
                "prompt_used": prompt,
                "temperature_used": temperature
            })
            
        return candidates
