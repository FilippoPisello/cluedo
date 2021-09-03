"""
Tests for the Cluedo class
"""
import unittest

from cluedo import CluedoGame


class TestCluedo(unittest.TestCase):
    def setUp(self) -> None:
        self.game1 = CluedoGame(6)
        self.game2 = CluedoGame(3)

    def test_players_labels(self):
        labels = self.game1.create_players_labels(3)
        expected_labels = [
            "Player 1",
            "Player 2",
            "You",
            "Player 4",
            "Player 5",
            "Player 6",
        ]
        self.assertEqual(labels, expected_labels)

        labels = self.game2.create_players_labels(1, "User")
        expected_labels = [
            "User",
            "Player 2",
            "Player 3",
        ]
        self.assertEqual(labels, expected_labels)


if __name__ == "__main__":
    unittest.main()
