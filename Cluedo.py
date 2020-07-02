
class CluedoGame:
    def __init__(self, players_number=6, nerd_mode=True):
        self.players_number = players_number
        self.players_list = []
        self.nerd_mode = nerd_mode
        self.suspects = []
        self.cards_not_owned = {}
        self.cards_owned = {}
        self.characters = ['Green', 'Mustard', 'Peacock', 'Plum', 'Scarlet',
                           'White']
        self.weapons = ['Axe', 'Baseball bat', 'Chandelier', 'Dumbell', 'Knife',
                        'Pistol', 'Poison', 'Rope', 'Trophy']
        self.rooms = ['Dining Room', 'Guest House', 'Hall', 'Kitchen',
                      'Living Room', 'Observatory', 'Patio', 'Spa', 'Theatre']
        self.items = self.characters + self.weapons + self.rooms
        self.cards_per_person = (len(self.items) - 3) // self.players_number
        self.cards_to_players = self.cards_per_person * self.players_number
        self.cards_on_table = len(self.items) - self.cards_to_players
        self.prob_guessing = 0

    # 1) MAIN: Regulating the alternation of the various game phases
    def main(self):
        self.game_start()
        player = 0
        yes_answers = ["Yes", "yes", "Y", "y", 1, "1"]

        while self.prob_guessing != 1:
            if self.players_list[player] == "You":
                action = input("Did you make an accusation? ")
                if action in yes_answers:
                    accusation = self.accusation()  # List of three items
                    player_showed = self.input_in_players("Which player showed "
                                                          "you a card?")
                    card_showed = self.input_in_accusation(accusation, "Which "
                                                           "card was shown to "
                                                           "you?")

                    self.remove_from_suspects(card_showed)
                    self.update_card_not_owned(self.players_list, card_showed,
                                               player_excl=player_showed)
                    players_passing = self.players_not_showing("You",
                                                               player_showed)
                    self.update_card_not_owned(players_passing, accusation)
                    self.update_card_owned(player_showed, card_showed)
                    self.interact_information()
                    self.disp_guessings_probab()

                    print(self.cards_owned)  # TO BE REMOVED
                    print(self.cards_not_owned)  # TO BE REMOVED
            else:
                print("Still to be coded")
                break

            player = self.go_to_next_player(player)

    # 2) GAME DYNAMICS: functions capturing specific dynamics of the game
    def game_start(self):
        self.players_order()
        self.suspects = []
        for list_ in [self.characters, self.weapons, self.rooms]:
            self.suspects.append(list_)
        for counter in range(self.cards_per_person):
            order = ["first", "second", "third", "fourth", "fifth", "sixth"
                     "seventh", "eighth", "ninth", "tenth"]
            card_number = order[counter]
            item = self.input_in_items(f"Please insert your {card_number} card")
            self.remove_from_suspects(item)
            self.cards_owned["You"][counter].append(item)
            self.update_card_not_owned(self.players_list, item,
                                       player_excl="You")

        print(self.cards_owned)  # TO BE REMOVED
        print()
        print(self.cards_not_owned)  # TO BE REMOVED
        print()
        print(self.suspects)
        self.disp_guessings_probab()
        return

    def card_revealed(self):
        item = self.input_in_items("Which card was revealed?")
        self.remove_from_suspects(item)
        self.update_card_not_owned(self.players_list, item)
        return

    def remove_from_suspects(self, item):
        for list_ in self.suspects:
            if item in list_: list_.remove(item)

    def accusation(self):
        character = self.input_in_items("Which character?")
        weapon = self.input_in_items("Which weapon?")
        room = self.input_in_items("Which room?")
        return [character, weapon, room]

    def players_not_showing(self, player_asking, player_showing):
        start_position = self.players_list.index(player_asking)
        end_position = self.players_list.index(player_showing)
        return self.players_list[start_position + 1 : end_position]

    def update_card_not_owned(self, players_list, card_input, player_excl=None):
        if type(card_input) == str: card_input = [card_input]
        if type(card_input) == list: card_input = card_input
        for card in card_input:
            for player in players_list:
                if player != player_excl:
                    # Not to repeat the card
                    if card not in self.cards_not_owned[player]:
                        self.cards_not_owned[player].append(card)
        return

    def update_card_owned(self, player_showing, card_showed):
        if type(card_showed) == str: card_showed = [card_showed]
        if type(card_showed) == list: card_showed = card_showed
        # To remove from the process any card which cannot be owned
        for item in card_showed:
            if item in self.cards_not_owned[player_showing]:
                card_showed.remove(item)
        # Not to repeat card already added
        if card_showed in self.cards_owned[player_showing]:
            return  # TO CHECK: AIM IS TO EXIT THE FUNCTION
        # Not to overwrite cards already determined
        n = 0
        while len(self.cards_owned[player_showing][n]) == 1:
            n = n + 1
        for card in card_showed:
            self.cards_owned[player_showing][n].append(card)
        return

    def interact_information(self):
        for player in self.players_list:
            for slot in self.cards_owned[player]:
                for card in slot:
                    if card in self.cards_not_owned[player]:
                        slot.remove(card)
                    # If only one card remains, it is certain by construction
                    if len(slot) == 1:
                        if card in self.suspects:
                            self.remove_from_suspects(card)
                            self.update_card_not_owned(self.players_list, card,
                                                       player_excl=player)

    # 3) UTILITIES: Functions propedeutic to the functioning of the main ones
    def input_in_items(self, text):
        text = text + " "
        player_input = input(text).title()
        while player_input not in self.items:
            help_word = "list"
            if player_input != help_word.title():
                print("Something went wrong. What you typed does not appear "
                      "among the items of the game. Please retry. If you would "
                      "like to see the list of items of the game type "
                      f"'{help_word}'.\n")
            player_input = input(text).title()
            if player_input == help_word.title():
                print("These are the characters:")
                print(*self.characters, sep=", ")
                print("\nThese are the weapons:")
                print(*self.weapons, sep=", ")
                print("\nThese are the rooms:")
                print(*self.rooms, sep=", ")
        return player_input

    def input_in_players(self, text):
        text = text + " "
        player_input = input(text).title()
        while player_input not in self.players_list:
            help_word = "list"
            if player_input != help_word.title():
                print("Something went wrong. What you typed does not appear "
                      "among the players in the game. Please retry. If you would "
                      "like to see the list of players in the game type "
                      f"'{help_word}'.\n")
            player_input = input(text).title()
            if player_input == help_word.title():
                print("These are the players:")
                print(*self.players_list, sep=", ")
        return player_input

    def input_in_accusation(self, accusation_list, text):
        text = text + " "
        player_input = input(text).title()
        while player_input not in accusation_list:
            help_word = "list"
            if player_input != help_word.title():
                print("Something went wrong. What you typed does not appear "
                      "among the items of the accusation. Please retry. If you "
                      "like to see the items in the accusation type "
                      f"'{help_word}'.\n")
            player_input = input(text).title()
            if player_input == help_word.title():
                print("These are the items in the accusation:")
                print(*accusation_list, sep=", ")
        return player_input

    def disp_guessings_probab(self):
        self.prob_guessing = ((1 / len(self.suspects[0]))
                              * (1 / len(self.suspects[1]))
                              * (1 / len(self.suspects[2]))
                              )
        prob_guessing = format(self.prob_guessing, ".2%")

        if self.prob_guessing == 1:
            print("You can solve the case with certainty now. "
                  "The three items are:")
            print(self.suspects[0][0])
            print(self.suspects[1][0])
            print(self.suspects[2][0])

        elif self.nerd_mode:
            print(f"The probability of randomly guessing is: {prob_guessing}")
        return

    def players_order(self):
        player_position = None
        while player_position not in range(1, self.players_number + 1):
            player_position = int(input("What is your position in the turn? "
                                        "Type 1 if first, 2 if second and so on"
                                        ". Please provide a number from 1 to "
                                        f"{self.players_number}. "))
            if player_position not in range(1, self.players_number + 1):
                print("The value you provided is not accepted, please retry.")
        for number in range(1, self.players_number + 1):
            self.players_list.append(f"Player {number}")
        self.players_list[player_position - 1] = "You"

        for player in self.players_list:
            self.cards_owned[player] = [[], [], []]
            self.cards_not_owned[player] = []
        return

    def go_to_next_player(self, index):
        while (index - self.players_number) >= -1:
            index = index - self.players_number
        index = index + 1
        if index not in range(0, self.players_number):
            print("Beware, the index is out of range given the number of "
                  "players! An error will occur")
        return index


# To test what was done up to now
game = CluedoGame(players_number=6)
game.main()
input("\nPress any key to exit ")
