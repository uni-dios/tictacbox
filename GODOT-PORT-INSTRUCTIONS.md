# LogiQube - Godot Port Instructions

**Project**: LogiQube 3D Port to Godot
**Original**: Python/Pygame 4×4×4 Tic-Tac-Toe (Phase 1 Complete)
**Target**: Godot 4.x with full 3D visualization and multi-platform deployment
**Status**: Planning/Initial Setup

---

## 🎯 Project Overview

We are porting **LogiQube** (a 4×4×4 strategic tic-tac-toe game) from Pygame to Godot 4.x to create a fully 3D experience with dynamic camera controls, visual effects, and cross-platform deployment capability.

### Why Godot?

- **3D Visualization**: Players can see the cube in true 3D space with orbital camera
- **Better UX**: Transparent layers, smooth animations, particle effects for winning lines
- **Cross-Platform**: One codebase → Steam, iOS, Android, Web
- **Future-Proof**: Ready for Phase 2 (Fun Mode with power-ups and effects)

---

## 📚 Background - What We're Porting

### Original Pygame Implementation (Phase 1 - COMPLETE)

**Repository**: `uni-dios/tictacbox` (branch: `claude/logiqube-game-spec-011CUisMtkiunndEWwUWbecA`)

**Core Features Already Built:**
- ✅ Complete 4×4×4 board logic (`src/board.py`)
- ✅ All 76 winning line definitions (`src/winning_lines.py`)
- ✅ Efficient win detection algorithm (checks only relevant lines)
- ✅ Move validation, turn alternation, draw detection
- ✅ Human vs Human gameplay
- ✅ Comprehensive test suite (8/8 tests passing)

**Game Rules:**
- 64 playable positions in a 4×4×4 cube
- 76 possible winning lines across 7 types:
  - 16 horizontal (within planes)
  - 16 vertical (within planes)
  - 8 diagonal (within planes)
  - 16 vertical (through planes)
  - 8 diagonal through planes (horizontal direction)
  - 8 diagonal through planes (vertical direction)
  - 4 3D corner diagonals
- Players alternate placing X or O
- First to complete any 4-in-a-row wins
- Board full with no winner = draw

**What Transfers Directly:**
- All game logic (Board class logic patterns)
- The 76 winning line coordinates
- Win detection algorithm
- Move validation rules
- Game state management patterns

**What Needs Rewriting:**
- ONLY the UI/rendering layer (was Pygame, now Godot)

---

## 🎨 Visual Design Specification

### Initial Board Display

**Layout:**
- 4 transparent planes stacked vertically (Layers 0-3, bottom to top)
- Each plane is a 4×4 grid of playable cells
- Sufficient vertical spacing between layers to see all boards clearly
- Grid lines visible on each transparent layer

**Visual Elements:**
- **Transparent plane materials** - can see through layers
- **Opaque grid lines** - clearly define the 64 playable cells
- **Layer identification** - visual distinction between layers (colored edges, tints, or labels)
- **Playable cells** - 64 cubes/squares positioned at grid intersections
- **Pieces** - 3D X and O models (or simple geometric representations)

### Camera System

**Controls:**
- **Orbit rotation**: Click-drag anywhere outside the board to rotate camera around cube
- **Zoom**: Mouse scroll wheel or pinch gesture (mobile)
- **Reset view**: Button to snap camera back to default "upright" position
- **Up/Down indicator**: Visual compass showing which direction is "up"

**Dynamic Layer Spacing (KEY FEATURE):**
- **Zoomed OUT** (far view): Layers compact together, approaching true cube shape
- **Zoomed IN** (close view): Layers spread apart vertically for better visibility
- Smooth interpolation between states based on camera distance
- Formula: `layer_spacing = base_spacing + (camera_distance * spread_factor)`

**Camera Behavior:**
- Free rotation in all axes (X, Y, Z)
- Maintain focus on cube center point
- Smooth transitions (no jarring movements)
- Prevent extreme angles that obscure the board
- Optional: Snap to orthogonal views (top, front, side) with hotkeys

### Visual Feedback

**Hover Effects:**
- Highlight cell under mouse cursor
- Show which layer/position would be selected
- Visual indicator if cell is occupied vs. available

**Move Placement:**
- Smooth animation when piece appears (scale up, fade in, or drop down)
- Distinct visuals for X (red) vs O (blue)
- Clear, readable even when viewing through transparent layers

**Winning Line:**
- **Highlight all 4 cells** in the winning line
- Gold/yellow glow effect
- Optional: Pulsing animation or particle trail connecting the 4 pieces
- Camera can auto-rotate to best viewing angle of winning line

**Turn Indicator:**
- UI overlay showing current player (X or O)
- Color-coded (red for X, blue for O)
- Move counter (X/64)

---

## 🏗️ Technical Architecture

### Scene Structure

