#ifndef CONSOLE_RENDERER_H
#define CONSOLE_RENDERER_H

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread> // For std::this_thread::sleep_for

// Platform-specific includes for console manipulation and input
#ifdef _WIN32
#include <windows.h> // For console handles, cursor positioning, colors
#include <conio.h>   // For _kbhit and _getch (non-blocking input)
#else
// For Linux/macOS, you'd typically use termios for non-blocking input
// and ANSI escape codes for console manipulation.
// This example primarily focuses on Windows for simplicity due to
// the "single file" and "basic" requirements.
// A full cross-platform solution would be significantly more complex
// for a single header without external dependencies like ncurses.
#endif

// --- Game Data Structures (Simplified for Renderer's needs) ---
// These structs define the data that the renderer needs to display.
// In a larger project, these would likely reside in separate game logic files.

// Defines different types of blocks, primarily used for color representation.
enum class BlockType : int {
    Empty = 0, // Represents an empty space, typically rendered as background color
    I = 1,     // Cyan
    O = 2,     // Yellow
    T = 3,     // Magenta
    S = 4,     // Green
    Z = 5,     // Red
    J = 6,     // Blue
    L = 7,     // Orange/White (depending on console capabilities)
    Border = 8 // For drawing game board borders
};

// Represents a 2D point on the console grid.
struct Point {
    int x;
    int y;

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// Represents the shape of a Tetromino (e.g., a 4x4 grid of blocks).
struct TetrominoShape {
    std::vector<std::vector<BlockType>> data; // e.g., a 4x4 matrix

    // Default constructor for an empty 4x4 shape.
    TetrominoShape() : data(4, std::vector<BlockType>(4, BlockType::Empty)) {}

    // Constructor to initialize with specific shape data.
    TetrominoShape(const std::vector<std::vector<BlockType>>& shapeData) : data(shapeData) {}
};

// Represents a Tetromino instance, including its shape, position, and type.
struct Tetromino {
    TetrominoShape shape;
    Point position; // Top-left corner of the Tetromino's bounding box on the board.
    BlockType type; // The type/color of the blocks that make up this Tetromino.

    Tetromino(const TetrominoShape& s, Point p, BlockType t)
        : shape(s), position(p), type(t) {}
};

// --- Input Commands ---
// Defines the possible actions a player can take via input.
enum class InputCommand {
    None,       // No input detected
    MoveLeft,
    MoveRight,
    Rotate,     // Rotate Tetromino
    Drop,       // Hard drop (instant fall)
    SoftDrop,   // Accelerate fall
    Quit        // Exit the game
};

// --- Console Renderer Class ---
// Handles all console output and input capture.
class ConsoleRenderer {
public:
    // Constants for the game board dimensions.
    static const int BOARD_WIDTH = 10;
    static const int BOARD_HEIGHT = 20;
    static const int TETROMINO_PREVIEW_SIZE = 4; // Tetromino shapes are typically 4x4.

    ConsoleRenderer() {
#ifdef _WIN32
        hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        // Store original console mode to restore later.
        // This is important for clean shutdown, though _kbhit/_getch
        // don't typically require extensive mode changes.
        GetConsoleMode(hConsole, &originalConsoleMode);
#else
        // For Linux/macOS, you would typically set the terminal to raw mode
        // using termios to get non-blocking, non-echoing input.
        // struct termios oldt, newt;
        // tcgetattr(STDIN_FILENO, &oldt);
        // newt = oldt;
        // newt.c_lflag &= ~(ICANON | ECHO); // Disable canonical mode and echoing
        // tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        // originalTermios = oldt; // Store to restore later
#endif
        clearScreen();
        setCursorPosition(0, 0);
        std::cout << "Initializing ConsoleRenderer..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    ~ConsoleRenderer() {
#ifdef _WIN32
        // Restore original console mode settings.
        SetConsoleMode(hConsole, originalConsoleMode);
#else
        // Restore original terminal settings.
        // tcsetattr(STDIN_FILENO, TCSANOW, &originalTermios);
#endif
        clearScreen();
        setCursorPosition(0, 0);
        std::cout << "ConsoleRenderer shutdown." << std::endl;
    }

