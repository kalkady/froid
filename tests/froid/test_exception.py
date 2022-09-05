

# imports - module imports
from froid.exception import (
    FroidError
)

# imports - test imports
import pytest

def test_froid_error():
    with pytest.raises(FroidError):
        raise FroidError