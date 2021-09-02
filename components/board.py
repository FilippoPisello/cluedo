from dataclasses import dataclass, field


@dataclass
class Board:
    """Describe the board as the object that contains cards to be revealed."""

    total_cards: int
    cards: set = field(default_factory=set)

    def add_card(self, card: str):
        """Add a card to the ones revealed in the board"""
        if self.all_cards_revealed:
            self.limit_reached_message()
            return
        self.cards.add(card)

    @property
    def all_cards_revealed(self):
        """Return true if number of stored cards correspond to maximum cards"""
        return len(self.total_cards) == self.cards

    def limit_reached_message(self):
        """Alert that a new card cannot be added to the board"""
        print("All the cards of the board have already been revealed")
