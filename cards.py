"""
cards.py

Functions for the deck of cards and the hands in blackjack.

Cards are stored as numbers:
2 to 9 are number cards.
10 is a 10, Jack, Queen, or King.
11 is an Ace. It counts as 1 if 11 would make the hand go over 21.
"""

import random

ACE = 11
BLACKJACK = 21


def create_deck():
    """
    Build a deck of 52 cards and shuffle it.

    Inputs:
    None

    Outputs:
    A shuffled list of card values.

    Side effects:
    None
    """
    deck = []

    # four of each number card, 2 through 9
    for value in range(2, 10):
        for suit in range(4):
            deck.append(value)

    # 10, Jack, Queen, and King in four suits makes sixteen 10s
    for i in range(16):
        deck.append(10)

    # four aces
    for suit in range(4):
        deck.append(ACE)

    random.shuffle(deck)
    return deck


def deal_initial_hand(deck):
    """
    Deal 2 cards from the deck.

    Inputs:
    deck: the list of cards left in the deck

    Outputs:
    A hand (list) with 2 cards in it.

    Side effects:
    Removes 2 cards from the deck.
    """
    hand = []
    hand.append(deck.pop())
    hand.append(deck.pop())
    return hand


def calculate_hand_total(hand):
    """
    Add up the cards in a hand. If the total is over 21 and the
    hand has an ace, the ace counts as 1 instead of 11.

    Inputs:
    hand: list of card values

    Outputs:
    The total of the hand.

    Side effects:
    None
    """
    total = 0
    aces = 0

    for card in hand:
        total = total + card
        if card == ACE:
            aces = aces + 1

    # each ace changed from 11 to 1 takes 10 off the total
    while total > BLACKJACK and aces > 0:
        total = total - 10
        aces = aces - 1

    return total


def hit(hand, deck):
    """
    Take a card from the deck and add it to the hand.

    Inputs:
    hand: list of card values
    deck: the list of cards left in the deck

    Outputs:
    The card that was drawn.

    Side effects:
    Removes 1 card from the deck and adds it to the hand.
    """
    card = deck.pop()
    hand.append(card)
    return card


def check_bust(total):
    """
    Check if a hand went over 21.

    Inputs:
    total: the total of a hand

    Outputs:
    True if the total is over 21, False if not.

    Side effects:
    None
    """
    if total > BLACKJACK:
        return True
    else:
        return False


def show_hand(hand):
    """
    Make a string that shows the cards in a hand and the total.
    Aces are shown as A.

    Inputs:
    hand: list of card values

    Outputs:
    A string like "A 10 (total 21)".

    Side effects:
    None
    """
    text = ""
    for card in hand:
        if card == ACE:
            text = text + "A "
        else:
            text = text + str(card) + " "

    total = calculate_hand_total(hand)
    return text + "(total " + str(total) + ")"
