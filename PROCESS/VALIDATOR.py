# python/python-process-lib/VALIDATOR.py
# v1 – Dynamic context-aware validator for code, pseudo-code, project structures & simulations

from typing import List, Dict, Any, Optional, Union
import re
import ast
from .BLEED_DETECTOR import BleedDetector  # lightweight bleed reporting only

class Validator:
    def __init__(self):
        self.bleed_detector = BleedDetector()

    def _parse_context(self, context_hint: str) -> Dict[str, str]:
        """Dynamically extract validation rules from context_hint (generic & adaptive)."""
        ctx = {}
        hint = context_hint.lower()
        # Generic pattern matching — works for any language/OS/framework/simulation
        if "lang:" in hint or "language:" in hint:
            ctx['language'] = re.search(r'(?:lang|language):(\w+)', hint).group(1) if re.search(r'(?:lang|language):(\w+)', hint) else "unknown"
        if "v" in hint or "ver" in hint:
            ctx['version'] = re.search(r'v?(\d+\.\d+)', hint).group(1) if re.search(r'v?(\d+\.\d+)', hint) else "unknown"
        if "os:" in hint or "os " in hint:
            ctx['os_type'] = re.search(r'os:(\w+)', hint).group(1) if re.search(r'os:(\w+)', hint) else "unknown"
        if "framework:" in hint or "project:" in hint:
            ctx['framework'] = re.search(r'(?:framework|project):(\w+)', hint).group(1) if re.search(r'(?:framework|project):(\w+)', hint) else "unknown"
        if "mode:" in hint or "simulation" in hint:
            ctx['mode'] = "simulation" if "simulation" in hint else "standard"
        return ctx

    def _run_syntax_check(self, code: str, ctx: Dict) -> Dict:
        """Use code_execution sandbox for syntax/runtime validation where possible."""
        try:
            # Python syntax (expandable to other languages via patterns)
            ast.parse(code)
            return {'valid': True, 'issues': [], 'type': 'syntax'}
        except SyntaxError as e:
            return {'valid': False, 'issues': [f"Syntax error: {str(e)}"], 'type': 'syntax'}
        except Exception as e:
            return {'valid': False, 'issues': [f"Validation error: {str(e)}"], 'type': 'runtime'}

    def _check_structure(self, content: str, ctx: Dict) -> Dict:
        """Context-aware structural / filesystem / simulation rule checks."""
        issues = []
        # Generic layout / rule validation based on detected context
        if ctx.get('framework') or ctx.get('language'):
            # Example generic checks — extendable for any project type
            if "layout" in content.lower() and not re.search(r'(src|lib|config|tests)', content, re.IGNORECASE):
                issues.append("Possible missing standard project directories")
        if ctx.get('mode') == "simulation":
            if not re.search(r'(state|transition|rule|condition)', content, re.IGNORECASE):
                issues.append("Simulation appears to lack state/transition rules")
        return {'valid': len(issues) == 0, 'issues': issues}

    def process(self,
                chunks_or_output: Union[List[Dict[str, Any]], str],
                context_hint: str = "") -> Dict[str, Any]:
        """Main entry point — dynamic validation based on context_hint + input."""
        # Normalize input
        if isinstance(chunks_or_output, str):
            chunks = [{'content': chunks_or_output}]
        else:
            chunks = chunks_or_output

        ctx = self._parse_context(context_hint)
        bleed_report = self.bleed_detector.process(" ".join(c.get('content', '') for c in chunks))

        issues = []
        suggestions = []
        validated_sections = []

        for i, chunk in enumerate(chunks):
            content = chunk.get('content', chunk.get('full_content', ''))
            # Syntax / runtime check
            syntax_result = self._run_syntax_check(content, ctx)
            if not syntax_result['valid']:
                issues.extend(syntax_result['issues'])
            # Structure / context-aware check
            struct_result = self._check_structure(content, ctx)
            if not struct_result['valid']:
                issues.extend(struct_result['issues'])
            validated_sections.append(content)  # report only — no stripping

        # Final holistic validation
        final_valid = len(issues) == 0

        if not final_valid:
            suggestions.append("Review issues above or provide more context_hint for deeper rules")

        summary = (f"VALIDATOR v1 complete — context: {ctx}, sections: {len(chunks)}, "
                   f"valid: {final_valid}, bleed_detected: {bleed_report.get('bleed_detected', False)}")

        return {
            'valid': final_valid,
            'issues': issues,
            'suggestions': suggestions,
            'detected_context': ctx,
            'bleed_report': bleed_report,
            'validated_output': "\n\n".join(validated_sections),  # clean but unchanged
            'summary': summary,
            'total_sections': len(chunks)
        }

# Example usage (Luna/ChaosEngine or any layer):
# validator = Validator()
# result = validator.process(chunks_or_output, context_hint="language:backend-v3 os:standard project:framework mode:simulation")
# print(result['summary'])
# if not result['valid']:
#     print(result['issues'])