    // Clears the entire console screen.
    void clearScreen() {
#ifdef _WIN32
        COORD coordScreen = { 0, 0 };
        DWORD cCharsWritten;
        CONSOLE_SCREEN_BUFFER_INFO csbi;
        DWORD dwConSize;

        // Get the number of character cells in the current buffer.
        if (!GetConsoleScreenBufferInfo(hConsole, &csbi)) return;
        dwConSize = csbi.dwSize.X * csbi.dwSize.Y;

        // Fill the entire screen with blanks.
        if (!FillConsoleOutputCharacter(hConsole, (TCHAR)' ',
            dwConSize, coordScreen, &cCharsWritten)) return;

        // Get the current text attribute.
        if (!GetConsoleScreenBufferInfo(hConsole, &csbi)) return;

        // Set the buffer's attributes accordingly.
        if (!FillConsoleOutputAttribute(hConsole, csbi.wAttributes,
            dwConSize, coordScreen, &cCharsWritten)) return;

        // Put the cursor at its top-left.
        SetConsoleCursorPosition(hConsole, coordScreen);
#else
        // ANSI escape code for clearing screen and moving cursor to home.
        std::cout << "\033[2J\033[H";
#endif
    }

    // Sets the console cursor position (0-indexed).
    void setCursorPosition(int x, int y) {
#ifdef _WIN32
        cursorCoord.X = x;
        cursorCoord.Y = y;
        SetConsoleCursorPosition(hConsole, cursorCoord);
#else
        // ANSI escape code for setting cursor position (row;column).
        // ANSI is 1-indexed, so add 1 to x and y.
        std::cout << "\033[" << y + 1 << ";" << x + 1 << "H";
#endif
    }

    // Sets the console text color based on BlockType.
    void setConsoleColor(BlockType type) {
#ifdef _WIN32
        WORD color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE; // Default white
        switch (type) {
            case BlockType::Empty: color = 0; break; // Black (default background)
            case BlockType::I: color = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_INTENSITY; break; // Cyan
            case BlockType::O: color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY; break; // Yellow
            case BlockType::T: color = FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY; break; // Magenta
            case BlockType::S: color = FOREGROUND_GREEN | FOREGROUND_INTENSITY; break; // Green
            case BlockType::Z: color = FOREGROUND_RED | FOREGROUND_INTENSITY; break; // Red
            case BlockType::J: color = FOREGROUND_BLUE | FOREGROUND_INTENSITY; break; // Blue
            case BlockType::L: color = FOREGROUND_RED | FOREGROUND_INTENSITY | FOREGROUND_GREEN; break; // Orange-ish (Yellow + Red)
            case BlockType::Border: color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE; break; // White for borders
            default: color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE; break; // Default to white
        }
        SetConsoleTextAttribute(hConsole, color);
#else
        // ANSI escape codes for colors.
        std::string colorCode;
        switch (type) {
            case BlockType::Empty: colorCode = "0"; break; // Reset to default
            case BlockType::I: colorCode = "36"; break; // Cyan
            case BlockType::O: colorCode = "33"; break; // Yellow
            case BlockType::T: colorCode = "35"; break; // Magenta
            case BlockType::S: colorCode = "32"; break; // Green
            case BlockType::Z: colorCode = "31"; break; // Red
            case BlockType::J: colorCode = "34"; break; // Blue
            case BlockType::L: colorCode = "33;1"; break; // Bright Yellow (closest to orange)
            case BlockType::Border: colorCode = "37"; break; // White
            default: colorCode = "37"; break; // White
        }
        std::cout << "\033[" << colorCode << "m";
#endif
    }

    // Draws a single block character at a given console coordinate.
    // Each game block is represented by two console characters for better aspect ratio.
    void drawBlock(int x, int y, BlockType type, const std::string& blockChar = "[]") {
        setCursorPosition(x, y);
        setConsoleColor(type);
        std::cout << blockChar;
        setConsoleColor(BlockType::Empty); // Reset color after drawing
    }

