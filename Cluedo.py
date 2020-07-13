
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
        self.weapons = ['Axe', 'Baseball Bat', 'Chandelier', 'Dumbell', 'Knife',
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
            action = input(f"Did {self.players_list[player].lower()} make "
                           "an accusation? ")
            if action in yes_answers:
                accusation = self.accusation()  # List of three items
                player_showed = self.input_in_list("Which player showed the "
                                                   "card?", type="players")
                players_passing = self.players_not_showing(self.players_list[player],
                                                           player_showed)
                self.update_card_not_owned(players_passing, accusation)
                # Distinguisihing the actions between "You" and the other players
                if self.players_list[player] == "You":
                    card_showed = self.input_in_list("Which card was shown to you?",
                                                     type="accusation",
                                                     accusation_list=accusation)
                    self.remove_from_suspects(card_showed)
                    self.update_card_not_owned(self.players_list, card_showed,
                                               player_excl=player_showed)

                    self.update_card_owned(player_showed, card_showed)
                    print("CARDS OWNED")
                    print(self.cards_owned)  # TO BE REMOVED
                    print("CARDS NOT OWNED")
                    print(self.cards_not_owned)  # TO BE REMOVED
                    print("SUSPECTS")
                    print(self.suspects)
                    print()
                    self.interact_information()
                    self.disp_guessings_probab()

                    print("CARDS OWNED")
                    print(self.cards_owned)  # TO BE REMOVED
                    print("CARDS NOT OWNED")
                    print(self.cards_not_owned)  # TO BE REMOVED
                    print("SUSPECTS")
                    print(self.suspects)
                    print()
                else:
                    self.update_card_owned(player_showed, accusation)
                    print("OWNED")
                    print(self.cards_owned)  # TO BE REMOVED
                    print("CARDS NOT OWNED")
                    print(self.cards_not_owned)  # TO BE REMOVED
                    print("SUSPECTS")
                    print(self.suspects)
                    print()
                    self.interact_information()
                    self.disp_guessings_probab()

                    print("CARDS OWNED")
                    print(self.cards_owned)  # TO BE REMOVED
                    print("CARDS NOT OWNED")
                    print(self.cards_not_owned)  # TO BE REMOVED
                    print("SUSPECTS")
                    print(self.suspects)
                    print()
            else:
                pass  # if no accusation go directly to the next player

            # Go to next player
            player = (player + 1) % self.players_number

        # If probability is 1, the game is solved
        self.disp_guessings_probab()

    # 2) GAME DYNAMICS: functions capturing specific dynamics of the game
    def game_start(self):
        self.players_order()
        self.suspects = [self.characters.copy(),
                         self.weapons.copy(),
                         self.rooms.copy()]
        for counter in range(self.cards_per_person):
            order = ["first", "second", "third", "fourth", "fifth", "sixth"
                     "seventh", "eighth", "ninth", "tenth"]
            card_number = order[counter]
            item = self.input_in_list(f"Please insert your {card_number} card",
                                      type="items")
            self.remove_from_suspects(item)
            self.cards_owned["You"][counter].append(item)
            self.update_card_not_owned(self.players_list, item,
                                       player_excl="You")
        print("OWNED")
        print(self.cards_owned)  # TO BE REMOVED
        print("CARDS NOT OWNED")
        print(self.cards_not_owned)  # TO BE REMOVED
        print("SUSPECTS")
        print(self.suspects)
        self.disp_guessings_probab()
        return

    def card_revealed(self):
        item = self.input_in_list("Which card was revealed?", type="items")
        self.remove_from_suspects(item)
        self.update_card_not_owned(self.players_list, item)
        return

    def remove_from_suspects(self, item):
        for list_ in self.suspects:
            if item in list_: list_.remove(item)

    def accusation(self):
        character = self.input_in_list("Which character?", type="characters")
        weapon = self.input_in_list("Which weapon?", type="weapons")
        room = self.input_in_list("Which room?", type="rooms")
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
        # Not to proceed further if information about the player is complete
        if self.all_cards_known(player=player_showing):
            return

        if type(card_showed) == str: card_showed = [card_showed]
        if type(card_showed) == list: card_showed = card_showed
        # To remove from the process any card which cannot be owned
        for item in card_showed:
            if item in self.cards_not_owned[player_showing]:
                card_showed.remove(item)
        # Not to repeat card already added
        if card_showed in self.cards_owned[player_showing]:
            return
        # Not to overwrite cards already determined
        n = 0
        while self.cards_owned[player_showing][n]:
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
                    item = slot[0]
                    if item in (self.suspects[0] or self.suspects[1]
                                or self.suspects[2]):
                        self.remove_from_suspects(item)
                        self.update_card_not_owned(self.players_list, item,
                                                   player_excl=player)
                    # Remove slots with less info than the ones of lenght 1
                    for slot in self.cards_owned[player]:
                        if item in slot and len(slot) > 1:
                            slot.clear()
                # Check not to be left with duplicates of lenght one
                if slot != []:
                    while self.cards_owned[player].count(slot) > 1:
                        self.cards_owned[player].remove(slot)
                        self.cards_owned[player].append([])
        # Repeat the updating with the most recent information
        for player in self.players_list:
            for slot in self.cards_owned[player]:
                for card in slot:
                    if card in self.cards_not_owned[player]:
                        slot.remove(card)

    # 3) UTILITIES: Functions propedeutic to the functioning of the main ones
    def input_in_list(self, text, type, accusation_list=None):
        text = text + " "
        player_input = input(text).title()
        type = type.lower()  # to capture capitaliztion erros in the code
        ref_list = {"characters" : self.characters, "weapons" : self.weapons,
                    "rooms" : self.rooms, "players" : self.players_list,
                    "accusation" : accusation_list, "items" : self.items}
        while player_input not in ref_list[type]:
            help_word = "list"
            if player_input != help_word.title():
                print("Something went wrong. What you typed does not appear "
                      f"among the {type}. Please retry. If you would "
                      "like to see the list of items of the game type "
                      f"'{help_word}'.\n")
            player_input = input(text).title()
            if player_input == help_word.title():
                print(f"These are the {type}:")
                print(*ref_list[type], sep=", ")
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

    def all_cards_known(self, player):
        '''
        Check if all the information is known about one player
        '''
        counter = 0
        for slot in self.cards_owned[player]:
            if len(slot) == 1:
                counter = counter + 1
        if counter == 3:
            return True
        else:
            return False

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


# To test what was done up to now
game = CluedoGame(players_number=6)
game.main()
input("\nPress any key to exit ")
