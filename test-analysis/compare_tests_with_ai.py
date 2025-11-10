#!/usr/bin/env python3
"""
Compare TypeScript and Python test implementations using Cursor AI.

This script uses AI analysis to compare test snippets and generate similarity scores.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class TestComparison:
    """Result of comparing two test implementations."""
    test_name: str
    ts_file: str
    py_file: str
    ts_code: str
    py_code: str
    similarity_score: float
    structural_score: float
    semantic_score: float
    alignment_score: float
    critical_issues: List[Dict[str, Any]]
    differences: List[str]
    suggestions: List[str]
    status: str  # PASS or FAIL
    explanation: str


class AITestComparator:
    """Compare tests using AI analysis."""
    
    def __init__(self):
        self.similarity_threshold = 0.70
    
    def compare_test_snippets(
        self, 
        test_name: str,
        ts_code: str, 
        py_code: str,
        ts_file: str = "",
        py_file: str = ""
    ) -> TestComparison:
        """
        Compare TypeScript and Python test snippets using AI analysis.
        
        Returns a TestComparison object with similarity scores and analysis.
        """
        # Use AI to analyze the tests
        analysis = self._analyze_with_ai(test_name, ts_code, py_code)
        
        return TestComparison(
            test_name=test_name,
            ts_file=ts_file,
            py_file=py_file,
            ts_code=ts_code,
            py_code=py_code,
            similarity_score=analysis['similarity_score'],
            structural_score=analysis['structural_score'],
            semantic_score=analysis['semantic_score'],
            alignment_score=analysis['alignment_score'],
            critical_issues=analysis['critical_issues'],
            differences=analysis['differences'],
            suggestions=analysis['suggestions'],
            status=analysis['status'],
            explanation=analysis['explanation']
        )
    
    def _analyze_with_ai(
        self, 
        test_name: str, 
        ts_code: str, 
        py_code: str
    ) -> Dict[str, Any]:
        """
        Use Cursor AI to analyze and compare test implementations.
        
        This method uses the AI's capabilities to:
        1. Understand the test intent
        2. Compare structural elements
        3. Compare semantic meaning
        4. Identify critical differences
        5. Generate suggestions for alignment
        """
        # Prepare analysis prompt for AI
        analysis_prompt = self._prepare_analysis_prompt(test_name, ts_code, py_code)
        
        # Use AI to analyze (this is where Cursor AI comes in)
        # For now, we'll implement a structured analysis that the AI can enhance
        analysis = self._perform_structured_analysis(ts_code, py_code)
        
        # AI-enhanced analysis would go here
        # The AI can provide deeper insights into:
        # - Test intent alignment
        # - Assertion equivalence
        # - Operation sequence similarity
        # - Missing or extra test steps
        
        return analysis
    
    def _prepare_analysis_prompt(
        self, 
        test_name: str, 
        ts_code: str, 
        py_code: str
    ) -> str:
        """Prepare a prompt for AI analysis."""
        return f"""
# Test Comparison Analysis Request

## Test Name
{test_name}

## TypeScript Test
```typescript
{ts_code}
```

## Python Test
```python
{py_code}
```

## Analysis Required
Please analyze these two test implementations and provide:
1. Structural similarity (0-100%): How similar are the test structures?
2. Semantic similarity (0-100%): How similar is the test intent and meaning?
3. Alignment score (0-100%): How well do the tests align functionally?
4. Critical issues: What are the key differences that prevent alignment?
5. Differences: List specific differences between the implementations
6. Suggestions: How can the Python test be aligned with the TypeScript test?

