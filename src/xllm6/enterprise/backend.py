"""Backend table generation for XLLM Enterprise.

This module handles the creation and management of backend tables
used by the XLLM Enterprise system for knowledge retrieval.
"""

import logging
import requests
from pathlib import Path
import json

from src.xllm6.enterprise.config import (
    TABLE_NAMES, DEFAULT_REPOSITORY_PATH, 
    DEFAULT_REPOSITORY2_PATH, DEFAULT_REPOSITORY3_PATH,
    DEFAULT_AGENT_MAP, get_tables_dict
)
from src.xllm6.enterprise.utils import (
    update_hash, update_nested_hash, get_value, clean_list,
    get_key_value_pairs, save_backend_tables, load_backend_tables,
    create_kw_map
)

# Set up logging
logger = logging.getLogger(__name__)

def update_dict(backend_tables, hash_crawl, backend_params):
    """Update dictionary and other tables with data from hash_crawl.
    
    Args:
        backend_tables (dict): Backend tables to update
        hash_crawl (dict): Data to update with
        backend_params (dict): Backend parameters
        
    Returns:
        dict: Updated backend tables
    """
    dictionary = backend_tables['dictionary']
    hash_pairs = backend_tables['hash_pairs']
    ctokens = backend_tables['ctokens']
    hash_context1 = backend_tables['hash_context1']
    hash_context2 = backend_tables['hash_context2']
    hash_context3 = backend_tables['hash_context3']
    hash_context4 = backend_tables['hash_context4']
    hash_context5 = backend_tables['hash_context5']
    hash_ID = backend_tables['hash_ID']
    hash_agents = backend_tables['hash_agents']
    full_content = backend_tables['full_content']
    ID_to_content = backend_tables['ID_to_content']
    ID_to_agents = backend_tables['ID_to_agents']
    ID_size = backend_tables['ID_size']
    stopwords = backend_tables['stopwords']
    
    data = ""
    for key in ('title', 'category', 'description', 'tag_list', 'meta'):
        value = get_value(key, hash_crawl)
        if value != '': 
            data += value + " "
    
    if data == "":
        return backend_tables
        
    data = data.lower()
    words = data.split()
    n_words = len(words)
    
    # Extract multi-tokens
    max_multitoken = backend_params['max_multitoken']
    stoplist = backend_tables['stopwords']
    
    for i in range(n_words):
        if i < n_words - 1:  # at least 2 tokens
            # Extract up to max_multitoken consecutive tokens
            for j in range(1, min(max_multitoken + 1, n_words - i + 1)):
                # Extract words[i:i+j]
                word = ""
                flag = True
                
                for k in range(j):
                    if len(words[i+k]) < 2 or words[i+k] in stoplist:
                        flag = False
                        break
                    # Add ~ between tokens in multitoken
                    if k > 0:
                        word += "~"
                    word += words[i+k]
                
                if flag and len(word) > 0:
                    update_tables(backend_tables, word, hash_crawl, backend_params)
                    dictionary = update_hash(dictionary, word)
    
    # Handle adjacent and non-adjacent word pairs
    maxDist = backend_params['maxDist']
    maxTerms = backend_params['maxTerms']
    
    # Create dictionary of extracted tokens
    tokens = []
    for word in dictionary:
        if word.count('~') < maxTerms:
            tokens.append(word)
    
    # Add pairs to hash_pairs (adjacent)
    # and ctokens (non-adjacent, within maxDist)
    for i in range(len(tokens)):
        for j in range(i+1, min(i+1+maxDist, len(tokens))):
            if i != j:
                if j == i+1:  # adjacent
                    key = (tokens[i], tokens[j])
                    hash_pairs = update_hash(hash_pairs, key)
                else:  # non-adjacent
                    key = (tokens[i], tokens[j])
                    ctokens = update_hash(ctokens, key)
    
    # Update backend tables
    backend_tables['dictionary'] = dictionary
    backend_tables['hash_pairs'] = hash_pairs
    backend_tables['ctokens'] = ctokens
    backend_tables['hash_context1'] = hash_context1
    backend_tables['hash_context2'] = hash_context2
    backend_tables['hash_context3'] = hash_context3
    backend_tables['hash_context4'] = hash_context4
    backend_tables['hash_context5'] = hash_context5
    backend_tables['hash_ID'] = hash_ID
    backend_tables['hash_agents'] = hash_agents
    backend_tables['full_content'] = full_content
    backend_tables['ID_to_content'] = ID_to_content
    backend_tables['ID_to_agents'] = ID_to_agents
    backend_tables['ID_size'] = ID_size
    
    return backend_tables


