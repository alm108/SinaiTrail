"""Shared bootstrap: make the repo root importable so tests can `import sinai_trail`.

Stdlib only. Imported for its side effect by every test module in this package.
"""
import sys
from pathlib import Path

# sig/tests/_bootstrap.py -> parents[2] == repo root (contains sinai_trail.py)
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"
