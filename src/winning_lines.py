"""
LogiQube - All 76 Winning Line Definitions
Coordinates are in (x, y, z) format where:
- x: column (0-3, left to right)
- y: row (0-3, front to back)
- z: plane/layer (0-3, bottom to top)
"""

from src.constants import BOARD_SIZE


def generate_winning_lines():
    """
    Generate all 76 possible winning lines in the 4x4x4 cube.
    Returns a list of tuples, where each tuple contains 4 coordinate tuples.
    """
    lines = []

    # ===== 1. HORIZONTAL LINES (within each plane) =====
    # 4 rows × 4 planes = 16 lines
    for z in range(BOARD_SIZE):  # Each plane
        for y in range(BOARD_SIZE):  # Each row in plane
            line = tuple((x, y, z) for x in range(BOARD_SIZE))
            lines.append(line)

    # ===== 2. VERTICAL LINES (within each plane) =====
    # 4 columns × 4 planes = 16 lines
    for z in range(BOARD_SIZE):  # Each plane
        for x in range(BOARD_SIZE):  # Each column in plane
            line = tuple((x, y, z) for y in range(BOARD_SIZE))
            lines.append(line)

    # ===== 3. DIAGONAL LINES (within each plane) =====
    # 2 diagonals × 4 planes = 8 lines
    for z in range(BOARD_SIZE):  # Each plane
        # Main diagonal (top-left to bottom-right)
        line1 = tuple((i, i, z) for i in range(BOARD_SIZE))
        lines.append(line1)

        # Anti-diagonal (top-right to bottom-left)
        line2 = tuple((i, BOARD_SIZE - 1 - i, z) for i in range(BOARD_SIZE))
        lines.append(line2)

    # ===== 4. VERTICAL LINES (through planes, straight up) =====
    # 16 positions × 1 line each = 16 lines
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            line = tuple((x, y, z) for z in range(BOARD_SIZE))
            lines.append(line)

    # ===== 5. DIAGONAL LINES (through planes, moving in X direction) =====
    # 8 lines total (4 starting positions × 2 Y directions)
    for y in range(BOARD_SIZE):
        # Moving right and up through planes
        line = tuple((i, y, i) for i in range(BOARD_SIZE))
        lines.append(line)

    for y in range(BOARD_SIZE):
        # Moving left and up through planes
        line = tuple((BOARD_SIZE - 1 - i, y, i) for i in range(BOARD_SIZE))
        lines.append(line)

    # ===== 6. DIAGONAL LINES (through planes, moving in Y direction) =====
    # 8 lines total (4 starting positions × 2 X directions)
    for x in range(BOARD_SIZE):
        # Moving back and up through planes
        line = tuple((x, i, i) for i in range(BOARD_SIZE))
        lines.append(line)

    for x in range(BOARD_SIZE):
        # Moving forward and up through planes
        line = tuple((x, BOARD_SIZE - 1 - i, i) for i in range(BOARD_SIZE))
        lines.append(line)

    # ===== 7. 3D DIAGONAL LINES (corner to corner through entire cube) =====
    # 4 main body diagonals = 4 lines

    # Diagonal 1: (0,0,0) to (3,3,3) - main diagonal
    lines.append(tuple((i, i, i) for i in range(BOARD_SIZE)))

    # Diagonal 2: (3,0,0) to (0,3,3) - x decreases, y and z increase
    lines.append(tuple((BOARD_SIZE - 1 - i, i, i) for i in range(BOARD_SIZE)))

    # Diagonal 3: (0,3,0) to (3,0,3) - x and z increase, y decreases
    lines.append(tuple((i, BOARD_SIZE - 1 - i, i) for i in range(BOARD_SIZE)))

    # Diagonal 4: (3,3,0) to (0,0,3) - x and y decrease, z increases
    lines.append(tuple((BOARD_SIZE - 1 - i, BOARD_SIZE - 1 - i, i) for i in range(BOARD_SIZE)))

    return lines


def validate_winning_lines(lines):
    """
    Validate that we have exactly 76 unique winning lines.
    Each line should have exactly 4 positions.
    Returns (is_valid, message)
    """
    # Check total count
    if len(lines) != 76:
        return False, f"Expected 76 lines, got {len(lines)}"

    # Check for duplicates
    unique_lines = set(lines)
    if len(unique_lines) != 76:
        return False, f"Found duplicate lines. Unique count: {len(unique_lines)}"

    # Check each line has 4 positions
    for i, line in enumerate(lines):
        if len(line) != 4:
            return False, f"Line {i} has {len(line)} positions, expected 4"

        # Check all coordinates are valid
        for pos in line:
            x, y, z = pos
            if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 0 <= z < BOARD_SIZE):
                return False, f"Invalid coordinate {pos} in line {i}"

    return True, "All 76 winning lines validated successfully!"


def get_lines_containing_position(x, y, z):
    """
    Get all winning lines that pass through a specific position.
    This is used for efficient win checking - only check lines containing the last move.

    Args:
        x, y, z: Coordinate of the position

    Returns:
        List of winning lines containing this position
    """
    all_lines = WINNING_LINES
    return [line for line in all_lines if (x, y, z) in line]


# Generate and validate winning lines on module import
WINNING_LINES = generate_winning_lines()
is_valid, message = validate_winning_lines(WINNING_LINES)

if not is_valid:
    raise ValueError(f"Winning lines validation failed: {message}")

# Print validation message for confirmation
print(f"✓ {message}")


# Export count breakdown for reference
LINE_COUNTS = {
    "horizontal_in_plane": 16,
    "vertical_in_plane": 16,
    "diagonal_in_plane": 8,
    "vertical_through_planes": 16,
    "diagonal_through_planes_x": 8,
    "diagonal_through_planes_y": 8,
    "3d_corner_diagonals": 4,
    "total": 76
}
