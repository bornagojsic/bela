"""
Player module for the Bela card game.

This module contains the Player class and card-related utility functions.
"""


def sort_card(card):
    """
    Sorts cards based on their value for ordering purposes.

    Args:
        card (str): Card string in format "value+suit" (e.g. "7♠", "A♥")

    Returns:
        int: Numeric value representing the card's sorting priority
    """
    card_value = card[:-1]  # Remove suit symbol
    if card_value in "7 8 9 10".split():
        return int(card_value) - 10
    elif card_value == "B":  # Jack
        return 2
    elif card_value == "D":  # Queen
        return 3
    elif card_value == "K":  # King
        return 4
    elif card_value == "A":  # Ace
        return 11


def calculate_card_value(card, trump_suit):
    """
    Calculates the value of a card based on whether it's a trump card.

    Args:
        card (str): Card string in format "value+suit" (e.g. "7♠", "A♥")
        trump_suit (str): The current trump suit symbol

    Returns:
        float: Numeric value of the card for scoring purposes
    """
    if card[-1] == trump_suit:  # If card is of trump suit
        card_value = card[:-1]  # Remove suit symbol
        if card_value in ["7", "8"]:
            return int(card_value) / 100
        elif card_value == "9":
            return 14
        elif card_value == "10":
            return 10
        elif card_value == "B":  # Jack
            return 20
        elif card_value == "D":  # Queen
            return 3
        elif card_value == "K":  # King
            return 4
        elif card_value == "A":  # Ace
            return 11
    else:  # Non-trump card
        card_value = card[:-1]  # Remove suit symbol
        if card_value in "7 8 9".split():
            return int(card_value) / 100
        elif card_value == "10":
            return 10
        elif card_value == "B":  # Jack
            return 2
        elif card_value == "D":  # Queen
            return 3
        elif card_value == "K":  # King
            return 4
        elif card_value == "A":  # Ace
            return 11


class Player:
    """Represents a player in the Bela card game."""

    def __init__(self, name, is_ai, cards):
        """
        Initializes a player.

        Args:
            name (str): Player's name
            is_ai (bool): True if this is an AI player, False for human
            cards (list): List of card strings the player holds
        """
        self.name = name
        self.is_ai = is_ai
        self.cards = cards
        self.empty_slots = 0  # Count of empty positions in hand
        self.points = 0       # Points accumulated in current round
        self.total_points = 0 # Total points across all rounds

    def sort_cards(self):
        """Sorts the player's cards by suit and value."""
        # Remove empty slots temporarily
        for _ in range(self.empty_slots):
            self.cards.remove("empty")

        # Separate cards by suit
        spades = [card for card in self.cards if '♠' in card]
        hearts = [card for card in self.cards if '♥' in card]
        diamonds = [card for card in self.cards if '♦' in card]
        clubs = [card for card in self.cards if '♣' in card]

        # Sort each suit
        for suit_cards in [spades, hearts, diamonds, clubs]:
            suit_cards.sort(key=sort_card)

        # Reconstruct the hand with sorted suits and empty slots
        self.cards = spades + hearts + diamonds + clubs + self.empty_slots * ["empty"]

    def play_card(self, card):
        """
        Removes a card from the player's hand when played.

        Args:
            card (str): The card to be played

        Returns:
            str: The card that was played
        """
        print(self.name, self.empty_slots, self.cards)
        card_index = self.cards.index(card)
        self.cards[card_index] = "empty"
        self.empty_slots += 1
        self.sort_cards()
        print(self.name, self.empty_slots, self.cards)
        return card

    def get_available_suits(self):
        """
        Gets the suits of cards currently in the player's hand.

        Returns:
            list: List of unique suit symbols present in the hand
        """
        suits = [card[-1] for card in self.cards if card != "empty"]
        # Return unique suits in order of appearance
        return list(dict.fromkeys(suits))

    def get_remaining_cards(self):
        """
        Gets the cards still in the player's hand (excluding empty slots).

        Returns:
            list: List of cards currently held by the player
        """
        return self.cards[:8 - self.empty_slots]