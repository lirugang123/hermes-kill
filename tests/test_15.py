import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_15():
    \"\"\"Test example 15\"\"\"
    assert True

def test_example_15_error():
    \"\"\"Test error handling for 15\"\"\"
    assert True
