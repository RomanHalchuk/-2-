import random

def get_initial_pencils():
    """Запитує кількість олівців від користувача"""
    while True:
        pencils = input("How many pencils would you like to use:\n> ")
        if not pencils.isdigit():
            print("The number of pencils should be numeric")
            continue

        pencils = int(pencils)
        if pencils <= 0:
            print("The number of pencils should be positive")
            continue

        return pencils


def get_first_player(players):
    """Запитує, хто ходить першим"""
    while True:
        first = input(f"Who will be the first ({', '.join(players)})?\n> ")
        if first not in players:
            print(f"Choose between {', '.join(players)}")
            continue
        return first


def bot_move(pencils_left):
    """Розрахунок ходу бота по виграшній стратегії"""
    if pencils_left % 4 == 0:
        return 3
    elif pencils_left % 4 == 3:
        return 2
    elif pencils_left % 4 == 2:
        return 1
    else:
        return random.randint(1, 3)


def player_move(pencils_left):
    """Хід користувача з перевіркою правильності введення"""
    while True:
        move = input("> ")
        if move not in ('1', '2', '3'):
            print("Possible values: '1', '2' or '3'")
            continue

        move = int(move)
        if move > pencils_left:
            print("Too many pencils were taken")
            continue

        return move


def game():
    players = ["John", "Jack"]  # John - гравець, Jack - бот
    pencils = get_initial_pencils()
    current_player = get_first_player(players)

    print("|" * pencils)
    while pencils > 0:
        print(f"{current_player}'s turn!")

        if current_player == "Jack":  # бот
            move = bot_move(pencils)
            print(move)
        else:  # гравець
            move = player_move(pencils)

        pencils -= move
        if pencils == 0:
            winner = players[1] if current_player == players[0] else players[0]
            print(f"{winner} won!")
            break

        print("|" * pencils)
        current_player = players[1] if current_player == players[0] else players[0]


if __name__ == "__main__":
    game()
