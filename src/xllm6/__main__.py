"""Entry point for running the XLLM6 package directly."""

import argparse
import sys


def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description="XLLM6 - Large Language Model Framework")
    parser.add_argument(
        "--mode",
        choices=["dev", "user"],
        default="user",
        help="Run mode: 'dev' for developers, 'user' for end-users (default: user)",
    )
    args = parser.parse_args()

    if args.mode == "dev":
        # Import and run developer version
        from .xllm6 import main as dev_main

        dev_main()
    else:
        # Import and run end-user version
        from .xllm6_short import main as user_main

        user_main()


if __name__ == "__main__":
    sys.exit(main())
