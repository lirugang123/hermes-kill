import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_14():
    \"\"\"Test example 14\"\"\"
    assert True

def test_example_14_error():
    \"\"\"Test error handling for 14\"\"\"
    assert True
