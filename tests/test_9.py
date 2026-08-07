import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_9():
    \"\"\"Test example 9\"\"\"
    assert True

def test_example_9_error():
    \"\"\"Test error handling for 9\"\"\"
    assert True
