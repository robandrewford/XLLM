"""Developer testing tool for XLLM Enterprise.

This module provides testing functionality for the XLLM Enterprise system,
allowing developers to evaluate the system's performance against a set of
sample prompts with known answers.
"""

import sys
import logging
import time
from pathlib import Path

from src.xllm6.enterprise.config import get_backend_params, get_frontend_params, get_tables_dict
from src.xllm6.enterprise.backend import generate_backend_tables, load_backend_tables_from_disk
from src.xllm6.enterprise.processor import process_query

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_test_prompts(file_path):
    """Load test prompts from a file.
    
    Args:
        file_path (str): Path to the file containing test prompts
        
    Returns:
        list: List of (prompt, expected_answer) tuples
    """
    prompts = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ' | ' in line:
                    parts = line.split(' | ', 1)
                    prompt = parts[0].strip()
                    expected = parts[1].strip() if len(parts) > 1 else ""
                    prompts.append((prompt, expected))
        
        logger.info(f"Loaded {len(prompts)} test prompts from {file_path}")
    except Exception as e:
        logger.error(f"Error loading test prompts: {str(e)}")
        
    return prompts


def calculate_relevancy_score(result, expected_answer):
    """Calculate relevancy score between result and expected answer.
    
    Args:
        result (str): Generated result
        expected_answer (str): Expected answer
        
    Returns:
        float: Relevancy score (0.0 to 1.0)
    """
    # Simple implementation - could be enhanced with more sophisticated matching
    if not expected_answer:
        return 0.0
        
    # Convert to lowercase and tokenize
    result_tokens = set(result.lower().split())
    expected_tokens = set(expected_answer.lower().split())
    
    # Calculate token overlap
    if not expected_tokens:
        return 0.0
        
    intersection = result_tokens.intersection(expected_tokens)
    score = len(intersection) / len(expected_tokens)
    
    return min(score, 1.0)


def run_tests(backend_tables, prompts, output_file=None):
    """Run tests against the prompt set.
    
    Args:
        backend_tables (dict): Backend tables
        prompts (list): List of (prompt, expected_answer) tuples
        output_file (str, optional): Path to output file. Defaults to None.
        
    Returns:
        dict: Test results statistics
    """
    # Get frontend parameters with relevancy mode enabled
    frontend_params = get_frontend_params()
    frontend_params['relevancyMode'] = True
    frontend_params['fineTuneMode'] = False  # Disable fine-tuning for testing
    
    results = []
    scores = []
    total_time = 0
    
    # Open output file if specified
    out_file = None
    if output_file:
        try:
            out_file = open(output_file, 'w', encoding='utf-8')
            out_file.write("XLLM Enterprise Testing Results\n")
            out_file.write("==============================\n\n")
        except Exception as e:
            logger.error(f"Error opening output file: {str(e)}")
            output_file = None
    
    # Process each prompt
    for i, (prompt, expected) in enumerate(prompts):
        try:
            # Record start time
            start_time = time.time()
            
            # Process query
            result, _ = process_query(prompt, backend_tables, frontend_params.copy())
            
            # Record end time
            end_time = time.time()
            processing_time = end_time - start_time
            total_time += processing_time
            
            # Calculate relevancy score
            score = calculate_relevancy_score(result, expected)
            scores.append(score)
            
            # Add result to list
            results.append({
                'prompt': prompt,
                'expected': expected,
                'result': result,
                'score': score,
                'time': processing_time
            })
            
            # Write to output file
            if out_file:
                out_file.write(f"Test {i+1}: {prompt}\n")
                out_file.write(f"Expected: {expected}\n")
                out_file.write(f"Relevancy Score: {score:.2f}\n")
                out_file.write(f"Processing Time: {processing_time:.2f}s\n")
                out_file.write(f"Result:\n{result}\n\n")
                out_file.write("-" * 80 + "\n\n")
                
            # Print progress
            logger.info(f"Processed prompt {i+1}/{len(prompts)} - Score: {score:.2f}")
            
        except Exception as e:
            logger.error(f"Error processing prompt {i+1}: {str(e)}")
            if out_file:
                out_file.write(f"Test {i+1}: {prompt}\n")
                out_file.write(f"ERROR: {str(e)}\n\n")
                out_file.write("-" * 80 + "\n\n")
    
    # Close output file
    if out_file:
        avg_score = sum(scores) / len(scores) if scores else 0
        avg_time = total_time / len(prompts) if prompts else 0
        
        out_file.write("\nSummary Statistics\n")
        out_file.write("=================\n")
        out_file.write(f"Total Prompts: {len(prompts)}\n")
        out_file.write(f"Average Relevancy Score: {avg_score:.2f}\n")
        out_file.write(f"Average Processing Time: {avg_time:.2f}s\n")
        out_file.write(f"Total Processing Time: {total_time:.2f}s\n")
        
        out_file.close()
    
    # Return statistics
    return {
        'total_prompts': len(prompts),
        'avg_score': sum(scores) / len(scores) if scores else 0,
        'avg_time': total_time / len(prompts) if prompts else 0,
        'total_time': total_time,
        'min_score': min(scores) if scores else 0,
        'max_score': max(scores) if scores else 0
    }


