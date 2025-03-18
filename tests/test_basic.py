"""Basic tests for the xllm6 package."""

from xllm6 import __version__


def test_version():
    """Test that version is set correctly."""
    assert __version__ == "0.1.0"


def test_xllm6_class_init():
    """Test that the XLLM6 class can be initialized."""
    from xllm6 import XLLM6

    xllm6 = XLLM6()
    assert xllm6 is not None
    assert hasattr(xllm6, "dictionary")
    assert hasattr(xllm6, "word_pairs")
    assert hasattr(xllm6, "stopwords")


def test_xllm6_short_class_init():
    """Test that the XLLM6Short class can be initialized."""
    from xllm6 import XLLM6Short

    xllm6_short = XLLM6Short()
    assert xllm6_short is not None
    assert hasattr(xllm6_short, "dictionary")
    assert hasattr(xllm6_short, "embeddings")
    assert hasattr(xllm6_short, "DATA_PATH")
