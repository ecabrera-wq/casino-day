"""
scenes.py

The parts of the day that happen before and after the casino:
waking up, getting to Atlantic City, and dinner. Also has the
menu function that every part of the game uses to ask the
player for a choice.

Money and chips are the same thing in this game: 1 chip = $1.
"""

import random

LATE_FEE = 3
BREAKFAST_COST = 2
BUS_COST = 5
TRAIN_COST = 8
PIZZA_COST = 3
STEAK_COST = 12


def is_valid_option(choice, number_of_options):
    """
    Check if the player typed one of the menu numbers.

    Inputs:
    choice: what the player typed
    number_of_options: how many options are on the menu

    Outputs:
    True if choice is a number from 1 to number_of_options,
    False if not.

    Side effects:
    None
    """
    for option in range(1, number_of_options + 1):
        if choice == str(option):
            return True
    return False


def get_menu_choice(number_of_options):
    """
    Ask the player to pick a menu option. Keep asking until they
    type a number that is on the menu.

    Inputs:
    number_of_options: how many options are on the menu

    Outputs:
    The player's choice as a string, like "1".

    Side effects:
    Prints messages and asks the player for input.
    """
    choice = input("Choose an option: ")

    while not is_valid_option(choice, number_of_options):
        print("Please type a number from 1 to", number_of_options)
        choice = input("Choose an option: ")

    return choice


def morning_scene(chips):
    """
    The player wakes up in their dorm and decides whether to
    snooze. Snoozing too many times makes them miss the early bus.

    Inputs:
    chips: how much money the player has

    Outputs:
    Updated amount of money.

    Side effects:
    Prints the story and asks the player for input.
    """
    print()
    print("--- MORNING ---")
    print("Your alarm goes off in your dorm. It's casino day!")
    print("1. Get up right away")
    print("2. Hit snooze")

    choice = get_menu_choice(2)

    if choice == "2":
        # you don't know how many times you'll snooze
        snoozes = random.randint(1, 4)
        for alarm in range(1, snoozes + 1):
            print("Snooze number", alarm, "... zzz")

        if snoozes >= 3:
            print("You overslept and missed the early bus!")
            print("A later ticket costs $" + str(LATE_FEE), "more.")
            chips = chips - LATE_FEE
        else:
            print("You got a little more sleep and still made it.")
    else:
        print("You get up on time. Nice discipline.")

    print("Do you want to grab breakfast at the bodega for $"
          + str(BREAKFAST_COST) + "?")
    print("1. Yes")
    print("2. No, save the money")

    choice = get_menu_choice(2)

    if choice == "1":
        print("Bacon, egg, and cheese. You're ready for the day.")
        chips = chips - BREAKFAST_COST
    else:
        print("Your stomach is growling, but you saved $"
              + str(BREAKFAST_COST) + ".")

    return chips


def travel_scene(chips):
    """
    The player picks how to get to Atlantic City. Something random
    can happen on the way.

    Inputs:
    chips: how much money the player has

    Outputs:
    Updated amount of money.

    Side effects:
    Prints the story and asks the player for input.
    """
    print()
    print("--- GETTING THERE ---")
    print("How do you want to get to Atlantic City?")
    print("1. Bus from Port Authority ($" + str(BUS_COST) + ")")
    print("2. Train ($" + str(TRAIN_COST) + ", but more comfortable)")

    choice = get_menu_choice(2)

    if choice == "1":
        chips = chips - BUS_COST
        event = random.choice(["traffic", "found_money", "quiet"])
    else:
        chips = chips - TRAIN_COST
        event = random.choice(["found_money", "quiet"])

    if event == "traffic":
        print("You get stuck in traffic for an hour. Ugh.")
    elif event == "found_money":
        print("You find $2 between the seats. Lucky start!")
        chips = chips + 2
    else:
        print("The ride is quiet. You nap the whole way.")

    print("You arrive at the casino and trade your cash for",
          chips, "chips.")
    return chips


def dinner_scene(chips):
    """
    After the casino, the player picks where to eat dinner.

    Inputs:
    chips: how much money the player has

    Outputs:
    Updated amount of money.

    Side effects:
    Prints the story and asks the player for input.
    """
    print()
    print("--- DINNER ---")

    if chips <= 0:
        print("You're out of money, so you eat crackers on the bus home.")
        return chips

    print("You're hungry after the casino. Where do you eat?")
    print("1. Pizza slice ($" + str(PIZZA_COST) + ")")
    print("2. Steakhouse ($" + str(STEAK_COST) + ")")
    print("3. Skip dinner and eat at home")

    choice = get_menu_choice(3)

    if choice == "1" and chips >= PIZZA_COST:
        print("A classic slice. Not bad.")
        chips = chips - PIZZA_COST
    elif choice == "2" and chips >= STEAK_COST:
        print("You treat yourself to a steak dinner.")
        chips = chips - STEAK_COST
    elif choice == "3":
        print("You head straight home and make instant noodles.")
    else:
        print("You can't afford that, so you eat at home.")

    return chips
