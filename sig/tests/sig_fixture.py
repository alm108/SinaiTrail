"""Minimal parser for a `.sig` fixture's `# CLAIMS` block.

A CLAIMS block is the trailing region of a fixture beginning with a line whose
stripped text starts with `# CLAIMS`. Each subsequent non-empty line of the form

    key := value

contributes one claim. Comment lines (`#`) inside the block are ignored. This is
deliberately tiny: the fixture's *claims* are what the conformance tests bind to the
reference implementation, so the parser only needs to recover key/value pairs.
"""
from __future__ import annotations

from pathlib import Path


def parse_claims(path: str | Path) -> dict[str, str]:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    # find the CLAIMS header
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("# claims"):
            start = i + 1
            break
    if start is None:
        raise ValueError(f"no '# CLAIMS' block found in {path}")

    claims: dict[str, str] = {}
    for line in lines[start:]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if ":=" not in s:
            continue
        key, _, value = s.partition(":=")
        claims[key.strip()] = value.strip()
    return claims
