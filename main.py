#!/usr/bin/env python3
"""
Todo Console Application - CLI Entry Point

This is the CLI entry point for the in-memory todo console application.
For the web API version, see server.py
"""

import sys
import os

# Check if running in web context (if server.py exists and we're not running CLI-specific commands)
if __name__ == "__main__":
    # Only run CLI when explicitly called
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    from cli.cli_interface import TodoCLI


    def main():
        """Main function to run the Todo CLI application."""
        try:
            # Check for --no-color flag
            use_color = True
            if '--no-color' in sys.argv or '-nc' in sys.argv:
                use_color = False

            print("Welcome to the Todo CLI Application!")
            cli = TodoCLI(use_color=use_color)
            cli.run()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user. Exiting...")
            sys.exit(130)  # Standard exit code for SIGINT
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)  # Standard exit code for general errors


    main()