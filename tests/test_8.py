import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_8():
    \"\"\"Test example 8\"\"\"
    assert True

def test_example_8_error():
    \"\"\"Test error handling for 8\"\"\"
    assert True