def update_tables(backend_tables, word, hash_crawl, backend_params):
    """Update all tables with a specific word.
    
    Args:
        backend_tables (dict): Backend tables to update
        word (str): Word to update with
        hash_crawl (dict): Data to update with
        backend_params (dict): Backend parameters
        
    Returns:
        None
    """
    category = get_value('category', hash_crawl)
    tag_list = get_value('tag_list', hash_crawl)
    title = get_value('title', hash_crawl)
    description = get_value('description', hash_crawl)
    meta = get_value('meta', hash_crawl)
    ID = get_value('ID', hash_crawl)
    agents = get_value('agents', hash_crawl)
    full_content = get_value('full_content', hash_crawl)
    
    # Extract weight from backend parameters
    extra_weights = backend_params['extraWeights']
    word = word.lower()  # add stemming
    weight = 1.0  
    flag = ''
    
    # Update context tables
    if word in category or category in word:   
        context1 = backend_tables['hash_context1'] 
        weight = extra_weights['category']
        flag = 'category'
        context1 = update_nested_hash(context1, category, word, weight)
        backend_tables['hash_context1'] = context1
        
    if word in tag_list or tag_list in word:   
        context2 = backend_tables['hash_context2']
        weight = extra_weights['tag_list']
        flag = 'tag_list'
        context2 = update_nested_hash(context2, tag_list, word, weight)
        backend_tables['hash_context2'] = context2
        
    if word in title or title in word:   
        context3 = backend_tables['hash_context3']
        weight = extra_weights['title'] 
        flag = 'title'
        context3 = update_nested_hash(context3, title, word, weight)
        backend_tables['hash_context3'] = context3
        
    if word in description or description in word:   
        context4 = backend_tables['hash_context4']
        weight = extra_weights['description']
        flag = 'description'
        context4 = update_nested_hash(context4, description, word, weight)
        backend_tables['hash_context4'] = context4
        
    if word in meta or meta in word:   
        context5 = backend_tables['hash_context5']
        weight = extra_weights['meta']
        flag = 'meta'
        context5 = update_nested_hash(context5, meta, word, weight)
        backend_tables['hash_context5'] = context5
        
    # Update ID and agents tables
    if flag != '':
        hash_ID = backend_tables['hash_ID']
        hash_ID = update_nested_hash(hash_ID, word, ID, weight)
        backend_tables['hash_ID'] = hash_ID
        
        if agents != '':
            hash_agents = backend_tables['hash_agents']
            hash_agents = update_nested_hash(hash_agents, word, agents, weight)
            backend_tables['hash_agents'] = hash_agents
            
            ID_to_agents = backend_tables['ID_to_agents']
            ID_to_agents = update_nested_hash(ID_to_agents, ID, agents, weight)
            backend_tables['ID_to_agents'] = ID_to_agents
            
    # Update full content
    if flag != '' and full_content != '':
        full_context = backend_tables['full_content']
        full_context = update_nested_hash(full_context, word, full_content, weight)
        backend_tables['full_content'] = full_context
        
        ID_to_content = backend_tables['ID_to_content']
        ID_to_content[ID] = full_content
        backend_tables['ID_to_content'] = ID_to_content


