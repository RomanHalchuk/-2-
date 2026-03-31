class CoffeeMachine:
    """
    Клас, що імітує роботу кавомашини.
    Керується через стан (state).
    """

    def __init__(self):
        # Ініціалізація початкових ресурсів
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        # Початковий стан машини
        self.state = "action"

    def _safe_int_conversion(self, text):
        """Допоміжний метод: намагається перетворити текст на число."""
        try:
            return int(text)
        except ValueError:
            print("Будь ласка, введіть коректне число!")
            return None

    def handle_input(self, user_input):
        """
        Головний розподільник команд.
        Залежно від поточного стану (self.state) викликає потрібний метод.
        """
        if self.state == "action":
            self.main_menu_handler(user_input)
        elif self.state == "buy":
            self.buy_coffee(user_input)
        elif self.state.startswith("fill"):
            self.fill_resources(user_input)

    def main_menu_handler(self, action):
        """Обробляє основні команди головного меню."""
        if action == "buy":
            self.state = "buy"
            print("Що бажаєте купити? 1 - еспресо, 2 - лате, 3 - капучино, back – назад:")

        elif action == "fill":
            self.state = "fill_water"
            print("Скільки мл води ви хочете додати:")

        elif action == "take":
            print(f"Я видала вам ${self.money}")
            self.money = 0

        elif action == "remaining":
            self.display_status()

        elif action == "exit":
            self.state = "exit"

        else:
            print("Невідома команда. Виберіть: buy, fill, take, remaining, exit.")

    def buy_coffee(self, choice):
        """Логіка купівлі та приготування кави."""
        if choice == "back":
            self.state = "action"
            return

        # Рецепти напоїв
        recipes = {
            "1": {"water": 250, "milk": 0, "beans": 16, "cost": 4},   # Еспресо
            "2": {"water": 350, "milk": 75, "beans": 20, "cost": 7},   # Лате
            "3": {"water": 200, "milk": 100, "beans": 12, "cost": 6},  # Капучино
        }

        drink = recipes.get(choice)
        if not drink:
            print("Немає такого варіанту.")
            self.state = "action"
            return

        # Перевірка ресурсів перед приготуванням
        if self.water < drink["water"]:
            print("Вибачте, не вистачає води!")
        elif self.milk < drink["milk"]:
            print("Вибачте, не вистачає молока!")
        elif self.beans < drink["beans"]:
            print("Вибачте, не вистачає зерен!")
        elif self.cups < 1:
            print("Вибачте, закінчилися стаканчики!")
        else:
            # Списуємо ресурси та додаємо гроші
            self.water -= drink["water"]
            self.milk -= drink["milk"]
            self.beans -= drink["beans"]
            self.cups -= 1
            self.money += drink["cost"]
            print("Ресурсів достатньо, готую вашу каву!")

        # Повертаємось у головне меню
        self.state = "action"

    def fill_resources(self, amount):
        """
        Покрокове поповнення запасів.
        Стан змінюється за ланцюжком: вода -> молоко -> зерна -> стаканчики.
        """
        value = self._safe_int_conversion(amount)
        if value is None:
            return

        if self.state == "fill_water":
            self.water += value
            self.state = "fill_milk"
            print("Скільки мл молока додати:")

        elif self.state == "fill_milk":
            self.milk += value
            self.state = "fill_beans"
            print("Скільки грамів зерен додати:")

        elif self.state == "fill_beans":
            self.beans += value
            self.state = "fill_cups"
            print("Скільки стаканчиків додати:")

        elif self.state == "fill_cups":
            self.cups += value
            self.state = "action"  # Завершили поповнення, повернення в меню

    def display_status(self):
        """Вивід поточних запасів машини."""
        print("\nСтан кавомашини:")
        print(f"{self.water} мл води")
        print(f"{self.milk} мл молока")
        print(f"{self.beans} г кавових зерен")
        print(f"{self.cups} одноразових стаканчиків")
        print(f"${self.money} грошей всередині\n")


# --- Запуск програми ---
machine = CoffeeMachine()

while machine.state != "exit":
    if machine.state == "action":
        print("Виберіть дію (buy, fill, take, remaining, exit):")

    user_inp = input("> ")
    machine.handle_input(user_inp)