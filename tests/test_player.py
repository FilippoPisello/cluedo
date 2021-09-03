"""Test player class"""

import unittest

from components.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.pl1 = Player("Test", 3)

    def test_all_cards_known_false(self):
        """All cards known is false when player is created"""
        self.assertFalse(self.pl1.all_cards_known)

    def test_all_cards_known_true(self):
        """All cards known is true if player is assigned all the cards"""
        self.pl1.cards_owned = [{"Spa"}, {"Green"}, {"Axe"}]
        self.assertTrue(self.pl1.all_cards_known)

    def test_card_not_owned_is_added(self):
        """Card added to not owned is stored correctly"""
        # Adding one card when none is present
        self.pl1.add_cards_not_owned({"Spa"})
        self.assertEqual(self.pl1.cards_not_owned, {"Spa"})

        # Adding a card when already present
        self.pl1.add_cards_not_owned({"Spa"})
        self.assertEqual(self.pl1.cards_not_owned, {"Spa"})

        # Adding two cards when none is present
        self.pl1.cards_not_owned = set()
        self.pl1.add_cards_not_owned({"Spa", "Green"})
        self.assertEqual(self.pl1.cards_not_owned, {"Spa", "Green"})

        # Adding one duplicate and one new
        self.pl1.add_cards_not_owned({"Spa", "Axe"})
        self.assertEqual(self.pl1.cards_not_owned, {"Spa", "Green", "Axe"})

    def test_remove_card_not_owned(self):
        """Card is removed from the owned ones"""
        # Remove an existing card
        self.pl1.cards_owned = [{"Spa"}, {"Spa", "Axe"}, {"Green"}]
        self.pl1.remove_cards_owned({"Spa"})
        self.assertEqual(self.pl1.cards_owned, [set(), {"Axe"}, {"Green"}])

        # Remove a non-existing card
        self.pl1.cards_owned = [{"Spa"}, {"Spa", "Axe"}, {"Green"}]
        self.pl1.remove_cards_owned({"Rope"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Spa", "Axe"}, {"Green"}])

    def test_card_not_owned_is_removed_from_owned(self):
        """Card added to not owned is removed from the owned ones"""
        # Add an existing owed card to the non-owned ones
        self.pl1.cards_owned = [{"Spa"}, {"Spa", "Axe"}, {"Green"}]
        self.pl1.add_cards_not_owned({"Spa"})
        self.assertEqual(self.pl1.cards_owned, [set(), {"Axe"}, {"Green"}])

        # No effect if add a non-owned card to the non-owned ones
        self.pl1.add_cards_not_owned({"Rope"})
        self.assertEqual(self.pl1.cards_owned, [set(), {"Axe"}, {"Green"}])

    def test_single_card_added_to_owned(self):
        """Single card is correctly added to the owned ones"""
        # Add a single card when no card is owned
        self.pl1.add_cards_owned({"Spa"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, set(), set()])

        # Add a single new card when one individual card is owned
        self.pl1.add_cards_owned({"Green"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green"}, set()])

        # Add a single new card when a pair of cards is owned
        self.pl1.cards_owned = [{"Spa", "Axe"}, set(), set()]
        self.pl1.add_cards_owned({"Green"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa", "Axe"}, {"Green"}, set()])

        # Add a duplicate single card when that card is owned as single
        self.pl1.add_cards_owned({"Green"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa", "Axe"}, {"Green"}, set()])

        # Add a duplicate single card when that card is owned as pair
        self.pl1.add_cards_owned({"Spa"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green"}, set()])

        # Add a duplicate single card when that card is owned as pair twice
        self.pl1.cards_owned = [{"Spa", "Axe"}, {"Green"}, {"Rope", "Spa"}]
        self.pl1.add_cards_owned({"Spa"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green"}, set()])

    def test_multiple_cards_added_to_owned(self):
        """Multiple cards are correctly added to owned ones"""
        # Add multiple cards when no card is owned
        self.pl1.add_cards_owned({"Spa", "Green"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa", "Green"}, set(), set()])

        # Add multiple new cards when a pair of cards is owned
        self.pl1.add_cards_owned({"Axe", "Rope"})
        expected = [{"Spa", "Green"}, {"Axe", "Rope"}, set()]
        self.assertEqual(self.pl1.cards_owned, expected)

        # Add multiple new cards when one individual card is owned
        self.pl1.cards_owned = [{"Spa"}, set(), set()]
        self.pl1.add_cards_owned({"Green", "Rope"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green", "Rope"}, set()])

        # Add a duplicate pair of cards when the pair is owned
        self.pl1.add_cards_owned({"Green", "Rope"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green", "Rope"}, set()])

        # Add a pair of cards when one is owned as single
        self.pl1.add_cards_owned({"Spa", "Axe"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green", "Rope"}, set()])

        # Add three cards when two are owned as a pair
        self.pl1.add_cards_owned({"Green", "Rope", "Axe"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green", "Rope"}, set()])

        # Add two cards when are included in a set of three
        self.pl1.cards_owned = [{"Spa"}, {"Green", "Rope", "Axe"}, set()]
        self.pl1.add_cards_owned({"Green", "Rope"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Green", "Rope"}, set()])

    def test_cards_added_to_owned_when_not_owned(self):
        """Not owned cards are correctly from owned cards"""
        # Add two cards when one of them is not owned
        self.pl1.cards_not_owned = {"Green"}
        self.pl1.add_cards_owned({"Green", "Spa"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, set(), set()])

        # Add three cards when one of them is not owned
        self.pl1.add_cards_owned({"Green", "Rope", "Knife"})
        self.assertEqual(self.pl1.cards_owned, [{"Spa"}, {"Rope", "Knife"}, set()])


if __name__ == "__main__":
    unittest.main()
