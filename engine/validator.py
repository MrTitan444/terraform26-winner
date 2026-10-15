"""
TERRAFORM Survivor Constraint Validator
Enforces the non-negotiable ground rule:
The survivor has no instruments and no lab. The System must not ask for,
quote, or depend on scientific readings, fixed chemical values, or lab metrics.
Any checks suggested must be doable with eyes, hands, and household items,
and amounts must be described in everyday terms (a handful, a bucketful, a pace, a hand's depth).
"""

import re
from typing import List, Tuple, Dict, Any

FORBIDDEN_PATTERNS = [
    r'\bpH\b',
    r'\bppm\b',
    r'\bNPK\b',
    r'\b10-10-10\b',
    r'\bfertilizer grade\b',
    r'\belectrical conductivity\b',
    r'\bEC reading\b',
    r'\bmillisiemens\b',
    r'\bmicrograms\b',
    r'\bmilligrams\b',
    r'\bcentimeters\b',  # prefer hand-spans / finger-widths
    r'\bmilliliters\b',  # prefer drops / cups / bucketfuls
    r'\bgrams\b',        # prefer pinches / handfuls
    r'\bacidic: [0-9]',
    r'\balkaline: [0-9]',
    r'\bdegrees celsius\b',
    r'\bdegrees fahrenheit\b',
    r'\bparts per million\b'
]

UNIT_CONVERSIONS = {
    "10-20 cm": "about one hand-span",
    "40-50 cm": "about knee-high",
    "1 meter": "about one walking pace",
    "10 liters": "one bucketful",
    "500 ml": "about two cups",
    "2-3 cm": "about one thumb-joint deep"
}

def validate_text(text: str) -> Tuple[bool, List[str]]:
    """
    Checks if text violates the survivor ground rule.
    Returns (is_compliant, list_of_violations).
    """
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            violations.append(f"Forbidden scientific term found: '{matches[0]}'")
    return len(violations) == 0, violations

def sanitize_text(text: str) -> str:
    """
    Replaces common accidental scientific units with everyday survivor units.
    """
    sanitized = text
    for sci, surv in UNIT_CONVERSIONS.items():
        sanitized = re.sub(re.escape(sci), surv, sanitized, flags=re.IGNORECASE)
    
    # Strip any standalone pH or NPK terms if present
    sanitized = re.sub(r'\bpH\b(\s*[0-9]+(\.[0-9]+)?)?', 'sweet/sour balance', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\bNPK\b', 'soil nourishment balance', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\bppm\b', 'trace parts', sanitized, flags=re.IGNORECASE)
    return sanitized
