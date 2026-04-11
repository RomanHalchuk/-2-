import random


class GameEngine:
    BASE_SET = ["rock", "paper", "scissors"]

    # Состояния системы
    MODE_PREPARE = 0
    MODE_ACTIVE = 1
    MODE_SHUTDOWN = 2

    def __init__(self, data_file: str = "rating.txt"):
        self.source = data_file
        self.user_id = ""
        self.points = 0
        self.actions = self.BASE_SET.copy()
        self.current_mode = self.MODE_PREPARE

    def _sync_points(self) -> None:
        """Загрузка очков из локального хранилища."""
        try:
            with open(self.source, "r", encoding="utf-8") as f:
                for entry in f:
                    uid, val = entry.strip().split()
                    if uid == self.user_id:
                        self.points = int(val)
                        return
        except (FileNotFoundError, ValueError):
            pass
        self.points = 0

    def initialize_session(self) -> None:
        self.user_id = input("Введите ваш логин:\n> ").strip()
        print(f"Приветствуем, {self.user_id}!")
        self._sync_points()
        self.display_manual()

    def display_manual(self):
        print("Доступные команды:")
        print("!start  - запуск игровой сессии")
        print("!rating - текущий счет")
        print("!exit   - завершение работы")
        print("Вы также можете задать свой набор вариантов через запятую до начала игры.")

    def update_rules(self, raw_data: str) -> None:
        cleaned = raw_data.strip()
        if not cleaned:
            self.actions = self.BASE_SET.copy()
        else:
            self.actions = [item.strip() for item in cleaned.split(",")]
        print("Параметры игры обновлены.")

    def _evaluate_win(self, p_choice: str, c_choice: str) -> bool:
        """Определяет, выиграл ли компьютер по круговой системе."""
        pos = self.actions.index(p_choice)
        # Сдвигаем список, чтобы текущий выбор игрока стал точкой отсчета
        reordered = self.actions[pos + 1:] + self.actions[:pos]
        # В кастомных правилах проигрышными считаются первые пол-списка после выбора игрока
        loss_zone = len(reordered) // 2
        return c_choice in reordered[:loss_zone]

    def execute_round(self, p_move: str) -> None:
        c_move = random.choice(self.actions)

        if c_move == p_move:
            print(f"Ничья ({c_move})")
            self.points += 50
        elif self._evaluate_win(p_move, c_move):
            print(f"Компьютер победил, выбрав {c_move}")
        else:
            print(f"Победа! Компьютер выбрал {c_move} и проиграл")
            self.points += 100

    def _process_logic(self, val: str):
        # Общие команды для любого состояния
        if val == "!exit":
            print("Сессия завершена.")
            self.current_mode = self.MODE_SHUTDOWN
            return

        if val == "!rating":
            print(f"Ваш текущий баланс: {self.points}")
            return

        # Логика режима ожидания
        if self.current_mode == self.MODE_PREPARE:
            if val == "!help":
                self.display_manual()
            elif val == "!start":
                print("Игра началась. Удачи!")
                self.current_mode = self.MODE_ACTIVE
            else:
                self.update_rules(val)

        # Логика активной игры
        elif self.current_mode == self.MODE_ACTIVE:
            if val in self.actions:
                self.execute_round(val)
            else:
                print("Некорректный ввод. Выберите вариант из списка или !exit.")

    def start(self):
        self.initialize_session()

        while self.current_mode != self.MODE_SHUTDOWN:
            raw_input = input("> ").strip()
            if not raw_input:
                continue
            self._process_logic(raw_input)


if __name__ == "__main__":
    core = GameEngine()
    core.start()