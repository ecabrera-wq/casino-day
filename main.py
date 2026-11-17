"""
main.py

Casino Day: a day trip from my dorm to Atlantic City. You wake
up, travel to the casino, play up to 5 rounds of blackjack, and
get dinner. Try to come home with more money than you left with.

Run with: python main.py
(cards.py and scenes.py must be in the same folder.)
"""

import random

import cards
import scenes

STARTING_CHIPS = 30
WIN_CHIPS = 60
MAX_ROUNDS = 5
DEALER_STANDS_ON = 17


def show_rules():
    """
    Ask the player if they want to learn how blackjack works,
    and explain the rules if they do.

    Inputs:
    None

    Outputs:
    None

    Side effects:
    Prints the rules and asks the player for input.
    """
    print("Do you know how to play blackjack?")
    print("1. Yes, skip the rules")
    print("2. No, explain it to me")

    choice = scenes.get_menu_choice(2)

    if choice == "2":
        print()
        print("HOW BLACKJACK WORKS")
        print("- The goal is to get closer to 21 than the dealer.")
        print("- Cards 2-9 are worth their number.")
        print("- 10, Jack, Queen, and King are worth 10.")
        print("- An Ace (A) is worth 11, or 1 if 11 would put you"
              " over 21.")
        print("- You start with 2 cards. You can see 1 dealer card.")
        print("- HIT means take another card.")
        print("- STAND means keep your cards and end your turn.")
        print("- BUST means going over 21. If you bust, you lose.")
        print("- The dealer has to keep hitting until they have 17.")
        print("- If you tie with the dealer, it's a PUSH and you")
        print("  get your bet back.")


def choose_bet(chips):
    """
    Ask the player how much they want to bet.

    Inputs:
    chips: how many chips the player has

    Outputs:
    The amount the player bets.

    Side effects:
    Prints the menu and asks the player for input.
    """
    print("How much do you want to bet?")
    print("1. 5 chips")
    print("2. 10 chips")
    print("3. All in")

    choice = scenes.get_menu_choice(3)

    if choice == "1":
        bet = 5
    elif choice == "2":
        bet = 10
    else:
        bet = chips

    # you can't bet more chips than you have
    if bet > chips:
        bet = chips

    print("You bet", bet, "chips.")
    return bet


def validate_choice(choice):
    """
    Check if the player typed hit or stand.

    Inputs:
    choice: what the player typed

    Outputs:
    True if the choice is hit or stand, False if not.

    Side effects:
    None
    """
    if choice == "hit" or choice == "stand":
        return True
    else:
        return False


def get_player_choice():
    """
    Ask the player to type hit or stand. Keep asking until they
    type one of those.

    Inputs:
    None

    Outputs:
    The player's choice, either "hit" or "stand".

    Side effects:
    Prints messages and asks the player for input.
    """
    choice = input("Type hit (take a card) or stand (keep your cards): ")
    choice = choice.lower()

    while not validate_choice(choice):
        print("You can only type hit or stand.")
        choice = input("Type hit or stand: ").lower()

    return choice


def player_turn(player_hand, deck):
    """
    Let the player keep hitting until they stand or reach 21.

    Inputs:
    player_hand: the player's cards
    deck: the list of cards left in the deck

    Outputs:
    The player's final total.

    Side effects:
    Asks the player for input, prints their cards, and moves
    cards from the deck to the player's hand.
    """
    total = cards.calculate_hand_total(player_hand)
    choice = "hit"

    while choice == "hit" and total < cards.BLACKJACK:
        choice = get_player_choice()

        if choice == "hit":
            card = cards.hit(player_hand, deck)
            total = cards.calculate_hand_total(player_hand)
            print("You drew a card. Your cards:",
                  cards.show_hand(player_hand))

    return total


def dealer_turn(dealer_hand, deck):
    """
    The dealer keeps hitting until their total is 17 or more.

    Inputs:
    dealer_hand: the dealer's cards
    deck: the list of cards left in the deck

    Outputs:
    The dealer's final total.

    Side effects:
    Prints the dealer's cards and moves cards from the deck to
    the dealer's hand.
    """
    print("Dealer's cards:", cards.show_hand(dealer_hand))
    total = cards.calculate_hand_total(dealer_hand)

    while total < DEALER_STANDS_ON:
        cards.hit(dealer_hand, deck)
        total = cards.calculate_hand_total(dealer_hand)
        print("Dealer hits:", cards.show_hand(dealer_hand))

    return total


def determine_winner(player_total, dealer_total, player_busted,
                     dealer_busted):
    """
    Decide who won the round.

    Inputs:
    player_total: the player's final total
    dealer_total: the dealer's final total
    player_busted: True if the player went over 21
    dealer_busted: True if the dealer went over 21

    Outputs:
    "player", "dealer", or "push" (a tie).

    Side effects:
    None
    """
    if player_busted:
        return "dealer"
    elif dealer_busted:
        return "player"
    elif player_total > dealer_total:
        return "player"
    elif dealer_total > player_total:
        return "dealer"
    else:
        return "push"


