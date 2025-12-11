import random

WORDS = ['python', 'java', 'javascript', 'php']
MAX_ATTEMPTS = 8


def display_hidden_word(hidden_word):
    """Выводит текущее состояние загаданного слова"""
    print(''.join(hidden_word))


def get_letter_input(guessed_letters):
    """Получает корректный ввод буквы от пользователя"""
    while True:
        letter = input('Input a letter: > ').strip()

        if len(letter) != 1:
            print('You should input a single letter')
        elif not letter.isalpha() or not letter.islower():
            print('Please enter a lowercase English letter')
        elif letter in guessed_letters:
            print("You've already guessed this letter")
        else:
            return letter


def play_game():
    word = random.choice(WORDS)
    hidden_word = ['-' for _ in word]
    guessed_letters = set()
    attempts = MAX_ATTEMPTS

    while attempts > 0:
        print()
        display_hidden_word(hidden_word)
        letter = get_letter_input(guessed_letters)
        guessed_letters.add(letter)

        if letter in word:
            if letter in hidden_word:
                print('No improvements')
            else:
                for i, char in enumerate(word):
                    if char == letter:
                        hidden_word[i] = letter
        else:
            print("That letter doesn't appear in the word")
            attempts -= 1

        if '-' not in hidden_word:
            print(f'You guessed the word {word}!')
            print('You survived!')
            return

    print('You lost!')


def main():
    print('HANGMAN')
    while True:
        command = input('Type "play" to play the game, "exit" to quit: > ').strip()
        if command == 'play':
            play_game()
        elif command == 'exit':
            break


if __name__ == '__main__':
    main()
