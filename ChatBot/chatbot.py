def greet(bot_name, birth_year):
    print(f"Hello! My name is {bot_name}.")
    print(f"I was created in {birth_year}.")


def remind_name():
    name = input("Please, remind me your name.\n> ")
    print(f"What a great name you have, {name}!")
    return name


def guess_age():
    print("Let me guess your age.")
    print("Enter remainders of dividing your age by 3, 5 and 7.")
    rem3 = int(input("> "))
    rem5 = int(input("> "))
    rem7 = int(input("> "))
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105
    print(f"Your age is {age}; that's a good time to start programming!")
    return age


def count_numbers():
    print("Now I will prove to you that I can count to any number you want.")
    num = int(input("> "))
    for i in range(num + 1):
        print(f"{i} !")
    print("Completed, have a nice day!")


def programming_test():
    print("Let's test your programming knowledge.")
    print("Why do we use methods?")
    print("1. To repeat a statement multiple times.")
    print("2. To decompose a program into several small subroutines.")
    print("3. To determine the execution time of a program.")
    print("4. To interrupt the execution of a program.")

    while True:
        answer = input("> ")
        if answer == "2":
            break
        print("Please, try again.")
    print("Congratulations, have a nice day!")


def main():
    greet("DICT_Bot", 2025)
    remind_name()
    guess_age()
    count_numbers()
    programming_test()


if __name__ == "__main__":
    main()
