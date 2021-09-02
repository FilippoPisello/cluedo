from dataclasses import dataclass


@dataclass
class Cards:
    """Describe the cards present in the Cluedo game"""

    characters: list
    weapons: list
    rooms: list

    @property
    def all_cards(self) -> list[str]:
        """Returns a single list containing characters, weapons and rooms"""
        return self.characters + self.weapons + self.rooms

    @property
    def number(self) -> int:
        """Returns the number of cards"""
        return len(self.all_cards)