```
Main (Node3D)
├── GameBoard (Node3D)
│   ├── Layer0 (Node3D) - bottom plane
│   │   ├── GridMesh (MeshInstance3D) - transparent plane with grid
│   │   └── Cells (Node3D)
│   │       ├── Cell_0_0_0 (Area3D + MeshInstance3D)
│   │       ├── Cell_1_0_0 (Area3D + MeshInstance3D)
│   │       └── ... (16 cells total)
│   ├── Layer1 (Node3D)
│   ├── Layer2 (Node3D)
│   └── Layer3 (Node3D) - top plane
├── Camera3D (with orbit camera script)
├── DirectionalLight3D
├── UI (CanvasLayer)
│   ├── PlayerIndicator (Label)
│   ├── MoveCounter (Label)
│   ├── ResetButton (Button)
│   └── CompassIndicator (Control)
└── GameController (Node - main game logic script)
```

### Code Architecture

**Core Scripts:**

1. **`game_board.gd`** (attached to GameBoard node)
   - Manages the 3D visual representation
   - Generates 64 cell positions programmatically
   - Updates piece visuals when moves are made
   - Handles dynamic layer spacing based on camera distance
   - Highlights winning line

2. **`game_controller.gd`** (attached to GameController node)
   - Ports logic from Python `Board` class
   - Maintains 3D array: `board[z][y][x]` (0=empty, 1=X, 2=O)
   - Validates moves
   - Checks win conditions (uses 76 winning lines)
   - Manages game state (playing, win, draw)
   - Turn alternation

3. **`winning_lines.gd`** (autoload singleton)
   - Contains all 76 winning line coordinate arrays
   - Helper function: `get_lines_containing_position(x, y, z)`
   - Validation functions

4. **`orbit_camera.gd`** (attached to Camera3D)
   - Handles mouse drag for rotation
   - Zoom with scroll wheel
   - Reset to default view
   - Smooth interpolation
   - Communicates zoom level to GameBoard for layer spacing

5. **`cell.gd`** (attached to each cell Area3D)
   - Detects mouse hover
   - Emits signal when clicked
   - Stores its (x, y, z) coordinate
   - Updates visual state (empty, X, O, highlighted, winning)

### Data Flow

```
User clicks cell
  ↓
cell.gd detects click → emits signal with (x, y, z)
  ↓
game_controller.gd receives signal
  ↓
validates move via is_valid_move(x, y, z)
  ↓
if valid: updates board[z][y][x], checks win
  ↓
emits signal to game_board.gd
  ↓
game_board.gd updates 3D visuals (place X or O piece)
  ↓
if win: highlights winning line, shows winner UI
```

---

## 🔧 Implementation Phases

### Phase 1: Basic 3D Scene Setup ✅ (CURRENT)
- [x] Create Godot project
- [x] Set up VS Code integration
- [x] Test basic scene with cube and camera
- [ ] Create project documentation

### Phase 2: Procedural Board Generation
- [ ] Write script to generate 4×4×4 grid of cells (64 positions)
- [ ] Create transparent plane materials with grid lines
- [ ] Position 4 layers with proper spacing
- [ ] Add basic lighting

### Phase 3: Camera Controller
- [ ] Implement orbit camera (click-drag rotation)
- [ ] Add zoom controls (scroll wheel)
- [ ] Create reset view button
- [ ] Add up/down compass indicator
- [ ] Implement dynamic layer spacing based on zoom

### Phase 4: Core Game Logic (Port from Python)
- [ ] Port `Board` class to `game_controller.gd`
- [ ] Port 76 winning lines to `winning_lines.gd` (autoload)
- [ ] Implement win detection algorithm
- [ ] Add move validation
- [ ] Game state management

### Phase 5: Interaction & Visual Feedback
- [ ] Cell click detection (ray casting from mouse)
- [ ] Hover effects on cells
- [ ] Place X/O piece visuals (3D models or simple shapes)
- [ ] Turn indicator UI
- [ ] Move counter display

### Phase 6: Win Conditions & Effects
- [ ] Winning line highlight (gold glow)
- [ ] Win announcement UI
- [ ] Draw detection and display
- [ ] Optional: Camera auto-rotate to winning line
- [ ] Particle effects for winning line

### Phase 7: Polish & Menus
- [ ] Main menu scene
- [ ] Game mode selection (Classic vs Fun - Classic only for now)
- [ ] Reset/New game functionality
- [ ] Settings menu (camera sensitivity, visual options)
- [ ] Instructions/tutorial overlay

### Phase 8: Testing & Optimization
- [ ] Test all 76 winning conditions in 3D
- [ ] Performance optimization (should be very fast with only 64 cells)
- [ ] Mobile touch controls
- [ ] Different screen resolutions

