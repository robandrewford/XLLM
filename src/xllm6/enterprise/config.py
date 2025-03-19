"""Configuration settings for XLLM Enterprise Module.

This module provides standard configuration parameters for the enterprise
backend and frontend processors, ensuring consistent settings across
different components.
"""

import os
from pathlib import Path

# Define data paths
DATA_DIR = Path(os.environ.get("XLLM_DATA_DIR", "data/enterprise"))
DEFAULT_REPOSITORY_PATH = DATA_DIR / "repository.txt"
DEFAULT_REPOSITORY2_PATH = DATA_DIR / "repository2.txt"
DEFAULT_REPOSITORY3_PATH = DATA_DIR / "repository3.txt"

# Define standard backend table names
TABLE_NAMES = (
    'dictionary',     # multitokens (key = multitoken)
    'hash_pairs',     # multitoken associations (key = pairs of multitokens)
    'ctokens',        # not adjacent pairs in hash_pairs (key = pairs of multitokens)
    'hash_context1',  # categories (key = multitoken)
    'hash_context2',  # tags (key = multitoken)
    'hash_context3',  # titles (key = multitoken)
    'hash_context4',  # descriptions (key = multitoken)
    'hash_context5',  # meta (key = multitoken)
    'hash_ID',        # text entity ID table (key = multitoken, value is list of IDs)
    'hash_agents',    # agents (key = multitoken)
    'full_content',   # full content (key = multitoken)
    'ID_to_content',  # full content attached to text entity ID (key = text entity ID)
    'ID_to_agents',   # map text entity ID to agents list (key = text entity ID)
    'ID_size',        # content size (key = text entity ID)
    'KW_map',         # for singularization, map kw to single-token dictionary entry
    'stopwords',      # stopword list
)

# Default stopwords
DEFAULT_STOPWORDS = (
    '', '-', 'in', 'the', 'and', 'to', 'of', 'a', 'this', 'for', 'is', 'with', 'from',
    'as', 'on', 'an', 'that', 'it', 'are', 'within', 'will', 'by', 'or', 'its', 'can',
    'your', 'be', 'about', 'used', 'our', 'their', 'you', 'into', 'using', 'these',
    'which', 'we', 'how', 'see', 'below', 'all', 'use', 'across', 'provide', 'provides',
    'aims', 'one', '&', 'ensuring', 'crucial', 'at', 'various', 'through', 'find', 'ensure',
    'more', 'another', 'but', 'should', 'considered', 'provided', 'must', 'whether',
    'located', 'where', 'begins', 'any', 'what', 'some', 'under', 'does', 'belong',
    'included', 'part', 'associated'
)

# Default agent mappings
DEFAULT_AGENT_MAP = {
    'template': 'Template',
    'policy': 'Policy',
    'governance': 'Governance',
    'documentation': 'Documentation',
    'best practice': 'Best Practices',
    'bestpractice': 'Best Practices',
    'standard': 'Standards',
    'naming': 'Naming',
    'glossary': 'Glossary',
    'historical data': 'Data',
    'overview': 'Overview',
    'training': 'Training',
}

def get_backend_params():
    """Get default backend parameters.

    Returns:
        dict: Backend processing parameters
    """
    return {
        'max_multitoken': 4,  # max. consecutive terms per multi-token for inclusion in dictionary
        'maxDist': 3,         # max. position delta between 2 multitokens to link them in hash_pairs
        'maxTerms': 3,        # maxTerms must be <= max_multitoken
        'extraWeights':       # default weight is 1
        {
            'description': 0.0,
            'category': 0.3,
            'tag_list': 0.4,
            'title': 0.2,
            'meta': 0.1
        }
    }

def get_frontend_params():
    """Get default frontend parameters.

    Returns:
        dict: Frontend processing parameters
    """
    return {
        'show': ('dict', 'pairs', 'category', 'tags', 'titles', 'ID', 'whole'),
        'maxTokenCount': 100,
        'maxOutputLines': 50,
        'relevancyMode': True,
        'minRelScore': 0.5,
        'maxRelScore': 3.0,
        'fineTuneMode': True,
        'wordMaxDist': 2,
        'ContextMultitokenMinSize': 1,
        'minOutputListSize': 1,
        'minTokenLen': 2,
        'maxTokenCount': 80,
        'minPrintSize': 2,
        'maxNeighb': 20,
        'maxPairs': 200
    }

def get_tables_dict():
    """Initialize an empty backend tables dictionary.

    Returns:
        dict: Empty backend tables structure
    """
    tables = {}
    for name in TABLE_NAMES:
        tables[name] = {}
    tables['stopwords'] = DEFAULT_STOPWORDS
    return tables 