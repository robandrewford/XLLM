"""XLLM Short - Main program for end-users."""

from . import xllm_util as llm

class XLLMShort:
    """XLLM Short - Main program for end-users that reads pre-created tables."""
    
    def __init__(self):
        """Initialize the XLLMShort class."""

if __name__ == "__main__":
    xllm_short = XLLMShort()
    if xllm_short.load_data():
        xllm_short.run() 