import random


class MathChallenge:
    def __init__(self):
        self.options = {
            1: "простые операции с числами от 2 до 9",
            2: "возведение в квадрат чисел от 11 до 29"
        }
        self.correct_count = 0
        self.current_lv = None

    def select_mode(self):
        while True:
            print("Выберите уровень сложности:")
            for k, v in self.options.items():
                print(f"{k} - {v}")

            user_input = input("> ").strip()
            if user_input in ("1", "2"):
                self.current_lv = int(user_input)
                break
            print("Ошибка формата. Введите 1 или 2.")

    def create_question(self):
        if self.current_lv == 1:
            val1 = random.randint(2, 9)
            val2 = random.randint(2, 9)
            sign = random.choice(["+", "-", "*"])
            expr = f"{val1} {sign} {val2}"
            return expr, eval(expr)
        else:
            num = random.randint(11, 29)
            return str(num), num ** 2

    def capture_input(self):
        while True:
            try:
                return int(input("> "))
            except ValueError:
                print("Требуется ввести целое число.")

    def export_data(self):
        print("Желаете сохранить результат в файл? (yes/no)")
        answer = input("> ").lower()
        if answer in ("yes", "y", "да"):
            username = input("Ваше имя: > ")
            # Добавляем пустую строку в конце записи, как просил преподаватель
            with open("results.txt", "a", encoding="utf-8") as out:
                record = (f"{username}: {self.correct_count}/5 на уровне {self.current_lv} "
                          f"({self.options[self.current_lv]}).\n")
                out.write(record)
            print("Данные записаны в 'results.txt'.")

    def start_session(self):
        while True:
            self.correct_count = 0
            self.select_mode()

            for _ in range(5):
                question, valid_res = self.create_question()
                print(question)
                if self.capture_input() == valid_res:
                    print("Верно!")
                    self.correct_count += 1
                else:
                    print("Ошибка!")

            print(f"Ваш результат: {self.correct_count}/5.")
            self.export_data()

            # Исправление: предлагаем продолжить или выбрать другой уровень
            print("\nХотите попробовать еще раз или выбрать другой уровень? (yes/no)")
            next_step = input("> ").lower()
            if next_step not in ("yes", "y", "да"):
                print("Программа завершена.")
                break


if __name__ == "__main__":
    app = MathChallenge()
    app.start_session()