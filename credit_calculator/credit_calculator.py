import math
import argparse


class CreditCalculator:
    def __init__(self, args):
        self.type = args.type
        self.principal = args.principal
        self.payment = args.payment
        self.periods = args.periods
        self.interest = args.interest

        if self.interest is None or self.interest <= 0:
            print("Incorrect parameters")
            exit()

        self.i = self.interest / (12 * 100)

    def calc_annuity_payment(self):
        a = self.principal * (self.i * (1 + self.i) ** self.periods) / (
            (1 + self.i) ** self.periods - 1
        )
        a = math.ceil(a)
        print(f"Your annuity payment = {a}!")
        print(f"Overpayment = {int(a * self.periods - self.principal)}")

    def calc_principal(self):
        p = self.payment / (
            (self.i * (1 + self.i) ** self.periods) / ((1 + self.i) ** self.periods - 1)
        )
        p = math.floor(p)
        print(f"Your loan principal = {p}!")
        print(f"Overpayment = {int(self.payment * self.periods - p)}")

    def calc_periods(self):
        n = math.log(self.payment / (self.payment - self.i * self.principal), 1 + self.i)
        n = math.ceil(n)

        years = n // 12
        months = n % 12

        parts = []
        if years > 0:
            parts.append(f"{years} year" if years == 1 else f"{years} years")
        if months > 0:
            parts.append(f"{months} month" if months == 1 else f"{months} months")

        print(f"It will take {' and '.join(parts)} to repay this loan!")
        print(f"Overpayment = {int(self.payment * n - self.principal)}")

    def calc_diff(self):
        total = 0
        for m in range(1, self.periods + 1):
            d = self.principal / self.periods + self.i * (
                self.principal - self.principal * (m - 1) / self.periods
            )
            d = math.ceil(d)
            total += d
            print(f"Month {m}: payment is {d}")
        print(f"Overpayment = {int(total - self.principal)}")

    def validate(self):
        params = [self.principal, self.payment, self.periods, self.interest]
        if any(x is not None and x < 0 for x in params):
            return False

        if self.type == "diff" and self.payment is not None:
            return False

        count = sum(x is not None for x in [self.principal, self.payment, self.periods])
        if count < 2:
            return False

        return True

    def run(self):
        if not self.validate():
            print("Incorrect parameters")
            return

        if self.type == "annuity":
            if self.payment is None:
                self.calc_annuity_payment()
            elif self.principal is None:
                self.calc_principal()
            elif self.periods is None:
                self.calc_periods()

        elif self.type == "diff":
            self.calc_diff()
        else:
            print("Incorrect parameters")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--type", choices=["annuity", "diff"])
    parser.add_argument("--principal", type=float)
    parser.add_argument("--payment", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    args = parser.parse_args()

    calc = CreditCalculator(args)
    calc.run()