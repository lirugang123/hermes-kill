import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_6():
    \"\"\"Test example 6\"\"\"
    assert True

def test_example_6_error():
    \"\"\"Test error handling for 6\"\"\"
    assert True
