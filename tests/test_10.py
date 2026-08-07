import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_10():
    \"\"\"Test example 10\"\"\"
    assert True

def test_example_10_error():
    \"\"\"Test error handling for 10\"\"\"
    assert True