### Phase 9: Multi-Platform Export
- [ ] Windows build (Steam)
- [ ] macOS build
- [ ] Linux build
- [ ] Android build (touch controls)
- [ ] iOS build (requires Mac + Apple Developer account)

---

## 🎮 Game Modes & Monetization

### Classic Mode (FREE)
- Human vs Human gameplay
- All 76 winning conditions
- Full 3D visualization
- Complete game experience
- **Purpose**: Hook players, prove concept, build audience

### Fun Mode ($5 unlock) - PHASE 2
- Multi-line scoring (game continues until board full)
- Power-ups system (earned by completing lines)
- Winner = most completed lines
- Particle effects, animations, more spectacle
- **Purpose**: Premium experience, revenue generation

### Platform Strategy

**Steam (PC/Mac/Linux):**
- $5 for full game (Classic + Fun Mode)
- Steam achievements (win with each line type, etc.)
- Potentially Steam Workshop for custom skins

**Mobile (iOS/Android):**
- Classic Mode: FREE
- Fun Mode: $4.99 IAP unlock
- Ad-supported option for free tier (optional)

**Goal**: Test market, build portfolio, learn what works, move to next game

---

## 📋 Coordinate System (CRITICAL)

**Must match Python implementation exactly:**

```
(x, y, z) where:
- x: column (0-3, left to right when viewed from front)
- y: row (0-3, front to back)
- z: plane/layer (0-3, bottom to top)

Example positions:
- (0, 0, 0) = front-left corner of bottom layer
- (3, 3, 3) = back-right corner of top layer
- (1, 1, 1) = interior position
```

**In Godot 3D space:**
- X-axis: left (-) to right (+)
- Y-axis: down (-) to up (+)  ← NOTE: Godot Y is UP
- Z-axis: forward (-) to back (+)

**Mapping:**
- Game x → Godot X
- Game y → Godot Z (careful!)
- Game z → Godot Y

**Cell position in 3D space:**
```gdscript
var cell_spacing = 1.0  # units between cells
var position = Vector3(
    game_x * cell_spacing,
    game_z * layer_spacing,  # dynamic based on zoom
    game_y * cell_spacing
)
```

---

## 🎨 Visual Style Guide

### Color Palette

