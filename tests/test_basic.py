"""Basic tests for XLLM."""

from xllm import __version__
from xllm import XLLM
from xllm import XLLMShort

def test_version():
    """Test version string."""
    assert isinstance(__version__, str)
    assert len(__version__.split(".")) == 3

def test_xllm():
    """Test XLLM class."""
    xllm = XLLM()
    assert isinstance(xllm, XLLM)

def test_xllm_short():
    """Test XLLMShort class."""
    xllm_short = XLLMShort()
    assert isinstance(xllm_short, XLLMShort)
