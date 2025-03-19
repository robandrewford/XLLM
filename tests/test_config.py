"""Tests for config module."""

import pytest
from xllm.enterprise.config import (
    get_backend_params,
    get_frontend_params,
    get_tables_dict,
)

def test_config():
    """Test config module."""
    assert get_backend_params is not None
    assert get_frontend_params is not None
    assert get_tables_dict is not None 