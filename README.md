# LogiQube

**4×4×4 Strategic Tic-Tac-Toe** - *The Ultimate 3D Strategy Battle*

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![LogiQube Banner](https://img.shields.io/badge/LogiQube-4x4x4%20Tic--Tac--Toe-brightgreen)

---

## 🎮 About

LogiQube is a three-dimensional tic-tac-toe game played on a **4×4×4 cubic board** (64 total positions). Unlike traditional 3×3 tic-tac-toe which often ends in draws, the 4×4×4 format provides **76 possible winning lines** and genuine strategic depth while remaining accessible to new players.

Players compete to complete a line of **4 markers** in any direction through the cubic playing field - horizontally, vertically, diagonally, or through 3D space!

### Key Features

- ✅ **76 Winning Lines** across 7 different types
- ✅ **Interactive GUI** with visual feedback and hover effects
- ✅ **Human vs Human** gameplay mode
- ✅ **Smart Win Detection** using efficient algorithms
- ✅ **Main Menu** with mode selection
- ✅ **Full Test Coverage** - all winning conditions validated
- 🚧 **AI Opponents** (Easy, Medium, Hard) - *Coming in Phase 2*

---

## 📋 Table of Contents

- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Game Rules](#-game-rules)
- [Winning Conditions](#-winning-conditions)
- [Controls](#-controls)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/uni-dios/tictacbox.git
   cd tictacbox
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

---

## 🎯 How to Play

1. **Launch the game** by running `python main.py`
2. **Select game mode** from the main menu:
   - Human vs Human (available now)
   - Human vs AI (coming soon)
3. **Click any empty cell** to place your marker (X or O)
4. **Win by completing** any line of 4 markers in any direction
5. **Press R** to reset the game at any time

### Understanding the Board

The game displays **4 layers (planes)** side-by-side:

```
Layer 0    Layer 1    Layer 2    Layer 3
(Bottom)                         (Top)

□ □ □ □    □ □ □ □    □ □ □ □    □ □ □ □
□ □ □ □    □ □ □ □    □ □ □ □    □ □ □ □
□ □ □ □    □ □ □ □    □ □ □ □    □ □ □ □
□ □ □ □    □ □ □ □    □ □ □ □    □ □ □ □
```

Each layer is a 4×4 grid, stacked vertically to form a cube.

---

## 📐 Game Rules

1. **Players alternate turns** - X goes first, then O
2. **Click any empty cell** to place your marker
3. **First player to get 4 in a row wins** - in any direction
4. **Game ends in a draw** if all 64 cells are filled with no winner
5. **Winning line is highlighted** in gold when game ends

---

## 🏆 Winning Conditions

There are **76 possible winning lines** in LogiQube:

### 1. Horizontal Lines (within a plane) - **16 lines**
- 4 rows × 4 planes
- Example: `(0,0,0) → (1,0,0) → (2,0,0) → (3,0,0)`

### 2. Vertical Lines (within a plane) - **16 lines**
- 4 columns × 4 planes
- Example: `(0,0,0) → (0,1,0) → (0,2,0) → (0,3,0)`

### 3. Diagonal Lines (within a plane) - **8 lines**
- 2 diagonals × 4 planes
- Example: `(0,0,0) → (1,1,0) → (2,2,0) → (3,3,0)`

### 4. Vertical Lines (through planes) - **16 lines**
- Straight up through all 4 layers
- Example: `(0,0,0) → (0,0,1) → (0,0,2) → (0,0,3)`

### 5. Diagonal Lines (through planes, horizontal) - **8 lines**
- Rising diagonally while moving horizontally
- Example: `(0,0,0) → (1,0,1) → (2,0,2) → (3,0,3)`

### 6. Diagonal Lines (through planes, vertical) - **8 lines**
- Rising diagonally while moving vertically
- Example: `(0,0,0) → (0,1,1) → (0,2,2) → (0,3,3)`

### 7. 3D Corner Diagonals - **4 lines**
- Corner to corner through entire cube
- Example: `(0,0,0) → (1,1,1) → (2,2,2) → (3,3,3)`

**Total: 76 winning lines**

---

## ⌨️ Controls

| Key/Action | Function |
|-----------|----------|
| **Left Click** | Place marker on empty cell |
| **R** | Reset/New game |
| **C** | Toggle coordinate display (debug) |
| **ESC** | Quit game |
| **Mouse Hover** | Preview cell selection |

---

## 📁 Project Structure

```
tictacbox/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── test_game.py           # Test suite
├── src/
│   ├── __init__.py        # Package init
│   ├── constants.py       # Game constants and colors
│   ├── winning_lines.py   # All 76 winning line definitions
│   ├── board.py           # Board logic and game state
│   ├── ui.py              # Pygame UI rendering
│   └── game.py            # Main game controller
├── LICENSE                # MIT License
└── README.md             # This file
```

---

## 🛠️ Development

### Running Tests

Run the comprehensive test suite to validate all game logic:

```bash
python test_game.py
```

The test suite validates:
- All 76 winning lines are correctly generated
- Move validation (bounds checking, occupied cells)
- Win detection for all 7 line types
- Draw condition detection
- Game state management

### Code Overview

**Core Components:**

1. **Board Class** (`src/board.py`)
   - Manages 4×4×4 game state using NumPy arrays
   - Move validation and execution
   - Efficient win detection (only checks relevant lines)
   - Helper methods for AI (coming in Phase 2)

2. **UI Class** (`src/ui.py`)
   - Pygame-based rendering
   - 4 planes displayed side-by-side
   - Mouse input handling
   - Visual effects (hover, winning line highlight)

3. **Game Class** (`src/game.py`)
   - Game loop and event handling
   - Coordinates Board and UI
   - Main menu implementation

4. **Winning Lines** (`src/winning_lines.py`)
   - Programmatically generates all 76 lines
   - Validation and helper functions
   - Efficient line lookup by position

---

## 🧪 Testing

### Test Results

```
✓ All 76 winning lines validated successfully!
✓ Move Validation - PASSED
✓ Horizontal Win - PASSED
✓ Vertical Win - PASSED
✓ Diagonal Win - PASSED
✓ 3D Vertical Win - PASSED
✓ 3D Diagonal Win - PASSED
✓ Draw Condition - PASSED

Passed: 8/8
```

### Adding Tests

To add new tests, edit `test_game.py` and add test functions following this pattern:

```python
def test_your_feature():
    """Test description."""
    board = Board()
    # ... test logic ...
    assert condition, "Error message"
    return True
```

---

## 🗺️ Roadmap

### ✅ Phase 1: Core Game (COMPLETED)
- [x] Basic board implementation
- [x] All 76 winning line detection
- [x] Pygame UI with 4 planes
- [x] Human vs Human mode
- [x] Win/Draw detection
- [x] Main menu
- [x] Visual feedback
- [x] Comprehensive testing

### 🚧 Phase 2: AI Implementation (In Progress)
- [ ] Easy AI (reactive defense, random offense)
- [ ] Medium AI (proactive defense, single-line strategy)
- [ ] Hard AI (predictive strategy, multi-threat)
- [ ] AI difficulty selection menu
- [ ] Performance optimization

### 📅 Phase 3: Visual Polish (Planned)
- [ ] Animations for piece placement
- [ ] Particle effects for winning line
- [ ] Sound effects (place, win, draw)
- [ ] Background music (toggleable)
- [ ] Improved UI/UX design
- [ ] Tutorial/instructions overlay

### 🔮 Phase 4: Fun Mode (Future)
- [ ] Extended gameplay (most lines wins)
- [ ] Power-ups system
- [ ] Scoring system
- [ ] Multiplayer over network

---

## 📊 Technical Details

### Coordinate System

```
(x, y, z) where:
- x: column (0-3, left to right)
- y: row (0-3, front to back)
- z: plane/layer (0-3, bottom to top)
```

### Data Structures

**Board Representation:**
```python
board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]

# Values:
# 0 = empty
# 1 = Player X
# 2 = Player O
```

**Win Detection Algorithm:**
- O(76) worst case, but typically checks only ~7-15 relevant lines
- Only examines lines containing the most recent move
- Pre-computed winning line coordinates

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

---

## 🙏 Acknowledgments

- Inspired by classic 3D tic-tac-toe games
- Built with Python and Pygame
- Developed as an educational strategic game project

---

## 📞 Contact & Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/uni-dios/tictacbox/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/uni-dios/tictacbox/discussions)

---

## 🎮 Screenshots

*Coming soon - screenshots of gameplay, menu, and winning conditions*

---

**Enjoy playing LogiQube! May the best strategist win! 🏆**
