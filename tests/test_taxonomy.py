"""Tests for taxonomy module."""

import pytest
from xllm.build_taxonomy import taxonomy
from xllm.build_taxonomy import reallocate

def test_taxonomy():
    """Test taxonomy module."""
    assert taxonomy is not None

def test_reallocate():
    """Test reallocate module."""
    assert reallocate is not None 