import random


class ArithmeticTest:
    def __init__(self):
        self.levels = {
            1: "simple operations with numbers 2-9",
            2: "integral squares of 11-29"
        }
        self.score = 0
        self.level = None

    def get_level(self):
        while True:
            print("Which level do you want? Enter a number:")
            print("1 - simple operations with numbers 2-9")
            print("2 - integral squares of 11-29")
            try:
                level = int(input("> "))
                if level in self.levels:
                    self.level = level
                    return
            except ValueError:
                pass
            print("Incorrect format.")

    def generate_task(self):
        if self.level == 1:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            op = random.choice(["+", "-", "*"])
            expression = f"{a} {op} {b}"
            return expression, eval(expression)
        else:
            n = random.randint(11, 29)
            return str(n), n * n

    def get_answer(self):
        while True:
            try:
                return int(input("> "))
            except ValueError:
                print("Incorrect format.")

    def save_result(self):
        decision = input(
            "Would you like to save your result to the file? Enter yes or no.\n> "
        )
        if decision.lower() in ("yes", "y"):
            name = input("What is your name?\n> ")
            with open("results.txt", "a") as file:
                file.write(
                    f"{name}: {self.score}/5 in level {self.level} "
                    f"({self.levels[self.level]}).\n"
                )
            print('The results are saved in "results.txt".')

    def run(self):
        self.get_level()

        for _ in range(5):
            task, correct_answer = self.generate_task()
            print(task)
            user_answer = self.get_answer()

            if user_answer == correct_answer:
                print("Right!")
                self.score += 1
            else:
                print("Wrong!")

        print(f"Your mark is {self.score}/5.")
        self.save_result()


if __name__ == "__main__":
    test = ArithmeticTest()
    test.run()