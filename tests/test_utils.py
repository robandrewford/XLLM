"""Tests for utils module."""

import pytest
from xllm.enterprise.utils import (
    update_hash,
    update_nested_hash,
    get_value,
)

def test_utils():
    """Test utils module."""
    assert update_hash is not None
    assert update_nested_hash is not None
    assert get_value is not None 