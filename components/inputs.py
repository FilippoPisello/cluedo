"""Functions to collect user's inputs"""


def get_user_position(players_number) -> int:
    """Returns an integer for the position of the user in the turn."""
    player_position = None
    while player_position not in range(1, players_number + 1):
        player_position = int(
            input(
                "What is your position in the turn? Type 1 if first, 2 if "
                "second and so on. Please provide a number from 1 to "
                f"{players_number}. "
            )
        )
        if player_position not in range(1, players_number + 1):
            print("The value you provided is not accepted, please retry.")
    return player_position


def get_users_cards(total_cards_per_user: int, items_list: list) -> list[str]:
    """Returns list of cards owned by the user"""
    user_cards = []

    order = [
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
    ]
    for card_counter in order[:total_cards_per_user]:
        msg_displayed = f"Please insert your {card_counter} card"
        user_cards.append(input_in_list(msg_displayed, items_list))
    return user_cards


def get_user_action(active_player_name):
    """Collect user input on the action to be performed"""
    msg_displayed = (
        f"It's the turn of {active_player_name}. "
        "Enter:\n1 if he/she made an accusation \n2 if he/she did not make an "
        "accusation \n3 if a card from the table was revealed.\n"
    )
    actions_allowed = ["1", "2", "3"]
    return input_in_list(msg_displayed, actions_allowed)


def get_accusation(
    characters_list: list[str], weapons_list: list[str], rooms_list: list[str]
) -> list[str]:
    """Collect user input on cards in the accusation"""
    character = input_in_list("Which character?", characters_list)
    weapon = input_in_list("Which weapon?", weapons_list)
    room = input_in_list("Which room?", rooms_list)
    return [character, weapon, room]


def get_player_who_showed(players_names: list[str]) -> str:
    """Collect name of the player who showed the card"""
    msg_displayed = "Which player showed the card?"
    return input_in_list(msg_displayed, players_names)


def get_card_from_accusation(accusation_list: list[str]) -> str:
    """Collect card that was shown among the accusation ones"""
    msg_displayed = "Which card was shown to you?"
    return input_in_list(msg_displayed, accusation_list)


def input_in_list(message: str, control_list: list) -> str:
    """Collects user input and returns it only when in control list"""
    player_input = input(message + "\n").strip().title()

    while player_input not in control_list:
        help_word = "list"

        if player_input != help_word.title():
            print(
                "Something went wrong. What you typed does not appear among the accepted values! "
                "If you would like to see the list of accepted keywords type "
                f"'{help_word}'.\n"
            )

        player_input = input(message + "\n").title().strip().title()
        if player_input == help_word.title():
            print("These are the accepted values:")
            print(*control_list, sep=", ")
    return player_input
