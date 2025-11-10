#!/usr/bin/env python3
"""
Compare TypeScript and Python test implementations (Hybrid Version with Phase 1 Improvements).

This script parses test code from both languages, extracts the sequence of operations,
and performs fuzzy matching to verify they implement the same test logic.

Phase 1 Improvements:
- Enhanced assertion normalization (toBe ↔ ==, toBeUndefined ↔ is None)
- Mock framework normalization (jest.fn() ↔ Mock())
- Undefined/null check normalization
"""

import ast
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
import subprocess

try:
    from tree_sitter import Language, Parser
    import tree_sitter_typescript as ts_ts
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False


# ===========================
# CONFIGURATION CONSTANTS
# ===========================

# Scoring Weights
# These weights determine the relative importance of different similarity metrics.
# The values were chosen based on empirical testing to balance structural exactness
# with semantic equivalence across TypeScript and Python test implementations.
STRUCTURAL_WEIGHT = 0.3  # Weight for exact sequence matching (30%)
SEMANTIC_WEIGHT = 0.7    # Weight for intent-based matching (70%)

# Semantic scoring sub-components
INTENT_SEQUENCE_WEIGHT = 0.5      # Weight for intent sequence similarity
INTENT_SET_WEIGHT = 0.3           # Weight for order-independent intent matching
TYPE_DISTRIBUTION_WEIGHT = 0.2    # Weight for step type distribution similarity

# Pass/Fail Thresholds
DEFAULT_SIMILARITY_THRESHOLD = 0.70  # Default threshold for PASS (70%)
SEMANTIC_FALLBACK_THRESHOLD = 0.40   # Semantic threshold for special cases (40%)
TOTAL_FALLBACK_THRESHOLD = 0.30      # Total threshold for special cases (30%)
FUZZY_MATCH_THRESHOLD = 0.70         # Threshold for fuzzy intent matching (70%)

# Normalization Limits
MAX_DICT_NORMALIZATION_ITERATIONS = 10  # Max iterations for nested dict normalization
MAX_LINE_LENGTH = 2000  # Maximum line length before truncation

# Test Framework Names
TEST_FRAMEWORK_FUNCTIONS = ['test', 'describe', 'it', 'beforeEach', 'afterEach', 'pytest', 'fixture']

# Mock/Callback Patterns
# Use word boundaries to avoid false positives (e.g., 'subscribe' containing 'cb')
MOCK_FUNCTION_PATTERNS = [r'\bmock_', r'\bcallback\b', r'\bcb\b', r'_cb\b',
                          r'\bgood_?cb\b', r'\bbad_?cb\b', r'\bfinal_?cb\b']
SETUP_FUNCTION_NAMES = ['type', 'mock', 'magicmock', 'patch', 'fixture', 'setup']
SETUP_VARIABLE_PREFIXES = ['mock_', 'test_', 'fixture_', 'setup_', 'given_']

# Default Directory Paths (can be overridden via environment variables or config)
import os
DEFAULT_TS_BASE_DIR = os.environ.get('TS_BASE_DIR', 'wallet-toolbox')
DEFAULT_PY_BASE_DIR = os.environ.get('PY_BASE_DIR', 'py-wallet-toolbox/tests')


