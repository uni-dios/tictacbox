"""
LogiQube - Main Game Controller
Orchestrates board logic and UI
"""

import pygame
from src.board import Board
from src.ui import GameUI
from src.constants import *


class Game:
    """
    Main game controller for LogiQube.
    Handles game loop, events, and coordinates between Board and UI.
    """

    def __init__(self):
        """Initialize the game."""
        self.board = Board()
        self.ui = GameUI()
        self.running = True
        self.mode = MODE_HUMAN_VS_HUMAN  # Default mode
        self.ai_difficulty = None

    def handle_events(self):
        """Handle pygame events."""
        mouse_pos = pygame.mouse.get_pos()

        # Update hover position
        self.ui.hover_position = self.ui.get_position_from_mouse(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # R key to reset game
                if event.key == pygame.K_r:
                    self.reset_game()
                # C key to toggle coordinate display (debug)
                elif event.key == pygame.K_c:
                    self.ui.show_coordinates = not self.ui.show_coordinates
                # ESC to quit
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(mouse_pos)

    def handle_click(self, mouse_pos):
        """
        Handle mouse click events.

        Args:
            mouse_pos: (x, y) tuple of mouse position
        """
        # Get board position from mouse
        position = self.ui.get_position_from_mouse(mouse_pos)

        if position is None:
            return

        x, y, z = position

        # Try to make the move
        if self.board.make_move(x, y, z):
            # Move was successful
            if self.board.game_status == STATE_WIN:
                print(f"Player {self.board.winner} wins!")
                print(f"Winning line: {self.board.winning_line}")
            elif self.board.game_status == STATE_DRAW:
                print("Game is a draw!")

    def reset_game(self):
        """Reset the game to initial state."""
        self.board.reset()
        print("Game reset!")

    def render(self):
        """Render the current game state."""
        self.ui.draw_board(self.board)

        # Draw winning line if game is won
        if self.board.game_status == STATE_WIN:
            self.ui.draw_winning_line(self.board)

        # Draw reset button
        button_width = 120
        button_height = 40
        button_x = WINDOW_WIDTH - button_width - 20
        button_y = 20

        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.ui.draw_button("Reset (R)", button_x, button_y,
                                       button_width, button_height, mouse_pos)

        # Handle button click
        if is_hover and pygame.mouse.get_pressed()[0]:
            self.reset_game()

        # Draw instructions
        self._draw_instructions()

        self.ui.update_display()

    def _draw_instructions(self):
        """Draw game instructions on screen."""
        instructions = [
            "Click any empty cell to place your marker",
            "Press R to reset game",
            "Press ESC to quit"
        ]

        y_start = WINDOW_HEIGHT - 150
        for i, instruction in enumerate(instructions):
            text = self.ui.font_small.render(instruction, True, COLOR_TEXT)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_start + i * 25))
            self.ui.screen.blit(text, text_rect)

    def run(self):
        """Main game loop."""
        print("╔════════════════════════════════════════╗")
        print("║        LogiQube - 4x4x4 Tic-Tac-Toe    ║")
        print("╚════════════════════════════════════════╝")
        print("\nControls:")
        print("  • Click to place marker")
        print("  • R - Reset game")
        print("  • C - Toggle coordinates (debug)")
        print("  • ESC - Quit")
        print("\nGame started! Player X goes first.\n")

        while self.running:
            self.handle_events()
            self.render()

        self.ui.quit()


class MainMenu:
    """
    Main menu for game mode selection.
    """

    def __init__(self):
        """Initialize the main menu."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LogiQube - Main Menu")
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

    def draw_menu(self):
        """Draw the main menu."""
        self.screen.fill(COLOR_BG)

        # Title
        title = self.font_large.render("LogiQube", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.font_small.render("4x4x4 Strategic Tic-Tac-Toe", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)

        # Menu options
        mouse_pos = pygame.mouse.get_pos()
        button_width = 300
        button_height = 60
        button_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 250

        # Human vs Human button
        button_rect_1 = pygame.Rect(button_x, start_y, button_width, button_height)
        is_hover_1 = button_rect_1.collidepoint(mouse_pos)
        color_1 = COLOR_BUTTON_HOVER if is_hover_1 else COLOR_BUTTON
        pygame.draw.rect(self.screen, color_1, button_rect_1)
        pygame.draw.rect(self.screen, COLOR_GRID, button_rect_1, 2)

        text_1 = self.font_medium.render("Human vs Human", True, COLOR_TEXT)
        text_rect_1 = text_1.get_rect(center=button_rect_1.center)
        self.screen.blit(text_1, text_rect_1)

        # Human vs AI button (coming soon)
        button_rect_2 = pygame.Rect(button_x, start_y + 80, button_width, button_height)
        is_hover_2 = button_rect_2.collidepoint(mouse_pos)
        color_2 = (60, 60, 70)  # Disabled color
        pygame.draw.rect(self.screen, color_2, button_rect_2)
        pygame.draw.rect(self.screen, COLOR_GRID, button_rect_2, 2)

        text_2 = self.font_small.render("Human vs AI (Coming Soon)", True, (150, 150, 150))
        text_rect_2 = text_2.get_rect(center=button_rect_2.center)
        self.screen.blit(text_2, text_rect_2)

        # Quit button
        button_rect_3 = pygame.Rect(button_x, start_y + 160, button_width, button_height)
        is_hover_3 = button_rect_3.collidepoint(mouse_pos)
        color_3 = COLOR_BUTTON_HOVER if is_hover_3 else COLOR_BUTTON
        pygame.draw.rect(self.screen, color_3, button_rect_3)
        pygame.draw.rect(self.screen, COLOR_GRID, button_rect_3, 2)

        text_3 = self.font_medium.render("Quit", True, COLOR_TEXT)
        text_rect_3 = text_3.get_rect(center=button_rect_3.center)
        self.screen.blit(text_3, text_rect_3)

        pygame.display.flip()
        self.clock.tick(60)

        return is_hover_1, is_hover_2, is_hover_3

    def run(self):
        """Run the main menu and return selected mode."""
        running = True
        selected_mode = None

        while running:
            is_hover_1, is_hover_2, is_hover_3 = self.draw_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if is_hover_1:
                            selected_mode = MODE_HUMAN_VS_HUMAN
                            running = False
                        elif is_hover_3:
                            pygame.quit()
                            return None

        return selected_mode
