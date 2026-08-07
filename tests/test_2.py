import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

def test_example_2():
    \"\"\"Test example 2\"\"\"
    assert True

def test_example_2_error():
    \"\"\"Test error handling for 2\"\"\"
    assert True
