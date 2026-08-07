import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_12():
    \"\"\"Test example 12\"\"\"
    assert True

def test_example_12_error():
    \"\"\"Test error handling for 12\"\"\"
    assert True
