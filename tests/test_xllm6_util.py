"""Tests for the XLLM6 utility functions."""

from xllm6 import xllm6_util


def test_trim():
    """Test the trim function."""
    assert xllm6_util.trim("test.") == "test"
    assert xllm6_util.trim("test,") == "test"
    assert xllm6_util.trim("test.,") == "test"


def test_text_to_hash():
    """Test the text_to_hash function."""
    text = "{'key1': 10, 'key2': 20}"
    result = xllm6_util.text_to_hash(text)
    assert result == {"key1": 10, "key2": 20}


def test_text_to_list():
    """Test the text_to_list function."""
    text = "('item1', 'item2', 'item3')"
    result = xllm6_util.text_to_list(text)
    assert result == ("item1", "item2", "item3")


def test_create_hash():
    """Test the create_hash function."""
    items = ["item1", "item2", "item1", "item3"]
    result = xllm6_util.create_hash(items)
    assert result == {"item1": 2, "item2": 1, "item3": 1}


def test_reject():
    """Test the reject function."""
    stopwords = ("of", "the", "in")
    assert xllm6_util.reject("", stopwords) is True
    assert xllm6_util.reject("1test", stopwords) is True
    assert xllm6_util.reject("of", stopwords) is True
    assert xllm6_util.reject("example", stopwords) is False
