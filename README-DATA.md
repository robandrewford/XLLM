# XLLM6 Data Structures Overview

## Roles and Responsibilities

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

## 1. Core Tables (in data/xllm6/)

### dictionary (xllm6_dictionary.txt)

- **Format**: Tab-separated key-value pairs (word\tcount)
- **Definition**: Core dictionary of words with their counts
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Primary lookup table for word existence and frequency

### arr_url (xllm6_arr_url.txt)

- **Format**: Line-based, tab-separated (ID\tURL)
- **Definition**: Maps URL IDs to actual URLs (one-to-one mapping)
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Reference for source URLs of words/concepts

### stopwords (stopwords.txt)

- **Format**: Comma-separated list
- **Definition**: Words not accepted in dictionary
- **Creation**: Both hardcoded in `xllm6.py` and loaded from file
- **Usage**: Filtering unwanted words during processing (xllm6.py) and query optimization (xllm6_short.py)

## 2. Hash Tables (in data/xllm6/)

### url_map (xllm6_url_map.txt)

- **Format**: Tab-separated hash structure
- **Definition**: URL IDs attached to words in dictionary
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Links words to their source URLs

### hash_category (xllm6_hash_category.txt)

- **Format**: Tab-separated hash structure
- **Definition**: Categories attached to words
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Categorization of terms

### hash_related (xllm6_hash_related.txt)

- **Format**: Tab-separated hash structure
- **Definition**: Related topics for each word
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Topic relationships

### hash_see (xllm6_hash_see.txt)

- **Format**: Tab-separated hash structure
- **Definition**: "See also" topics for each word
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Cross-references between topics

## 3. Word Relationship Tables

### word_pairs (not in xllm6_short.py)

- **Format**: Tab-separated pairs with counts
- **Definition**: Pairs of 1-token words found in same word, with count
- **Creation**: Created and used only by xllm6.py
- **Usage**: Single-token word co-occurrence tracking

### word2_pairs (not in xllm6_short.py)

- **Format**: Tab-separated pairs with counts
- **Definition**: Pairs of multi-token words found on same URL
- **Creation**: Created and used only by xllm6.py
- **Usage**: Multi-token word co-occurrence tracking

### compressed_word2_hash (xllm6_compressed_word2_hash.txt)

- **Format**: Tab-separated hash structure
- **Definition**: Optimized version of word2_hash
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Efficient word relationship lookup

### ngrams_table (not in xllm6_short.py)

- **Format**: Line-based list
- **Definition**: N-grams of words found during crawling
- **Creation**: Created and used only by xllm6.py
- **Usage**: N-gram pattern analysis

### compressed_ngrams_table (xllm6_compressed_ngrams_table.txt)

- **Format**: Line-based list
- **Definition**: Highest-count ngrams only
- **Creation**: Created by xllm6.py, used by both
- **Usage**: N-gram pattern analysis in query processing

## 4. Intermediate Data Structures

### word_hash (In-Memory Only)

- **Format**: In-memory dictionary
- **Definition**: Maps 1-token words to associated 1-token words
- **Creation**: Created and used only by xllm6.py
- **Usage**: Creates embeddings, temporary during processing

### word2_hash (In-Memory Only)

- **Format**: In-memory dictionary
- **Definition**: Maps multi-token words to associated multi-token words
- **Creation**: Created and used only by xllm6.py
- **Usage**: Creates compressed_word2_hash and embeddings2

### utf_map

- **Format**: Python dictionary (also saved as utf_map.txt)
- **Definition**: Character conversion mappings
- **Creation**: Hardcoded in both files
- **Usage**: Text normalization

## 5. Embedding Tables

### embeddings (xllm6_embeddings.txt)

- **Format**: Tab-separated hash with float weights
- **Definition**: Single-token word embeddings
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Word similarity and relationships

### embeddings2 (xllm6_embeddings2.txt)

- **Format**: Tab-separated hash with float weights
- **Definition**: Multi-token word embeddings
- **Creation**: Created by xllm6.py, used by both
- **Usage**: Complex term relationships

### pmi_table and pmi_table2 (Not in xllm6_short.py)

- **Format**: Tab-separated hash with weights
- **Definition**: PMI (Pointwise Mutual Information) calculations
- **Creation**: Created and used only by xllm6.py
- **Usage**: Intermediate step for creating embeddings

## 6. Results

### results (xllm6_results.txt)

- **Format**: Text output
- **Definition**: Query results output
- **Creation**: Generated by xllm6_short.py during query processing
- **Usage**: User-facing results display