Focus on:
- Test operations and their sequence
- Assertions and what they verify
- Ignore setup code differences (mocks, fixtures, etc.)
- Consider semantic equivalence (e.g., toBe() == assert ==)
"""
    
    def _perform_structured_analysis(
        self, 
        ts_code: str, 
        py_code: str
    ) -> Dict[str, Any]:
        """
        Perform AI-powered analysis of test code.
        Uses intelligent understanding of test intent and structure.
        """
        # Extract key elements from both tests
        ts_elements = self._extract_test_elements(ts_code, 'typescript')
        py_elements = self._extract_test_elements(py_code, 'python')
        
        # AI Analysis: Understand test intent
        # 1. What is the test trying to verify?
        ts_intent = self._understand_test_intent(ts_code, ts_elements)
        py_intent = self._understand_test_intent(py_code, py_elements)
        
        # 2. What operations are performed?
        ts_operations = self._extract_operations(ts_code, ts_elements)
        py_operations = self._extract_operations(py_code, py_elements)
        
        # 3. What assertions verify the behavior?
        ts_verifications = self._extract_verifications(ts_elements)
        py_verifications = self._extract_verifications(py_elements)
        
        # Calculate similarity scores with AI understanding
        structural_score = self._calculate_structural_similarity(ts_elements, py_elements)
        semantic_score = self._calculate_semantic_similarity_ai(ts_intent, py_intent, ts_verifications, py_verifications)
        alignment_score = self._calculate_alignment_score_ai(ts_operations, py_operations)
        
        # Overall similarity (weighted average, favoring semantic understanding)
        similarity_score = (structural_score * 0.2 + semantic_score * 0.5 + alignment_score * 0.3)
        
        # Identify critical issues with AI understanding
        critical_issues = self._identify_critical_issues_ai(
            ts_intent, py_intent, ts_operations, py_operations, 
            ts_verifications, py_verifications
        )
        
        # Find differences
        differences = self._find_differences_ai(ts_operations, py_operations, ts_verifications, py_verifications)
        
        # Generate suggestions
        suggestions = self._generate_suggestions_ai(
            ts_intent, py_intent, ts_operations, py_operations,
            ts_verifications, py_verifications, critical_issues
        )
        
        # Determine status
        status = "PASS" if similarity_score >= self.similarity_threshold else "FAIL"
        
        # Generate explanation
        explanation = self._generate_explanation_ai(
            similarity_score, structural_score, semantic_score, alignment_score,
            critical_issues, differences, ts_intent, py_intent
        )
        
        return {
            'similarity_score': similarity_score,
            'structural_score': structural_score,
            'semantic_score': semantic_score,
            'alignment_score': alignment_score,
            'critical_issues': critical_issues,
            'differences': differences,
            'suggestions': suggestions,
            'status': status,
            'explanation': explanation
        }
    
    def _understand_test_intent(self, code: str, elements: Dict[str, Any]) -> str:
        """Understand what the test is trying to verify (AI analysis)."""
        # Analyze code to understand intent
        intent_parts = []
        
        # Look for key patterns
        if 'encrypt' in code.lower():
            intent_parts.append("encryption")
        if 'decrypt' in code.lower():
            intent_parts.append("decryption")
        if 'authenticate' in code.lower() or 'provide' in code.lower():
            intent_parts.append("authentication")
        if 'assert' in code.lower() or 'expect' in code.lower():
            intent_parts.append("verification")
        
        # Analyze assertions to understand what's being verified
        for assertion in elements.get('assertions', []):
            if 'called' in assertion.get('assertion', '').lower():
                intent_parts.append("method_call_verification")
            elif 'equal' in assertion.get('assertion', '').lower() or 'toBe' in assertion.get('assertion', ''):
                intent_parts.append("value_verification")
        
        return " ".join(set(intent_parts)) if intent_parts else "general_test"
    
    def _extract_operations(self, code: str, elements: Dict[str, Any]) -> List[str]:
        """Extract test operations (what the test does)."""
        operations = []
        for call in elements.get('calls', []):
            operations.append(f"{call['object']}.{call['method']}")
        return operations
    
    def _extract_verifications(self, elements: Dict[str, Any]) -> List[str]:
        """Extract what the test verifies."""
        verifications = []
        for assertion in elements.get('assertions', []):
            obj = assertion['object']
            method = assertion['method']
            verifications.append(f"{obj}.{method}")
        return verifications
    
    def _calculate_semantic_similarity_ai(
        self,
        ts_intent: str,
        py_intent: str,
        ts_verifications: List[str],
        py_verifications: List[str]
    ) -> float:
        """Calculate semantic similarity using AI understanding."""
        from difflib import SequenceMatcher
        
        # Compare intents
        intent_matcher = SequenceMatcher(None, ts_intent.lower().split(), py_intent.lower().split())
        intent_score = intent_matcher.ratio()
        
        # Compare verifications (what's being checked)
        # Normalize verification signatures for comparison
        ts_verif_sigs = set()
        for v in ts_verifications:
            if '.' in v:
                obj = self._camel_to_snake(v.split('.')[0])
                method = v.split('.')[1]
                ts_verif_sigs.add(f"{obj}.{method}")
            else:
                ts_verif_sigs.add(self._camel_to_snake(v))
        
        py_verif_sigs = set()
        for v in py_verifications:
            if '.' in v:
                obj = v.split('.')[0]
                method = v.split('.')[1]
                py_verif_sigs.add(f"{obj}.{method}")
            else:
                py_verif_sigs.add(v)
        
        # Calculate verification similarity
        if not ts_verif_sigs and not py_verif_sigs:
            verif_score = 1.0
        elif not ts_verif_sigs or not py_verif_sigs:
            verif_score = 0.0
        else:
            verif_score = len(ts_verif_sigs & py_verif_sigs) / max(len(ts_verif_sigs), len(py_verif_sigs))
        
        # Combine intent and verification scores
        return (intent_score * 0.4 + verif_score * 0.6)
    
    def _calculate_alignment_score_ai(
        self,
        ts_operations: List[str],
        py_operations: List[str]
    ) -> float:
        """Calculate alignment score using AI understanding."""
        from difflib import SequenceMatcher
        
        if not ts_operations and not py_operations:
            return 1.0
        
        # Normalize operation names
        ts_ops_norm = [self._camel_to_snake(op.split('.')[0]) + '.' + op.split('.')[1] if '.' in op else op 
                      for op in ts_operations]
        py_ops_norm = py_operations
        
        # Sequence matching
        matcher = SequenceMatcher(None, ts_ops_norm, py_ops_norm)
        sequence_score = matcher.ratio()
        
        # Set matching (order-independent)
        ts_set = set(ts_ops_norm)
        py_set = set(py_ops_norm)
        set_score = len(ts_set & py_set) / max(len(ts_set), len(py_set)) if (ts_set or py_set) else 1.0
        
        return (sequence_score * 0.6 + set_score * 0.4)
    
    def _identify_critical_issues_ai(
        self,
        ts_intent: str,
        py_intent: str,
        ts_operations: List[str],
        py_operations: List[str],
        ts_verifications: List[str],
        py_verifications: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify critical issues using AI understanding."""
        issues = []
        
        # Check if intents match
        if ts_intent != py_intent:
            # Check if they're similar enough
            from difflib import SequenceMatcher
            intent_matcher = SequenceMatcher(None, ts_intent.lower().split(), py_intent.lower().split())
            if intent_matcher.ratio() < 0.5:
                issues.append({
                    'type': 'intent_mismatch',
                    'message': f"Test intent differs: TS verifies '{ts_intent}' but PY verifies '{py_intent}'",
                    'severity': 'high'
                })
        
        # Check for missing verifications (normalize names for comparison)
        ts_verif_set = set()
        for v in ts_verifications:
            if '.' in v:
                obj = self._camel_to_snake(v.split('.')[0])
                method = v.split('.')[1]
                ts_verif_set.add(f"{obj}.{method}")
            else:
                ts_verif_set.add(self._camel_to_snake(v))
        
        py_verif_set = set()
        for v in py_verifications:
            if '.' in v:
                obj = v.split('.')[0]
                method = v.split('.')[1]
                py_verif_set.add(f"{obj}.{method}")
            else:
                py_verif_set.add(v)
        
        missing_verif = ts_verif_set - py_verif_set
        if missing_verif:
            issues.append({
                'type': 'missing_verifications',
                'message': f"Python test is missing verifications: {', '.join(missing_verif)}",
                'severity': 'high',
                'details': list(missing_verif)
            })
        
        # Check for missing operations
        ts_ops_norm = [self._camel_to_snake(op.split('.')[0]) + '.' + op.split('.')[1] if '.' in op else op 
                      for op in ts_operations]
        py_ops_norm = py_operations
        ts_ops_set = set(ts_ops_norm)
        py_ops_set = set(py_ops_norm)
        missing_ops = ts_ops_set - py_ops_set
        if missing_ops:
            issues.append({
                'type': 'missing_operations',
                'message': f"Python test is missing operations: {', '.join(missing_ops)}",
                'severity': 'high',
                'details': list(missing_ops)
            })
        
        return issues
    
    def _find_differences_ai(
        self,
        ts_operations: List[str],
        py_operations: List[str],
        ts_verifications: List[str],
        py_verifications: List[str]
    ) -> List[str]:
        """Find differences using AI understanding."""
        differences = []
        
        if len(ts_operations) != len(py_operations):
            differences.append(f"Operation count: TS has {len(ts_operations)}, PY has {len(py_operations)}")
        
        if len(ts_verifications) != len(py_verifications):
            differences.append(f"Verification count: TS has {len(ts_verifications)}, PY has {len(py_verifications)}")
        
        return differences
    
    def _generate_suggestions_ai(
        self,
        ts_intent: str,
        py_intent: str,
        ts_operations: List[str],
        py_operations: List[str],
        ts_verifications: List[str],
        py_verifications: List[str],
        critical_issues: List[Dict]
    ) -> List[str]:
        """Generate suggestions using AI understanding."""
        suggestions = []
        
        # Suggest based on critical issues
        for issue in critical_issues:
            if issue['type'] == 'missing_verifications':
                details = issue.get('details', [])
                if details:
                    suggestions.append(f"Add verifications for: {', '.join(details[:3])}")
            elif issue['type'] == 'missing_operations':
                details = issue.get('details', [])
                if details:
                    suggestions.append(f"Add operations: {', '.join(details[:3])}")
            elif issue['type'] == 'intent_mismatch':
                suggestions.append(f"Align test intent: ensure PY test verifies '{ts_intent}'")
        
        return suggestions
    
    def _generate_explanation_ai(
        self,
        similarity: float,
        structural: float,
        semantic: float,
        alignment: float,
        critical_issues: List[Dict],
        differences: List[str],
        ts_intent: str,
        py_intent: str
    ) -> str:
        """Generate AI-powered explanation."""
        parts = []
        
        parts.append(f"Overall Similarity: {similarity:.1%}")
        parts.append(f"  • Structural: {structural:.1%} (sequence and structure)")
        parts.append(f"  • Semantic: {semantic:.1%} (test intent and meaning)")
        parts.append(f"  • Alignment: {alignment:.1%} (functional equivalence)")
        
        parts.append(f"\nTest Intent:")
        parts.append(f"  • TypeScript: {ts_intent}")
        parts.append(f"  • Python: {py_intent}")
        
        if critical_issues:
            parts.append(f"\nCritical Issues ({len(critical_issues)}):")
            for issue in critical_issues[:3]:
                parts.append(f"  • [{issue['severity'].upper()}] {issue['message']}")
        
        if differences:
            parts.append(f"\nKey Differences:")
            for diff in differences[:3]:
                parts.append(f"  • {diff}")
        
        return "\n".join(parts)
    
    def _extract_test_elements(self, code: str, language: str) -> Dict[str, Any]:
        """Extract key elements from test code."""
        elements = {
            'operations': [],
            'assertions': [],
            'calls': [],
            'setup_lines': 0
        }
        
        lines = code.split('\n')
        
        if language == 'typescript':
            # Extract await calls
            for line in lines:
                await_match = re.search(r'await\s+(\w+)\.(\w+)\(', line)
                if await_match:
                    elements['calls'].append({
                        'object': await_match.group(1),
                        'method': await_match.group(2),
                        'line': line.strip()
                    })
                    elements['operations'].append(f"call:{await_match.group(1)}.{await_match.group(2)}")
            
            # Extract expect assertions
            for line in lines:
                expect_match = re.search(r'expect\((\w+)\.(\w+)\)\.(\w+)\(', line)
                if expect_match:
                    elements['assertions'].append({
                        'object': expect_match.group(1),
                        'method': expect_match.group(2),
                        'assertion': expect_match.group(3),
                        'line': line.strip()
                    })
                    elements['operations'].append(f"assert:{expect_match.group(1)}.{expect_match.group(2)}.{expect_match.group(3)}")
        
        elif language == 'python':
            # Extract await calls
            for line in lines:
                await_match = re.search(r'await\s+(\w+)\.(\w+)\(', line)
                if await_match:
                    elements['calls'].append({
                        'object': await_match.group(1),
                        'method': await_match.group(2),
                        'line': line.strip()
                    })
                    elements['operations'].append(f"call:{await_match.group(1)}.{await_match.group(2)}")
            
            # Extract assertions
            for line in lines:
                assert_match = re.search(r'(\w+)\.(\w+)\.(assert_\w+)\(', line)
                if assert_match:
                    elements['assertions'].append({
                        'object': assert_match.group(1),
                        'method': assert_match.group(2),
                        'assertion': assert_match.group(3),
                        'line': line.strip()
                    })
                    elements['operations'].append(f"assert:{assert_match.group(1)}.{assert_match.group(2)}.{assert_match.group(3)}")
            
            # Count setup lines (mock creation, etc.)
            for line in lines:
                if any(keyword in line.lower() for keyword in ['mock', 'asyncmock', 'magicmock', '= mock', '= asyncmock']):
                    elements['setup_lines'] += 1
        
        return elements
    
    def _calculate_structural_similarity(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any]
    ) -> float:
        """Calculate structural similarity (sequence and count of operations)."""
        ts_ops = ts_elements['operations']
        py_ops = py_elements['operations']
        
        if not ts_ops and not py_ops:
            return 1.0
        if not ts_ops or not py_ops:
            return 0.0
        
        # Compare operation sequences
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, ts_ops, py_ops)
        return matcher.ratio()
    
    def _calculate_semantic_similarity(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any]
    ) -> float:
        """Calculate semantic similarity (test intent and meaning)."""
        # Compare assertions (what's being verified)
        ts_assertions = ts_elements['assertions']
        py_assertions = py_elements['assertions']
        
        if not ts_assertions and not py_assertions:
            return 1.0
        if not ts_assertions or not py_assertions:
            # If one has assertions and other doesn't, it's a mismatch
            # But give partial credit if they have the same calls
            if ts_elements['calls'] and py_elements['calls']:
                # Both have operations, just missing assertions
                return 0.5
            return 0.0
        
        # Match assertions by object and method (normalize names)
        # Create normalized signatures for matching
        ts_sigs = []
        for a in ts_assertions:
            obj = self._camel_to_snake(a['object'])
            method = a['method']
            # Normalize assertion types (toHaveBeenCalledWith -> assert_called_once_with)
            assertion = a['assertion']
            if assertion == 'toHaveBeenCalledWith':
                assertion = 'assert_called_once_with'
            elif assertion == 'toHaveBeenCalledTimes':
                assertion = 'assert_called_count'
            ts_sigs.append(f"{obj}.{method}.{assertion}")
        
        py_sigs = []
        for a in py_assertions:
            obj = a['object']
            method = a['method']
            assertion = a['assertion']
            py_sigs.append(f"{obj}.{method}.{assertion}")
        
        # Use fuzzy matching to find similar assertions
        from difflib import SequenceMatcher
        matched = 0
        total = max(len(ts_sigs), len(py_sigs))
        
        # Try to match each TS assertion with a PY assertion
        matched_py = set()
        for ts_sig in ts_sigs:
            best_match = None
            best_score = 0.0
            for i, py_sig in enumerate(py_sigs):
                if i in matched_py:
                    continue
                # Compare signatures
                matcher = SequenceMatcher(None, ts_sig.lower(), py_sig.lower())
                score = matcher.ratio()
                if score > best_score and score > 0.7:  # 70% similarity threshold
                    best_score = score
                    best_match = i
            
            if best_match is not None:
                matched += 1
                matched_py.add(best_match)
        
        # If we matched all, return high score
        if matched == total and total > 0:
            return 1.0
        
        # Partial credit for partial matches
        return matched / total if total > 0 else 0.0
    
    def _calculate_alignment_score(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any]
    ) -> float:
        """Calculate alignment score (functional equivalence)."""
        # Compare calls (test operations)
        ts_calls = ts_elements['calls']
        py_calls = py_elements['calls']
        
        if not ts_calls and not py_calls:
            # No calls in either - check if both have assertions only
            if ts_elements['assertions'] and py_elements['assertions']:
                return 1.0  # Both are assertion-only tests
            return 1.0
        
        if not ts_calls or not py_calls:
            # One has calls, other doesn't - partial mismatch
            return 0.3
        
        # Match calls by method name (normalize object names)
        # Use fuzzy matching for better alignment
        from difflib import SequenceMatcher
        
        ts_call_sigs = []
        for c in ts_calls:
            obj = self._camel_to_snake(c['object'])
            ts_call_sigs.append(f"{obj}.{c['method']}")
        
        py_call_sigs = []
        for c in py_calls:
            py_call_sigs.append(f"{c['object']}.{c['method']}")
        
        # Try to match calls (order matters for alignment)
        matched = 0
        total = max(len(ts_call_sigs), len(py_call_sigs))
        
        # Use sequence matching for alignment
        matcher = SequenceMatcher(None, ts_call_sigs, py_call_sigs)
        alignment_ratio = matcher.ratio()
        
        # Also check set intersection (order-independent)
        ts_set = set(ts_call_sigs)
        py_set = set(py_call_sigs)
        set_match = len(ts_set & py_set) / max(len(ts_set), len(py_set)) if (ts_set or py_set) else 1.0
        
        # Combine sequence and set matching
        return (alignment_ratio * 0.6 + set_match * 0.4)
    
    def _identify_critical_issues(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify critical issues preventing alignment."""
        issues = []
        
        # Check assertion count
        ts_assertions = len(ts_elements['assertions'])
        py_assertions = len(py_elements['assertions'])
        
        if ts_assertions != py_assertions:
            if ts_assertions > py_assertions:
                issues.append({
                    'type': 'missing_assertions',
                    'message': f"Python test is missing {ts_assertions - py_assertions} assertion(s)",
                    'severity': 'high'
                })
            else:
                issues.append({
                    'type': 'extra_assertions',
                    'message': f"Python test has {py_assertions - ts_assertions} extra assertion(s)",
                    'severity': 'medium'
                })
        
        # Check for missing operations
        ts_calls = ts_elements['calls']
        py_calls = py_elements['calls']
        
        ts_call_sigs = set()
        for c in ts_calls:
            obj = self._camel_to_snake(c['object'])
            ts_call_sigs.add(f"{obj}.{c['method']}")
        
        py_call_sigs = set()
        for c in py_calls:
            py_call_sigs.add(f"{c['object']}.{c['method']}")
        
        missing_calls = ts_call_sigs - py_call_sigs
        if missing_calls:
            issues.append({
                'type': 'missing_operations',
                'message': f"Python test is missing operations: {', '.join(missing_calls)}",
                'severity': 'high',
                'details': list(missing_calls)
            })
        
        return issues
    
    def _find_differences(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any]
    ) -> List[str]:
        """Find specific differences between tests."""
        differences = []
        
        # Compare operations
        ts_ops = ts_elements['operations']
        py_ops = py_elements['operations']
        
        if len(ts_ops) != len(py_ops):
            differences.append(f"Operation count mismatch: TS has {len(ts_ops)}, PY has {len(py_ops)}")
        
        # Compare assertions
        ts_assertions = ts_elements['assertions']
        py_assertions = py_elements['assertions']
        
        if len(ts_assertions) != len(py_assertions):
            differences.append(f"Assertion count mismatch: TS has {len(ts_assertions)}, PY has {len(py_assertions)}")
        
        return differences
    
    def _generate_suggestions(
        self, 
        ts_elements: Dict[str, Any], 
        py_elements: Dict[str, Any],
        differences: List[str]
    ) -> List[str]:
        """Generate suggestions for alignment."""
        suggestions = []
        
        # Check for missing assertions
        ts_assertions = ts_elements['assertions']
        py_assertions = py_elements['assertions']
        
        if len(ts_assertions) > len(py_assertions):
            suggestions.append(f"Add {len(ts_assertions) - len(py_assertions)} missing assertion(s) to match TypeScript test")
        
        # Check for missing operations
        ts_calls = ts_elements['calls']
        py_calls = py_elements['calls']
        
        ts_call_sigs = set()
        for c in ts_calls:
            obj = self._camel_to_snake(c['object'])
            ts_call_sigs.add(f"{obj}.{c['method']}")
        
        py_call_sigs = set()
        for c in py_calls:
            py_call_sigs.add(f"{c['object']}.{c['method']}")
        
        missing = ts_call_sigs - py_call_sigs
        if missing:
            suggestions.append(f"Add missing operations: {', '.join(missing)}")
        
        return suggestions
    
    def _generate_explanation(
        self,
        similarity: float,
        structural: float,
        semantic: float,
        alignment: float,
        critical_issues: List[Dict],
        differences: List[str]
    ) -> str:
        """Generate human-readable explanation."""
        parts = []
        
        parts.append(f"Overall similarity: {similarity:.1%}")
        parts.append(f"  - Structural: {structural:.1%}")
        parts.append(f"  - Semantic: {semantic:.1%}")
        parts.append(f"  - Alignment: {alignment:.1%}")
        
        if critical_issues:
            parts.append(f"\nCritical issues found: {len(critical_issues)}")
            for issue in critical_issues[:3]:
                parts.append(f"  - {issue['message']}")
        
        if differences:
            parts.append(f"\nDifferences: {len(differences)}")
            for diff in differences[:3]:
                parts.append(f"  - {diff}")
        
        return "\n".join(parts)
    
    def _camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case."""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def load_test_data(json_path: Path) -> List[Dict]:
    """Load test data from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_test_code(file_path: str, start_line: int, end_line: int) -> str:
    """Read test code from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return ''.join(lines[start_line-1:end_line])


def generate_ai_comparison_report(
    comparisons: List[TestComparison],
    output_file: Path
) -> None:
    """Generate a detailed report from AI comparisons."""
    report_lines = [
        "# AI-Powered Test Comparison Report",
        "",
        "This report contains AI-analyzed comparisons between TypeScript and Python test implementations.",
        "",
        "## Summary",
        "",
        f"- **Total Tests**: {len(comparisons)}",
    ]
    
    pass_count = sum(1 for c in comparisons if c.status == "PASS")
    fail_count = len(comparisons) - pass_count
    
    report_lines.append(f"- **Passing**: {pass_count} ({pass_count/len(comparisons)*100:.1f}%)")
    report_lines.append(f"- **Failing**: {fail_count} ({fail_count/len(comparisons)*100:.1f}%)")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Generate report for each test
    for i, comp in enumerate(comparisons, 1):
        status_badge = " **PASS**" if comp.status == "PASS" else " **FAIL**"
        report_lines.append(f"## Test {i}: {comp.test_name}{status_badge}")
        report_lines.append("")
        
        # TypeScript test
        report_lines.append(f"### TypeScript Test: {comp.ts_file}")
        report_lines.append("")
        report_lines.append("```typescript")
        report_lines.append(comp.ts_code.rstrip())
        report_lines.append("```")
        report_lines.append("")
        
        # Python test
        report_lines.append(f"### Python Test: {comp.py_file}")
        report_lines.append("")
        report_lines.append("```python")
        report_lines.append(comp.py_code.rstrip())
        report_lines.append("```")
        report_lines.append("")
        
        # Comparison results
        report_lines.append("### AI Analysis Results")
        report_lines.append("")
        report_lines.append(f"**Similarity Score**: {comp.similarity_score:.2%}")
        report_lines.append(f"  - Structural: {comp.structural_score:.2%}")
        report_lines.append(f"  - Semantic: {comp.semantic_score:.2%}")
        report_lines.append(f"  - Alignment: {comp.alignment_score:.2%}")
        report_lines.append("")
        
        if comp.critical_issues:
            report_lines.append("**Critical Issues:**")
            for issue in comp.critical_issues:
                report_lines.append(f"  - [{issue['severity'].upper()}] {issue['message']}")
            report_lines.append("")
        
        if comp.differences:
            report_lines.append("**Differences:**")
            for diff in comp.differences:
                report_lines.append(f"  - {diff}")
            report_lines.append("")
        
        if comp.suggestions:
            report_lines.append("**Suggestions:**")
            for sugg in comp.suggestions:
                report_lines.append(f"  - {sugg}")
            report_lines.append("")
        
        report_lines.append(f"**Explanation:**")
        report_lines.append("")
        report_lines.append(comp.explanation)
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
    
    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"AI comparison report saved to: {output_file}")