def play_round():
    """
    Play one hand of blackjack with a new shuffled deck.

    Inputs:
    None

    Outputs:
    "player", "dealer", or "push".

    Side effects:
    Prints the cards and asks the player for input.
    """
    deck = cards.create_deck()
    player_hand = cards.deal_initial_hand(deck)
    dealer_hand = cards.deal_initial_hand(deck)

    # only show the dealer's first card, like in a real casino
    print("Dealer shows:", cards.show_hand([dealer_hand[0]]))
    print("Your cards:", cards.show_hand(player_hand))

    player_total = player_turn(player_hand, deck)
    player_busted = cards.check_bust(player_total)

    if player_busted:
        print("You went over 21. That's a bust!")
        dealer_total = cards.calculate_hand_total(dealer_hand)
    else:
        dealer_total = dealer_turn(dealer_hand, deck)

    dealer_busted = cards.check_bust(dealer_total)

    return determine_winner(player_total, dealer_total,
                            player_busted, dealer_busted)


def update_chips(chips, winner, bet):
    """
    Add or take away the bet depending on who won.

    Inputs:
    chips: how many chips the player has
    winner: "player", "dealer", or "push"
    bet: how many chips the player bet

    Outputs:
    Updated number of chips.

    Side effects:
    Prints who won the round.
    """
    if winner == "player":
        print("You win", bet, "chips!")
        chips = chips + bet
    elif winner == "dealer":
        print("The dealer wins. You lose", bet, "chips.")
        chips = chips - bet
    else:
        print("It's a push (tie). You keep your chips.")

    return chips


def random_event(chips):
    """
    Generate a random event that may change the player's chips.

    Inputs:
    chips: how many chips the player has

    Outputs:
    Updated number of chips.

    Side effects:
    Prints what happened.
    """
    event = random.choice(["found_chips", "spilled_drink",
                           "free_snack", "nothing"])

    if event == "found_chips":
        print("You find 3 chips on the floor. You gain 3 chips.")
        chips = chips + 3
    elif event == "spilled_drink" and chips > 1:
        print("You spill your drink and tip the dealer 1 chip.")
        chips = chips - 1
    elif event == "free_snack":
        print("A waiter brings you a free snack. Nice!")
    else:
        print("Nothing happens.")

    return chips


def casino_scene(chips):
    """
    Play up to 5 rounds of blackjack. Stop early if the player
    runs out of chips or reaches the chip goal.

    Inputs:
    chips: how many chips the player has

    Outputs:
    Updated number of chips.

    Side effects:
    Prints each round and asks the player for input.
    """
    print()
    print("--- THE CASINO ---")
    show_rules()

    round_number = 0

    while (round_number < MAX_ROUNDS and not is_broke(chips)
           and chips < WIN_CHIPS):
        round_number = round_number + 1

        print()
        print("Round", round_number, "of", MAX_ROUNDS)
        print("Chips:", chips)

        bet = choose_bet(chips)
        winner = play_round()
        chips = update_chips(chips, winner, bet)
        chips = random_event(chips)

    if chips >= WIN_CHIPS:
        print("You hit", WIN_CHIPS, "chips! You cash out early.")

    print("You leave the casino with", chips, "chips.")
    return chips


def is_broke(chips):
    """
    Check if the player has no money left.

    Inputs:
    chips: how many chips the player has

    Outputs:
    True if the player has 0 or fewer chips, False if not.

    Side effects:
    None
    """
    if chips <= 0:
        return True
    else:
        return False


def check_win(chips):
    """
    Decide if the player won the day. Uses is_broke() first.

    Inputs:
    chips: how much money the player has at the end of the day

    Outputs:
    True if the player came home with more money than they
    started with, False if not.

    Side effects:
    None
    """
    if is_broke(chips):
        return False
    elif chips > STARTING_CHIPS:
        return True
    else:
        return False


def main():
    """
    Run the whole day from start to finish.

    Inputs:
    None

    Outputs:
    None

    Side effects:
    Prints the story and asks the player for input.
    """
    name = input("What is your name? ")

    chips = STARTING_CHIPS

    print()
    print("Welcome to Casino Day,", name + "!")
    print("You're taking a day trip from your dorm to Atlantic City.")
    print("You have $" + str(chips), "for the whole day.")
    print("Come home with more than $" + str(STARTING_CHIPS),
          "to win!")

    chips = scenes.morning_scene(chips)
    chips = scenes.travel_scene(chips)
    chips = casino_scene(chips)
    chips = scenes.dinner_scene(chips)

    print()
    print("--- END OF THE DAY ---")
    print("You get back to your dorm with $" + str(chips) + ".")

    if check_win(chips):
        print("You beat the casino today. Good job,", name + "!")
    else:
        print("The casino won today. Better luck next time,",
              name + ".")


if __name__ == "__main__":
    main()
