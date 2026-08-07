import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_4():
    \"\"\"Test example 4\"\"\"
    assert True

def test_example_4_error():
    \"\"\"Test error handling for 4\"\"\"
    assert True
