"""Query processing for XLLM Enterprise.

This module handles query processing and result generation
for the XLLM Enterprise system.
"""

import logging
from collections import defaultdict

from src.xllm6.enterprise.config import get_frontend_params
from src.xllm6.enterprise.utils import update_hash, update_nested_hash, get_value

# Set up logging
logger = logging.getLogger(__name__)

def custom_pmi(word, token, backend_tables):
    """Calculate custom PMI (Pointwise Mutual Information) between word and token.
    
    Args:
        word (str): Word to calculate PMI for
        token (str): Token to calculate PMI with
        backend_tables (dict): Backend tables
        
    Returns:
        float: PMI value
    """
    dictionary = backend_tables['dictionary']
    
    if word not in dictionary or token not in dictionary:
        return 0.0
        
    corpus_size = sum(dictionary.values())
    word_count = dictionary[word]
    token_count = dictionary[token]
    
    # If either word is too rare, return 0
    if word_count < 2 or token_count < 2:
        return 0.0
        
    # Check co-occurrence
    pair = (word, token)
    rpair = (token, word)
    hash_pairs = backend_tables['hash_pairs']
    ctokens = backend_tables['ctokens']
    
    pair_count = hash_pairs.get(pair, 0) + hash_pairs.get(rpair, 0)
    pair_count += ctokens.get(pair, 0) + ctokens.get(rpair, 0)
    
    if pair_count == 0:
        return 0.0
        
    # Calculate PMI
    expected = (word_count * token_count) / corpus_size
    pmi = pair_count / expected
    
    return pmi


def distill_frontend_tables(q_dictionary, q_embeddings, frontend_params):
    """Purge frontend tables (q_dictionary and q_embeddings).
    
    Args:
        q_dictionary (dict): Query dictionary
        q_embeddings (dict): Query embeddings
        frontend_params (dict): Frontend parameters
        
    Returns:
        tuple: Purged q_dictionary and q_embeddings
    """
    max_token_count = frontend_params['maxTokenCount']
    
    # First purge q_dictionary
    local_hash = {}
    
    for key in q_dictionary:
        # Remove entries with too many tokens
        if q_dictionary[key] > max_token_count:
            local_hash[key] = 1
            
    # Remove redundant entries
    for keyA in q_dictionary:
        for keyB in q_dictionary:
            nA = q_dictionary[keyA]
            nB = q_dictionary[keyB]
            if keyA != keyB:
                if (keyA in keyB and nA == nB) or (keyA in keyB.split('~')):
                    local_hash[keyA] = 1
                    
    # Apply purge to q_dictionary
    for key in list(local_hash.keys()):
        if key in q_dictionary:
            del q_dictionary[key]
    
    # Then purge q_embeddings
    local_hash = {}
    
    for key in q_embeddings:
        if key[0] not in q_dictionary:
            local_hash[key] = 1
            
    # Apply purge to q_embeddings
    for key in list(local_hash.keys()):
        if key in q_embeddings:
            del q_embeddings[key]
    
    return q_dictionary, q_embeddings


