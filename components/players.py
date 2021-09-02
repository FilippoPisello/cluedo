from .player import Player


class Players:
    """Class to construct and store multiple Player objects"""

    def __init__(
        self, number_of_players: int, cards_per_player: int, user_position: int
    ):
        self.number = number_of_players
        self.names = self.create_players_labels(user_position)
        self.list = self.create_players_list(self.names, cards_per_player)
        self.active = self.list[0]

    @property
    def active_index(self):
        return self.list.index(self.active)

    @staticmethod
    def create_players_list(
        players_labels: list[str], cards_per_player: int
    ) -> list[Player]:
        """Create a list of players"""
        return [Player(name, cards_per_player) for name in players_labels]

    def create_players_labels(self, user_position: int) -> list[str]:
        """Return list of players labels"""
        return [
            f"Player {i}" if i != user_position else "You"
            for i in range(1, self.number + 1)
        ]

    def make_next_player_active(self) -> None:
        """Make that active player is the next in the turn"""
        new_index = (self.active_index + 1) % self.number
        self.active = self.list[new_index]

    def get_player_by_name(self, player_name: str) -> Player:
        """Return a player object given its name in string form"""
        for player in self.list:
            if player.name == player_name:
                return player
        raise ValueError(f"There is no player named {player_name}")

    def range_of_players(self, last_player: Player) -> list[Player]:
        """Return list of players between active player and last_player,
        exclusive on both hands"""
        start = self.active_index + 1
        end = self.list.index(last_player) + 1
        return self.list[start:end]

    def display_players_info(self):
        """Prints out info for all the players"""
        for player in self.list:
            print(player)
            print()
