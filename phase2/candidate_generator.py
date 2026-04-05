from typing import List, Dict
from phase2.dl_generator import DLCodeGenerator

class CandidateGenerator:

    def __init__(self, dl_generator: DLCodeGenerator=None):
        self.dl_generator = dl_generator if dl_generator else DLCodeGenerator()
        self.strategies = [{'prompt': 'Improve the readability and clarity of this code', 'temperature': 0.5}, {'prompt': 'Reduce nesting and simplify the logic', 'temperature': 0.7}, {'prompt': 'Refactor this code for strict maintainability and best practices', 'temperature': 0.85}]

    def generate_candidates(self, code: str) -> List[Dict[str, str]]:
        candidates = []
        for i, strategy in enumerate(self.strategies):
            prompt = strategy['prompt']
            temperature = strategy['temperature']
            print(f'Generating candidate {i + 1}/{len(self.strategies)} (Temp: {temperature})...')
            generated_code = self.dl_generator.generate(code=code, prompt=prompt, temperature=temperature)
            candidates.append({'id': f'candidate_{i + 1}', 'code': generated_code, 'prompt_used': prompt, 'temperature_used': temperature})
        return candidates