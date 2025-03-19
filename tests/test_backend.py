"""Tests for backend module."""

import pytest
from xllm.enterprise.backend import (
    generate_backend_tables,
    load_backend_tables,
    load_backend_tables_from_disk,
)

def test_backend():
    """Test backend module."""
    assert generate_backend_tables is not None
    assert load_backend_tables is not None
    assert load_backend_tables_from_disk is not None 