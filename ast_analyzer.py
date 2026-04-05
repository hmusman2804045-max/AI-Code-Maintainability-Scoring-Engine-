import ast
import os

def _get_max_nesting_depth(tree):

    NESTING_NODES = (
        ast.If,
        ast.For,
        ast.While,
        ast.With,
        ast.Try,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    )

    def _walk_depth(node, current_depth):

        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, NESTING_NODES):
                child_depth = _walk_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = _walk_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)

        return max_depth

    return _walk_depth(tree, 0)

def _get_cyclomatic_complexity(tree):

    complexity = 1

    for node in ast.walk(tree):
        if isinstance(node, (
            ast.If,
            ast.For,
            ast.While,
            ast.ExceptHandler,
            ast.With,
            ast.Assert,
        )):
            complexity += 1

        if isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1

    return complexity

def _get_avg_function_length(tree):

    function_lengths = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                length = node.end_lineno - node.lineno + 1
                function_lengths.append(length)

    if not function_lengths:
        return 0

    return sum(function_lengths) / len(function_lengths)

def _check_recursion(tree):

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name

            for inner_node in ast.walk(node):
                if isinstance(inner_node, ast.Call):
                    if isinstance(inner_node.func, ast.Name):
                        if inner_node.func.id == func_name:
                            return 1

    return 0

def _count_global_variables(tree):

    global_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            global_count += len(node.names)

    return global_count

def extract_features(source):

    if os.path.isfile(source):
        with open(source, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        code = source

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "error": True,
            "message": f"Syntax error in code: {e.msg}",
            "line": e.lineno,
        }

    num_functions   = 0
    num_loops       = 0
    num_if          = 0
    num_try_except  = 0
    num_return      = 0

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_functions += 1

        elif isinstance(node, (ast.For, ast.While)):
            num_loops += 1

        elif isinstance(node, ast.If):
            num_if += 1

        elif isinstance(node, ast.Try):
            num_try_except += 1

        elif isinstance(node, ast.Return):
            num_return += 1

    line_count          = len(code.splitlines())
    max_nesting_depth   = _get_max_nesting_depth(tree)
    cyclomatic_complexity = _get_cyclomatic_complexity(tree)
    avg_function_length = _get_avg_function_length(tree)
    recursion_flag      = _check_recursion(tree)
    global_variable_count = _count_global_variables(tree)

    features = {
        "num_functions":        num_functions,
        "num_loops":            num_loops,
        "num_if":               num_if,
        "num_try_except":       num_try_except,
        "num_return":           num_return,
        "line_count":           line_count,
        "max_nesting_depth":    max_nesting_depth,
        "cyclomatic_complexity":cyclomatic_complexity,
        "avg_function_length":  round(avg_function_length, 2),
        "recursion_flag":       recursion_flag,
        "global_variable_count":global_variable_count,
    }

    return features

if __name__ == "__main__":

    sample_code = "def sample():\n    pass"

    result = extract_features(sample_code)

    print("=" * 50)
    print("  AST Feature Extraction Results")
    print("=" * 50)
    for feature, value in result.items():
        print(f"  {feature:<25} : {value}")
    print("=" * 50)