def update_params(option, saved_query, sample_queries, frontend_params, backend_tables):
    """Update frontend parameters based on user options.
    
    Args:
        option (str): User option
        saved_query (str): Saved query
        sample_queries (list): Sample queries
        frontend_params (dict): Frontend parameters
        backend_tables (dict): Backend tables
        
    Returns:
        tuple: Updated frontend_params, query, and message
    """
    show = frontend_params['show']
    message = ""
    query = ""
    
    if option == "":
        message = (
            "No command entered. Available commands (enter number):\n"
            "1 Show dictionary entries\n"
            "2 Show word pairs\n"
            "3 Show categories\n"
            "4 Show tags\n"
            "5 Show titles\n"
            "6 Show ID entries\n"
            "7 Show whole content\n"
            "8 Show all (dictionary, pairs, categories, tags, titles, ID, whole)\n"
            "9 Clear display\n"
        )
    elif option.startswith("/show "):
        parts = option.split()
        if len(parts) > 1:
            section = parts[1].lower()
            if section == "dict":
                show = ('dict',)
                message = "Showing dictionary entries"
            elif section == "pairs":
                show = ('pairs',)
                message = "Showing word pairs"
            elif section == "category":
                show = ('category',)
                message = "Showing categories"
            elif section == "tags":
                show = ('tags',)
                message = "Showing tags"
            elif section == "titles":
                show = ('titles',)
                message = "Showing titles"
            elif section == "id":
                show = ('ID',)
                message = "Showing ID entries"
            elif section == "whole":
                show = ('whole',)
                message = "Showing whole content"
            elif section == "all":
                show = ('dict', 'pairs', 'category', 'tags', 'titles', 'ID', 'whole')
                message = "Showing all sections"
            else:
                message = f"Unknown section: {section}"
    elif option.startswith("/sample"):
        parts = option.split()
        if len(parts) > 1:
            try:
                index = int(parts[1])
                if 1 <= index <= len(sample_queries):
                    query = sample_queries[index-1]
                    message = f"Loaded sample query: {query}"
                else:
                    message = f"Sample index out of range: {index}"
            except ValueError:
                message = f"Invalid sample index: {parts[1]}"
    elif option.startswith("/q"):
        parts = option.split()
        if len(parts) > 1:
            try:
                index = int(parts[1])
                if 1 <= index <= len(saved_query):
                    query = saved_query[index-1]
                    message = f"Loaded saved query: {query}"
                else:
                    message = f"Query index out of range: {index}"
            except ValueError:
                message = f"Invalid query index: {parts[1]}"
    elif option == "1":
        show = ('dict',)
        message = "Showing dictionary entries"
    elif option == "2":
        show = ('pairs',)
        message = "Showing word pairs"
    elif option == "3":
        show = ('category',)
        message = "Showing categories"
    elif option == "4":
        show = ('tags',)
        message = "Showing tags"
    elif option == "5":
        show = ('titles',)
        message = "Showing titles"
    elif option == "6":
        show = ('ID',)
        message = "Showing ID entries"
    elif option == "7":
        show = ('whole',)
        message = "Showing whole content"
    elif option == "8":
        show = ('dict', 'pairs', 'category', 'tags', 'titles', 'ID', 'whole')
        message = "Showing all sections"
    elif option == "9":
        frontend_params['maxOutputLines'] = 0
        message = "Display cleared"
    elif option.startswith("/mode"):
        parts = option.split()
        if len(parts) > 1:
            mode = parts[1].lower()
            if mode == "relevancy":
                frontend_params['relevancyMode'] = True
                message = "Relevancy mode enabled"
            elif mode == "normal":
                frontend_params['relevancyMode'] = False
                message = "Normal mode enabled"
            else:
                message = f"Unknown mode: {mode}"
    elif option.startswith("/tune"):
        parts = option.split()
        if len(parts) > 1:
            mode = parts[1].lower()
            if mode == "on":
                frontend_params['fineTuneMode'] = True
                message = "Fine-tuning enabled"
            elif mode == "off":
                frontend_params['fineTuneMode'] = False
                message = "Fine-tuning disabled"
            else:
                message = f"Unknown tune mode: {mode}"
    elif option.startswith("/limit"):
        parts = option.split()
        if len(parts) > 1:
            try:
                limit = int(parts[1])
                frontend_params['maxOutputLines'] = limit
                message = f"Output limit set to {limit} lines"
            except ValueError:
                message = f"Invalid limit: {parts[1]}"
    elif option.startswith("/min"):
        parts = option.split()
        if len(parts) > 1:
            try:
                min_size = int(parts[1])
                frontend_params['minOutputListSize'] = min_size
                message = f"Minimum output list size set to {min_size}"
            except ValueError:
                message = f"Invalid minimum size: {parts[1]}"
    else:
        # Assume it's a query
        query = option
    
    frontend_params['show'] = show
    return frontend_params, query, message


def process_query(query, backend_tables, frontend_params=None):
    """Process a query and generate results.
    
    Args:
        query (str): Query to process
        backend_tables (dict): Backend tables
        frontend_params (dict, optional): Frontend parameters. Defaults to None.
        
    Returns:
        tuple: Results as a string and updated frontend parameters
    """
    if frontend_params is None:
        frontend_params = get_frontend_params()
    
    # Check for command options
    if query.startswith('/'):
        saved_query = []  # Add your saved queries here
        sample_queries = []  # Add your sample queries here
        frontend_params, new_query, message = update_params(
            query, saved_query, sample_queries, frontend_params, backend_tables
        )
        
        # If it was just a command, return the message
        if not new_query:
            return message, frontend_params
            
        # Otherwise, use the new query
        query = new_query
    
    # Process query
    try:
        # Clean query
        query = query.lower().strip()
        
        # Generate query dictionary and embeddings
        q_dictionary = {}
        q_embeddings = {}
        
        # Split query into tokens
        tokens = query.split()
        
        # Check against dictionary
        dictionary = backend_tables['dictionary']
        for token in tokens:
            if token in dictionary:
                q_dictionary[token] = dictionary[token]
        
        # Check for multi-tokens in query
        for i in range(len(tokens) - 1):
            for j in range(2, min(frontend_params['maxTokenCount'], len(tokens) - i + 1)):
                multitoken = "~".join(tokens[i:i+j])
                if multitoken in dictionary:
                    q_dictionary[multitoken] = dictionary[multitoken]
        
        # Calculate embeddings for query tokens
        for word in q_dictionary:
            for token in dictionary:
                pmi = custom_pmi(word, token, backend_tables)
                if pmi > 0:
                    q_embeddings[(word, token)] = pmi
        
        # Apply fine-tuning if enabled
        if frontend_params['fineTuneMode']:
            # Real-time fine-tuning would go here
            # For now, we'll just purge the frontend tables
            q_dictionary, q_embeddings = distill_frontend_tables(
                q_dictionary, q_embeddings, frontend_params
            )
        
        # Generate results
        results = generate_results(q_dictionary, q_embeddings, backend_tables, frontend_params)
        
        return results, frontend_params
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"Error processing query: {str(e)}", frontend_params


