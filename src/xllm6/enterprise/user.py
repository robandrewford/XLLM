"""User interface for XLLM Enterprise.

This module provides an interactive prompt-based interface for the XLLM Enterprise system.
"""

import sys
import logging

from src.xllm6.enterprise.config import get_backend_params, get_frontend_params, get_tables_dict
from src.xllm6.enterprise.backend import generate_backend_tables, load_backend_tables_from_disk
from src.xllm6.enterprise.processor import process_query

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function for the XLLM Enterprise user interface."""
    try:
        # Check for file paths as command line arguments
        repository_path = None
        repository_path2 = None
        repository_path3 = None
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
        
        # Get frontend parameters
        frontend_params = get_frontend_params()
        
        # Print welcome message
        print("\nXLLM Enterprise Interactive Query System")
        print("----------------------------------------")
        print("Enter a query or command, or type 'exit' to quit.")
        print("Type '/help' for a list of commands.")
        
        # Main interaction loop
        while True:
            # Get user input
            query = input("\nQuery> ").strip()
            
            # Check for exit command
            if query.lower() in ('exit', 'quit'):
                break
                
            # Check for help command
            if query.lower() == '/help':
                print("\nAvailable commands:")
                print("  /show <section>   - Show results for a specific section")
                print("                       (dict, pairs, category, tags, titles, id, whole, all)")
                print("  /mode <mode>      - Set mode (relevancy, normal)")
                print("  /tune <on|off>    - Enable or disable fine-tuning")
                print("  /limit <n>        - Set maximum output lines")
                print("  /min <n>          - Set minimum output list size")
                print("  1-9               - Shortcut for display options")
                print("  exit, quit        - Exit the program")
                continue
                
            # Process query
            if query:
                results, frontend_params = process_query(query, backend_tables, frontend_params)
                print("\n" + results)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        print(f"Error: {str(e)}")
        
    print("\nThank you for using XLLM Enterprise!")

if __name__ == "__main__":
    main() 