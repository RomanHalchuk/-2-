class LinearAlgebraTool:
    def __init__(self, table):
        self.table = table
        self.h = len(table)
        self.w = len(table[0]) if self.h > 0 else 0

    def display(self):
        for line in self.table:
            # Печать с обрезкой лишних нулей после запятой
            print(' '.join(f"{round(val, 2):g}" for val in line))

    def sum_with(self, other_obj):
        if self.h != other_obj.h or self.w != other_obj.w:
            print("Ошибка: размеры не совпадают.")
            return None
        new_data = [[self.table[i][j] + other_obj.table[i][j] for j in range(self.w)]
                    for i in range(self.h)]
        return LinearAlgebraTool(new_data)

    def scale(self, factor):
        new_data = [[val * factor for val in line] for line in self.table]
        return LinearAlgebraTool(new_data)

    def dot_product(self, second):
        if self.w != second.h:
            print("Ошибка: невозможно перемножить данные таких форм.")
            return None
        res = [[sum(self.table[i][k] * second.table[k][j] for k in range(self.w))
                for j in range(second.w)] for i in range(self.h)]
        return LinearAlgebraTool(res)

    def transform(self, type_id=1):
        if type_id == 1:
            res = [[self.table[j][i] for j in range(self.h)] for i in range(self.w)]
        elif type_id == 2:
            res = [[self.table[self.h - 1 - j][self.w - 1 - i] for j in range(self.h)]
                   for i in range(self.w)]
        elif type_id == 3:
            res = [row[::-1] for row in self.table]
        elif type_id == 4:
            res = self.table[::-1]
        else:
            print("Тип трансформации не распознан.")
            return None
        return LinearAlgebraTool(res)

    def get_det(self):
        if self.h != self.w:
            print("Детерминант только для квадратных структур.")
            return None
        return self._compute_det(self.table)

    def _compute_det(self, mtx):
        size = len(mtx)
        if size == 1:
            return mtx[0][0]
        if size == 2:
            return mtx[0][0] * mtx[1][1] - mtx[0][1] * mtx[1][0]

        total = 0
        for col in range(size):
            sub_mtx = [row[:col] + row[col + 1:] for row in mtx[1:]]
            total += ((-1) ** col) * mtx[0][col] * self._compute_det(sub_mtx)
        return total

    def find_inverse(self):
        d = self.get_det()
        if d == 0 or d is None:
            print("Обратная форма не существует (определитель = 0).")
            return None

        n = self.h
        adj = []
        for r in range(n):
            row_adj = []
            for c in range(n):
                sub = [row[:c] + row[c + 1:] for i, row in enumerate(self.table) if i != r]
                row_adj.append(((-1) ** (r + c)) * self._compute_det(sub))
            adj.append(row_adj)

        final = [[adj[j][i] / d for j in range(n)] for i in range(n)]
        return LinearAlgebraTool(final)


def input_capture():
    while True:
        try:
            raw_size = input("Задайте размер (строки и столбцы через пробел): > ").split()
            r, c = map(int, raw_size)
            break
        except (ValueError, IndexError):
            print("Ошибка! Введите два целых числа.")

    content = []
    print(f"Введите значения для {r} строк:")
    for k in range(r):
        while True:
            row_vals = input(f"Строка {k + 1}: > ").split()
            if len(row_vals) != c:
                print(f"Ошибка! Нужно ровно {c} значений.")
                continue
            try:
                content.append([float(x) for x in row_vals])
                break
            except ValueError:
                print("Используйте только числовые значения.")
    return LinearAlgebraTool(content)


def run_app():
    while True:
        print("\n=== ВЫБОР ОПЕРАЦИИ ===")
        print("1. Сложение")
        print("2. Умножение на число")
        print("3. Перемножение двух матриц")
        print("4. Транспонирование")
        print("5. Вычисление детерминанта")
        print("6. Нахождение обратной матрицы")
        print("0. Выход")

        cmd = input("Номер действия: > ")

        if cmd == '1':
            m1 = input_capture()
            m2 = input_capture()
            res = m1.sum_with(m2)
            if res:
                print("Итоговая сумма:")
                res.display()

        elif cmd == '2':
            m = input_capture()
            # Защита от нечислового ввода константы
            while True:
                try:
                    val = float(input("Введите множитель: > "))
                    break
                except ValueError:
                    print("Ошибка: введите корректное число.")

            res = m.scale(val)
            print("Результат умножения:")
            res.display()

        elif cmd == '3':
            m1 = input_capture()
            m2 = input_capture()
            res = m1.dot_product(m2)
            if res:
                print("Результат произведения:")
                res.display()

        elif cmd == '4':
            print("Варианты: 1-Главная, 2-Побочная, 3-Вертикаль, 4-Горизонталь")
            try:
                t_type = int(input("Ваш выбор: > "))
                m = input_capture()
                res = m.transform(t_type)
                if res:
                    print("Результат:")
                    res.display()
            except ValueError:
                print("Ошибка: введите номер режима.")

        elif cmd == '5':
            m = input_capture()
            val = m.get_det()
            if val is not None:
                print(f"Определитель: {round(val, 4)}")

        elif cmd == '6':
            m = input_capture()
            res = m.find_inverse()
            if res:
                print("Обратная матрица:")
                res.display()

        elif cmd == '0':
            print("Программа завершена.")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    run_app()