def generate_results(q_dictionary, q_embeddings, backend_tables, frontend_params):
    """Generate results from processed query.
    
    Args:
        q_dictionary (dict): Query dictionary
        q_embeddings (dict): Query embeddings
        backend_tables (dict): Backend tables
        frontend_params (dict): Frontend parameters
        
    Returns:
        str: Generated results
    """
    results = []
    dictionary = backend_tables['dictionary']
    ID_to_agents = backend_tables['ID_to_agents']
    ID_size = backend_tables['ID_size']
    
    # Track sections to display
    show = frontend_params['show']
    
    # Track relevancy mode
    relevancy_mode = frontend_params['relevancyMode']
    
    # Map section labels to backend tables
    section_labels = {
        'dict': 'dictionary',
        'pairs': 'hash_pairs',
        'category': 'hash_context1',
        'tags': 'hash_context2',
        'titles': 'hash_context3',
        'descr.': 'hash_context4',
        'meta': 'hash_context5',
        'ID': 'hash_ID',
        'whole': 'full_content'
    }
    
    # Loop through sections to display
    for label in show:
        # Skip if label not in section_labels
        if label not in section_labels:
            continue
            
        table_name = section_labels[label]
        table = backend_tables[table_name]
        
        # Add section header
        results.append(f">>> RESULTS - SECTION: {label}\n")
        
        # Initialize local hash
        local_hash = {}
        
        # Initialize words to ignore
        ignore = set()
        
        # Skip to next section if dictionary is empty
        if not q_dictionary:
            results.append("(No matching words in query)\n")
            continue
        
        # Process each word in query dictionary
        for word in q_dictionary:
            # Skip words with too few tokens
            ntk3 = len(word.split('~'))
            if word in ignore or ntk3 < frontend_params['ContextMultitokenMinSize']:
                continue
                
            # Skip words not in table
            if word not in table:
                continue
                
            # Get content from table
            content = table[word]
            count = dictionary.get(word, 0)
            
            # Update local hash with content
            for item in content:
                local_hash = update_nested_hash(local_hash, item, word, count)
        
        # Display results from local hash
        for item in local_hash:
            hash2 = local_hash[item]
            
            # Skip if too few entries
            if len(hash2) < frontend_params['minOutputListSize']:
                continue
                
            # Add item header
            results.append(f"   {label}: {item} [{len(hash2)} entries]")
            
            # Add linked items
            for key in hash2:
                results.append(f"   Linked to: {key} ({hash2[key]})")
                
                # Add agent information for ID entries
                if label == 'ID' and item in ID_to_agents:
                    # Get agent list
                    local_agent_hash = ID_to_agents[item]
                    local_ID_list = tuple(local_agent_hash.keys())
                    
                    # Add agent information
                    results.append(f"   Agents: {local_ID_list}")
                    
                    # Build agent-word-ID mapping
                    agent_and_word_to_IDs = {}
                    for agent in local_ID_list:
                        key3 = (agent, key)  # key is a multitoken
                        agent_and_word_to_IDs = update_nested_hash(agent_and_word_to_IDs, key3, item)
            
            # Add blank line after item
            results.append("")
        
        # Add blank line after section
        results.append("")
    
    # Add summary information
    results.append("Above results based on words found in prompt, matched back to backend tables.")
    results.append("Numbers in parentheses are occurrences of word in corpus.\n")
    
    # Add agent-word-ID mapping section if available
    if 'ID' in show and 'ID_to_agents' in backend_tables:
        agent_and_word_to_IDs = {}
        
        # Build agent-word-ID mapping
        for word in q_dictionary:
            if word in backend_tables['hash_ID']:
                for entity_id in backend_tables['hash_ID'][word]:
                    if entity_id in ID_to_agents:
                        for agent in ID_to_agents[entity_id]:
                            key = (agent, word)
                            agent_and_word_to_IDs = update_nested_hash(agent_and_word_to_IDs, key, entity_id)
        
        # Add section header
        results.append("--------------------------------------------------------------------")
        results.append(">>> RESULTS - SECTION: (Agent, Multitoken) --> (ID list)")
        results.append("    empty unless labels 'ID' and 'Agents' are in 'show'.\n")
        
        # Track ID sizes
        hash_size = {}
        
        # Display agent-word-ID mapping
        for key in sorted(agent_and_word_to_IDs.keys()):
            ID_list = tuple(agent_and_word_to_IDs[key].keys())
            results.append(f"{key} --> {ID_list}")
            
            # Track ID sizes
            for entity_id in ID_list:
                if entity_id in ID_size:
                    hash_size[entity_id] = ID_size[entity_id]
        
        # Add ID sizes
        results.append("\n  ID  Size\n")
        for entity_id in hash_size:
            results.append(f"{entity_id:4d} {hash_size[entity_id]:5d}")
    
    # Join results and limit output
    max_lines = frontend_params['maxOutputLines']
    result_text = "\n".join(results)
    
    if max_lines > 0:
        result_lines = result_text.split("\n")
        if len(result_lines) > max_lines:
            result_text = "\n".join(result_lines[:max_lines])
            result_text += f"\n\n... (output truncated to {max_lines} lines) ..."
    
    return result_text 