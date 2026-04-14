#ifndef BOARD_H
#define BOARD_H

#include <vector>
#include <numeric>   // For std::iota, though not strictly needed for this implementation
#include <algorithm> // For std::all_of, std::fill, std::copy

// Interface for Tetromino that Board relies on.
// Any concrete Tetromino class must inherit from this interface
// to be used with the Board class. This allows for loose coupling.
class Tetromino {
public:
    // Returns the 4x4 shape of the tetromino. 0 for empty, non-zero for block.
    virtual const std::vector<std::vector<int>>& get_shape() const = 0;
    // Returns the x-coordinate (column) of the tetromino's top-left corner on the board.
    virtual int get_x() const = 0;
    // Returns the y-coordinate (row) of the tetromino's top-left corner on the board.
    virtual int get_y() const = 0;
    // Returns the integer ID representing the color/type of the tetromino's blocks.
    virtual int get_color_id() const = 0;
    // Returns the size of the square bounding box for the tetromino's shape (e.g., 4 for 4x4).
    virtual int get_size() const = 0;
    // Virtual destructor is crucial for polymorphic base classes.
    virtual ~Tetromino() = default;
};

class Board {
public:
    // Board dimensions
    static const int BOARD_ROWS = 20;
    static const int BOARD_COLS = 10;
    // Value representing an empty cell on the board
    static const int EMPTY_BLOCK = 0;

    // Constructor: Initializes the board grid with empty blocks.
    Board() {
        grid_.resize(BOARD_ROWS, std::vector<int>(BOARD_COLS, EMPTY_BLOCK));
    }

    // Resets the entire board, setting all cells to EMPTY_BLOCK.
    void reset() {
        for (int r = 0; r < BOARD_ROWS; ++r) {
            std::fill(grid_[r].begin(), grid_[r].end(), EMPTY_BLOCK);
        }
    }

    // Checks if a given Tetromino at the specified (x, y) position is valid.
    // A position is valid if all its blocks are within board boundaries
    // and do not collide with existing fixed blocks on the board.
    //
    // @param tetromino The Tetromino object to check.
    // @param x The x-coordinate (column) of the tetromino's top-left corner.
    // @param y The y-coordinate (row) of the tetromino's top-left corner.
    // @return True if the position is valid, false otherwise.
    bool is_valid_position(const Tetromino& tetromino, int x, int y) const {
        const auto& shape = tetromino.get_shape();
        int tetromino_size = tetromino.get_size();

        for (int r = 0; r < tetromino_size; ++r) {
            for (int c = 0; c < tetromino_size; ++c) {
                if (shape[r][c] != EMPTY_BLOCK) { // If there's a block in the tetromino's shape
                    int board_r = y + r;
                    int board_c = x + c;

                    // Check boundaries
                    if (!is_within_bounds(board_r, board_c)) {
                        return false;
                    }

                    // Check collision with existing blocks on the board
                    if (grid_[board_r][board_c] != EMPTY_BLOCK) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    // Places (fixes) the given Tetromino onto the board's grid at the specified (x, y) coordinates.
    // This method assumes that `is_valid_position` has already been called and returned true,
    // so no boundary or collision checks are performed here.
    //
    // @param tetromino The Tetromino object to place.
    // @param x The x-coordinate (column) of the tetromino's top-left corner.
    // @param y The y-coordinate (row) of the tetromino's top-left corner.
    void place_tetromino(const Tetromino& tetromino, int x, int y) {
        const auto& shape = tetromino.get_shape();
        int tetromino_size = tetromino.get_size();
        int color_id = tetromino.get_color_id();

        for (int r = 0; r < tetromino_size; ++r) {
            for (int c = 0; c < tetromino_size; ++c) {
                if (shape[r][c] != EMPTY_BLOCK) {
                    int board_r = y + r;
                    int board_c = x + c;
                    grid_[board_r][board_c] = color_id;
                }
            }
        }
    }

    // Clears any completed lines on the board and shifts blocks above them down.
    //
    // @return The number of lines that were cleared.
    int clear_lines() {
        int lines_cleared = 0;
        // Iterate from the bottom up to check for full rows
        for (int r = BOARD_ROWS - 1; r >= 0; --r) {
            if (is_row_full(r)) {
                remove_row(r);
                lines_cleared++;
                // After removing a row, the row above it shifts down to the current 'r' index.
                // To ensure this new row at 'r' is also checked (in case it's also full),
                // we increment 'r'. The loop's '--r' will then effectively re-check the same index.
                r++;
            }
        }
        return lines_cleared;
    }

    // Checks if the game is over.
    // This typically happens if a new Tetromino cannot be placed at its initial spawn position
    // due to existing blocks. A common heuristic is to check if the top-most rows
    // (e.g., row 0 or 1) contain any blocks.
    //
    // @return True if the game is over, false otherwise.
    bool is_game_over() const {
        // Game is over if any block exists in the top two rows (common spawn area).
        // Adjust this condition based on specific game rules if needed.
        for (int c = 0; c < BOARD_COLS; ++c) {
            if (grid_[0][c] != EMPTY_BLOCK || grid_[1][c] != EMPTY_BLOCK) {
                return true;
            }
        }
        return false;
    }

    // Returns a constant reference to the internal grid, useful for rendering or debugging.
    //
    // @return A const reference to the 2D vector representing the board grid.
    const std::vector<std::vector<int>>& get_grid() const { return grid_; }

private:
    // The 2D grid representing the game board.
    // Each cell stores an integer representing the block type/color,
    // or EMPTY_BLOCK if the cell is empty.
    std::vector<std::vector<int>> grid_;

    // Helper method to check if a given row and column are within the board's boundaries.
    //
    // @param r The row index.
    // @param c The column index.
    // @return True if (r, c) is within bounds, false otherwise.
    bool is_within_bounds(int r, int c) const {
        return r >= 0 && r < BOARD_ROWS && c >= 0 && c < BOARD_COLS;
    }

    // Helper method to check if a specific row is completely filled with blocks.
    //
    // @param row The row index to check.
    // @return True if the row is full, false otherwise.
    bool is_row_full(int row) const {
        // Use std::all_of to check if all cells in the row are not EMPTY_BLOCK.
        return std::all_of(grid_[row].begin(), grid_[row].end(),
                           [](int block_type){ return block_type != EMPTY_BLOCK; });
    }

    // Helper method to remove a specific row and shift all rows above it down by one.
    // The top-most row becomes empty after this operation.
    //
    // @param row The index of the row to remove.
    void remove_row(int row) {
        // Shift all rows above the given row down by one
        for (int r = row; r > 0; --r) {
            grid_[r] = grid_[r - 1]; // Copy the row above down
        }
        // Clear the top-most row (which is now empty after shifting)
        std::fill(grid_[0].begin(), grid_[0].end(), EMPTY_BLOCK);
    }
};

#endif // BOARD_H
