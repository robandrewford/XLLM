"""
Configuration management for enterprise features.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class EnterpriseConfig:
    """Configuration for enterprise features."""
    
    api_key: str
    model_name: str = "gpt-4"
    max_tokens: int = 2000
    temperature: float = 0.7
    organization_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ValueError("API key is required")
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature must be between 0 and 1")
        if self.max_tokens < 1:
            raise ValueError("Max tokens must be positive") 