## 7. Taxonomy Tables (in src/xllm6/build-taxonomy/)

### xllm6_smallDictionary.txt

- **Format**: Tab-separated key-value pairs (word\tcount)
- **Definition**: Streamlined dictionary containing only words relevant to taxonomy building
- **Creation**: Created by taxonomy.py during create_taxonomy_tables() execution
- **Usage**: Serves as the foundation for taxonomy connection analysis

### xllm6_topWords.txt

- **Format**: Line-based list of words with weights
- **Definition**: Most significant words identified for taxonomy organization
- **Creation**: Generated by first phase of taxonomy building in taxonomy.py
- **Usage**: Anchor points around which taxonomy connections are built

### xllm6_connectedTopWords.txt

- **Format**: Tab-separated relationship structure
- **Definition**: Maps relationships between high-importance taxonomy words
- **Creation**: Created during taxonomy relationship extraction phase
- **Usage**: Primary structure for taxonomy hierarchy generation

### xllm6_connectedByTopWord.txt

- **Format**: Hash-based connection mapping
- **Definition**: Words connected through taxonomy top words
- **Creation**: Derived from connectedTopWords through relationship expansion
- **Usage**: Expands taxonomy connections beyond direct relationships

### xllm6_wordGroups.txt

- **Format**: Line-based groups of related words
- **Definition**: Clusters of semantically related words
- **Creation**: Created through hierarchical clustering in taxonomy.py
- **Usage**: Forms the basis for category assignments

### xllm6_assignedCategories.txt

- **Format**: Tab-separated word-to-category mapping
- **Definition**: Final taxonomy category assignments for words
- **Creation**: Final phase of taxonomy building, may include manual adjustments
- **Usage**: Maps dictionary words to their taxonomy categories

### xllm6_missingConnections.txt

- **Format**: Line-based pairs of words
- **Definition**: Word pairs that should be connected but aren't automatically linked
- **Creation**: Generated through gap analysis in the taxonomy structure
- **Usage**: Identifies and fixes potential taxonomy connection gaps

## 8. Taxonomy Processing Tools

### reallocate.py

- **Format**: Python script
- **Definition**: Taxonomy validation and category reallocation tool
- **Creation**: Created as part of the taxonomy refinement process
- **Usage**: Compares and validates assigned categories with source categories

The reallocate.py script serves as a crucial validation component for the taxonomy system. It performs the following functions:

- Category Detection: Assigns categories to URLs based on the words they contain
- Weight Calculation: Computes category weights using either a "depth" or "relevancy" approach
- Comparison Analysis: Compares detected categories with original Wolfram categories
- Feedback Generation: Outputs validation data to detectedCategories.txt

This script helps improve the quality of the taxonomy by identifying misalignments between automatically assigned categories and source categories.

## Taxonomy System Overview

The XLLM taxonomy system creates a hierarchical organization of knowledge through multi-stage processing:

- Dictionary Filtering: Creating a focused dictionary of taxonomy-relevant terms
- Relationship Extraction: Identifying connections between terms based on co-occurrence and semantic relationships
- Category Assignment: Applying a hierarchical category structure to terms
- Validation and Refinement: Cross-checking assignments against source data and identifying gaps
- Integration: Making the taxonomy structure available for knowledge retrieval and organization

The taxonomy component enhances query processing by providing structured navigation paths through the knowledge base, enabling more precise and contextually relevant results.

## Process Flow

### 1. Developer Process (xllm6.py)

- **Input**: `crawl_final_stats.txt` (raw Wolfram crawl data)
- **Process**:
  - Process crawled data
  - Extract and build dictionaries
  - Create word relationships
  - Generate embeddings
- **Outputs**: All data tables stored in data/xllm6/ directory

### 2. End-User Process (xllm6_short.py)

- **Setup**:
  - Check for existing data tables
  - Download missing tables from GitHub if needed (using `_download_files()`)
  - Load tables using xllm6_util.py functions

- **Query Processing**:
  - **Input**: User query string
  - **Process**:
    - Clean and process query
    - Find matching words in dictionary
    - Look up related information
    - Format and display results
  - **Output**: `xllm6_results.txt`

---

The system is designed as a two-stage process:

1. Developers use `xllm6.py` to process raw crawled data once, creating persistent tables
2. End-users use `xllm6_short.py` to efficiently query the knowledge base without needing access to or processing of the raw data

## Behavior of xllm6.py with Existing Tables

Running xllm6.py will **overwrite** existing tables rather than creating tables with different names or merging data. This happens because:

