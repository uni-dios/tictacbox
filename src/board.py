"""
LogiQube - Board Logic and Game State Management
"""

import numpy as np
from src.constants import BOARD_SIZE, EMPTY, PLAYER_X, PLAYER_O, STATE_PLAYING, STATE_WIN, STATE_DRAW
from src.winning_lines import WINNING_LINES, get_lines_containing_position


class Board:
    """
    Manages the game board state and logic for LogiQube (4x4x4 Tic-Tac-Toe).
    """

    def __init__(self):
        """Initialize an empty game board."""
        self.reset()

    def reset(self):
        """Reset the board to initial state."""
        # 3D array: board[z][y][x] where z=plane, y=row, x=column
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = PLAYER_X
        self.game_status = STATE_PLAYING
        self.winner = None
        self.winning_line = None
        self.move_history = []
        self.move_count = 0

    def is_valid_move(self, x, y, z):
        """
        Check if a move is valid.

        Args:
            x, y, z: Coordinates of the position

        Returns:
            bool: True if move is valid, False otherwise
        """
        # Check bounds
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 0 <= z < BOARD_SIZE):
            return False

        # Check if position is empty
        if self.board[z][y][x] != EMPTY:
            return False

        # Check if game is still in progress
        if self.game_status != STATE_PLAYING:
            return False

        return True

    def make_move(self, x, y, z):
        """
        Make a move at the specified position.

        Args:
            x, y, z: Coordinates of the position

        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.is_valid_move(x, y, z):
            return False

        # Place the piece
        self.board[z][y][x] = self.current_player
        self.move_history.append((x, y, z, self.current_player))
        self.move_count += 1

        # Check for win
        won, winning_line = self.check_win(x, y, z)
        if won:
            self.game_status = STATE_WIN
            self.winner = self.current_player
            self.winning_line = winning_line
            return True

        # Check for draw (board full)
        if self.move_count >= BOARD_SIZE ** 3:
            self.game_status = STATE_DRAW
            return True

        # Switch player
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

        return True

    def check_win(self, x, y, z):
        """
        Check if the last move resulted in a win.
        Only checks lines that contain the most recent move for efficiency.

        Args:
            x, y, z: Coordinates of the last move

        Returns:
            tuple: (is_win: bool, winning_line: tuple or None)
        """
        player = self.board[z][y][x]

        # Get only lines that pass through this position
        relevant_lines = get_lines_containing_position(x, y, z)

        for line in relevant_lines:
            # Check if all positions in this line belong to the current player
            if all(self.board[pos[2]][pos[1]][pos[0]] == player for pos in line):
                return True, line

        return False, None

    def get_empty_positions(self):
        """
        Get all empty positions on the board.

        Returns:
            list: List of (x, y, z) tuples for empty positions
        """
        empty_positions = []
        for z in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                for x in range(BOARD_SIZE):
                    if self.board[z][y][x] == EMPTY:
                        empty_positions.append((x, y, z))
        return empty_positions

    def get_position_value(self, x, y, z):
        """
        Get the value at a specific position.

        Args:
            x, y, z: Coordinates

        Returns:
            int: EMPTY, PLAYER_X, or PLAYER_O
        """
        return self.board[z][y][x]

    def count_in_line(self, line, player):
        """
        Count how many pieces a player has in a specific line.

        Args:
            line: Tuple of 4 coordinate tuples
            player: PLAYER_X or PLAYER_O

        Returns:
            int: Number of player's pieces in this line
        """
        count = 0
        for x, y, z in line:
            if self.board[z][y][x] == player:
                count += 1
        return count

    def is_line_blocked(self, line, player):
        """
        Check if a line is blocked (contains opponent's piece).

        Args:
            line: Tuple of 4 coordinate tuples
            player: PLAYER_X or PLAYER_O to check for

        Returns:
            bool: True if line contains opponent's piece
        """
        opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
        for x, y, z in line:
            if self.board[z][y][x] == opponent:
                return True
        return False

    def get_winning_moves(self, player):
        """
        Find all positions where player can win on next move.

        Args:
            player: PLAYER_X or PLAYER_O

        Returns:
            list: List of (x, y, z) positions that would win the game
        """
        winning_moves = []

        for line in WINNING_LINES:
            # Check if player has 3 in this line and it's not blocked
            player_count = self.count_in_line(line, player)
            if player_count == 3 and not self.is_line_blocked(line, player):
                # Find the empty position in this line
                for x, y, z in line:
                    if self.board[z][y][x] == EMPTY:
                        if (x, y, z) not in winning_moves:
                            winning_moves.append((x, y, z))

        return winning_moves

    def get_threat_positions(self, player, threat_level=2):
        """
        Find positions where player has threat_level pieces in a line.

        Args:
            player: PLAYER_X or PLAYER_O
            threat_level: Number of pieces in line (default 2)

        Returns:
            list: List of (x, y, z) positions in threatened lines
        """
        threat_positions = []

        for line in WINNING_LINES:
            player_count = self.count_in_line(line, player)
            if player_count == threat_level and not self.is_line_blocked(line, player):
                # Add all empty positions in this line
                for x, y, z in line:
                    if self.board[z][y][x] == EMPTY:
                        if (x, y, z) not in threat_positions:
                            threat_positions.append((x, y, z))

        return threat_positions

    def get_state_dict(self):
        """
        Get the current game state as a dictionary.

        Returns:
            dict: Complete game state
        """
        return {
            'board': self.board.copy(),
            'current_player': self.current_player,
            'game_status': self.game_status,
            'winner': self.winner,
            'winning_line': self.winning_line,
            'move_history': self.move_history.copy(),
            'move_count': self.move_count
        }

    def __str__(self):
        """String representation of the board for debugging."""
        result = []
        for z in range(BOARD_SIZE - 1, -1, -1):  # Top to bottom
            result.append(f"\n=== Plane {z} ===")
            for y in range(BOARD_SIZE):
                row = []
                for x in range(BOARD_SIZE):
                    val = self.board[z][y][x]
                    if val == EMPTY:
                        row.append('.')
                    elif val == PLAYER_X:
                        row.append('X')
                    else:
                        row.append('O')
                result.append(' '.join(row))
        return '\n'.join(result)
