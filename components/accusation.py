from dataclasses import dataclass


@dataclass
class Accusation:
    """Class representing an accusation made of three cards"""

    character: str
    weapon: str
    room: str

    @property
    def items_list(self) -> list[str]:
        return [self.character, self.weapon, self.room]

    @property
    def items_set(self) -> set[str]:
        return {self.character, self.weapon, self.room}

    @classmethod
    def from_list(cls, input_list: list[str]):
        """Create Accusation obj from list of form ['character', 'weapon', 'room']"""
        if not len(input_list) == 3:
            raise ValueError(
                f"Accusation list must be of len 3, {input_list} was passed"
            )
        return cls(input_list[0], input_list[1], input_list[2])