def process_entities(entities, backend_tables, backend_params, agent_map=None):
    """Process entities from repository data.
    
    Args:
        entities (list): Entities to process
        backend_tables (dict): Backend tables to update
        backend_params (dict): Backend parameters
        agent_map (dict, optional): Agent mapping. Defaults to None.
        
    Returns:
        dict: Updated backend tables
    """
    if agent_map is None:
        agent_map = DEFAULT_AGENT_MAP
        
    ID_size = backend_tables['ID_size']
    entity_list = ()
    
    for entity_raw in entities:
        entity = entity_raw.split("~~")
        agent_list = ()
        
        if len(entity) > 1 and entity[1] not in entity_list:
            try:
                entity_list = (*entity_list, entity[1])
                entity_ID = int(entity[0])
                entity = entity[1].split("{")
                hash_crawl = {}
                hash_crawl['ID'] = entity_ID
                ID_size[entity_ID] = len(entity[1])
                hash_crawl['full_content'] = entity_raw
                
                key_value_pairs = get_key_value_pairs(entity)
                
                for key in key_value_pairs:
                    hash_crawl[key] = key_value_pairs[key]
                    # Handle agent extraction
                    if key == 'category' or key == 'title':
                        value = key_value_pairs[key].lower()
                        # Look for agent matches
                        for term in agent_map:
                            if term in value:
                                agent = agent_map[term]
                                agent_list = (*agent_list, agent)
                                
                hash_crawl['agents'] = agent_list
                backend_tables = update_dict(backend_tables, hash_crawl, backend_params)
                
            except Exception as e:
                logger.error(f"Error processing entity: {str(e)}")
                continue
    
    backend_tables['ID_size'] = ID_size
    return backend_tables


def load_repository_data(repository_path=None, remote_url=None):
    """Load repository data from file or URL.
    
    Args:
        repository_path (str, optional): Path to repository file. Defaults to None.
        remote_url (str, optional): URL to remote repository. Defaults to None.
        
    Returns:
        str: Repository data
    """
    data = ""
    
    if remote_url:
        try:
            response = requests.get(remote_url)
            data = response.text
            logger.info(f"Successfully loaded repository data from {remote_url}")
        except Exception as e:
            logger.error(f"Error loading repository data from {remote_url}: {str(e)}")
    elif repository_path:
        try:
            with open(repository_path, "r", encoding="utf-8") as f:
                data = f.read()
            logger.info(f"Successfully loaded repository data from {repository_path}")
        except Exception as e:
            logger.error(f"Error loading repository data from {repository_path}: {str(e)}")
    
    return data


def generate_backend_tables(repository_path=None, repository_path2=None, repository_path3=None, 
                          remote_url=None, backend_params=None, save_path="", agent_map=None):
    """Generate backend tables from repository data.
    
    Args:
        repository_path (str, optional): Path to repository file. Defaults to None.
        repository_path2 (str, optional): Path to second repository file. Defaults to None.
        repository_path3 (str, optional): Path to third repository file. Defaults to None.
        remote_url (str, optional): URL to remote repository. Defaults to None.
        backend_params (dict, optional): Backend parameters. Defaults to None.
        save_path (str, optional): Path to save tables to. Defaults to "".
        agent_map (dict, optional): Agent mapping. Defaults to None.
        
    Returns:
        dict: Generated backend tables
    """
    if backend_params is None:
        from src.xllm6.enterprise.config import get_backend_params
        backend_params = get_backend_params()
        
    if agent_map is None:
        agent_map = DEFAULT_AGENT_MAP
        
    # Initialize backend tables
    backend_tables = get_tables_dict()
    
    # Load repository data
    if repository_path3:
        # Use pre-combined repository
        data = load_repository_data(repository_path3)
    elif repository_path and repository_path2:
        # Combine two repositories
        data1 = load_repository_data(repository_path)
        data2 = load_repository_data(repository_path2)
        data = data1 + "\n" + data2
    elif repository_path:
        # Use single repository
        data = load_repository_data(repository_path)
    elif remote_url:
        # Use remote repository
        data = load_repository_data(remote_url=remote_url)
    else:
        # Use default repository
        data = load_repository_data(DEFAULT_REPOSITORY_PATH)
        
    if not data:
        logger.error("No repository data loaded")
        return backend_tables
        
    # Process entities
    entities = data.split("\n")
    backend_tables = process_entities(entities, backend_tables, backend_params, agent_map)
    
    # Create keyword map for singularization
    backend_tables['KW_map'] = create_kw_map(backend_tables['dictionary'])
    
    # Save backend tables
    if save_path:
        save_backend_tables(backend_tables, save_path)
        
    return backend_tables


def load_backend_tables_from_disk(path=""):
    """Load backend tables from disk.
    
    Args:
        path (str, optional): Path to load tables from. Defaults to "".
        
    Returns:
        dict: Loaded backend tables
    """
    return load_backend_tables(TABLE_NAMES, path) 