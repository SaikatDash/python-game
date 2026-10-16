import unittest
from collections.abc import Iterator

from game import play_game


def scripted_input(answers: list[str]):
    answers_iterator: Iterator[str] = iter(answers)

    def input_fn(_: str) -> str:
        return next(answers_iterator)

    return input_fn


class GameTests(unittest.TestCase):
    def test_rescue_requires_power_keycard_and_distress_signal(self):
        output: list[str] = []
        ending = play_game(
            scripted_input(["e", "r", "q", "b", "s", "x"]),
            output.append,
        )

        self.assertEqual(ending, "rescued")
        self.assertIn("ENDING: RESCUED", output)
        self.assertIn("SCORE: 100 (+25 rescue bonus)", output)

    def test_escape_without_signal_has_a_different_ending(self):
        output: list[str] = []
        ending = play_game(
            scripted_input(["q", "e", "r", "x"]),
            output.append,
        )

        self.assertEqual(ending, "lost")
        self.assertIn("ENDING: LOST IN ORBIT", output)
        self.assertIn("SCORE: 50", output)

    def test_invalid_choice_is_rejected(self):
        output: list[str] = []
        ending = play_game(
            scripted_input(["invalid", "q", "q", "e", "r", "x"]),
            output.append,
        )

        self.assertEqual(ending, "lost")
        self.assertTrue(any("Please choose one of" in line for line in output))

    def test_returning_to_completed_areas_does_not_duplicate_points(self):
        output: list[str] = []
        ending = play_game(
            scripted_input(["e", "r", "e", "q", "q", "b", "s", "b", "x"]),
            output.append,
        )

        self.assertEqual(ending, "rescued")
        self.assertIn("SCORE: 100 (+25 rescue bonus)", output)


if __name__ == "__main__":
    unittest.main()
