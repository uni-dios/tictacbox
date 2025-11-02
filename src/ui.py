"""
LogiQube - Pygame User Interface
Displays 4x4x4 board as 4 planes side-by-side
"""

import pygame
import sys
from src.constants import *
from src.board import Board


class GameUI:
    """
    Handles all rendering and user interaction for LogiQube.
    """

    def __init__(self):
        """Initialize Pygame and UI components."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LogiQube - 4x4x4 Strategic Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Calculate plane positions (4 planes side-by-side)
        self.plane_positions = self._calculate_plane_positions()

        # UI state
        self.hover_position = None  # (x, y, z) or None
        self.show_coordinates = False  # For debugging

    def _calculate_plane_positions(self):
        """
        Calculate screen positions for each of the 4 planes.

        Returns:
            list: List of (screen_x, screen_y) tuples for top-left corner of each plane
        """
        total_width = (CELL_SIZE * BOARD_SIZE + GRID_PADDING * 2) * 4 + PLANE_MARGIN * 3
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 200  # Leave space for header

        positions = []
        for i in range(BOARD_SIZE):
            plane_x = start_x + i * (CELL_SIZE * BOARD_SIZE + GRID_PADDING * 2 + PLANE_MARGIN)
            positions.append((plane_x, start_y))

        return positions

    def get_position_from_mouse(self, mouse_pos):
        """
        Convert mouse position to board coordinates (x, y, z).

        Args:
            mouse_pos: (mouse_x, mouse_y) tuple

        Returns:
            (x, y, z) tuple or None if not over a valid position
        """
        mouse_x, mouse_y = mouse_pos

        # Check each plane
        for z in range(BOARD_SIZE):
            plane_x, plane_y = self.plane_positions[z]
            grid_x = plane_x + GRID_PADDING
            grid_y = plane_y + GRID_PADDING

            # Check if mouse is within this plane's grid
            if (grid_x <= mouse_x < grid_x + CELL_SIZE * BOARD_SIZE and
                    grid_y <= mouse_y < grid_y + CELL_SIZE * BOARD_SIZE):

                # Calculate cell position
                x = (mouse_x - grid_x) // CELL_SIZE
                y = (mouse_y - grid_y) // CELL_SIZE

                return (x, y, z)

        return None

    def draw_board(self, board):
        """
        Draw the entire game board with all 4 planes.

        Args:
            board: Board instance
        """
        # Clear screen
        self.screen.fill(COLOR_BG)

        # Draw title
        title = self.font_large.render("LogiQube", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw each plane
        for z in range(BOARD_SIZE):
            self._draw_plane(board, z)

        # Draw current player indicator
        self._draw_status(board)

    def _draw_plane(self, board, z):
        """
        Draw a single plane of the board.

        Args:
            board: Board instance
            z: Plane index (0-3)
        """
        plane_x, plane_y = self.plane_positions[z]

        # Draw plane background
        bg_rect = pygame.Rect(plane_x, plane_y,
                              CELL_SIZE * BOARD_SIZE + GRID_PADDING * 2,
                              CELL_SIZE * BOARD_SIZE + GRID_PADDING * 2)
        pygame.draw.rect(self.screen, COLOR_PLANE_BG, bg_rect)
        pygame.draw.rect(self.screen, COLOR_GRID, bg_rect, 2)

        # Draw plane label
        label = self.font_small.render(f"Layer {z}", True, COLOR_TEXT)
        label_rect = label.get_rect(center=(plane_x + bg_rect.width // 2, plane_y - 15))
        self.screen.blit(label, label_rect)

        grid_x = plane_x + GRID_PADDING
        grid_y = plane_y + GRID_PADDING

        # Draw grid and cells
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                cell_rect = pygame.Rect(
                    grid_x + x * CELL_SIZE,
                    grid_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                # Draw hover effect
                if self.hover_position == (x, y, z) and board.is_valid_move(x, y, z):
                    pygame.draw.rect(self.screen, COLOR_HOVER, cell_rect)

                # Draw cell border
                pygame.draw.rect(self.screen, COLOR_GRID, cell_rect, 1)

                # Draw piece if present
                value = board.get_position_value(x, y, z)
                if value == PLAYER_X:
                    self._draw_x(cell_rect)
                elif value == PLAYER_O:
                    self._draw_o(cell_rect)

                # Draw coordinates (debug mode)
                if self.show_coordinates:
                    coord_text = self.font_small.render(f"{x},{y},{z}", True, COLOR_TEXT)
                    self.screen.blit(coord_text, (cell_rect.x + 2, cell_rect.y + 2))

    def _draw_x(self, rect):
        """Draw an X in the given cell rectangle."""
        padding = 8
        pygame.draw.line(self.screen, COLOR_X,
                        (rect.x + padding, rect.y + padding),
                        (rect.right - padding, rect.bottom - padding), 4)
        pygame.draw.line(self.screen, COLOR_X,
                        (rect.right - padding, rect.y + padding),
                        (rect.x + padding, rect.bottom - padding), 4)

    def _draw_o(self, rect):
        """Draw an O in the given cell rectangle."""
        center = rect.center
        radius = rect.width // 2 - 8
        pygame.draw.circle(self.screen, COLOR_O, center, radius, 4)

    def _draw_status(self, board):
        """
        Draw game status information (current player, winner, etc.).

        Args:
            board: Board instance
        """
        status_y = WINDOW_HEIGHT - 100

        if board.game_status == STATE_PLAYING:
            # Show current player
            player_name = "X" if board.current_player == PLAYER_X else "O"
            color = COLOR_X if board.current_player == PLAYER_X else COLOR_O
            text = self.font_medium.render(f"Current Player: {player_name}", True, color)
        elif board.game_status == STATE_WIN:
            # Show winner
            winner_name = "X" if board.winner == PLAYER_X else "O"
            color = COLOR_X if board.winner == PLAYER_X else COLOR_O
            text = self.font_medium.render(f"Player {winner_name} Wins!", True, color)
        else:  # STATE_DRAW
            text = self.font_medium.render("Game Draw!", True, COLOR_TEXT)

        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, status_y))
        self.screen.blit(text, text_rect)

        # Draw move count
        move_text = self.font_small.render(f"Moves: {board.move_count}/64", True, COLOR_TEXT)
        move_rect = move_text.get_rect(center=(WINDOW_WIDTH // 2, status_y + 40))
        self.screen.blit(move_text, move_rect)

    def draw_winning_line(self, board):
        """
        Highlight the winning line if game is won.

        Args:
            board: Board instance
        """
        if board.game_status != STATE_WIN or board.winning_line is None:
            return

        # Draw highlights on all cells in winning line
        for x, y, z in board.winning_line:
            plane_x, plane_y = self.plane_positions[z]
            grid_x = plane_x + GRID_PADDING
            grid_y = plane_y + GRID_PADDING

            cell_rect = pygame.Rect(
                grid_x + x * CELL_SIZE,
                grid_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Draw pulsing highlight
            pygame.draw.rect(self.screen, COLOR_WIN_LINE, cell_rect, 4)

    def draw_button(self, text, x, y, width, height, mouse_pos):
        """
        Draw a button and return True if it's being hovered.

        Args:
            text: Button text
            x, y: Button position
            width, height: Button dimensions
            mouse_pos: Current mouse position

        Returns:
            bool: True if mouse is over button
        """
        button_rect = pygame.Rect(x, y, width, height)
        is_hover = button_rect.collidepoint(mouse_pos)

        # Draw button
        color = COLOR_BUTTON_HOVER if is_hover else COLOR_BUTTON
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, COLOR_GRID, button_rect, 2)

        # Draw text
        text_surface = self.font_small.render(text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

        return is_hover

    def update_display(self):
        """Update the display and tick the clock."""
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS

    def quit(self):
        """Clean up and quit Pygame."""
        pygame.quit()
        sys.exit()
