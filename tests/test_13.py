import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_13():
    \"\"\"Test example 13\"\"\"
    assert True

def test_example_13_error():
    \"\"\"Test error handling for 13\"\"\"
    assert True
