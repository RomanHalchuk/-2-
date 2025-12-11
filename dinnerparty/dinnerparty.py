import random


def get_friends():
    """Зчитування кількості друзів та їхніх імен."""
    num_friends = int(input("Enter the number of friends joining (including you):\n> "))
    if num_friends <= 0:
        print("No one is joining for the party")
        return {}, 0
    else:
        print("Enter the name of every friend (including you), each on a new line:")
        friends = {}
        for _ in range(num_friends):
            name = input()
            friends[name] = 0
        return friends, num_friends


def split_bill(friends, num_friends, total_amount):
    """Розподіл рахунку між друзями."""
    split_amount = round(total_amount / num_friends, 2)
    for friend in friends:
        friends[friend] = split_amount
    return friends


def apply_lucky_feature(friends, total_amount, num_friends):
    """Опція 'Щасливчик'."""
    use_lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')

    if use_lucky == "Yes":
        lucky_one = random.choice(list(friends.keys()))
        print(f"{lucky_one} is the lucky one!")
        split_amount = round(total_amount / (num_friends - 1), 2)
        for friend in friends:
            friends[friend] = 0 if friend == lucky_one else split_amount
    else:
        print("No one is going to be lucky")

    return friends


def main():
    friends, num_friends = get_friends()
    if not friends:
        return

    total_amount = float(input("Enter the total amount:\n> "))
    friends = split_bill(friends, num_friends, total_amount)
    friends = apply_lucky_feature(friends, total_amount, num_friends)

    print(friends)


if __name__ == "__main__":
    main()
