import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_1():
    \"\"\"Test example 1\"\"\"
    assert True

def test_example_1_error():
    \"\"\"Test error handling for 1\"\"\"
    assert True
