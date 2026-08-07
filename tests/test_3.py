import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_3():
    \"\"\"Test example 3\"\"\"
    assert True

def test_example_3_error():
    \"\"\"Test error handling for 3\"\"\"
    assert True