    // Draws the main game board, including its border.
    void drawBoard(const std::vector<std::vector<BlockType>>& board) {
        // Draw top and bottom borders
        setConsoleColor(BlockType::Border);
        for (int i = 0; i < BOARD_WIDTH * 2 + 2; ++i) {
            setCursorPosition(i, 0);
            std::cout << "#";
            setCursorPosition(i, BOARD_HEIGHT + 1);
            std::cout << "#";
        }
        // Draw left and right borders
        for (int i = 0; i < BOARD_HEIGHT + 2; ++i) {
            setCursorPosition(0, i);
            std::cout << "#";
            setCursorPosition(BOARD_WIDTH * 2 + 1, i);
            std::cout << "#";
        }
        setConsoleColor(BlockType::Empty); // Reset color

        // Draw board content
        for (int y = 0; y < BOARD_HEIGHT; ++y) {
            for (int x = 0; x < BOARD_WIDTH; ++x) {
                // Offset by 1 for border, and x*2 for 2-char wide blocks
                drawBlock(x * 2 + 1, y + 1, board[y][x], "  ");
            }
        }
    }

    // Draws a Tetromino (either the current falling one or the next preview).
    void drawTetromino(const Tetromino& tetromino) {
        for (int y = 0; y < TETROMINO_PREVIEW_SIZE; ++y) {
            for (int x = 0; x < TETROMINO_PREVIEW_SIZE; ++x) {
                if (tetromino.shape.data[y][x] != BlockType::Empty) {
                    // Adjust position for board coordinates (offset by 1 for border)
                    drawBlock((tetromino.position.x + x) * 2 + 1,
                              tetromino.position.y + y + 1,
                              tetromino.type, "[]");
                }
            }
        }
    }

    // Draws the next Tetromino in a separate preview area to the right of the board.
    void drawNextTetromino(const Tetromino& nextTetromino) {
        int startX = BOARD_WIDTH * 2 + 5; // Offset from main board
        int startY = 2;

        setCursorPosition(startX, startY - 1);
        setConsoleColor(BlockType::Border);
        std::cout << "NEXT:";
        setConsoleColor(BlockType::Empty);

        // Draw the 4x4 preview area, clearing previous blocks if any
        for (int y = 0; y < TETROMINO_PREVIEW_SIZE; ++y) {
            for (int x = 0; x < TETROMINO_PREVIEW_SIZE; ++x) {
                if (nextTetromino.shape.data[y][x] != BlockType::Empty) {
                    drawBlock(startX + x * 2, startY + y, nextTetromino.type, "[]");
                } else {
                    drawBlock(startX + x * 2, startY + y, BlockType::Empty, "  ");
                }
            }
        }
    }

    // Displays the player's score.
    void drawScore(int score) {
        int startX = BOARD_WIDTH * 2 + 5;
        int startY = TETROMINO_PREVIEW_SIZE + 5; // Below the next tetromino preview

        setCursorPosition(startX, startY);
        setConsoleColor(BlockType::Border);
        std::cout << "SCORE: " << score;
        setConsoleColor(BlockType::Empty);
    }

    // Main rendering function that orchestrates drawing all game elements.
    void render(const std::vector<std::vector<BlockType>>& board,
                const Tetromino& currentTetromino,
                const Tetromino& nextTetromino,
                int score) {
        // For a basic renderer, redrawing everything is simpler than
        // tracking and redrawing only changed areas, though it can cause flicker.
        // drawBoard already overwrites its area, so no full clear needed here.

        drawBoard(board);
        drawTetromino(currentTetromino);
        drawNextTetromino(nextTetromino);
        drawScore(score);

        // Ensure the cursor is moved out of the game area to prevent interference
        setCursorPosition(0, BOARD_HEIGHT + 3);
        std::cout.flush(); // Ensure all output is immediately written to console
    }

    // Captures user keyboard input.
    InputCommand getInput() {
#ifdef _WIN32
        if (_kbhit()) { // Check if a key has been pressed
            int key = _getch(); // Read the character without echoing it to console
            if (key == 0 || key == 0