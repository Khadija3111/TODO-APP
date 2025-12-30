#!/usr/bin/env python3
"""
Todo Console Application - Main Entry Point

This is the main entry point for the in-memory todo console application.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.cli_interface import TodoCLI


def main():
    """Main function to run the Todo application."""
    print("Welcome to the Todo Application!")
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()