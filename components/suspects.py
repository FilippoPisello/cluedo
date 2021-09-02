class Suspects:
    """The suspects from the user perspective"""

    def __init__(self, characters: list, weapons: list, rooms: list):
        self.characters = set(characters)
        self.weapons = set(weapons)
        self.rooms = set(rooms)

    @property
    def guessing_probability(self):
        """Return probability of correctly making an accusation by randomly
        picking from the available suspects"""
        return 1 / (len(self.characters) * len(self.weapons) * len(self.rooms))

    def remove_multiple_from_suspects(self, items: list[str]) -> None:
        """Remove items from suspects if present, evaluated individually"""
        for item in items:
            self.remove_one_from_suspects(item)

    def remove_one_from_suspects(self, item: str) -> None:
        """Remove item from suspects if present"""
        self.characters.discard(item)
        self.weapons.discard(item)
        self.rooms.discard(item)

    def display_guessing_probability_message(self):
        """Display a message about the guessing probability"""
        prob = self.guessing_probability
        if prob == 1:
            print("You can solve the case with certainty now.\nThe three items are:")
            print(self.characters)
            print(self.weapons)
            print(self.rooms)
        else:
            prob = format(prob, ".2%")
            print(f"The probability of randomly guessing is: {prob}")
