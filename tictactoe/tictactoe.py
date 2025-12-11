def print_board(board):
    """Виводить ігрове поле на екран"""
    print("---------")
    for row in board:
        print(f"| {' '.join(row)} |")
    print("---------")


def check_state(board):
    """Перевіряє поточний стан гри"""
    lines = [
        # Рядки
        *board,
        # Стовпці
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Діагоналі
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    x_wins = any(line == ["X"]*3 for line in lines)
    o_wins = any(line == ["O"]*3 for line in lines)
    empty_cells = any("_" in row for row in board)

    if x_wins and o_wins:
        return "Impossible"
    if x_wins:
        return "X wins"
    if o_wins:
        return "O wins"
    if empty_cells:
        return "Game not finished"
    return "Draw"


def valid_coordinates(coords):
    """Перевіряє, що координати — два числа від 1 до 3"""
    try:
        x, y = map(int, coords.split())
        return 1 <= x <= 3 and 1 <= y <= 3
    except (ValueError, TypeError):
        return False


def make_move(board, player):
    """Зчитує координати від гравця і робить хід"""
    while True:
        print(f"\nХід гравця: {player}")
        coords = input("Введіть координати (рядок і стовпець через пробіл):\n> ")

        if not valid_coordinates(coords):
            print("Координати повинні бути два числа від 1 до 3!")
            continue

        row, col = map(lambda x: int(x) - 1, coords.split())

        if board[row][col] != "_":
            print("Ця клітинка вже зайнята! Оберіть іншу!")
            continue

        board[row][col] = player
        break


def main():
    board = [["_"]*3 for _ in range(3)]
    print_board(board)

    current_player = "X"

    while True:
        make_move(board, current_player)
        print_board(board)

        state = check_state(board)
        if state in ["X wins", "O wins", "Draw"]:
            print(state)
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()
