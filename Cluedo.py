
class CluedoGame:
    def __init__(self, players_number=6):
        self.players_number = players_number
        self.suspects = []
        self.my_cards = []
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

    def game_start(self):
        for list_ in [self.characters, self.weapons, self.rooms]:
            self.suspects.append(list_)
        for counter in range(self.cards_per_person):
            order = ["first", "second", "third", "fourth", "fifth", "sixth"
                     "seventh", "eighth", "ninth", "tenth"]
            card_number = order[counter]
            item = self.input_in_items(f"Please insert your {card_number} card")
            self.my_cards.append(item)
            self.remove_from_suspects(item)

        print(self.suspects)  # to be removed
        return

    def input_in_items(self, text):
        text = text + " "
        player_input = str.capitalize(input(text))
        while player_input not in self.items:
            help_word = "list"
            if player_input != str.capitalize(help_word):
                print("Something went wrong. What you typed does not appear "
                      "among the items of the game. Please retry. If you would "
                      "like to see the list of items of the game type "
                      f"'{help_word}'.\n")
            player_input = str.capitalize(input(text))
            if player_input == str.capitalize(help_word):
                print("These are the characters:")
                print(*self.characters, sep=", ")
                print("\nThese are the weapons:")
                print(*self.weapons, sep=", ")
                print("\nThese are the rooms:")
                print(*self.rooms, sep=", ")
        return player_input

    def remove_from_suspects(self, item):
        for list_ in self.suspects:
            if item in list_: list_.remove(item)


# To test what was done up to now
game = CluedoGame(players_number=6)
game.game_start()
