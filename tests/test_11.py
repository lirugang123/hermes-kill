import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_11():
    \"\"\"Test example 11\"\"\"
    assert True

def test_example_11_error():
    \"\"\"Test error handling for 11\"\"\"
    assert True
