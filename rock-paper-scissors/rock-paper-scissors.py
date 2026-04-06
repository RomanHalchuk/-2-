import random


class RockPaperScissors:
    DEFAULT_OPTIONS = ["rock", "paper", "scissors"]

    STATE_WAIT = "WAIT"
    STATE_PLAY = "PLAY"
    STATE_EXIT = "EXIT"

    def __init__(self, rating_file: str = "rating.txt"):
        self.rating_file = rating_file
        self.name = ""
        self.rating = 0
        self.options = self.DEFAULT_OPTIONS.copy()
        self.state = self.STATE_WAIT


    def load_rating(self) -> None:
        try:
            with open(self.rating_file, "r") as f:
                for line in f:
                    user, value = line.strip().split()
                    if user == self.name:
                        self.rating = int(value)
                        return
        except FileNotFoundError:
            pass
        self.rating = 0

    def setup_player(self) -> None:
        self.name = input("Enter your name:\n> ")
        print(f"Hello, {self.name}")
        self.load_rating()
        self.print_help()

    def print_help(self):
        print("Commands:")
        print("!start  - start game")
        print("!rating - show rating")
        print("!exit   - quit")
        print("Before start you can input custom options separated by command.")


    def set_options(self, raw: str) -> None:
        raw = raw.strip()
        if raw == "":
            self.options = self.DEFAULT_OPTIONS.copy()
        else:
            self.options = [x.strip() for x in raw.split(",")]


    def get_computer_choice(self) -> str:
        return random.choice(self.options)

    def computer_wins(self, user: str, computer: str) -> bool:
        idx = self.options.index(user)
        rotated = self.options[idx + 1:] + self.options[:idx]
        half = len(rotated) // 2
        return computer in rotated[:half]

    def process_round(self, user_choice: str) -> None:
        computer_choice = self.get_computer_choice()

        if computer_choice == user_choice:
            print(f"There is a draw ({computer_choice})")
            self.rating += 50
            return

        if self.computer_wins(user_choice, computer_choice):
            print(f"Sorry, but the computer chose {computer_choice}")
        else:
            print(f"Well done. The computer chose {computer_choice} and failed")
            self.rating += 100


    def handle_wait_state(self, user_input: str):
        if user_input == "!help":
            self.print_help()

        elif user_input == "!rating":
            print(f"Your rating: {self.rating}")

        elif user_input == "!exit":
            print("Bye!")
            self.state = self.STATE_EXIT

        elif user_input == "!start":
            print("Okay, let's start")
            self.state = self.STATE_PLAY

        else:
            self.set_options(user_input)
            print("Options updated.")

    def handle_play_state(self, user_input: str):
        if user_input == "!exit":
            print("Bye!")
            self.state = self.STATE_EXIT

        elif user_input == "!rating":
            print(f"Your rating: {self.rating}")

        elif user_input in self.options:
            self.process_round(user_input)

        else:
            print("Invalid input")


    def run(self):
        self.setup_player()

        while self.state != self.STATE_EXIT:
            user_input = (input("> ").strip())

            if self.state == self.STATE_WAIT:
                self.handle_wait_state(user_input)
            elif self.state == self.STATE_PLAY:
                self.handle_play_state(user_input)



if __name__ == "__main__":
    game = RockPaperScissors()
    game.run()