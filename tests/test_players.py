"""
Tests for the Players class
"""
import unittest

from components.players import Players


class TestPlayers(unittest.TestCase):
    def setUp(self) -> None:
        self.pls1 = Players(6, 3, 1)

    def test_players_labels(self):
        labels = self.pls1.create_players_labels(3)
        expected_labels = [
            "Player 1",
            "Player 2",
            "You",
            "Player 4",
            "Player 5",
            "Player 6",
        ]
        self.assertEqual(labels, expected_labels)


if __name__ == "__main__":
    unittest.main()
