"""Base exception classes for XLLM."""


class XLLMError(Exception):
    """Base exception for all XLLM errors."""

    def __init__(self, message: str = "An error occurred in XLLM") -> None:
        """Initialize the exception.

        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(self.message) 