1. The code initializes empty data structures in the `__init__` method
2. The `process_crawled_data` method populates these structures from scratch
3. There is no merge logic in the code to combine new data with existing data
4. The direct naming relationship between data structures and output files suggests a straightforward overwrite approach

If you need to preserve existing data while running xllm6.py, it's recommended to make backup copies of the table files before processing.

## 8. XLLM Enterprise Module

### Enterprise Process Flow

#### xllm-enterprise-v2.py (Core Implementation)

- Processes corporate document corpus data
- Creates backend tables for enterprise knowledge retrieval
- Implements real-time fine-tuning algorithms
- Handles entity extraction and relationship mapping
- Designed for organizational knowledge management

#### xllm_enterprise_util.py (Utility Library)

- Provides shared functions for enterprise modules
- Handles data cleaning and transformation
- Implements key-value extraction algorithms
- Manages frontend/backend table distillation
- Centralizes common code to reduce duplication

#### xllm-enterprise-v2-user.py (End-User Tool)

- Uses pre-created tables from the backend
- Provides interactive prompt-based interface
- Accepts keyboard input for real-time queries
- Implements real-time fine-tuning for query responses
- Designed for daily use by non-technical stakeholders

#### xllm-enterprise-v2-dev.py (Developer Tool)

- Loads test prompts from text files
- Tests system against known answer sets
- Generates performance metrics and relevancy scores
- Does not implement real-time fine-tuning
- Designed for system evaluation and improvement

### Core Backend Tables

#### ID_size (backend_ID_size.txt)

- **Format**: Simple key-value storage
- **Definition**: Maps entity IDs to their token counts
- **Creation**: Created by core processor during corpus ingestion
- **Usage**: Size tracking for entity management

#### ID_to_content (backend_ID_to_content.txt)

- **Format**: ID-indexed content mapping
- **Definition**: Links entity IDs to their full content
- **Creation**: Generated during initial corpus processing
- **Usage**: Content retrieval during query processing

#### hash_ID (backend_hash_ID.txt)

- **Format**: Hashed ID lookup structure
- **Definition**: Fast access hash map for entity IDs
- **Creation**: Built during backend table generation
- **Usage**: Efficient entity retrieval

#### ID_to_agents (backend_ID_to_agents.txt)

- **Format**: ID-to-agent mapping
- **Definition**: Links entities to their associated agents
- **Creation**: Created during agent classification
- **Usage**: Agent-based information retrieval

### Data Processing Components

#### dictionary (backend_dictionary.txt)

- **Format**: Token-count pairs
- **Definition**: Core vocabulary with frequency counts
- **Creation**: Created through corpus tokenization
- **Usage**: Fundamental lookup for token existence

#### embeddings (backend_embeddings.txt)

- **Format**: Vector representations
- **Definition**: Semantic embeddings for tokens and entities
- **Creation**: Generated through relationship extraction
- **Usage**: Semantic similarity calculations

#### hash_pairs (backend_hash_pairs.txt)

- **Format**: Token pair relationships
- **Definition**: Co-occurrence patterns between tokens
- **Creation**: Built through position analysis
- **Usage**: Relationship inference between concepts

#### KW_map (backend_KW_map.txt)

- **Format**: Keyword mapping structure
- **Definition**: Maps keywords to their semantic context
- **Creation**: Generated during keyword extraction
- **Usage**: Keyword-based query enhancement

### Enterprise Data Processing

#### 1. Corpus Ingestion

- **Input**: Repository text files (repository.txt, repository2.txt, repository3.txt)
- **Process**:
  - Parse entity documents
  - Extract key-value pairs
  - Generate multitoken structures
  - Build backend hash tables
- **Output**: Backend tables in text format

#### 2. Query Processing

- **Input**: User prompts (keyboard or file)
- **Process**:
  - Extract query intent
  - Match against backend structures
  - Apply real-time fine-tuning (user mode only)
  - Generate contextually relevant responses
- **Output**: Response text with relevancy metrics (dev mode)

### PDF Processing Components

#### PDF_Chunking_Nvidia.py

- **Format**: Python processor
- **Definition**: Specialized PDF parser for technical documents
- **Creation**: Purpose-built for multimodal PDF handling
- **Usage**: Converts PDF technical content to usable corpus data

The enterprise module serves as an advanced implementation of xLLM technology specifically designed for corporate knowledge bases. Unlike the general-purpose xllm6 module, it's optimized for organizational knowledge extraction, including specialized handling of technical documentation and multimodal content integration.