@dataclass
class TestStep:
    """Represents a single step in a test."""
    type: str  # 'call', 'assignment', 'assertion', 'await', 'return'
    target: Optional[str] = None  # Variable being assigned to
    function: Optional[str] = None  # Function being called
    args: List[str] = None  # Argument names/values
    operator: Optional[str] = None  # For assertions: '==', '!=', etc.

    def __post_init__(self):
        if self.args is None:
            self.args = []

    def normalize(self) -> 'TestStep':
        """Normalize names for comparison (camelCase -> snake_case)."""
        normalized = TestStep(
            type=self.type,
            target=self._normalize_name(self.target) if self.target else None,
            function=self._normalize_name(self.function) if self.function else None,
            args=[self._normalize_name(arg) for arg in self.args],
            operator=self.operator
        )
        return normalized

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Convert camelCase/snake_case to normalized form."""
        if not name:
            return name

        # Convert camelCase to snake_case
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        name = name.lower()

        # Remove common prefixes/suffixes
        name = re.sub(r'^(test_|_test)', '', name)
        name = re.sub(r'(_test|test_)$', '', name)

        return name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class PythonTestParser:
    """Parse Python test code and extract test steps."""

    def parse_test(self, code: str) -> List[TestStep]:
        """Parse Python test code and return list of steps."""
        # Dedent the code to handle indented methods
        import textwrap
        code = textwrap.dedent(code)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"Python syntax error: {e}")
            return []

        steps = []

        # Find test functions (including async)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test_'):
                steps.extend(self._parse_function(node))

        return steps

    def _parse_function(self, func_node: ast.FunctionDef) -> List[TestStep]:
        """Parse a function and extract steps."""
        steps = []

        for stmt in func_node.body:
            step = self._parse_statement(stmt)
            if step:
                steps.append(step)

        return steps

    def _parse_statement(self, stmt: ast.AST) -> Optional[TestStep]:
        """Parse a single statement."""
        # Assignment
        if isinstance(stmt, ast.Assign):
            target = self._get_name(stmt.targets[0]) if stmt.targets else None

            # Handle await expressions
            value = stmt.value
            if isinstance(value, ast.Await):
                value = value.value

            # Check if RHS is a function call
            if isinstance(value, ast.Call):
                func_name = self._get_name(value.func)
                args = [self._get_name(arg) for arg in value.args]

                return TestStep(
                    type='assignment',
                    target=target,
                    function=func_name,
                    args=args
                )
            else:
                return TestStep(
                    type='assignment',
                    target=target
                )

        # Function call (expression statement)
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            func_name = self._get_name(stmt.value.func)
            args = [self._get_name(arg) for arg in stmt.value.args]

            return TestStep(
                type='call',
                function=func_name,
                args=args
            )

        # Assert statement
        elif isinstance(stmt, ast.Assert):
            # Handle assert all(...) or assert any(...)
            if isinstance(stmt.test, ast.Call):
                func_name = self._get_name(stmt.test.func)
                if func_name in ['all', 'any']:
                    # Extract the comparison from generator expression
                    if stmt.test.args and isinstance(stmt.test.args[0], ast.GeneratorExp):
                        gen_exp = stmt.test.args[0]
                        if isinstance(gen_exp.elt, ast.Compare):
                            # Extract the comparison
                            left = self._get_name(gen_exp.elt.left)
                            op = self._get_operator(gen_exp.elt.ops[0])
                            right = self._get_name(gen_exp.elt.comparators[0]) if gen_exp.elt.comparators else None
                            # For all(), we can represent it as checking all elements match
                            target = f"all({left} {op} {right})" if right else f"all({left})"
                            return TestStep(
                                type='assertion',
                                target=target,
                                operator='==',
                                args=['true'] if func_name == 'all' else []
                            )
                        else:
                            # Just extract the element expression
                            condition = self._get_name(gen_exp.elt)
                            return TestStep(
                                type='assertion',
                                target=condition,
                                operator='==',
                                args=['true'] if func_name == 'all' else []
                            )
                    elif stmt.test.args:
                        # Simple condition
                        condition = self._get_name(stmt.test.args[0])
                        return TestStep(
                            type='assertion',
                            target=condition,
                            operator='==',
                            args=['true'] if func_name == 'all' else []
                        )
            
            if isinstance(stmt.test, ast.Compare):
                left = self._get_name(stmt.test.left)
                op = self._get_operator(stmt.test.ops[0])
                right = self._get_name(stmt.test.comparators[0]) if stmt.test.comparators else None
                
                # Phase 1: Normalize "is None" to "is_undefined" for comparison
                if op == 'is' and right and right.lower() == 'none':
                    op = 'is_undefined'
                    right = None

                return TestStep(
                    type='assertion',
                    target=left,
                    operator=op,
                    args=[right] if right else []
                )

        # Await expression
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Await):
            return TestStep(type='await')

        return None

    def _get_name(self, node: ast.AST) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = self._get_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        elif isinstance(node, ast.Subscript):
            # Handle array indexing like r[i] or a[i]
            value = self._get_name(node.value)
            slice_val = self._get_name(node.slice) if hasattr(node, 'slice') and node.slice else ''
            return f"{value}[{slice_val}]" if slice_val else f"{value}[]"
        elif isinstance(node, ast.Call):
            # For call expressions, return the full call representation
            func_name = self._get_name(node.func)
            args = [self._get_name(arg) for arg in node.args]
            args_str = ', '.join(args) if args else ''
            return f"{func_name}({args_str})"
        elif isinstance(node, ast.Compare):
            # Handle comparisons like r[i] == a[i]
            left = self._get_name(node.left)
            op = self._get_operator(node.ops[0]) if node.ops else '=='
            right = self._get_name(node.comparators[0]) if node.comparators else ''
            return f"{left} {op} {right}" if right else left
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Dict):
            # Handle dictionary literals like {"partial": {}}
            # For comparison purposes, we'll represent it as a simplified form
            keys = [self._get_name(k) if k else '' for k in node.keys]
            values = [self._get_name(v) for v in node.values]
            pairs = [f"{k}:{v}" for k, v in zip(keys, values) if k]
            return '{' + ', '.join(pairs) + '}' if pairs else '{}'
        # Note: ast.Str and ast.Num were deprecated in Python 3.8 and removed in 3.14
        # ast.Constant handles all constant values (strings, numbers, etc.) in Python 3.8+
        return ""

    def _get_operator(self, op: ast.AST) -> str:
        """Get operator as string."""
        op_map = {
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.In: 'in',
            ast.NotIn: 'not in'
        }
        # Phase 1: Return normalized operator (will be further normalized in _normalize_assertion_operators)
        return op_map.get(type(op), str(op))


class TypeScriptTestParser:
    """Parse TypeScript test code and extract test steps using AST parsing."""

    def __init__(self):
        """Initialize the parser with tree-sitter if available."""
        self.parser = None
        self.language = None
        self.use_ast = False
        
        if TREE_SITTER_AVAILABLE:
            try:
                # Initialize tree-sitter TypeScript parser
                self.language = Language(ts_ts.language_typescript())
                self.parser = Parser(self.language)
                self.use_ast = True
            except Exception as e:
                print(f"Warning: Could not initialize tree-sitter parser: {e}")
                print("Falling back to regex-based parsing")
                self.use_ast = False

    def parse_test(self, code: str) -> List[TestStep]:
        """Parse TypeScript test code using AST or regex patterns."""
        if self.use_ast:
            return self._parse_with_ast(code)
        else:
            return self._parse_with_regex(code)

    def _parse_with_ast(self, code: str) -> List[TestStep]:
        """Parse TypeScript code using tree-sitter AST."""
        steps = []
        
        try:
            tree = self.parser.parse(bytes(code, 'utf8'))
            root_node = tree.root_node
            
            # Build parent map for easier traversal
            parent_map = {}
            def build_parent_map(node, parent=None):
                parent_map[node] = parent
                if hasattr(node, 'children'):
                    for child in node.children:
                        build_parent_map(child, node)
            build_parent_map(root_node)
            
            # Use regex only to check if code contains test() calls (flow control)
            has_test_call = bool(re.search(r'\btest\s*\(|it\s*\(|describe\s*\(', code))
            
            if has_test_call:
                # Find test functions (test(), it(), describe() calls)
                test_functions = self._find_test_functions(root_node, code, parent_map)
                
                if test_functions:
                    # We found test() calls - extract from their bodies only
                    for test_func in test_functions:
                        func_steps = self._extract_steps_from_function(test_func, code, parent_map)
                        steps.extend(func_steps)
                else:
                    # No test functions found in AST, but regex detected test() - parse root
                    # This handles edge cases where AST structure is different
                    root_steps = self._extract_statements_from_node(root_node, code, parent_map)
                    steps.extend(root_steps)
            else:
                # No test() wrapper - parse statements directly from root (code snippets)
                root_steps = self._extract_statements_from_node(root_node, code, parent_map)
                steps.extend(root_steps)
            
            return steps
        except (AttributeError, IndexError, KeyError) as e:
            # Specific errors from tree-sitter parsing
            import warnings
            warnings.warn(
                f"Tree-sitter AST parsing failed with {type(e).__name__}: {e}. "
                f"Falling back to regex parsing.",
                RuntimeWarning
            )
            return self._parse_with_regex(code)
        except UnicodeDecodeError as e:
            # Unicode encoding issues
            import warnings
            warnings.warn(
                f"Unicode decoding error: {e}. Falling back to regex parsing.",
                RuntimeWarning
            )
            return self._parse_with_regex(code)
        except Exception as e:
            # Catch-all for unexpected errors, but log them
            import warnings
            warnings.warn(
                f"Unexpected error in AST parsing: {type(e).__name__}: {e}. "
                f"Falling back to regex parsing. This may indicate a bug.",
                RuntimeWarning
            )
            return self._parse_with_regex(code)

    def _parse_with_regex(self, code: str) -> List[TestStep]:
        """Fallback regex-based parsing (original implementation)."""
        steps = []

        # Remove comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        lines = code.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('{') or line.startswith('}'):
                continue

            step = self._parse_line(line)
            if step:
                steps.append(step)

        return steps

    def _find_test_functions(self, node, code: str, parent_map: dict) -> List:
        """Find test function calls (test, it, describe) using AST."""
        test_functions = []
        
        # Check if this node is a call_expression (could be nested in expression_statement)
        if node.type == 'call_expression':
            # Check if this is a test function call
            func_name = self._get_function_name(node, code)
            if func_name in ['test', 'it', 'describe']:
                # Find the arrow function or function expression argument
                if hasattr(node, 'children'):
                    for child in node.children:
                        if child.type == 'arguments' and hasattr(child, 'children'):
                            # Look for arrow_function or function in arguments
                            for arg_child in child.children:
                                if arg_child.type in ['arrow_function', 'function', 'function_expression']:
                                    test_functions.append(arg_child)
        
        # Recursively search children
        if hasattr(node, 'children'):
            for child in node.children:
                test_functions.extend(self._find_test_functions(child, code, parent_map))
        
        return test_functions

    def _get_function_name(self, node, code: str) -> str:
        """Extract function name from a call expression."""
        if node.type == 'call_expression':
            for child in node.children:
                if child.type == 'identifier':
                    return code[child.start_byte:child.end_byte]
                elif child.type == 'member_expression':
                    # Handle obj.method() - get the method name
                    for subchild in child.children:
                        if subchild.type == 'property_identifier':
                            return code[subchild.start_byte:subchild.end_byte]
        return ''

    def _extract_steps_from_function(self, func_node, code: str, parent_map: dict) -> List[TestStep]:
        """Extract test steps from a function body."""
        steps = []
        
        # Find the function body - could be statement_block or expression_statement
        body = None
        if hasattr(func_node, 'children'):
            for child in func_node.children:
                if child.type == 'statement_block':
                    body = child
                    break
                elif child.type == 'expression_statement':
                    # Single expression function body
                    step = self._parse_statement(child, code, parent_map)
                    if step:
                        steps.append(step)
                    return steps
        
        if body:
            # Extract all statements from the body (handles nested blocks)
            body_steps = self._extract_statements_from_node(body, code, parent_map)
            steps.extend(body_steps)
        
        return steps
    
    def _extract_statements_from_node(self, node, code: str, parent_map: dict) -> List[TestStep]:
        """Recursively extract all statements from a node, handling nested blocks and control flow."""
        steps = []
        
        if not hasattr(node, 'children'):
            return steps
        
        for child in node.children:
            # Skip punctuation and braces
            if child.type in ['{', '}', '(', ')', ',', ';', ':', '=>']:
                continue
            
            # Handle statement blocks (nested blocks)
            if child.type == 'statement_block':
                # Recursively extract from nested blocks
                nested_steps = self._extract_statements_from_node(child, code, parent_map)
                steps.extend(nested_steps)
            # Handle for loops - extract from the body
            elif child.type == 'for_statement' or child.type == 'for_in_statement' or child.type == 'for_of_statement':
                # Extract statements from the loop body
                if hasattr(child, 'children'):
                    for subchild in child.children:
                        if subchild.type == 'statement_block':
                            loop_steps = self._extract_statements_from_node(subchild, code, parent_map)
                            steps.extend(loop_steps)
                        elif subchild.type == 'expression_statement':
                            # Single statement loop body
                            step = self._parse_statement(subchild, code, parent_map)
                            if step:
                                steps.append(step)
            # Handle if statements - extract from then/else blocks
            elif child.type == 'if_statement':
                if hasattr(child, 'children'):
                    for subchild in child.children:
                        if subchild.type == 'statement_block':
                            if_steps = self._extract_statements_from_node(subchild, code, parent_map)
                            steps.extend(if_steps)
            # Handle variable declarations
            elif child.type in ['lexical_declaration', 'variable_declaration']:
                step = self._parse_variable_declaration(child, code)
                if step:
                    steps.append(step)
            # Handle expression statements
            elif child.type == 'expression_statement':
                step = self._parse_statement(child, code, parent_map)
                if step:
                    steps.append(step)
            # Handle other statement types
            elif child.type.endswith('_statement'):
                step = self._parse_statement(child, code, parent_map)
                if step:
                    steps.append(step)
        
        return steps

    def _get_statements(self, node) -> List:
        """Get all statement nodes from a block."""
        statements = []
        
        if node.type == 'statement_block':
            for child in node.children:
                if child.type.endswith('_statement') or child.type == 'expression_statement':
                    statements.append(child)
        elif node.type == 'expression_statement':
            statements.append(node)
        
        return statements

    def _parse_statement(self, node, code: str, parent_map: dict) -> Optional[TestStep]:
        """Parse a statement node into a TestStep."""
        if not hasattr(node, 'children') or not node.children:
            return None
        
        # Check for expect() assertions - these are member_expression chains
        if node.type == 'expression_statement':
            expr = node.children[0]
            if expr:
                # Check if it's expect().toBe() pattern
                expect_step = self._parse_expect_assertion(expr, code, parent_map)
                if expect_step:
                    return expect_step
                
                # Check for other function calls
                if expr.type == 'call_expression':
                    return self._parse_function_call(expr, code)
        
        return None

    def _parse_expect_assertion(self, expr_node, code: str, parent_map: dict) -> Optional[TestStep]:
        """Parse expect().toBe() or expect().not.toBe() patterns using AST."""
        # expect().toBe() structure:
        # call_expression (toBe)
        #   -> member_expression
        #       -> call_expression (expect)
        #       -> property_identifier (toBe)
        
        if expr_node.type != 'call_expression':
            return None
        
        # Get the method name (toBe, toEqual, etc.)
        method_name = self._get_function_name(expr_node, code)
        if method_name not in ['toBe', 'toEqual', 'toStrictEqual', 'toBeGreaterThan', 
                              'toBeLessThan', 'toBeTruthy', 'toBeFalsy', 'toBeGreaterThanOrEqual',
                              'toBeLessThanOrEqual', 'toBeNull', 'toBeUndefined', 'toBeDefined']:
            return None
        
        method_call = expr_node
        expect_call = None
        is_not = False
        
        # Find the member_expression that contains expect()
        if hasattr(expr_node, 'children'):
            for child in expr_node.children:
                if child.type == 'member_expression':
                    # Traverse to find expect() call
                    expect_call = self._find_expect_in_member_expression(child, code)
                    # Check for 'not' in the chain
                    if self._has_not_in_chain(child, code):
                        is_not = True
                    break
        
        if not expect_call:
            return None
        
        # Get arguments
        expect_arg = self._get_first_argument(expect_call, code)
        method_arg = self._get_first_argument(method_call, code)
        
        if not expect_arg:
            return None
        
        target = code[expect_arg.start_byte:expect_arg.end_byte]
        # Remove await keyword (async differences are whitelisted)
        target = re.sub(r'\bawait\s+', '', target).strip()
        
        if is_not:
            method_name = f'not.{method_name}'
        
        operator = self._jest_to_operator(method_name)
        arg_text = code[method_arg.start_byte:method_arg.end_byte].strip() if method_arg else ''
        
        return TestStep(
            type='assertion',
            target=target,
            operator=operator,
            args=[arg_text] if arg_text else []
        )
    
    def _find_expect_in_member_expression(self, node, code: str):
        """Find expect() call within a member_expression."""
        if not hasattr(node, 'children'):
            return None
        
        for child in node.children:
            if child.type == 'call_expression':
                func_name = self._get_function_name(child, code)
                if func_name == 'expect':
                    return child
            elif child.type == 'member_expression':
                result = self._find_expect_in_member_expression(child, code)
                if result:
                    return result
        return None
    
    def _has_not_in_chain(self, node, code: str) -> bool:
        """Check if 'not' appears in a member_expression chain."""
        if not hasattr(node, 'children'):
            return False
        
        for child in node.children:
            if child.type == 'property_identifier':
                prop_name = code[child.start_byte:child.end_byte]
                if prop_name == 'not':
                    return True
            elif child.type == 'member_expression':
                if self._has_not_in_chain(child, code):
                    return True
        return False
    
    def _get_first_argument(self, call_node, code: str):
        """Get the first argument from a call_expression."""
        if not hasattr(call_node, 'children'):
            return None
        
        for child in call_node.children:
            if child.type == 'arguments' and hasattr(child, 'children'):
                for arg_child in child.children:
                    if arg_child.type not in ['(', ')', ',']:
                        return arg_child
        return None

    def _parse_variable_declaration(self, node, code: str) -> Optional[TestStep]:
        """Parse variable declaration (const/let/var x = ...) using AST."""
        if not hasattr(node, 'children'):
            return None
        
        target = None
        value_node = None
        
        # Find the variable declarator
        for child in node.children:
            if child.type == 'variable_declarator':
                if hasattr(child, 'children'):
                    for subchild in child.children:
                        if subchild.type == 'identifier':
                            target = code[subchild.start_byte:subchild.end_byte]
                        elif subchild.type in ['call_expression', 'await_expression', 'new_expression', 
                                               'object', 'array', 'binary_expression', 'member_expression']:
                            # Handle await expressions by getting the inner expression
                            if subchild.type == 'await_expression':
                                if hasattr(subchild, 'children'):
                                    for await_child in subchild.children:
                                        if await_child.type == 'call_expression':
                                            value_node = await_child
                                            break
                            else:
                                value_node = subchild
                break
        
        if not target:
            return None
        
        # Check if value is a function call
        if value_node and value_node.type == 'call_expression':
            func_name = self._get_call_expression_name(value_node, code)
            args = self._get_call_arguments(value_node, code)
            
            return TestStep(
                type='assignment',
                target=target,
                function=func_name,
                args=args
            )
        elif value_node:
            # Assignment without function call
            value_text = code[value_node.start_byte:value_node.end_byte]
            # Remove await keyword if present
            value_text = re.sub(r'\bawait\s+', '', value_text).strip()
            return TestStep(
                type='assignment',
                target=target,
                args=[value_text]
            )
        
        return None

    def _parse_function_call(self, call_node, code: str) -> Optional[TestStep]:
        """Parse a function call expression."""
        func_name = self._get_call_expression_name(call_node, code)
        
        # Skip expect() calls (handled separately)
        if func_name == 'expect':
            return None
        
        args = self._get_call_arguments(call_node, code)
        
        return TestStep(
            type='call',
            function=func_name,
            args=args
        )

    def _get_call_expression_name(self, call_node, code: str) -> str:
        """Get the function name from a call expression using AST."""
        if not hasattr(call_node, 'children'):
            return ''
        
        for child in call_node.children:
            if child.type == 'identifier':
                return code[child.start_byte:child.end_byte]
            elif child.type == 'member_expression':
                # Handle obj.method() - return "obj.method"
                parts = []
                if hasattr(child, 'children'):
                    for subchild in child.children:
                        if subchild.type in ['identifier', 'property_identifier', 'shorthand_property_identifier']:
                            parts.append(code[subchild.start_byte:subchild.end_byte])
                        elif subchild.type == 'member_expression':
                            # Handle nested member expressions like obj.prop.method()
                            nested_name = self._get_call_expression_name(subchild, code)
                            if nested_name:
                                parts.append(nested_name)
                return '.'.join(parts) if parts else ''
        return ''

    def _get_call_arguments(self, call_node, code: str) -> List[str]:
        """Extract arguments from a call expression using AST."""
        args = []
        
        if not hasattr(call_node, 'children'):
            return args
        
        for child in call_node.children:
            if child.type == 'arguments':
                # Get argument nodes (skip punctuation)
                if hasattr(child, 'children'):
                    for arg_node in child.children:
                        if arg_node.type not in ['(', ')', ',']:
                            arg_text = code[arg_node.start_byte:arg_node.end_byte]
                            # Remove await keyword (async differences are whitelisted)
                            arg_text = re.sub(r'\bawait\s+', '', arg_text).strip()
                            args.append(arg_text)
        
        return args

    def _parse_line(self, line: str) -> Optional[TestStep]:
        """Parse a single line of TypeScript (regex fallback)."""
        # Expect assertions
        match = re.match(r'expect\((.*?)\)\.(?:not\.)?(\w+)\((.*?)\)', line)
        if match:
            target, assertion, arg = match.groups()
            target = re.sub(r'\bawait\s+', '', target).strip()
            if 'not.' in line and line.find('not.') < line.find(assertion):
                assertion = f'not.{assertion}'
            operator = self._jest_to_operator(assertion)
            return TestStep(
                type='assertion',
                target=target,
                operator=operator,
                args=[arg.strip()] if arg.strip() else []
            )

        # Variable assignment with function call
        match = re.match(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            target, func, args_str = match.groups()
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            args = [re.sub(r'\bawait\s+', '', arg) for arg in args]
            return TestStep(
                type='assignment',
                target=target,
                function=func,
                args=args
            )

        # Assignment without function call
        match = re.match(r'(?:const|let|var)\s+(\w+)\s*=\s*(.+)', line)
        if match:
            target, value = match.groups()
            return TestStep(
                type='assignment',
                target=target,
                args=[value.rstrip(';')]
            )

        # Function call
        match = re.match(r'(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            func, args_str = match.groups()
            if func == 'expect':
                return None
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            args = [re.sub(r'\bawait\s+', '', arg) for arg in args]
            return TestStep(
                type='call',
                function=func,
                args=args
            )

        return None

    def _jest_to_operator(self, jest_assertion: str) -> str:
        """Convert Jest assertion to operator."""
        mapping = {
            'toBe': '==',
            'toEqual': '==',
            'toStrictEqual': '==',
            'not.toBe': '!=',
            'not.toEqual': '!=',
            'toBeGreaterThan': '>',
            'toBeGreaterThanOrEqual': '>=',
            'toBeLessThan': '<',
            'toBeLessThanOrEqual': '<=',
            'toBeTruthy': '== true',
            'toBeFalsy': '== false',
            'toBeNull': '== null',
            'toBeUndefined': '== undefined',
            'toBeDefined': '!= undefined',
        }
        return mapping.get(jest_assertion, jest_assertion)


class TestComparator:
    """Compare test implementations."""

    def __init__(self):
        self.py_parser = PythonTestParser()
        self.ts_parser = TypeScriptTestParser()

    def compare_tests(self, ts_code: str, py_code: str) -> Dict[str, Any]:
        """Compare TypeScript and Python test implementations."""

        # Parse both tests
        ts_steps = self.ts_parser.parse_test(ts_code)
        py_steps = self.py_parser.parse_test(py_code)

        # Filter out test framework calls (test(), describe(), etc.)
        ts_steps = [s for s in ts_steps if not (s.type == 'call' and s.function in ['test', 'describe', 'it', 'beforeEach', 'afterEach'])]
        py_steps = [s for s in py_steps if not (s.type == 'call' and s.function in ['pytest', 'fixture'])]
        
        # Filter out Python setup code (mock creation, fixtures, etc.)
        # This whitelists setup code so it doesn't affect similarity scores
        py_steps = [s for s in py_steps if not self._is_setup_code(s)]
        
        # Normalize async/await differences - remove async markers from arguments
        # This whitelists async differences so they don't affect similarity scores
        for step in ts_steps + py_steps:
            if step.args:
                step.args = [re.sub(r'\bawait\s+', '', arg) for arg in step.args]
                step.args = [re.sub(r'\basync\s+', '', arg) for arg in step.args]
            if step.target:
                step.target = re.sub(r'\bawait\s+', '', step.target)
                step.target = re.sub(r'\basync\s+', '', step.target)

        # Normalize steps
        ts_normalized = [step.normalize() for step in ts_steps]
        py_normalized = [step.normalize() for step in py_steps]

        # Normalize assignment+assertion patterns to match direct function calls in assertions
        # e.g., "count = func()" + "assert count == X" should match "expect(func()).toBe(X)"
        ts_normalized = self._normalize_assignment_assertion_patterns(ts_normalized)
        py_normalized = self._normalize_assignment_assertion_patterns(py_normalized)

        # Phase 1: Enhanced semantic normalization
        # Normalize mock functions (jest.fn() ↔ Mock() ↔ custom functions)
        ts_normalized = self._normalize_mock_functions(ts_normalized)
        py_normalized = self._normalize_mock_functions(py_normalized)
        
        # Normalize assertion operators (toBe ↔ ==, toBeUndefined ↔ is None)
        ts_normalized = self._normalize_assertion_operators(ts_normalized)
        py_normalized = self._normalize_assertion_operators(py_normalized)


        # Phase 2: Multi-tier scoring (Structural × 0.3 + Semantic × 0.7)
        structural_score = self._calculate_structural_similarity(ts_normalized, py_normalized)
        semantic_score = self._calculate_semantic_similarity(ts_normalized, py_normalized)
        
        # Hybrid score: Weight semantic more heavily
        similarity = (structural_score * 0.3) + (semantic_score * 0.7)

        # Find matching and differing steps
        matches, differences = self._align_steps(ts_normalized, py_normalized)
        
        # Analyze and generate suggestions
        ts_steps_detailed = [step.to_dict() for step in ts_steps]
        py_steps_detailed = [step.to_dict() for step in py_steps]
        analysis = self.analyze_and_suggest(
            ts_normalized, py_normalized, 
            ts_steps_detailed, py_steps_detailed,
            similarity, differences, semantic_score
        )

        return {
            'ts_steps': len(ts_steps),
            'py_steps': len(py_steps),
            'similarity': similarity,
            'structural_score': structural_score,
            'semantic_score': semantic_score,
            'matches': matches,
            'differences': differences,
            'ts_steps_detailed': ts_steps_detailed,
            'py_steps_detailed': py_steps_detailed,
            'analysis': analysis,
        }

    def _calculate_structural_similarity(self, ts_steps: List[TestStep], py_steps: List[TestStep]) -> float:
        """Calculate structural similarity (exact sequence matching)."""
        if not ts_steps and not py_steps:
            return 1.0
        if not ts_steps or not py_steps:
            return 0.0

        # Convert steps to comparable strings
        ts_strings = [self._step_to_string(step) for step in ts_steps]
        py_strings = [self._step_to_string(step) for step in py_steps]

        # Use SequenceMatcher for sequence comparison
        matcher = SequenceMatcher(None, ts_strings, py_strings)
        return matcher.ratio()
    
    def _calculate_semantic_similarity(self, ts_steps: List[TestStep], py_steps: List[TestStep]) -> float:
        """Phase 2: Calculate semantic similarity based on test intent."""
        if not ts_steps and not py_steps:
            return 1.0
        if not ts_steps or not py_steps:
            return 0.0
        
        # Extract test intents
        ts_intents = self._extract_test_intents(ts_steps)
        py_intents = self._extract_test_intents(py_steps)
        
        # Compare intents using sequence matching
        matcher = SequenceMatcher(None, ts_intents, py_intents)
        intent_similarity = matcher.ratio()
        
        # Also use fuzzy matching for intent sets (not just sequence)
        # This helps when tests have same operations but in different order
        intent_set_similarity = self._compare_intent_sets(ts_intents, py_intents)
        
        # Also consider step type distribution (e.g., same ratio of assertions/assignments)
        ts_types = [step.type for step in ts_steps]
        py_types = [step.type for step in py_steps]
        type_distribution = self._compare_type_distribution(ts_types, py_types)
        
        # Combine: sequence similarity, set similarity, and type distribution
        semantic_score = (intent_similarity * 0.5) + (intent_set_similarity * 0.3) + (type_distribution * 0.2)
        
        return semantic_score
    
    def _compare_intent_sets(self, ts_intents: List[str], py_intents: List[str]) -> float:
        """Compare intent sets (order-independent) using fuzzy matching."""
        from collections import Counter
        
        if not ts_intents and not py_intents:
            return 1.0
        if not ts_intents or not py_intents:
            return 0.0
        
        # Count occurrences of each intent
        ts_counter = Counter(ts_intents)
        py_counter = Counter(py_intents)
        
        # Get all unique intents
        all_intents = set(ts_intents + py_intents)
        
        # Calculate similarity for each intent
        total_ts = len(ts_intents)
        total_py = len(py_intents)
        
        similarities = []
        for intent in all_intents:
            ts_count = ts_counter.get(intent, 0)
            py_count = py_counter.get(intent, 0)
            
            # Ratio of occurrences
            ts_ratio = ts_count / total_ts if total_ts > 0 else 0
            py_ratio = py_count / total_py if total_py > 0 else 0
            
            # Similarity is based on how close the ratios are
            # If both have it, similarity is high
            # If one has it and other doesn't, similarity is lower
            if ts_count > 0 and py_count > 0:
                # Both have it - similarity based on ratio closeness
                similarity = 1.0 - abs(ts_ratio - py_ratio)
            elif ts_count > 0 or py_count > 0:
                # Only one has it - check if similar intent exists
                # Use fuzzy matching to find similar intents
                best_match = self._find_similar_intent(intent, 
                                                      py_intents if ts_count > 0 else ts_intents)
                if best_match and best_match[1] > 0.7:  # 70% similarity threshold
                    similarity = best_match[1] * 0.5  # Penalize for not exact match
                else:
                    similarity = 0.0
            else:
                similarity = 1.0  # Neither has it (shouldn't happen)
            
            # Weight by frequency
            weight = (ts_ratio + py_ratio) / 2
            similarities.append(similarity * weight)
        
        # Return weighted average
        total_weight = sum((ts_counter.get(i, 0) / total_ts + py_counter.get(i, 0) / total_py) / 2 
                          for i in all_intents) if all_intents else 1.0
        return sum(similarities) / total_weight if total_weight > 0 else 0.0
    
    def _find_similar_intent(self, intent: str, intent_list: List[str]) -> tuple:
        """Find most similar intent in list using fuzzy matching."""
        if not intent_list:
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        for other_intent in intent_list:
            matcher = SequenceMatcher(None, intent, other_intent)
            score = matcher.ratio()
            if score > best_score:
                best_score = score
                best_match = other_intent
        
        return best_match, best_score
    
    def _extract_test_intents(self, steps: List[TestStep]) -> List[str]:
        """Phase 2: Extract semantic intent from test steps."""
        intents = []
        for step in steps:
            if step.type == 'assertion':
                # Extract what's being verified
                target = step.target or 'value'
                operator = step.operator or '=='
                # Normalize target for intent (remove variable names, keep structure)
                intent_target = self._normalize_intent_target(target)
                # Normalize operator for intent
                intent_operator = self._normalize_intent_operator(operator)
                
                # Special handling for callback/mock verification patterns
                # toHaveBeenCalledTimes() and "callback" in call_order are equivalent
                # Check if this is a callback verification step
                is_callback_verification = False
                if intent_operator == 'in_check' and ('callback' in intent_target.lower() or 'call_order' in str(step.target).lower()):
                    is_callback_verification = True
                elif step.function and ('verify_mock_called' in step.function.lower() or 'tohavebeencalled' in step.function.lower()):
                    is_callback_verification = True
                elif step.type == 'call' and step.function and ('tohavebeencalled' in step.function.lower()):
                    is_callback_verification = True
                
                if is_callback_verification:
                    intent = "verify_callback_called"
                else:
                    intent = f"verify_{intent_target}_{intent_operator}"
                intents.append(intent)
            elif step.type == 'assignment':
                # Extract what operation is being performed
                function = step.function or 'assign'
                # Normalize function name for intent (listActions -> list_actions -> list)
                intent_function = self._normalize_intent_function(function)
                
                # Special handling: jest.fn() and custom callback functions are equivalent
                if intent_function == 'mock_function' or 'callback' in function.lower():
                    intent = "create_callback"
                else:
                    intent = f"assign_{intent_function}"
                intents.append(intent)
            elif step.type == 'call':
                # Extract what function is being called
                function = step.function or 'call'
                # Normalize function name for intent
                intent_function = self._normalize_intent_function(function)
                
                # Special handling: bindCallback and bind_callback are equivalent
                if 'bind' in intent_function and 'callback' in intent_function:
                    intent = "bind_callback"
                elif 'trigger' in intent_function and 'callback' in intent_function:
                    intent = "trigger_callbacks"
                else:
                    intent = f"call_{intent_function}"
                intents.append(intent)
        return intents
    
    def _normalize_intent_target(self, target: str) -> str:
        """Normalize target for intent extraction (remove variable names)."""
        if not target:
            return 'value'

        # Replace variable names with generic placeholders
        # e.g., "r.length" -> "array.length", "a.inputs" -> "object.property"
        target_lower = target.lower()

        # Common patterns - check these first with proper word boundaries
        # Use regex for more precise matching
        import re

        # Check for .length property access or len() function
        if re.search(r'\.length\b', target_lower) or re.search(r'\blen\(', target_lower):
            return 'array_length'
        # Check for .every() method or all() function
        if re.search(r'\.every\(', target_lower) or re.search(r'\ball\(', target_lower):
            return 'array_all'
        # Check for undefined/none checks
        if re.search(r'\bundefined\b', target_lower) or re.search(r'\bnone\b', target_lower) or 'not in' in target_lower:
            return 'undefined_check'
        # Check for Array.isArray or is_array
        if re.search(r'\bisarray\(', target_lower) or re.search(r'\bis_array\(', target_lower):
            return 'is_array'
        
        # Property access patterns (e.g., r.totalActions, result.totalActions -> object_total)
        # Also handle "totalActions in" (Python style membership check)
        if '.' in target:
            parts = target.split('.')
            if len(parts) >= 2:
                # Extract property name (last part)
                property_name = parts[-1].lower()
                # Normalize property names (totalActions -> total_actions -> total)
                property_normalized = self._normalize_property_name(property_name)
                return f"object_{property_normalized}"
        
        # Handle Python-style membership checks (e.g., "totalActions in result")
        # These are semantically equivalent to property access
        if ' in ' in target_lower:
            # Extract the property name before "in"
            parts = target_lower.split(' in ')
            if len(parts) >= 1:
                property_name = parts[0].strip().strip('"\'')
                property_normalized = self._normalize_property_name(property_name)
                return f"object_{property_normalized}"
        
        # Function call patterns (e.g., storage.countProvenTxs(...) -> call_result_count_proven)
        if '(' in target:
            # Extract function name before (
            func_match = target.split('(')[0].strip()
            if '.' in func_match:
                func_name = func_match.split('.')[-1]
                func_normalized = self._normalize_intent_function(func_name)
                return f"call_result_{func_normalized}"
        
        # Simple variable names (e.g., "count", "r", "a") -> generic value
        # But preserve structure hints
        if target_lower in ['count', 'r', 'a', 'result', 'value', 'param']:
            return 'value'
        
        return 'value'
    
    def _normalize_intent_operator(self, operator: str) -> str:
        """Normalize operator for intent extraction."""
        if not operator:
            return 'equals'
        
        operator_lower = operator.lower()
        
        # Map to semantic categories
        if operator_lower in ['==', 'tobe', 'to_be', 'toequal', 'to_equal']:
            return 'equals'
        if operator_lower in ['!=', 'not.tobe', 'not_to_be']:
            return 'not_equals'
        if operator_lower in ['is_undefined', 'tobeundefined', 'to_be_undefined', '== undefined', '== none', 'is none']:
            return 'is_undefined'
        if operator_lower in ['>=', 'tobegreaterthanorequal', 'to_be_greater_than_or_equal']:
            return 'greater_or_equal'
        if operator_lower in ['>', 'tobegreaterthan', 'to_be_greater_than']:
            return 'greater'
        if operator_lower in ['<=', 'tobelessthanorequal', 'to_be_less_than_or_equal']:
            return 'less_or_equal'
        if operator_lower in ['<', 'tobelessthan', 'to_be_less_than']:
            return 'less'
        if 'in' in operator_lower:
            return 'in_check'
        
        return operator_lower.replace(' ', '_').replace('.', '_')
    
    def _normalize_intent_function(self, function: str) -> str:
        """Normalize function name for intent extraction."""
        if not function:
            return 'unknown'
        
        func_lower = function.lower()
        
        # Normalize common patterns
        # listActions -> list_actions -> list
        # countProvenTxs -> count_proven_txs -> count_proven
        # bindCallback -> bind_callback -> bind
        
        # Convert camelCase to snake_case
        import re
        func_normalized = re.sub('([a-z0-9])([A-Z])', r'\1_\2', func_lower)
        func_normalized = func_normalized.lower()
        
        # Extract base operation (remove common suffixes)
        # list_actions -> list, count_proven_txs -> count_proven, bind_callback -> bind
        if '_' in func_normalized:
            parts = func_normalized.split('_')
            # Keep first 2 parts max (e.g., count_proven, not count_proven_txs)
            if len(parts) >= 2:
                return '_'.join(parts[:2])
            return parts[0]
        
        return func_normalized
    
    def _normalize_property_name(self, property_name: str) -> str:
        """Normalize property name for intent (totalActions -> total)."""
        if not property_name:
            return 'property'
        
        # Remove quotes if present
        property_name = property_name.strip().strip('"\'')
        
        # Convert camelCase to snake_case
        import re
        normalized = re.sub('([a-z0-9])([A-Z])', r'\1_\2', property_name.lower())
        
        # Extract meaningful base
        # totalActions -> total_actions -> total
        # actionsLength -> actions_length -> actions
        # inputs -> inputs
        if '_' in normalized:
            parts = normalized.split('_')
            # For compound names, prefer the first meaningful part
            # But keep common patterns like "total_actions" -> "total"
            if len(parts) >= 2:
                # If first part is a common prefix (total, num, count), use it
                if parts[0] in ['total', 'num', 'count', 'all', 'some']:
                    return parts[0]
                # Otherwise, use first two parts joined
                return '_'.join(parts[:2])
            return parts[0]
        
        # Single word - return as is
        return normalized
    
    def _compare_type_distribution(self, ts_types: List[str], py_types: List[str]) -> float:
        """Compare the distribution of step types between tests."""
        from collections import Counter
        
        ts_counter = Counter(ts_types)
        py_counter = Counter(py_types)
        
        # Get all unique types
        all_types = set(ts_types + py_types)
        if not all_types:
            return 1.0
        
        # Calculate ratio for each type
        total_ts = len(ts_types) if ts_types else 1
        total_py = len(py_types) if py_types else 1
        
        similarities = []
        for step_type in all_types:
            ts_ratio = ts_counter.get(step_type, 0) / total_ts
            py_ratio = py_counter.get(step_type, 0) / total_py
            # Similarity is 1 - absolute difference
            similarity = 1.0 - abs(ts_ratio - py_ratio)
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0

    def _step_to_string(self, step: TestStep) -> str:
        """Convert step to comparable string with normalized arguments."""
        parts = [step.type]
        if step.target:
            # Normalize semantically equivalent targets (r.length -> len(r), etc.)
            target = self._normalize_target(step.target)
            parts.append(f"target:{target}")
        if step.function:
            # Use the function as-is (should already be normalized by _normalize_mock_functions)
            parts.append(f"func:{step.function}")
        if step.operator:
            # Use the operator as-is (should already be normalized by _normalize_assertion_operators)
            parts.append(f"op:{step.operator}")
        if step.args:
            # Normalize args: strip quotes, normalize whitespace
            normalized_args = [self._normalize_arg(arg) for arg in step.args]
            parts.append(f"args:{','.join(normalized_args)}")
        return '|'.join(parts)

    def _normalize_assignment_assertion_patterns(self, steps: List[TestStep]) -> List[TestStep]:
        """Normalize assignment+assertion patterns to match direct function calls in assertions.

        Converts:
        - assignment: count = func(args)
        - assertion: count == value
        Into:
        - assertion: func(args) == value

        This makes Python's pattern match TypeScript's direct function call in expect().

        Note: This function should be called AFTER normalize() so that variable names
        are already normalized (camelCase -> snake_case).
        """
        normalized = []
        i = 0
        while i < len(steps):
            # Validate index bounds
            if i >= len(steps):
                break

            current = steps[i]

            # Check if this is an assignment followed by an assertion on the same variable
            # We need to check both exact match and normalized match
            if (i + 1 < len(steps) and
                current.type == 'assignment' and
                current.target and
                current.function and
                steps[i + 1].type == 'assertion' and
                steps[i + 1].target):

                next_step = steps[i + 1]

                # Compare normalized targets (handle both exact and fuzzy matches)
                # Normalize both for comparison
                current_target_norm = current.target.lower().strip()
                next_target_norm = next_step.target.lower().strip()

                # Check if targets match (exact or normalized)
                targets_match = (next_step.target == current.target or
                               next_target_norm == current_target_norm)

                if targets_match:
                    # This is assignment+assertion pattern - normalize to direct function call assertion
                    # Create a new assertion with the function call as the target
                    normalized_step = TestStep(
                        type='assertion',
                        target=f"{current.function}({','.join(current.args)})" if current.args else current.function,
                        operator=next_step.operator,
                        args=next_step.args
                    )
                    normalized.append(normalized_step)
                    i += 2  # Skip both steps
                    continue

            # If no pattern match, keep the current step as-is
            normalized.append(current)
            i += 1

        return normalized

    def _normalize_target(self, target: str) -> str:
        """Normalize semantically equivalent target expressions."""
        if not target:
            return target
        
        import re
        
        # Phase 1: Normalize undefined/null checks
        # .toBeUndefined() ↔ is None ↔ "x" not in obj
        # These all verify "value doesn't exist or is undefined"
        # Check for all possible forms (original and normalized)
        target_lower = target.lower()
        undefined_patterns = [
            'tobeundefined', 'to_be_undefined',  # Jest original and normalized
            'is none', 'is_none', 'isnone',      # Python forms
            '== undefined', '== none',           # Direct comparisons
            'is_undefined_check'                 # Already normalized
        ]
        if any(pattern in target_lower for pattern in undefined_patterns):
            return "is_undefined_check"
        if 'not in' in target_lower or 'not_in' in target_lower:
            # Check if it's a "key not in dict" pattern (undefined check)
            # Look for string literal followed by "not in"
            if re.search(r'["\']\w+["\']\s+(?:not\s+)?in', target):
                return "is_undefined_check"
        
        # Normalize r.length to len(r) for comparison (use word boundary)
        match = re.match(r'(\w+)\.length\b', target)
        if match:
            return f"len({match.group(1)})"

        # Normalize r.every((v, i) => v === a[i]) to all(elements_match)
        # and all(r[i] == a[i]) to all(elements_match)
        # Both represent "check all elements match"
        # Use word boundaries to avoid matching 'everything' or 'gallery'
        if re.search(r'\.every\(', target.lower()) or re.match(r'\ball\(', target):
            # Check if it's a comparison of array elements
            if '==' in target or '===' in target:
                return "all(elements_match)"
            return "all(elements_match)"
        
        # Normalize variable names: storage vs mock_storage are equivalent
        # Extract function calls and normalize the object name
        # e.g., "storage.countProvenTxs(...)" and "mock_storage.count_proven_txs(...)" should match
        # We normalize to just the function name for comparison
        func_call_match = re.match(r'(\w+)(?:\.|_)?(\w+)\(', target)
        if func_call_match:
            # Extract just the function name part, ignore the object name
            # This makes storage.func() and mock_storage.func() equivalent
            obj_name, func_name = func_call_match.groups()
            # Keep the full call but normalize object names
            normalized_obj = 'storage' if 'storage' in obj_name.lower() or 'mock' in obj_name.lower() else obj_name
            # Replace the object name with normalized version
            target = re.sub(r'^(\w+)(?:\.|_)?', f'{normalized_obj}.', target, count=1)
        
        # Normalize dictionary/object spacing in function call arguments
        # { partial: {} } should match {partial:{}} and { partial:{} }
        if '{' in target and '}' in target:
            # Remove all whitespace inside dictionaries (handles nested dicts)
            import re
            import warnings
            # Recursively remove whitespace from dictionary contents
            # Match innermost dicts first, then work outward
            iteration = 0
            while iteration < MAX_DICT_NORMALIZATION_ITERATIONS:
                new_target = re.sub(r'\{([^{}]*)\}', lambda m: '{' + re.sub(r'\s+', '', m.group(1)) + '}', target)
                if new_target == target:
                    break
                target = new_target
                iteration += 1

            # Warn if we hit the iteration limit (normalization may be incomplete)
            if iteration >= MAX_DICT_NORMALIZATION_ITERATIONS:
                warnings.warn(
                    f"Dictionary normalization hit max iterations ({MAX_DICT_NORMALIZATION_ITERATIONS}) "
                    f"for target: {target[:50]}... Normalization may be incomplete.",
                    RuntimeWarning
                )

        return target

    def _normalize_arg(self, arg: str) -> str:
        """Normalize argument values for comparison."""
        if not arg:
            return arg
        
        # Strip surrounding quotes (single or double)
        arg = arg.strip()
        if (arg.startswith("'") and arg.endswith("'")) or (arg.startswith('"') and arg.endswith('"')):
            arg = arg[1:-1]
        
        # Normalize dictionary/object argument spacing
        # { partial: {} } should match {partial:{}} and { partial:{} }
        import re
        if arg.startswith('{') and arg.endswith('}'):
            # Remove all whitespace inside the dictionary
            arg = re.sub(r'\s+', '', arg)
        
        # Normalize string escape sequences
        # Both \x01\x02\x03\x04 (string representation) and actual bytes should match
        # Check if this looks like a hex escape sequence pattern
        # Convert both \x01\x02\x03\x04 and actual control characters to a normalized form
        if '\\x' in arg or any(ord(c) < 32 and c not in '\t\n\r' for c in arg):
            # Normalize escape sequences to a standard representation
            # Replace \xHH with normalized form, or actual control chars
            arg = re.sub(r'\\x([0-9a-fA-F]{2})', r'\\x\1', arg)
            # For actual control characters, convert to \x notation
            normalized = []
            for char in arg:
                if ord(char) < 32 and char not in '\t\n\r':
                    normalized.append(f'\\x{ord(char):02x}')
                else:
                    normalized.append(char)
            arg = ''.join(normalized)
            # Normalize to lowercase hex
            arg = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: f'\\x{m.group(1).lower()}', arg)
        
        # Lowercase for case-insensitive comparison
        arg = arg.lower()
        
        # Remove extra whitespace (but preserve structure for non-dict args)
        if not (arg.startswith('{') and arg.endswith('}')):
            arg = ' '.join(arg.split())
        
        return arg

    def _is_setup_code(self, step: TestStep) -> bool:
        """Check if a step is setup code that should be whitelisted.
        
        Setup code includes:
        - Mock object creation (type(), Mock(), etc.)
        - Test fixture creation
        - But NOT assignments that call methods on mocks (those are test operations)
        """
        if step.type == 'assignment':
            # Check if it's creating a mock or test fixture (not using one)
            if step.function:
                # Mock creation patterns: type(), Mock(), MagicMock(), etc.
                # The function might be parsed as 'type(...)' or just 'type'
                setup_functions = ['type', 'mock', 'magicmock', 'patch', 'fixture', 'setup']
                func_lower = step.function.lower()
                
                # Check if function name starts with or equals a setup function
                # e.g., 'type(...)' or 'type' or 'mock(...)'
                if any(func_lower.startswith(setup_func + '(') or func_lower == setup_func 
                       for setup_func in setup_functions):
                    return True
                # If it contains 'type(' in the function name, it's likely mock creation
                if 'type(' in func_lower:
                    return True
            
            # Check if target name suggests setup AND it's creating a mock
            # mock_storage = type(...) is setup
            # count = mock_storage.count_proven_txs(...) is NOT setup
            if step.target:
                setup_prefixes = ['mock_', 'test_', 'fixture_', 'setup_', 'given_']
                target_lower = step.target.lower()
                if any(target_lower.startswith(prefix) for prefix in setup_prefixes):
                    # Only filter if it's creating the mock, not using it
                    # Check if function name indicates setup
                    if step.function:
                        func_lower = step.function.lower()
                        if any(func_lower.startswith(setup_func + '(') or func_lower == setup_func 
                               for setup_func in ['type', 'mock', 'magicmock']):
                            return True
                        if 'type(' in func_lower:
                            return True
        
        return False

    def _align_steps(self, ts_steps: List[TestStep], py_steps: List[TestStep]) -> Tuple[int, List[str]]:
        """Align steps and find matches/differences."""
        ts_strings = [self._step_to_string(step) for step in ts_steps]
        py_strings = [self._step_to_string(step) for step in py_steps]

        matcher = SequenceMatcher(None, ts_strings, py_strings)

        matches = 0
        differences = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                matches += (i2 - i1)
            elif tag == 'replace':
                differences.append(f"REPLACE: TS[{i1}:{i2}] <-> PY[{j1}:{j2}]")
            elif tag == 'delete':
                differences.append(f"DELETE: TS[{i1}:{i2}] (missing in Python)")
            elif tag == 'insert':
                differences.append(f"INSERT: PY[{j1}:{j2}] (extra in Python)")

        return matches, differences
    
    def analyze_and_suggest(self, ts_steps: List[TestStep], py_steps: List[TestStep], 
                           ts_steps_detailed: List[Dict], py_steps_detailed: List[Dict],
                           similarity: float, differences: List[str], semantic_score: float) -> Dict[str, Any]:
        """Analyze differences and generate suggestions for alignment."""
        suggestions = []
        critical_issues = []
        # Initial status based on similarity threshold
        # Also check for functional equivalence patterns (e.g., callback verification)
        status = "PASS" if similarity >= DEFAULT_SIMILARITY_THRESHOLD else "FAIL"

        # Special case: If semantic score is high enough, consider it functionally equivalent
        # even if total similarity is below threshold
        # This handles cases like callback tests where verification methods differ
        # (e.g., toHaveBeenCalledTimes vs "callback" in call_order)
        # Lower threshold for callback tests (40% semantic is reasonable for functional equivalence)
        if semantic_score >= SEMANTIC_FALLBACK_THRESHOLD and similarity >= TOTAL_FALLBACK_THRESHOLD:
            # High semantic similarity indicates functional equivalence despite structural differences
            # Check if this looks like a callback test pattern
            ts_intents = self._extract_test_intents(ts_steps)
            py_intents = self._extract_test_intents(py_steps)
            has_callback_pattern = any('callback' in intent.lower() or 'bind' in intent.lower() 
                                      for intent in ts_intents + py_intents)
            if has_callback_pattern or semantic_score >= 0.50:
                status = "PASS"
        
        # Analyze differences for critical issues
        # First, find all assertions in both test implementations (regardless of position)
        ts_assertions = [(i, step) for i, step in enumerate(ts_steps_detailed) if step.get('type') == 'assertion']
        py_assertions = [(i, step) for i, step in enumerate(py_steps_detailed) if step.get('type') == 'assertion']

        # Check for assertion count mismatch FIRST, before checking individual assertions
        if len(ts_assertions) != len(py_assertions):
            count_diff = abs(len(ts_assertions) - len(py_assertions))
            if len(ts_assertions) > len(py_assertions):
                critical_issues.append({
                    'type': 'missing_assertions',
                    'message': f"Missing {count_diff} assertion(s) in Python (TS has {len(ts_assertions)}, PY has {len(py_assertions)})",
                    'ts_count': len(ts_assertions),
                    'py_count': len(py_assertions)
                })
            else:
                critical_issues.append({
                    'type': 'extra_assertions',
                    'message': f"Extra {count_diff} assertion(s) in Python (TS has {len(ts_assertions)}, PY has {len(py_assertions)})",
                    'ts_count': len(ts_assertions),
                    'py_count': len(py_assertions)
                })

        # Match assertions by position (best effort - match first with first, etc.)
        # Check all assertions, even if counts don't match
        max_assertions = max(len(ts_assertions), len(py_assertions))
        for idx in range(max_assertions):
            # Validate indices before accessing
            if idx < len(ts_assertions) and idx < len(py_assertions):
                ts_idx, ts_step = ts_assertions[idx]
                py_idx, py_step = py_assertions[idx]

                ts_op = ts_step.get('operator', '')
                py_op = py_step.get('operator', '')
                ts_target = ts_step.get('target', '')
                py_target = py_step.get('target', '')

                # Check for operator mismatch (critical)
                if ts_op != py_op and not self._are_operators_equivalent(ts_op, py_op):
                    critical_issues.append({
                        'type': 'operator_mismatch',
                        'ts_step': ts_step,
                        'py_step': py_step,
                        'ts_index': ts_idx,
                        'py_index': py_idx,
                        'message': f"Assertion #{idx+1} operator mismatch: TS uses '{ts_op}' but PY uses '{py_op}'"
                    })
                    # Operator mismatch is always critical - fail the test
                    status = "FAIL"

                # Check for assertion value mismatch (only if values are truly different)
                ts_args = ts_step.get('args', [])
                py_args = py_step.get('args', [])
                if ts_args != py_args:
                    # Check if it's a critical value difference (not just formatting)
                    if not self._are_assertion_values_equivalent(ts_args, py_args, ts_op, py_op):
                        # Only mark as critical if it's a real value difference, not just quote formatting
                        critical_issues.append({
                            'type': 'value_mismatch',
                            'ts_step': ts_step,
                            'py_step': py_step,
                            'ts_index': ts_idx,
                            'py_index': py_idx,
                            'message': f"Assertion #{idx+1} value mismatch: TS expects {ts_args} but PY expects {py_args}"
                        })
                        # Only fail if similarity is already low OR this is a critical operator/value mismatch
                        if similarity < DEFAULT_SIMILARITY_THRESHOLD:
                            status = "FAIL"
            elif idx < len(ts_assertions):
                # TS has more assertions - PY is missing this one
                ts_idx, ts_step = ts_assertions[idx]
                # Already reported in count mismatch above
                pass
            else:
                # PY has more assertions - PY has extra
                py_idx, py_step = py_assertions[idx]
                # Already reported in count mismatch above
                pass
        
        # Generate suggestions based on differences
        if differences:
            for diff in differences:
                if diff.startswith("REPLACE"):
                    suggestions.append(self._generate_replacement_suggestion(diff, ts_steps_detailed, py_steps_detailed))
                elif diff.startswith("DELETE"):
                    suggestions.append(self._generate_deletion_suggestion(diff, ts_steps_detailed))
                elif diff.startswith("INSERT"):
                    suggestions.append(self._generate_insertion_suggestion(diff, py_steps_detailed))
        
        return {
            'status': status,
            'similarity': similarity,
            'critical_issues': critical_issues,
            'suggestions': suggestions,
            'summary': self._generate_summary(status, similarity, critical_issues, len(ts_steps), len(py_steps))
        }
    
    def _are_operators_equivalent(self, op1: str, op2: str) -> bool:
        """Check if two operators are semantically equivalent."""
        # Normalize operators
        op1_norm = op1.lower().replace(' ', '_')
        op2_norm = op2.lower().replace(' ', '_')
        
        equivalent_pairs = [
            ('==', 'tobe', 'to_be', 'toequal', 'to_equal'),
            ('!=', 'not.tobe', 'not_to_be'),
            ('>=', 'tobegreaterthanorequal', 'to_be_greater_than_or_equal'),
            ('>', 'tobegreaterthan', 'to_be_greater_than'),
            ('is_undefined', 'tobeundefined', 'to_be_undefined', '== undefined', '== none', 'is none'),
        ]
        
        for group in equivalent_pairs:
            if op1_norm in group and op2_norm in group:
                return True
        
        return op1_norm == op2_norm
    
    def _are_assertion_values_equivalent(self, ts_args: List[str], py_args: List[str], 
                                         ts_op: str, py_op: str) -> bool:
        """Check if assertion values are equivalent."""
        # Normalize and compare - ignore quote differences
        def normalize_arg(arg):
            arg_str = str(arg).strip()
            # Remove surrounding quotes (single or double)
            if (arg_str.startswith("'") and arg_str.endswith("'")) or \
               (arg_str.startswith('"') and arg_str.endswith('"')):
                arg_str = arg_str[1:-1]
            # Also handle nested quotes like "'value'" -> "value"
            if arg_str.startswith("'") and arg_str.endswith("'"):
                arg_str = arg_str[1:-1]
            if arg_str.startswith('"') and arg_str.endswith('"'):
                arg_str = arg_str[1:-1]
            return arg_str.lower()
        
        ts_normalized = [normalize_arg(a) for a in ts_args]
        py_normalized = [normalize_arg(a) for a in py_args]
        
        return ts_normalized == py_normalized
    
    def _generate_replacement_suggestion(self, diff: str, ts_steps: List[Dict], py_steps: List[Dict]) -> str:
        """Generate suggestion for replacement difference."""
        import re
        match = re.match(r'REPLACE: TS\[(\d+):(\d+)\] <-> PY\[(\d+):(\d+)\]', diff)
        if match:
            ts_start, ts_end, py_start, py_end = map(int, match.groups())
            ts_range = ts_steps[ts_start:ts_end]
            py_range = py_steps[py_start:py_end]
            
            if len(ts_range) == 1 and len(py_range) == 1:
                ts_step = ts_range[0]
                py_step = py_range[0]
                return f"Replace PY step {py_start}: {self._step_to_readable(py_step)} with TS equivalent: {self._step_to_readable(ts_step)}"
            else:
                return f"Replace PY steps {py_start}-{py_end} with TS steps {ts_start}-{ts_end}"
        return diff
    
    def _generate_deletion_suggestion(self, diff: str, ts_steps: List[Dict]) -> str:
        """Generate suggestion for deletion difference."""
        import re
        match = re.match(r'DELETE: TS\[(\d+):(\d+)\]', diff)
        if match:
            ts_start, ts_end = map(int, match.groups())
            missing_steps = ts_steps[ts_start:ts_end]
            step_descriptions = [self._step_to_readable(s) for s in missing_steps]
            return f"Add missing step(s) from TS: {', '.join(step_descriptions)}"
        return diff
    
    def _generate_insertion_suggestion(self, diff: str, py_steps: List[Dict]) -> str:
        """Generate suggestion for insertion difference."""
        import re
        match = re.match(r'INSERT: PY\[(\d+):(\d+)\]', diff)
        if match:
            py_start, py_end = map(int, match.groups())
            extra_steps = py_steps[py_start:py_end]
            step_descriptions = [self._step_to_readable(s) for s in extra_steps]
            return f"Remove extra PY step(s) or align with TS: {', '.join(step_descriptions)}"
        return diff
    
    def _step_to_readable(self, step: Dict) -> str:
        """Convert step dict to readable string."""
        parts = []
        if step.get('type'):
            parts.append(step['type'])
        if step.get('target'):
            parts.append(step['target'])
        if step.get('function'):
            parts.append(f"{step['function']}()")
        if step.get('operator'):
            parts.append(step['operator'])
        if step.get('args'):
            parts.append(f"args={step['args']}")
        return ' '.join(parts)
    
    def _generate_summary(self, status: str, similarity: float, critical_issues: List[Dict], 
                          ts_count: int, py_count: int) -> str:
        """Generate summary message."""
        if status == "PASS":
            return f"PASS: Tests are well-aligned ({similarity:.1%} similarity)"
        
        summary_parts = [f"FAIL: Tests need alignment ({similarity:.1%} similarity)"]
        
        if critical_issues:
            summary_parts.append(f"\nCritical Issues ({len(critical_issues)}):")
            for issue in critical_issues[:3]:  # Show first 3
                summary_parts.append(f"  - {issue['message']}")
        
        if ts_count != py_count:
            summary_parts.append(f"\nStep count mismatch: TS has {ts_count} steps, PY has {py_count} steps")
        
        return '\n'.join(summary_parts)

    def _normalize_mock_functions(self, steps: List[TestStep]) -> List[TestStep]:
        """Phase 1: Normalize mock framework functions to semantic equivalents.
        
        Converts:
        - jest.fn() ↔ Mock() ↔ custom function (for test purposes)
        - jest.fn().mockImplementation() ↔ Mock(spec=...) ↔ def callback(): raise
        All represent "mock function for testing"
        """
        normalized = []
        for step in steps:
            if step.type == 'assignment' and step.function:
                func_lower = step.function.lower()
                # Normalize Jest mocks (check both original and normalized forms)
                # After normalize(): jest.fn stays jest.fn (dots preserved), but check all variations
                # Also check for jest_fn (if dots were converted somehow)
                jest_patterns = ['jest.fn', 'jest_fn', 'jestfn']
                mock_impl_patterns = ['mockimplementation', 'mock_implementation', 'mockimplementation']
                
                if any(pattern in func_lower for pattern in jest_patterns + mock_impl_patterns):
                    step.function = 'mock_function'
                # Normalize Python mocks (check normalized forms too)
                elif func_lower in ['mock', 'magicmock', 'patch', 'mock_function']:
                    step.function = 'mock_function'
                # Normalize custom test functions that are clearly mocks
                elif step.target:
                    target_lower = step.target.lower()
                    # If it's assigned to a mock/callback variable, treat as mock
                    # Use word boundaries to avoid false positives (e.g., 'subscribe' containing 'cb')
                    import re
                    if any(re.search(pattern, target_lower) for pattern in MOCK_FUNCTION_PATTERNS):
                        step.function = 'mock_function'
            elif step.type == 'call' and step.function:
                func_lower = step.function.lower()
                # Normalize Jest mock verification (check all normalized forms)
                # After normalize(): toHaveBeenCalledTimes → to_have_been_called_times
                mock_verify_patterns = [
                    'tohavebeencalledtimes', 'to_have_been_called_times',
                    'tohavebeencalled', 'to_have_been_called',
                    'tohavebeencalledwith', 'to_have_been_called_with'
                ]
                if any(pattern in func_lower for pattern in mock_verify_patterns):
                    step.function = 'verify_mock_called'
            normalized.append(step)
        return normalized

    def _normalize_assertion_operators(self, steps: List[TestStep]) -> List[TestStep]:
        """Phase 1: Normalize assertion operators to semantic equivalents.
        
        Converts:
        - toBe, toEqual, toStrictEqual ↔ ==
        - toBeUndefined ↔ == undefined ↔ is None ↔ "x" not in obj
        - toBeNull ↔ == null
        - toBeTruthy ↔ == true
        - toBeFalsy ↔ == false
        """
        normalized = []
        for step in steps:
            if step.type == 'assertion' and step.operator:
                # Normalize Jest assertion operators (check both original and normalized forms)
                # After normalize(): toBe → to_be, toBeUndefined → to_be_undefined
                operator_lower = step.operator.lower()
                
                # IMPORTANT: Check for undefined/null FIRST, before general equality checks
                # because "== undefined" starts with "==" and would be caught by equality check
                # Undefined/null checks - check all possible forms
                # Note: _jest_to_operator converts toBeUndefined to "== undefined" (full string)
                if (operator_lower in ['tobeundefined', 'to_be_undefined', '== undefined', 'is none', 'is_undefined', 
                                      'is not none', 'is_not_none', 'isnone', 'is_none'] or
                    '== undefined' in operator_lower or '== none' in operator_lower or
                    (operator_lower == '==' and step.args and 
                     any(arg.lower() in ['undefined', 'none'] for arg in step.args))):
                    step.operator = 'is_undefined'
                    # Also normalize the target if it's an undefined check
                    if step.target:
                        target_lower = step.target.lower()
                        # Check if target contains == undefined pattern
                        if '== undefined' in target_lower or '== none' in target_lower:
                            # Extract the variable being checked (before the ==)
                            match = re.match(r'(\w+(?:\.\w+)*)', step.target)
                            if match:
                                step.target = f"{match.group(1)}_undefined_check"
                        # Check for "key" not in dict patterns
                        elif ('not in' in target_lower or 'not_in' in target_lower) and re.search(r'["\']\w+["\']', step.target):
                            step.target = 'is_undefined_check'
                        elif 'is_undefined_check' in target_lower:
                            step.target = 'is_undefined_check'
                # Equality operators - check all possible forms (but not == undefined/none)
                elif operator_lower in ['tobe', 'to_be', 'toequal', 'to_equal', 
                                       'tostrictequal', 'to_strict_equal'] or (
                    operator_lower.startswith('==') and 'undefined' not in operator_lower and 'none' not in operator_lower):
                    step.operator = '=='
                elif operator_lower in ['not.tobe', 'not_to_be', 'not.toequal', 'not_to_equal', '!='] or (
                    operator_lower.startswith('!=') and 'undefined' not in operator_lower and 'none' not in operator_lower):
                    step.operator = '!='
                elif operator_lower in ['tobenull', 'to_be_null', '== null']:
                    step.operator = '== null'
                
                # Truthiness checks
                elif operator_lower in ['tobetruthy', 'to_be_truthy', '== true']:
                    step.operator = '== true'
                elif operator_lower in ['tobefalsy', 'to_be_falsy', '== false']:
                    step.operator = '== false'
                
                # Comparison operators (already normalized, but ensure consistency)
                elif operator_lower in ['tobegreaterthan', 'to_be_greater_than', '>']:
                    step.operator = '>'
                elif operator_lower in ['tobegreaterthanorequal', 'to_be_greater_than_or_equal', '>=']:
                    step.operator = '>='
                elif operator_lower in ['tobelessthan', 'to_be_less_than', '<']:
                    step.operator = '<'
                elif operator_lower in ['tobelessthanorequal', 'to_be_less_than_or_equal', '<=']:
                    step.operator = '<='
                
                # Python-specific patterns - handle "in" and "not in" operators
                elif 'in' in operator_lower and step.target:
                    # Check if it's an existence check (key in dict) vs undefined check
                    if 'not in' in operator_lower or 'not_in' in operator_lower:
                        # Could be undefined check or membership check
                        # If target looks like a key check (string literal), treat as undefined
                        if re.search(r'["\']\w+["\']', step.target) or 'is_undefined_check' in step.target.lower():
                            step.operator = 'is_undefined'
                            step.target = 'is_undefined_check'
                        else:
                            step.operator = 'not in'
                    else:
                        step.operator = 'in'
            
            normalized.append(step)
        return normalized

    def compare_test_files(self, ts_file: str, ts_line_range: str,
                           py_file: str, py_line_range: str) -> Dict[str, Any]:
        """Compare tests from files using line ranges."""

        # Read TypeScript code
        ts_start, ts_end = map(int, ts_line_range.split('-'))
        with open(ts_file, 'r', encoding='utf-8') as f:
            ts_lines = f.readlines()
        ts_code = ''.join(ts_lines[ts_start-1:ts_end])

        # Read Python code
        py_start, py_end = map(int, py_line_range.split('-'))
        with open(py_file, 'r', encoding='utf-8') as f:
            py_lines = f.readlines()
        py_code = ''.join(py_lines[py_start-1:py_end])

        return self.compare_tests(ts_code, py_code)


def _generate_notes(analysis: Dict, ts_steps: int, py_steps: int, 
                    critical_issues: List[Dict], differences: List[str]) -> str:
    """Generate concise notes about what needs to be fixed."""
    notes = []
    
    # Count only assertions for comparison (ignore assignments)
    ts_assertions = sum(1 for step in analysis.get('ts_steps_detailed', []) if step.get('type') == 'assertion')
    py_assertions = sum(1 for step in analysis.get('py_steps_detailed', []) if step.get('type') == 'assertion')
    
    # Track which assertion indices have issues
    assertion_issues = {}
    
    # Check for critical issues first (these are more important than count differences)
    for issue in critical_issues:
        if issue['type'] == 'operator_mismatch':
            py_op = issue.get('py_step', {}).get('operator', '')
            ts_op = issue.get('ts_step', {}).get('operator', '')
            py_idx = issue.get('py_index', 0)
            # Find which assertion number this is (1-indexed)
            assertion_num = sum(1 for i, step in enumerate(analysis.get('py_steps_detailed', [])) 
                              if step.get('type') == 'assertion' and i < py_idx) + 1
            notes.append(f"Assertion #{assertion_num} comparator mismatch: '{py_op}' (PY) !== '{ts_op}' (TS)")
            assertion_issues[py_idx] = True
        elif issue['type'] == 'value_mismatch':
            ts_args = issue.get('ts_step', {}).get('args', [])
            py_args = issue.get('py_step', {}).get('args', [])
            py_idx = issue.get('py_index', 0)
            # Find which assertion number this is (1-indexed)
            assertion_num = sum(1 for i, step in enumerate(analysis.get('py_steps_detailed', [])) 
                              if step.get('type') == 'assertion' and i < py_idx) + 1
            # Show the actual values that need to change
            if ts_args and py_args:
                notes.append(f"Assertion #{assertion_num} value inconsistency: {py_args} (PY) → {ts_args} (TS)")
            else:
                notes.append(f"Assertion #{assertion_num} value inconsistency")
            assertion_issues[py_idx] = True
    
    # Only check for assertion count differences if there are no critical issues
    # OR if the count difference is significant (not just a mismatch in existing assertions)
    if ts_assertions != py_assertions and not critical_issues:
        if ts_assertions > py_assertions:
            notes.append(f"Increase assertions ({ts_assertions - py_assertions} missing)")
        else:
            notes.append(f"Reduce assertions ({py_assertions - ts_assertions} extra)")
    
    # Check for missing steps (only if no critical issues already cover this)
    if not critical_issues:
        for diff in differences:
            if diff.startswith("DELETE"):
                notes.append("Add missing assertions from TS")
            elif diff.startswith("INSERT"):
                notes.append("Remove extra assertions or align with TS")
    
    return "; ".join(notes) if notes else "Well aligned"


def _generate_detailed_report(test_data: List[Dict], comparator: 'TestComparator') -> None:
    """Generate a detailed report with code snippets, comparison results, and PASS/FAIL status."""
    from pathlib import Path

    # Single pass: Run all comparisons once and store results
    test_results = []
    for entry in test_data:
        # Use configurable base directories
        ts_file = str(Path(DEFAULT_TS_BASE_DIR) / entry['ts_file'])
        py_file = str(Path(DEFAULT_PY_BASE_DIR) / entry['py_file'])
        result = None
        status = "UNKNOWN"
        critical_issues = []
        error_msg = None

        try:
            ts_range = f"{entry['ts_start']}-{entry['ts_end']}"
            py_range = f"{entry['py_start']}-{entry['py_end']}"
            result = comparator.compare_test_files(ts_file, ts_range, py_file, py_range)
            analysis = result.get('analysis', {})
            status = analysis.get('status', 'UNKNOWN')
            critical_issues = analysis.get('critical_issues', [])
        except Exception as e:
            error_msg = str(e)

        test_results.append({
            'entry': entry,
            'ts_file': ts_file,
            'py_file': py_file,
            'result': result,
            'status': status,
            'critical_issues': critical_issues,
            'error_msg': error_msg
        })

    # Calculate summary statistics from stored results
    total_tests = len(test_results)
    pass_count = sum(1 for r in test_results if r['status'] == "PASS")
    fail_count = sum(1 for r in test_results if r['status'] == "FAIL")
    pass_percentage = (pass_count / total_tests * 100) if total_tests > 0 else 0
    fail_percentage = (fail_count / total_tests * 100) if total_tests > 0 else 0

    report_lines = [
        "# Test Comparison Detailed Report",
        "",
        "This document contains syntax-highlighted code snippets from both TypeScript and Python tests, ",
        "followed by the comparison results and PASS/FAIL status.",
        "",
        "## Summary",
        "",
        f"- **Total Tests**: {total_tests}",
        f"- **Passing**: {pass_count} ({pass_percentage:.1f}%)",
        f"- **Failing**: {fail_count} ({fail_percentage:.1f}%)",
        "",
        "---",
        ""
    ]

    # Use stored results to generate report
    for i, test_result in enumerate(test_results, 1):
        entry = test_result['entry']
        ts_file = test_result['ts_file']
        py_file = test_result['py_file']
        result = test_result['result']
        status = test_result['status']
        critical_issues = test_result['critical_issues']
        error_msg = test_result['error_msg']

        if error_msg:
            report_lines.append(f"*Error during comparison: {error_msg}*")
            report_lines.append("")
        
        # Create clickable links
        ts_link = _create_file_link(ts_file, entry['ts_start'], use_relative=True)
        py_link = _create_file_link(py_file, entry['py_start'], use_relative=True)
        status_badge = f" **{status}**" if status != "UNKNOWN" else ""
        
        # Show test name with status
        report_lines.append(f"## Test {i}: {entry['test_name']}{status_badge}")
        report_lines.append("")
        
        # Show TS header with file link
        report_lines.append(f"### TS Test: [{entry['ts_file']}]({ts_link})")
        report_lines.append("")
        
        # Only show code snippets, comparison results, and critical issues for FAIL tests
        if status == "FAIL":
            # Read TypeScript code and show it right after TS header
            try:
                with open(ts_file, 'r', encoding='utf-8') as f:
                    ts_lines = f.readlines()
                ts_start, ts_end = entry['ts_start'], entry['ts_end']
                ts_code_snippet = ''.join(ts_lines[ts_start-1:ts_end])
                
                report_lines.append("```typescript")
                report_lines.append(ts_code_snippet.rstrip())
                report_lines.append("```")
                report_lines.append("")
            except Exception as e:
                report_lines.append(f"*Error reading TypeScript file: {e}*")
                report_lines.append("")
        
        # Show PY header with file link
        report_lines.append(f"### PY Test: [{entry['py_file']}]({py_link})")
        report_lines.append("")
        
        # Only show Python code snippet for FAIL tests
        if status == "FAIL":
            # Read Python code
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    py_lines = f.readlines()
                py_start, py_end = entry['py_start'], entry['py_end']
                py_code_snippet = ''.join(py_lines[py_start-1:py_end])
                
                report_lines.append("```python")
                report_lines.append(py_code_snippet.rstrip())
                report_lines.append("```")
                report_lines.append("")
            except Exception as e:
                report_lines.append(f"*Error reading Python file: {e}*")
                report_lines.append("")
            
            # Show comparison results and critical issues
            if result:
                try:
                    structural = result.get('structural_score', result['similarity'])
                    semantic = result.get('semantic_score', result['similarity'])
                    
                    report_lines.append("### Comparison Results")
                    report_lines.append("")
                    report_lines.append(f"**Scores**: Structural: {structural:.2%} | Semantic: {semantic:.2%} | Total: {result['similarity']:.2%}")
                    report_lines.append("")
                    
                    # Show critical issues
                    if critical_issues:
                        report_lines.append("**Critical Issues:**")
                        for issue in critical_issues:
                            report_lines.append(f"- {issue['message']}")
                        report_lines.append("")
                    
                except Exception as e:
                    report_lines.append(f"*Error processing results: {e}*")
                    report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
    
    # Write report
    report_file = Path("test_comparison_detailed_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Detailed report saved to: {report_file}")
    print(f"  {_create_file_link(str(report_file), 1)}")


def _generate_markdown_table(rows: List[Dict]) -> str:
    """Generate a markdown table from the comparison results."""
    lines = [
        "# Test Comparison Results",
        "",
        "| Test Name | TypeScript File | Python File | Structural Score | Semantic Score | Total Similarity | Status | Notes |",
        "|-----------|-----------------|-------------|------------------|----------------|------------------|--------|-------|"
    ]
    
    for row in rows:
        # Escape pipe characters in notes
        notes = row['notes'].replace('|', '\\|')
        status = row.get('status', 'UNKNOWN')
        lines.append(
            f"| {row['test_name']} | {row['ts_link']} | {row['py_link']} | "
            f"{row['structural']} | {row['semantic']} | {row['total']} | {status} | {notes} |"
        )
    
    return '\n'.join(lines) + '\n'


def _step_to_readable_helper(step: Dict) -> str:
    """Helper function to convert step dict to readable string."""
    parts = []
    if step.get('type'):
        parts.append(step['type'])
    if step.get('target'):
        parts.append(step['target'])
    if step.get('function'):
        parts.append(f"{step['function']}()")
    if step.get('operator'):
        parts.append(step['operator'])
    if step.get('args'):
        parts.append(f"args={step['args']}")
    return ' '.join(parts)


def _create_file_link(file_path: str, line_number: int, use_relative: bool = False) -> str:
    """Create a clickable file link for VS Code/Cursor markdown.
    
    For markdown files, relative paths work best in VS Code/Cursor preview.
    """
    from pathlib import Path
    import os
    
    # Convert to absolute path first
    abs_path = Path(file_path).resolve()
    
    if use_relative:
        # Use relative path from current working directory
        try:
            rel_path = abs_path.relative_to(Path.cwd())
            # Use forward slashes for markdown compatibility
            rel_path_str = str(rel_path).replace(chr(92), '/')
            # VS Code/Cursor markdown supports line anchors with #L format
            return f"{rel_path_str}#L{line_number}"
        except ValueError:
            # If path is not relative to cwd, fall back to absolute
            pass
    
    # For markdown, use file:// protocol which works in VS Code/Cursor
    if os.name == 'nt':  # Windows
        # Windows: file:///C:/path/to/file:line
        url_path = str(abs_path).replace('\\', '/')
        if url_path[1] == ':':  # Drive letter
            url_path = '/' + url_path
        return f"file://{url_path}:{line_number}"
    else:  # Unix/Mac
        return f"file://{abs_path}:{line_number}"


def main():
    """Main function to demonstrate usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python compare_test_implementations_hybrid.py <mode> [args...]")
        print()
        print("Modes:")
        print("  test - Run on sample tests from test_ranges.json")
        print("  compare <ts_file> <ts_range> <py_file> <py_range> - Compare specific test")
        print()
        print("Example:")
        print("  python compare_test_implementations_hybrid.py test")
        print("  python compare_test_implementations_hybrid.py compare file.ts 10-20 file.py 30-40")
        print()
        print("Note: This is the hybrid version with Phase 1 & 2 improvements:")
        print("  - Enhanced assertion normalization")
        print("  - Mock framework normalization")
        print("  - Undefined/null check normalization")
        print("  - Multi-tier scoring (Structural × 0.3 + Semantic × 0.7)")
        return

    mode = sys.argv[1]
    comparator = TestComparator()

    if mode == 'test':
        # Load matching tests
        test_json_path = Path('test_ranges.json')
        if not test_json_path.exists():
            # Try alternative locations
            alt_paths = [
                Path('/tmp/test_ranges.json'),
                Path('py-wallet-toolbox/test-analysis/test_ranges.json'),
            ]
            for alt_path in alt_paths:
                if alt_path.exists():
                    test_json_path = alt_path
                    break
            else:
                print(f"Error: test_ranges.json not found. Please create it in the current directory.")
                return
        
        with open(test_json_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        print(f"Testing on {len(test_data)} tests...")
        print("="*80)

        # Prepare table data
        table_rows = []

        for i, entry in enumerate(test_data):
            print(f"\nTest {i+1}: {entry['test_name']}")
            print("-"*80)

            # Use configurable base directories instead of hard-coded paths
            ts_file = Path(DEFAULT_TS_BASE_DIR) / entry['ts_file']
            py_file = Path(DEFAULT_PY_BASE_DIR) / entry['py_file']

            # Convert to string for compatibility
            ts_file = str(ts_file)
            py_file = str(py_file)

            if 'ts_start' in entry and 'py_start' in entry:
                ts_range = f"{entry['ts_start']}-{entry['ts_end']}"
                py_range = f"{entry['py_start']}-{entry['py_end']}"
                
                # Create clickable links
                ts_link = _create_file_link(ts_file, entry['ts_start'])
                py_link = _create_file_link(py_file, entry['py_start'])
                
                # Format for better readability with clickable links
                # VS Code/Cursor terminals automatically make file:line clickable
                print(f"\nTypeScript Test (lines {entry['ts_start']}-{entry['ts_end']}):")
                print(f"   {ts_link}")
                print(f"\nPython Test (lines {entry['py_start']}-{entry['py_end']}):")
                print(f"   {py_link}")

                try:
                    result = comparator.compare_test_files(ts_file, ts_range, py_file, py_range)
                    analysis = result.get('analysis', {})

                    # Display PASS/FAIL status
                    status = analysis.get('status', 'UNKNOWN')
                    status_symbol = "[PASS]" if status == "PASS" else "[FAIL]"
                    print(f"\n{status_symbol} Status: {status}")
                    
                    print(f"\nTypeScript steps: {result['ts_steps']}")
                    print(f"Python steps: {result['py_steps']}")
                    # Phase 2: Show structural, semantic, and hybrid scores
                    structural = result.get('structural_score', result['similarity'])
                    semantic = result.get('semantic_score', result['similarity'])
                    print(f"Similarity: {result['similarity']:.2%} (Hybrid: Structural {structural:.2%} × 0.3 + Semantic {semantic:.2%} × 0.7)")
                    print(f"Matching steps: {result['matches']}")

                    # Show summary
                    if analysis.get('summary'):
                        summary_lines = analysis['summary'].split('\n')
                        for line in summary_lines:
                            print(line)

                    # Show critical issues
                    critical_issues = analysis.get('critical_issues', [])
                    if critical_issues:
                        print("\nCritical Issues:")
                        for issue in critical_issues:
                            print(f"  - {issue['message']}")
                            # Show step details
                            ts_step = issue.get('ts_step', {})
                            py_step = issue.get('py_step', {})
                            print(f"    TS step {issue.get('ts_index', '?')}: {_step_to_readable_helper(ts_step)}")
                            print(f"    PY step {issue.get('py_index', '?')}: {_step_to_readable_helper(py_step)}")


                    # Collect data for table - use relative paths for markdown
                    ts_link = _create_file_link(ts_file, entry['ts_start'], use_relative=True)
                    py_link = _create_file_link(py_file, entry['py_start'], use_relative=True)
                    structural = result.get('structural_score', result['similarity'])
                    semantic = result.get('semantic_score', result['similarity'])
                    # Pass detailed steps for assertion counting
                    analysis_with_steps = analysis.copy()
                    analysis_with_steps['ts_steps_detailed'] = result.get('ts_steps_detailed', [])
                    analysis_with_steps['py_steps_detailed'] = result.get('py_steps_detailed', [])
                    
                    notes = _generate_notes(
                        analysis_with_steps, 
                        result['ts_steps'], 
                        result['py_steps'],
                        critical_issues,
                        result['differences']
                    )
                    
                    # Use relative paths for markdown links (better compatibility)
                    py_file_rel = Path(py_file).relative_to(Path.cwd()) if Path(py_file).is_absolute() else py_file
                    ts_file_rel = Path(ts_file).relative_to(Path.cwd()) if Path(ts_file).is_absolute() else ts_file
                    
                    table_rows.append({
                        'test_name': entry['test_name'],
                        'py_link': f"[{Path(py_file).name}:{entry['py_start']}-{entry['py_end']}]({py_link})",
                        'ts_link': f"[{Path(ts_file).name}:{entry['ts_start']}-{entry['ts_end']}]({ts_link})",
                        'structural': f"{structural:.2%}",
                        'semantic': f"{semantic:.2%}",
                        'total': f"{result['similarity']:.2%}",
                        'status': status,
                        'notes': notes
                    })

                    # Show detailed steps (optional, can be toggled)
                    if status == "FAIL" or len(sys.argv) > 2 and '--verbose' in sys.argv:
                        print("\nTypeScript steps:")
                        for idx, step in enumerate(result['ts_steps_detailed']):
                            step_str = f"{step['type']}"
                            if step.get('target'):
                                step_str += f" {step['target']}"
                            if step.get('function'):
                                step_str += f" = {step['function']}()"
                            if step.get('operator'):
                                step_str += f" {step['operator']}"
                            print(f"  [{idx}] {step_str}")

                        print("\nPython steps:")
                        for idx, step in enumerate(result['py_steps_detailed']):
                            step_str = f"{step['type']}"
                            if step.get('target'):
                                step_str += f" {step['target']}"
                            if step.get('function'):
                                step_str += f" = {step['function']}()"
                            if step.get('operator'):
                                step_str += f" {step['operator']}"
                            print(f"  [{idx}] {step_str}")

                        if result['differences']:
                            print("\nDifferences:")
                            for diff in result['differences']:
                                print(f"  {diff}")

                except Exception as e:
                    print(f"Error: {e}")
                    import traceback
                    traceback.print_exc()
        
        # Generate markdown table
        if table_rows:
            md_table = _generate_markdown_table(table_rows)
            output_file = Path("test_comparison_results.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_table)
            print(f"\n{'='*80}")
            print(f"Markdown table saved to: {output_file}")
            print(f"  {_create_file_link(str(output_file), 1)}")
        
        # Generate detailed report with code snippets
        _generate_detailed_report(test_data, comparator)

    elif mode == 'compare' and len(sys.argv) == 6:
        ts_file, ts_range, py_file, py_range = sys.argv[2:6]

        result = comparator.compare_test_files(ts_file, ts_range, py_file, py_range)

        print(json.dumps(result, indent=2))

    else:
        print("Invalid arguments. Use --help for usage.")


if __name__ == '__main__':
    main()
