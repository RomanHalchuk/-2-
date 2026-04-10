import math
import argparse
import sys


class FinanceProcessor:
    def __init__(self, config):
        self.mode = config.type
        self.loan_sum = config.principal
        self.monthly_pay = config.payment
        self.duration = config.periods
        self.rate = config.interest

        # Проверка базовой валидности процентной ставки
        if self.rate is None or self.rate <= 0:
            print("Ошибка: параметры указаны неверно.")
            sys.exit()

        # Расчет месячного коэффициента
        self.base_rate = self.rate / (12 * 100)

    def _get_overpayment(self, total_paid, initial_sum):
        return int(total_paid - initial_sum)

    def solve_annuity(self):
        # Расчет ежемесячного взноса
        factor = (1 + self.base_rate) ** self.duration
        val = self.loan_sum * (self.base_rate * factor) / (factor - 1)
        val = math.ceil(val)
        print(f"Ваш ежемесячный аннуитетный платеж составит {val}.")
        print(f"Переплата по кредиту: {self._get_overpayment(val * self.duration, self.loan_sum)}")

    def solve_loan_body(self):
        # Расчет тела кредита
        factor = (1 + self.base_rate) ** self.duration
        val = self.monthly_pay / ((self.base_rate * factor) / (factor - 1))
        val = math.floor(val)
        print(f"Основная сумма займа: {val}.")
        print(f"Переплата по кредиту: {self._get_overpayment(self.monthly_pay * self.duration, val)}")

    def solve_timeframe(self):
        # Расчет срока погашения
        log_val = self.monthly_pay / (self.monthly_pay - self.base_rate * self.loan_sum)
        total_months = math.ceil(math.log(log_val, 1 + self.base_rate))

        y, m = divmod(total_months, 12)
        time_desc = []
        if y > 0:
            time_desc.append(f"{y} {'год' if y == 1 else 'года' if 2 <= y <= 4 else 'лет'}")
        if m > 0:
            time_desc.append(f"{m} {'месяц' if m == 1 else 'месяца' if 2 <= m <= 4 else 'месяцев'}")

        print(f"Срок выплаты составит {' и '.join(time_desc)}.")
        print(f"Переплата по кредиту: {self._get_overpayment(self.monthly_pay * total_months, self.loan_sum)}")

    def solve_differential(self):
        # Дифференцированные платежи
        cumulative = 0
        for month_idx in range(1, self.duration + 1):
            term = self.loan_sum * (month_idx - 1) / self.duration
            current_pay = (self.loan_sum / self.duration) + self.base_rate * (self.loan_sum - term)
            current_pay = math.ceil(current_pay)
            cumulative += current_pay
            print(f"Месяц {month_idx}: платеж — {current_pay}")

        print(f"Переплата по кредиту: {self._get_overpayment(cumulative, self.loan_sum)}")

    def check_validity(self):
        # Комплексная проверка входных данных
        core_params = [self.loan_sum, self.monthly_pay, self.duration, self.rate]
        if any(p is not None and p < 0 for p in core_params):
            return False

        if self.mode == "diff" and self.monthly_pay is not None:
            return False

        needed_args = [self.loan_sum, self.monthly_pay, self.duration]
        if sum(1 for x in needed_args if x is not None) < 2:
            return False

        return True

    def execute(self):
        if not self.check_validity():
            print("Ошибка: параметры указаны неверно.")
            return

        if self.mode == "annuity":
            if self.monthly_pay is None:
                self.solve_annuity()
            elif self.loan_sum is None:
                self.solve_loan_body()
            elif self.duration is None:
                self.solve_timeframe()
        elif self.mode == "diff":
            self.solve_differential()
        else:
            print("Ошибка: тип расчета не определен.")


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description="Кредитный калькулятор (аналитический модуль)")

    cli_parser.add_argument("--type", choices=["annuity", "diff"], help="Тип платежей")
    cli_parser.add_argument("--principal", type=float, help="Сумма кредита")
    cli_parser.add_argument("--payment", type=float, help="Ежемесячный платеж")
    cli_parser.add_argument("--periods", type=int, help="Количество месяцев")
    cli_parser.add_argument("--interest", type=float, help="Годовая процентная ставка")

    user_args = cli_parser.parse_args()
    engine = FinanceProcessor(user_args)
    engine.execute()