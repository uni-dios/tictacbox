#!/usr/bin/env python3
"""
LogiQube - Main Entry Point
4x4x4 Strategic Tic-Tac-Toe Game

Usage:
    python main.py
"""

import sys
from src.game import Game, MainMenu


def main():
    """Main entry point for LogiQube."""
    try:
        # Show main menu
        menu = MainMenu()
        selected_mode = menu.run()

        if selected_mode is None:
            # User quit from menu
            sys.exit(0)

        # Start game with selected mode
        game = Game()
        game.mode = selected_mode
        game.run()

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
