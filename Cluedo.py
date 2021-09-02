from typing import Union

import constants.defaults as cn

from components.cards import Cards
from components.suspects import Suspects
from components.player import Player
from components.board import Board
from components.accusation import Accusation
from components.players import Players

import components.inputs as inputs
import components.utilities as utilities


class CluedoGame:
    def __init__(self, players_number=6):
        self.players_number = players_number

        self.cards = Cards(cn.CHARACTERS, cn.WEAPONS, cn.ROOMS)

        # 3 are the cards to be guessed
        self.cards_per_person = (self.cards.number - 3) // self.players_number
        self.cards_to_players = self.cards_per_person * self.players_number
        self.cards_on_board = self.cards.number - self.cards_to_players - 3

        self.suspects = Suspects(cn.CHARACTERS, cn.WEAPONS, cn.ROOMS)
        self.board = Board(self.cards_on_board)

        self.players: Players = None

    # 1) MAIN: Regulating the alternation of the various game phases
    def main(self):
        self.initiate_game()
        self.display_game_info()

        while self.suspects.guessing_probability < 1:
            action = inputs.get_user_action(self.players.active.name)

            if action == "1":
                self.accusation_made_event()
                self.display_game_info()

            if action == "1" or action == "2":
                # Go to the next player
                self.players.make_next_player_active()

            if action == "3":
                self.card_revealed_event()
                self.display_game_info()

        # If probability is 1, the game is solved
        self.suspects.display_guessing_probability_message()

    # --------------------------------------------------------------------------
    # GAME SET UP
    # --------------------------------------------------------------------------
    def initiate_game(self):
        """Set up a new game getting all the required items ready"""
        self.initiate_players()
        self.register_users_cards()
        return

    def initiate_players(self):
        """Create the list of players"""
        user_position = inputs.get_user_position(self.players_number)

        self.players = Players(
            self.players_number, self.cards_per_person, user_position
        )
        return

    def register_users_cards(self) -> None:
        """Register the fact that users owns its initial cards."""
        user_owned_cards = inputs.get_users_cards(
            self.cards_per_person, self.cards.all_cards
        )

        self.suspects.remove_multiple_from_suspects(user_owned_cards)

        for card in user_owned_cards:
            self.update_card_owned(card, self.players.get_player_by_name("You"))

        self.update_card_not_owned(
            user_owned_cards, self.players.list, player_excluded="You"
        )

    # --------------------------------------------------------------------------
    # ACCUSATION HANDLING
    # --------------------------------------------------------------------------
    def accusation_made_event(self):
        """Handle the entire event of an accusation being made"""
        cs, wp, rm = self.cards.characters, self.cards.weapons, self.cards.rooms
        accusation_list = inputs.get_accusation(cs, wp, rm)
        accusation = Accusation.from_list(accusation_list)

        player_showed_name = inputs.get_player_who_showed(self.players.names)
        player_showed = self.players.get_player_by_name(player_showed_name)

        players_passing = self.players.range_of_players(player_showed)
        self.update_card_not_owned(accusation.items_set, players_passing)

        # Distinguishing the actions between "You" and the other players
        if self.players.active.name == "You":
            card_showed = inputs.get_card_from_accusation(accusation.items_list)

            self.suspects.remove_one_from_suspects(card_showed)
            self.update_card_not_owned(
                card_showed, self.players, player_excluded=player_showed
            )

            self.update_card_owned(player_showed, card_showed)

        else:
            self.update_card_owned(player_showed, accusation.items_list)

    def update_card_not_owned(
        self,
        card_input: Union[str, list],
        players_list: list[Player],
        player_excluded=Union[None, Player],
    ) -> None:
        """Registers that one or more players do not own one or more cards"""
        card_input_as_set = utilities.input_to_set(card_input)

        for player in players_list:
            if player != player_excluded:
                player.add_cards_not_owned(card_input_as_set)

    def update_card_owned(
        self, card_input: Union[str, list], player_to_update: Player
    ) -> None:
        # Not to proceed further if information about the player is complete
        if player_to_update.all_cards_known:
            return

        card_input_as_set = utilities.input_to_set(card_input)

        player_to_update.add_cards_owned(card_input_as_set)

    # --------------------------------------------------------------------------
    # CARD REVEALED HANDLING
    # --------------------------------------------------------------------------
    def card_revealed_event(self) -> None:
        """Handles the complete event of a card being revealed"""
        if self.board.all_cards_revealed:
            print(
                "It looks like all the cards on the table had already been"
                "revealed, please retry.\n"
            )
            return
        revealed_card = inputs.input_in_list(
            "Which card was revealed?", self.cards.all_cards
        )
        self.register_card_revealed(revealed_card)

    def register_card_revealed(self, revealed_card: str) -> None:
        """Register that a card has been revealed"""
        self.suspects.remove_one_from_suspects(revealed_card)
        self.update_card_not_owned(revealed_card, self.players)
        self.board.add_card(revealed_card)

    # --------------------------------------------------------------------------
    # INFORMATION DISPLAY
    # --------------------------------------------------------------------------
    def display_game_info(self):
        print("########################### SUSPECTS")
        print(self.suspects)
        print("########################### PLAYERS INFO")
        self.players.display_players_info()
        print("########################### BOARD")
        print(self.board)
        print()


if __name__ == "__main__":
    # To test what was done up to now
    game = CluedoGame(players_number=6)
    game.main()
    input("\nPress any key to exit ")
