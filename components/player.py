class Player:
    """Describe a player and the cards he/she owns"""

    def __init__(self, name: str, number_of_cards: int):
        self.name = name
        self.number_of_cards = number_of_cards
        self.cards_owned = [set() for _ in range(number_of_cards)]
        self.cards_not_owned = set()

    @property
    def all_cards_known(self) -> bool:
        """Returns true if all the player's cards are known"""
        if self.cards_owned == [x for x in self.cards_owned if len(x) == 1]:
            return True
        return False

    def add_cards_not_owned(self, cards: set) -> None:
        """Add ore or more cards to the list of the not owned ones."""
        self.cards_not_owned.union(set(cards))
        self.remove_cards_owned(cards)

    def remove_cards_owned(self, cards: set) -> None:
        """Remove one or more cards from the list of the owned ones."""
        # Remove not owned cards from the owned ones
        for slot in self.cards_owned:
            slot.difference(cards)

    def add_cards_owned(self, cards: set) -> None:
        """Add one or more cards from the list of the owned ones."""
        # Clean the incoming cards from the ones not owned
        cards = cards.difference(self.cards_not_owned)
        # Do nothing if same card(s) are already registered
        if cards in self.cards_owned:
            return
        for slot_ind, slot in enumerate(self.cards_owned):
            # Looking for the first empty slot not to overwrite info
            if not (slot):
                self.cards_owned[slot_ind].add(cards)
                break

    def __str__(self):
        return self.name

    def __eq__(self, other) -> bool:
        try:
            return self.name == other.name
        except AttributeError:
            return False

    def __ne__(self, other) -> bool:
        try:
            return self.name != other.name
        except AttributeError:
            return True
