"""Utility functions for XLLM Enterprise Module.

This module contains standardized utility functions used by both
backend table generation and frontend query processing components.
"""

import os
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_hash(hash_dict, key, count=1):
    """Update a hash dictionary with a new key or increment existing key.

    Args:
        hash_dict (dict): Dictionary to update
        key: Key to update
        count (int, optional): Value to increment by. Defaults to 1.

    Returns:
        dict: Updated dictionary
    """
    if key in hash_dict:
        hash_dict[key] += count
    else:
        hash_dict[key] = count
    return hash_dict


def update_nested_hash(hash_dict, key, value, count=1):
    """Update a nested hash dictionary with a new key-value pair.
    
    Args:
        hash_dict (dict): Dictionary to update
        key: Primary key
        value: Value or tuple of values to add/update for the key
        count (int, optional): Value to increment by. Defaults to 1.
        
    Returns:
        dict: Updated dictionary
    """
    if key in hash_dict:
        local_hash = hash_dict[key]
    else:
        local_hash = {}
        
    if not isinstance(value, tuple):
        value = (value,)
        
    for item in value:
        if item in local_hash:
            local_hash[item] += count
        else:
            local_hash[item] = count
            
    hash_dict[key] = local_hash
    return hash_dict


def get_value(key, hash_dict, default=''):
    """Safely get a value from a dictionary.
    
    Args:
        key: Key to look up
        hash_dict (dict): Dictionary to look in
        default: Default value if key not found. Defaults to ''.
        
    Returns:
        Value associated with key or default value
    """
    return hash_dict.get(key, default)


def clean_list(value):
    """Convert a string representation of a list to a tuple.
    
    Args:
        value (str): String representation of a list (e.g., "['a', 'b', ...]")
        
    Returns:
        tuple: Cleaned tuple of values
    """
    value = value.replace("[", "").replace("]", "")
    aux = value.split("~")
    value_list = ()
    
    for val in aux:
        val = val.replace("'", "").replace('"', "").lstrip()
        if val != '':
            value_list = (*value_list, val)
            
    return value_list


def get_key_value_pairs(entity):
    """Extract key-value pairs from an entity string.
    
    Args:
        entity (list): Entity split by "{" delimiter
        
    Returns:
        dict: Dictionary of key-value pairs extracted from the entity
    """
    hash_crawl = {}
    
    if len(entity) < 2:
        return hash_crawl
        
    item = entity[1]
    if item == "":
        return hash_crawl
        
    pairs = item.split("||")
    for pair in pairs:
        if "::" in pair:
            key_value = pair.split("::")
            if len(key_value) > 1:
                key = key_value[0]
                value = key_value[1]
                hash_crawl[key] = value
                
    return hash_crawl


def save_table(table, filename, path=""):
    """Save a table to a file.
    
    Args:
        table (dict): Table to save
        filename (str): Name of the file to save to
        path (str, optional): Path to save the file to. Defaults to "".
    """
    filepath = Path(path) / filename if path else Path(filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(table, f)
        logger.info(f"Successfully saved table to {filepath}")
    except Exception as e:
        logger.error(f"Error saving table to {filepath}: {str(e)}")


def load_table(filename, path=""):
    """Load a table from a file.
    
    Args:
        filename (str): Name of the file to load from
        path (str, optional): Path to load the file from. Defaults to "".
        
    Returns:
        dict: Loaded table or empty dict if file not found
    """
    filepath = Path(path) / filename if path else Path(filename)
    
    try:
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                table = json.load(f)
            logger.info(f"Successfully loaded table from {filepath}")
            return table
        else:
            logger.warning(f"File {filepath} not found, returning empty table")
            return {}
    except Exception as e:
        logger.error(f"Error loading table from {filepath}: {str(e)}")
        return {}


def load_backend_tables(table_names, path=""):
    """Load all backend tables.
    
    Args:
        table_names (list): List of table names to load
        path (str, optional): Path to load tables from. Defaults to "".
        
    Returns:
        dict: Dictionary of loaded tables
    """
    tables = {}
    
    for name in table_names:
        filename = f"backend_{name}.txt"
        tables[name] = load_table(filename, path)
        
    return tables


def save_backend_tables(tables, path=""):
    """Save all backend tables.
    
    Args:
        tables (dict): Dictionary of tables to save
        path (str, optional): Path to save tables to. Defaults to "".
    """
    for name, table in tables.items():
        filename = f"backend_{name}.txt"
        save_table(table, filename, path)


def create_kw_map(dictionary):
    """Create a keyword mapping for singularization.
    
    Args:
        dictionary (dict): Dictionary to create map from
        
    Returns:
        dict: Keyword mapping
    """
    kw_map = {}
    
    for key in dictionary:
        if '~' not in key:
            tokens = key.split(' ')
            for token in tokens:
                if token not in kw_map and len(token) > 2:
                    kw_map[token] = key
    
    return kw_map 