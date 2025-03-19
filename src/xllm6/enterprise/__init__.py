"""XLLM Enterprise Module.

This module provides corporate knowledge base functionality built on the XLLM framework.
It includes tools for processing corporate document corpora, creating backend knowledge tables,
and implementing real-time fine-tuning for enterprise question answering.
"""

__version__ = "2.0.0"

from src.xllm6.enterprise.config import get_backend_params, get_frontend_params
from src.xllm6.enterprise.backend import generate_backend_tables, load_backend_tables
from src.xllm6.enterprise.processor import process_query 