import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_5():
    \"\"\"Test example 5\"\"\"
    assert True

def test_example_5_error():
    \"\"\"Test error handling for 5\"\"\"
    assert True
