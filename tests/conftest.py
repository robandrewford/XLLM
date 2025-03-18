"""Configure pytest fixtures for the XLLM6 project."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_text_hash():
    """Sample text representing a hash dictionary."""
    return "{'word1': 10, 'word2': 5, 'word3': 3}"


@pytest.fixture
def sample_list_text():
    """Sample text representing a list."""
    return "('word1', 'word2', 'word3')"


@pytest.fixture
def sample_stopwords():
    """Sample stopwords for testing."""
    return ("of", "the", "in", "and", "but", "if", "or")


@pytest.fixture
def sample_dictionary():
    """Sample dictionary for testing."""
    return {"test": 10, "example": 5, "word": 3, "test~example": 2}


@pytest.fixture
def create_test_file(test_data_dir):
    """Create a test file with content in the test directory."""

    def _create_file(filename, content):
        path = Path(test_data_dir) / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(path)

    return _create_file


@pytest.fixture
def temp_file():
    """
    Fixture providing a temporary file for tests.

    Yields:
        str: Path to temporary file
    """
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)
