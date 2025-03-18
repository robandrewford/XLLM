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