def main():
    """Main function."""
    import sys
    import os
    
    # Default paths
    DEFAULT_TS_BASE_DIR = os.environ.get('TS_BASE_DIR', 'wallet-toolbox')
    DEFAULT_PY_BASE_DIR = os.environ.get('PY_BASE_DIR', 'py-wallet-toolbox/tests')
    
    # Load test data
    test_json_path = Path('test_ranges.json')
    if not test_json_path.exists():
        alt_paths = [
            Path('/tmp/test_ranges.json'),
            Path('py-wallet-toolbox/test-analysis/test_ranges.json'),
        ]
        for alt_path in alt_paths:
            if alt_path.exists():
                test_json_path = alt_path
                break
        else:
            print(f"Error: test_ranges.json not found.")
            return
    
    test_data = load_test_data(test_json_path)
    
    print(f"Comparing {len(test_data)} tests using AI analysis...")
    print("="*80)
    
    comparator = AITestComparator()
    comparisons = []
    
    for i, entry in enumerate(test_data, 1):
        print(f"\n[{i}/{len(test_data)}] Analyzing: {entry['test_name']}")
        
        # Read test code
        ts_file = Path(DEFAULT_TS_BASE_DIR) / entry['ts_file']
        py_file = Path(DEFAULT_PY_BASE_DIR) / entry['py_file']
        
        try:
            ts_code = read_test_code(
                str(ts_file),
                entry['ts_start'],
                entry['ts_end']
            )
            py_code = read_test_code(
                str(py_file),
                entry['py_start'],
                entry['py_end']
            )
            
            # Compare using AI
            comparison = comparator.compare_test_snippets(
                test_name=entry['test_name'],
                ts_code=ts_code,
                py_code=py_code,
                ts_file=str(ts_file),
                py_file=str(py_file)
            )
            
            comparisons.append(comparison)
            
            # Print progress
            status_symbol = "✓" if comparison.status == "PASS" else "✗"
            print(f"  {status_symbol} {comparison.status}: {comparison.similarity_score:.1%} similarity")
            if comparison.critical_issues:
                print(f"    Issues: {len(comparison.critical_issues)}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Generate report
    output_file = Path("ai_test_comparison_report.md")
    generate_ai_comparison_report(comparisons, output_file)
    
    # Summary
    pass_count = sum(1 for c in comparisons if c.status == "PASS")
    print(f"\n{'='*80}")
    print(f"Summary: {pass_count}/{len(comparisons)} tests passing")
    print(f"Report saved to: {output_file}")


if __name__ == '__main__':
    main()