def main():
    """Main function for the XLLM Enterprise developer testing tool."""
    try:
        # Check for command line arguments
        repository_path = None
        repository_path2 = None
        repository_path3 = None
        prompt_file = "enterprise_sample_prompts.txt"
        output_file = "xllm-enterprise-test-results.txt"
        load_from_disk = True
        
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if arg == "--generate":
                    load_from_disk = False
                elif arg.startswith("--repo="):
                    repository_path = arg[7:]
                elif arg.startswith("--repo2="):
                    repository_path2 = arg[8:]
                elif arg.startswith("--repo3="):
                    repository_path3 = arg[8:]
                elif arg.startswith("--prompts="):
                    prompt_file = arg[10:]
                elif arg.startswith("--output="):
                    output_file = arg[9:]
        
        # Load or generate backend tables
        if load_from_disk:
            print("Loading backend tables from disk...")
            backend_tables = load_backend_tables_from_disk()
            if not backend_tables.get('dictionary'):
                print("Backend tables not found or empty. Generating new tables...")
                backend_params = get_backend_params()
                backend_tables = generate_backend_tables(
                    repository_path=repository_path,
                    repository_path2=repository_path2,
                    repository_path3=repository_path3,
                    backend_params=backend_params,
                    save_path=""
                )
        else:
            print("Generating backend tables...")
            backend_params = get_backend_params()
            backend_tables = generate_backend_tables(
                repository_path=repository_path,
                repository_path2=repository_path2,
                repository_path3=repository_path3,
                backend_params=backend_params,
                save_path=""
            )
        
        # Load test prompts
        print(f"Loading test prompts from {prompt_file}...")
        prompts = load_test_prompts(prompt_file)
        
        if not prompts:
            print("No test prompts found. Exiting.")
            return
            
        # Run tests
        print(f"Running {len(prompts)} tests...")
        stats = run_tests(backend_tables, prompts, output_file)
        
        # Print summary statistics
        print("\nTest Results Summary:")
        print(f"Total Prompts: {stats['total_prompts']}")
        print(f"Average Relevancy Score: {stats['avg_score']:.2f}")
        print(f"Minimum Score: {stats['min_score']:.2f}")
        print(f"Maximum Score: {stats['max_score']:.2f}")
        print(f"Average Processing Time: {stats['avg_time']:.2f}s")
        print(f"Total Processing Time: {stats['total_time']:.2f}s")
        print(f"Detailed results written to {output_file}")
            
    except KeyboardInterrupt:
        print("\nTesting interrupted...")
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        print(f"Error: {str(e)}")
        
    print("\nXLLM Enterprise testing complete.")

if __name__ == "__main__":
    main() 