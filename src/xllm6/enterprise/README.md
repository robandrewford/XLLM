# XLLM Enterprise Module

This module provides corporate knowledge base functionality built on the XLLM framework. It includes tools for processing corporate document corpora, creating backend knowledge tables, and implementing real-time fine-tuning for enterprise question answering.

## Overview

The XLLM Enterprise module is an advanced implementation of XLLM technology specifically designed for corporate knowledge bases. Unlike the general-purpose XLLM6 module, it's optimized for organizational knowledge extraction, including specialized handling of technical documentation and multimodal content integration.

## Module Structure

The module is organized into several components:

### Core Components

- `config.py` - Configuration settings and parameters
- `utils.py` - Shared utility functions
- `backend.py` - Backend table generation
- `processor.py` - Query processing and result generation
- `pdf_processor.py` - Specialized PDF document processing

### User Interfaces

- `user.py` - Interactive prompt-based interface for end users
- `dev.py` - Testing and evaluation tool for developers

## Usage

### End User Interface

To use the interactive query interface:

```shell
python -m src.xllm6.enterprise.user
```

Options:

- `--generate` - Generate new backend tables instead of loading from disk
- `--repo=PATH` - Path to primary repository file
- `--repo2=PATH` - Path to secondary repository file
- `--repo3=PATH` - Path to combined repository file

### Developer Testing

To test the system with sample prompts:

```shell
python -m src.xllm6.enterprise.dev
```

Options:

- `--generate` - Generate new backend tables instead of loading from disk
- `--repo=PATH` - Path to primary repository file
- `--repo2=PATH` - Path to secondary repository file
- `--repo3=PATH` - Path to combined repository file
- `--prompts=PATH` - Path to prompt file (default: enterprise_sample_prompts.txt)
- `--output=PATH` - Path to output file (default: xllm-enterprise-test-results.txt)

### PDF Processing

To process a PDF document and convert it to repository format:

```shell
python -m src.xllm6.enterprise.pdf_processor path/to/document.pdf
```

Options:

- `--output`, `-o` - Output path for the generated entities

## Documentation

For detailed documentation, refer to:

- [XLLM Enterprise Documentation](https://github.com/VincentGranville/Large-Language-Models/blob/main/xllm6/enterprise/xllm-enterprise.pdf)
- [LLM Scores Documentation](https://github.com/VincentGranville/Large-Language-Models/blob/main/xllm6/enterprise/LLM-scores.pdf)

The complete documentation is available in the book "Building Disruptive AI & LLM Apps from Scratch", available on [MLtechniques.com e-store](https://mltechniques.com/shop/).

## Repository Files

The module uses three types of repository files:

1. `repository.txt` - Primary repository file
2. `repository2.txt` - Secondary repository file
3. `repository3.txt` - Combined repository file (concatenation of 1 and 2)

All input data comes from an anonymized corporate corpus, dealing with a sub-LLM.

## Backend Tables

The module generates and uses the following backend tables:

- `backend_dictionary.txt` - Core dictionary of tokens with frequency counts
- `backend_hash_pairs.txt` - Associations between tokens
- `backend_hash_context*.txt` - Contextual information tables
- `backend_ID_*.txt` - Entity ID mapping tables
- `backend_embeddings.txt` - Semantic embeddings for tokens and entities

## Notes

- The user interface calls the real-time fine-tuning function, allowing for prompt-by-prompt interaction.
- The developer interface loads test prompts from a file for batch testing and evaluation.
