# XLLM6 Code Structure Overview

## System Architecture

### Directory Structure

```text
/
├── data/
│   ├── xllm6/              # Core data tables for base XLLM system
│   └── enterprise/         # Enterprise-specific data tables
│
├── mvp/                    # Minimum viable product components and backend tables
│   └── README.md           # MVP documentation
│
└── src/
    └── xllm6/              # Source code for XLLM system
        ├── __init__.py     # Package initialization
        ├── __main__.py     # Entry point for the package
        ├── xllm6.py        # Core developer processing tool
        ├── xllm6_short.py  # End-user query interface
        ├── xllm6_util.py   # Shared utility functions
        ├── build-taxonomy/ # Taxonomy building components
        └── enterprise/     # Enterprise-specific components
            ├── __init__.py
            ├── config.py
            ├── utils.py
            ├── backend.py
            ├── processor.py
            ├── user.py
            ├── dev.py
            └── pdf_processor.py
```

## Core System Components

### xllm6.py (Developer Tool)

- Processes raw crawled data from Wolfram
- Creates all data tables from scratch
- Performs heavy text processing and relationship extraction
- No built-in query interface
- Designed for initial data pipeline setup

### xllm6_short.py (End-User Tool)

- Uses pre-created tables (does not process raw data)
- Can download tables from GitHub if not locally available
- Provides interactive query functionality
- Includes spelling correction and query processing
- Designed for consumption of processed data

### xllm6_util.py (Shared Utilities)

- Provides common functions for both tools
- Handles file operations and data loading
- Implements shared text processing functions
- Manages table generation and updates
- Centralizes common code to reduce duplication

## Enterprise Module Components

### enterprise/__init__.py

- __Format__: Python package initialization
- __Definition__: Enterprise module entry point
- __Creation__: Created during enterprise module setup
- __Usage__: Exports enterprise module components

### enterprise/config.py

- __Format__: Python configuration module
- __Definition__: Centralizes enterprise settings
- __Creation__: Created during enterprise module setup
- __Usage__: Manages enterprise-specific configurations

### enterprise/utils.py

- __Format__: Python utility module
- __Definition__: Enterprise-specific utility functions
- __Creation__: Created during enterprise module setup
- __Usage__: Provides shared enterprise functionality

### enterprise/backend.py

- __Format__: Python processor
- __Definition__: Core enterprise data processing
- __Creation__: Created during enterprise module setup
- __Usage__: Handles enterprise data ingestion and table generation

### enterprise/processor.py

- __Format__: Python processor
- __Definition__: Enterprise query processing
- __Creation__: Created during enterprise module setup
- __Usage__: Manages enterprise-specific query handling

### enterprise/user.py

- __Format__: Python interface
- __Definition__: End-user query interface
- __Creation__: Created during enterprise module setup
- __Usage__: Provides interactive enterprise query functionality

### enterprise/dev.py

- __Format__: Python interface
- __Definition__: Developer testing interface
- __Creation__: Created during enterprise module setup
- __Usage__: Enables enterprise system testing and validation

### enterprise/pdf_processor.py

- __Format__: Python processor
- __Definition__: PDF document processor
- __Creation__: Created during enterprise module setup
- __Usage__: Converts PDFs to enterprise repository format

## Data Flow

### Base System Flow

1. __Raw Data Ingestion__
   - Source: Wolfram crawled data (crawl_final_stats.txt)
   - Processor: xllm6.py
   - Function: process_crawled_data()

2. __Core Table Generation__
   - Dictionary: Word-count pairs (xllm6_dictionary.txt)
   - URL Mapping: URL-to-ID mappings (xllm6_arr_url.txt)
   - Categorization: Word-to-category mappings (hash tables)

3. __End-User Query Flow__
   - Table Loading: xllm6_short.py loads tables
   - Query Processing: User input processing
   - Result Generation: Formatted output

### Enterprise System Flow

1. __Corporate Data Ingestion__
   - Sources:
     - Repository files (repository.txt, repository2.txt, repository3.txt)
     - PDF documents (processed by pdf_processor.py)
   - Processor: backend.py
   - Function: generate_backend_tables()

2. __Enterprise Table Generation__
   - Dictionary: Token-count pairs (backend_dictionary.txt)
   - Entity Mapping: Entity-ID mappings (backend_ID_*.txt)
   - Context Information: Contextual data (backend_hash_context*.txt)

3. __Enterprise Query Flow__
   - Table Loading: user.py/dev.py loads tables
   - Query Processing: processor.py handles queries
   - Result Generation: Contextual results
   - Fine-Tuning: Real-time optimization (user mode)

## Integration Points

### PDF to Repository Conversion

pdf_processor.py converts PDF documents to repository format:

- PDF parsing using PyMuPDF (fitz)
- Text block extraction with formatting
- Heading, bullet list, and section identification
- Entity format conversion:

```text
entityID~~{title::value||category::value||tag_list::value||meta::value||description::value}
```

### Backend to Processor Flow

1. backend.py generates tables from repository data
2. user.py/dev.py load tables into memory
3. processor.py processes queries
4. Real-time fine-tuning optimizes results

## Advanced Features

### Real-Time Fine-Tuning

- Initial query dictionaries and embeddings generation
- distill_frontend_tables() purges redundant entries
- Query processing optimization
- Enabled in user mode, disabled in dev mode

### Relevancy Scoring

- Test prompts loaded from enterprise_sample_prompts.txt
- Expected answers processed alongside prompts
- calculate_relevancy_score() determines match quality
- Scores and statistics saved to output file

## System Requirements

### Software Requirements

- Python 3.7+ (3.11+ recommended)
- PyMuPDF for PDF processing
- Significant disk space for backend tables
- 8GB+ RAM recommended for large documents

### File Format Compatibility

- Entity format: ID~~{key::value}
- PDF processor maintains entity format
- Custom data sources must convert to entity format

### Memory Management

- Backend tables can grow to several GB
- PDF processing requires significant memory
- Incremental processing recommended for large datasets

## Validation Test Plan

### Base System Validation

1. __Data Processing Validation__
   - Verify table creation in /data/xllm6/
   - Check table structure and relationships

2. __Query Functionality Test__
   - Verify table loading
   - Confirm response generation

### Enterprise System Validation

1. __Repository Processing Test__
   - Verify backend table generation
   - Check table structure and content

2. __PDF Conversion Test__
   - Verify entity formation
   - Ensure backend processor compatibility

3. __User Interface Test__
   - Test interactive query functionality
   - Verify real-time fine-tuning effects

4. __Dev Mode Testing__
   - Verify relevancy scoring
   - Check performance metrics

## Enterprise Module Integration

The enterprise module extends the base XLLM system with specialized corporate knowledge processing capabilities:

- Modular design for flexible deployment
- Clear separation of processing, storage, and retrieval
- Specialized handling of technical documentation
- Multimodal content integration
- Real-time fine-tuning for improved results

By running the recommended validation tests, users can verify the functionality described in the documentation and ensure correct integration between system components.
