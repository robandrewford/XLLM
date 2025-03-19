# XLLM - Large Language Model with X-Embeddings

XLLM is an innovative Large Language Model that leverages unique x-embeddings to provide efficient and accurate knowledge retrieval. The project is designed as a two-stage system: a developer tool for processing and organizing knowledge bases, and an end-user tool for querying and retrieving information. It features specialized enterprise capabilities for corporate knowledge management, including real-time fine-tuning and multimodal content processing. The system's architecture emphasizes efficient data structures, optimized query processing, and robust taxonomy building, making it particularly suitable for both general-purpose knowledge bases and enterprise-specific applications.

## Project Structure

- `src/xllm/`: Core implementation
  - `enterprise/`: Corporate knowledge management module
  - `build-taxonomy/`: Taxonomy generation tools
  - `utils/`: Shared utility functions
- `mvp/`: MVP implementation
- `tests/`: Unit tests
- `data/`: Data storage and processing
  - `xllm/`: Core data tables
  - `enterprise/`: Enterprise-specific data

## Getting Started

```bash
# Install dependencies
make setup

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

## Core Components

1. **Developer Tools**
   - `xllm.py`: Processes raw data and creates knowledge tables
   - `xllm-enterprise.py`: Enterprise knowledge base processor
   - `xllm-enterprise-dev.py`: Enterprise testing and evaluation

2. **End-User Tools**
   - `xllm_short.py`: Interactive query interface
   - `xllm-enterprise-user.py`: Enterprise query interface

3. **Utilities**
   - `xllm_util.py`: Core text processing functions
   - `pdf_processor.py`: PDF document processing

## Features

- Efficient knowledge retrieval using x-embeddings
- Real-time fine-tuning for enterprise queries
- Taxonomy-based knowledge organization
- Multimodal content processing
- Interactive query interfaces
- Comprehensive testing framework

## Dependencies

- Python 3.11+
- uv for package management
- ruff for formatting and linting
- pytest for testing

For detailed documentation, see:

- [Data Structures Overview](README-DATA.md)
- [Code Architecture](README-CODE.md)