**Board:**
- Grid lines: Light gray/white (#CCCCCC)
- Transparent planes: Slight blue tint with ~20% opacity
- Background: Dark gradient (space/void aesthetic)

**Pieces:**
- X: Red (#FF6464) - warm, aggressive
- O: Blue (#6496FF) - cool, defensive
- Winning line: Gold (#FFD700) - celebratory

**UI:**
- Background: Dark semi-transparent (#000000AA)
- Text: White (#FFFFFF)
- Buttons: Subtle gray (#444444) with hover states

**Layers (optional tinting):**
- Layer 0: Slight red tint
- Layer 1: Slight green tint
- Layer 2: Slight blue tint
- Layer 3: Slight yellow tint

### Materials

**Transparent Grid Planes:**
```gdscript
# StandardMaterial3D properties:
- Transparency: Enabled
- Albedo Color: (1, 1, 1, 0.2)  # 20% opacity
- Metallic: 0.0
- Roughness: 0.3
- Emission: Slight glow on grid lines
```

**Pieces (X and O):**
```gdscript
# For X and O meshes:
- Albedo: Player color (red or blue)
- Metallic: 0.2
- Roughness: 0.4
- Emission: Slight glow (0.1 strength)
```

**Winning Line Glow:**
```gdscript
# When piece is part of winning line:
- Emission: Gold color (#FFD700)
- Emission Energy: 2.0 (bright glow)
- Optional: Pulsing animation
```

---

## 🧪 Testing Requirements

### Functional Tests (must all pass)

**Win Detection:**
- [ ] Test horizontal win in each of 4 planes (16 lines)
- [ ] Test vertical win in each of 4 planes (16 lines)
- [ ] Test diagonal win in each of 4 planes (8 lines)
- [ ] Test vertical through all planes (16 lines)
- [ ] Test diagonal through planes, X direction (8 lines)
- [ ] Test diagonal through planes, Y direction (8 lines)
- [ ] Test 4 corner-to-corner 3D diagonals (4 lines)
- **Total: All 76 winning lines must be detectable**

**Game Logic:**
- [ ] Cannot place on occupied cell
- [ ] Cannot play after game ends
- [ ] Draw detected when board full
- [ ] Reset clears board properly
- [ ] Turn alternation works correctly

**Visual:**
- [ ] All 64 cells are clickable
- [ ] Hover shows correct cell
- [ ] Pieces appear in correct 3D positions
- [ ] Winning line highlights correctly
- [ ] Camera rotation works smoothly
- [ ] Layer spacing responds to zoom

**Performance:**
- [ ] 60 FPS on mid-range hardware
- [ ] No lag when rotating camera
- [ ] Instant response to clicks

---

## 📖 Reference Documents

### Original Specification
See `GAME-SPEC.md` (or original spec document) for complete game rules, winning conditions breakdown, and original design intent.

### Python Implementation
Repository: `uni-dios/tictacbox`
Branch: `claude/logiqube-game-spec-011CUisMtkiunndEWwUWbecA`

**Key Files to Reference:**
- `src/board.py` - Game logic patterns to port
- `src/winning_lines.py` - Exact coordinate arrays to replicate
- `src/constants.py` - Game constants
- `test_game.py` - Test cases to replicate in Godot

### Godot Resources
- **Godot 4.x Docs**: https://docs.godotengine.org/en/stable/
- **3D Tutorial**: https://docs.godotengine.org/en/stable/tutorials/3d/
- **GDScript Reference**: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/

---

## 🚀 Development Workflow

### Recommended Process

1. **Scene Building in Godot Editor:**
   - Visual layout of 3D objects
   - Node hierarchy setup
   - Material/mesh assignment
   - Inspector property configuration

2. **Code Writing in VS Code:**
   - All `.gd` script editing
   - Git commits
   - Claude AI assistance
   - Syntax highlighting

3. **Testing in Godot:**
   - Press F5 to run
   - Check Output panel for print statements
   - Debug with breakpoints (if needed)
   - Visual verification

### Git Workflow

- **Main branch**: Production-ready code
- **Feature branches**: `feature/camera-controls`, `feature/board-generation`, etc.
- **Commit often**: Small, atomic commits with clear messages
- **Push regularly**: Keep remote in sync for Claude Code access

### Claude Code Integration

**When asking for help:**
- Share the Godot repo URL
- Specify which `.gd` file you're working on
- Describe the issue or feature clearly
- Reference this document for context

**What Claude can do:**
- Read all `.gd`, `.tscn`, and project files
- Write GDScript code
- Debug issues
- Suggest architecture improvements
- Generate procedural mesh code
- Port Python logic to GDScript

---

## 📝 Current Status

**Phase**: Initial Setup ✅
**Next Steps**:
1. Finish project documentation (this file)
2. Begin procedural board generation
3. Set up transparent grid materials
4. Implement basic orbit camera

**Blockers**: None
**Questions**: None

---

## 🎯 Success Criteria

### Godot Port Complete When:
- ✅ Full 3D visualization of 4×4×4 cube
- ✅ All 76 winning conditions work correctly
- ✅ Smooth camera controls (orbit, zoom, reset)
- ✅ Dynamic layer spacing based on zoom
- ✅ Winning line highlighting with effects
- ✅ Touch controls work on mobile
- ✅ Game is fun and visually appealing
- ✅ Can export to all target platforms (Steam, iOS, Android)

### Phase 1 (Classic Mode) Complete When:
- ✅ Everything above
- ✅ Main menu functional
- ✅ Reset/New game works
- ✅ UI is polished and clear
- ✅ No critical bugs
- ✅ Ready for player testing

---

## 💡 Design Philosophy

**Keep It Simple:**
- Classic Mode is intentionally minimalist
- Focus on clarity over complexity
- 3D should enhance, not obscure, the game

**Player-Focused:**
- Controls must be intuitive
- Visual feedback at every step
- No confusion about game state

**Performance:**
- 60 FPS is non-negotiable
- Fast loading times
- Responsive on mobile devices

**Extensibility:**
- Code organized for easy addition of Fun Mode later
- Clean separation: logic vs. visuals
- Modular systems (camera, board, UI independent)

---

## 🔮 Future Enhancements (Post-Launch)

- **Online Multiplayer**: Play against friends over network
- **AI Opponents**: Easy, Medium, Hard (from original spec)
- **Replay System**: Review past games
- **Custom Themes**: Different visual styles for the board
- **Accessibility**: Colorblind modes, screen reader support
- **Leaderboards**: Track wins/stats
- **Achievements**: Steam/mobile achievements
- **Spectator Mode**: Watch others play with flying camera

---

## 📞 Questions & Decisions Log

**Q: Should we use CSG (Constructive Solid Geometry) or MeshInstance3D for cells?**
A: MeshInstance3D - simpler, better performance, more control

**Q: Procedural generation or manual placement?**
A: Procedural - easier to maintain, parameterized spacing

**Q: How to handle transparent overlapping?**
A: Use depth sorting, proper alpha blending, emission for highlights

**Q: Should camera orbit around center or allow free movement?**
A: Orbit around fixed center point - simpler UX, always focused on game

**Q: Touch controls - how to rotate vs. select cell?**
A: Two-finger drag to rotate, single tap to select cell

---

**This document is the source of truth for LogiQube Godot development.**

**Last Updated**: 2025-11-02
**Version**: 1.0
**Status**: Active Development

---

**Let's build something amazing! 🎮✨**
