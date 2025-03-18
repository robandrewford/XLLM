# XLLM6 - Large Language Model with X-Embeddings

This repository contains the XLLM6 project - a Large Language Model with unique x-embeddings feature.

## Project Structure

- `src/xllm6`: Core XLLM6 code implementation
- `mvp`: MVP implementation
- `tests`: Unit tests for XLLM6 code

## Getting Started

```bash
# Install the package in development mode
make setup

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

## Features

XLLM6 consists of three main components:

1. `xllm6_util.py`: Library with text processing functions
2. `xllm6_short.py`: Program for end-users that reads pre-created tables
3. `xllm6.py`: Program for developers that creates tables from crawled data

## Dependencies

This project uses:

- uv for package management
- ruff for formatting and linting
- pytest for testing
