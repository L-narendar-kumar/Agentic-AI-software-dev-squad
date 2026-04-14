#pragma once

#include <array>
#include <vector>
#include <cstdint>   // For int8_t, uint8_t
#include <stdexcept> // For std::out_of_range

// Define Point struct for block coordinates
struct Point {
    int8_t x, y; // Using int8_t as coordinates are small (e.g., -3 to 3 for relative, 0 to 20 for absolute)
};

// Define Tetromino types
enum class TetrominoType : uint8_t {
    I = 0, O, T, S, Z, J, L,
    COUNT // Helper for array sizing, represents the number of Tetromino types
};

// Define Rotation states
enum class RotationState : uint8_t {
    R0 = 0, R90, R180, R270,
    COUNT // Helper for array sizing, represents the number of rotation states
};

// Helper to convert enum to int for array indexing
inline uint8_t to_int(TetrominoType type) { return static_cast<uint8_t>(type); }
inline uint8_t to_int(RotationState state) { return static_cast<uint8_t>(state); }

class Tetromino {
public:
    // Constructor: Initializes a Tetromino of a given type at a starting position.
    // boardWidth and boardHeight are needed for boundary checks.
    Tetromino(TetrominoType type, int startX, int startY, int boardWidth, int boardHeight);

    // Getters for current state
    TetrominoType getType() const { return _type; }
    int getX() const { return _x; }
    int getY() const { return _y; }
    RotationState getRotationState() const { return _rotationState; }

    // Returns the 4 blocks of the current shape, relative to the Tetromino's (x,y) pivot.
    // These are the local coordinates within the Tetromino's 4x4 or 3x3 bounding box.
    const std::array<Point, 4>& getCurrentShapeBlocks() const;

    // Returns the 4 blocks of the current shape, in absolute board coordinates.
    std::array<Point, 4> getAbsoluteBlocks() const;

    // Movement functions: Attempt to move the Tetromino.
    // Returns true if movement was successful, false if blocked by boundaries or other blocks.
    // 'board' represents the occupied cells on the game board (true = occupied).
    bool moveLeft(const std::vector<std::vector<bool>>& board);
    bool moveRight(const std::vector<std::vector<bool>>& board);
    bool moveDown(const std::vector<std::vector<bool>>& board);

    // Rotation functions: Attempt to rotate the Tetromino.
    // Returns true if rotation was successful, false if blocked.
    bool rotateClockwise(const std::vector<std::vector<bool>>& board);
    bool rotateCounterClockwise(const std::vector<std::vector<bool>>& board);

private:
    TetrominoType _type;
    int _x, _y; // Top-left corner of the Tetromino's bounding box on the game board
    RotationState _rotationState;

    int _boardWidth;
    int _boardHeight;

    // Static data for all Tetromino shapes and their rotation states.
    // SHAPE_DATA[TetrominoType][RotationState][BlockIndex]
    // Coordinates are relative to the top-left of a 4x4 (for I) or 3x3 (for others) bounding box.
    // The pivot for rotation is implicitly handled by these pre-calculated shapes.
    static const std::array<std::array<std::array<Point, 4>, to_int(RotationState::COUNT)>, to_int(TetrominoType::COUNT)> SHAPE_DATA;

    // Helper function to get the block configuration for a specific rotation state.
    const std::array<Point, 4>& _getShapeBlocks(RotationState rotation) const;

    // Helper function to check if a Tetromino at a given position and rotation
    // would be valid (within boundaries and not colliding with existing blocks).
    bool _isValidPosition(int testX, int testY, RotationState testRotation,
                          const std::vector<std::vector<bool>>& board) const;
};

// --- Static SHAPE_DATA Definition ---
// This static member definition must be in the header file as per the "single file" instruction.
// Coordinates are relative to the top-left of a 4x4 grid for all shapes.
const std::array<std::array<std::array<Point, 4>, to_int(RotationState::COUNT)>, to_int(TetrominoType::COUNT)> Tetromino::SHAPE_DATA = {
    // I-Tetromino
    {{
        // R0
        {{{ {0,1}, {1,1}, {2,1}, {3,1} }}},
        // R90
        {{{ {2,0}, {2,1}, {2,2}, {2,3} }}},
        // R180
        {{{ {0,2}, {1,2}, {2,2}, {3,2} }}},
        // R270
        {{{ {1,0}, {1,1}, {1,2}, {1,3} }}},
    }},
    // O-Tetromino (all rotations are the same)
    {{
        // R0
        {{{ {1,1}, {2,1}, {1,2}, {2,2} }}},
        // R90
        {{{ {1,1}, {2,1}, {1,2}, {2,2} }}},
        // R180
        {{{ {1,1}, {2,1}, {1,2}, {2,2} }}},
        // R270
        {{{ {1,1}, {2,1}, {1,2}, {2,2} }}},
    }},
    // T-Tetromino
    {{
        // R0
        {{{ {0,1}, {1,1}, {2,1}, {1,0} }}},
        // R90
        {{{ {1