"""Behavior tests for the Bash dice roller."""

from pathlib import Path
import re
import subprocess
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "dice.sh"


class DiceTests(unittest.TestCase):
    def run_script(self, *arguments, direct=False):
        command = [str(SCRIPT)] if direct else ["bash", str(SCRIPT)]
        return subprocess.run(
            command + [str(arg) for arg in arguments],
            capture_output=True, text=True, timeout=5, cwd="/tmp",
        )

    def check_rolls(self, count, sides, direct=False):
        result = self.run_script(count, sides, direct=direct)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        rolls = re.findall(r"^Die (\d+): (\d+)$", result.stdout, re.MULTILINE)
        self.assertEqual(len(rolls), count, result.stdout)
        self.assertEqual([int(index) for index, _ in rolls], list(range(1, count + 1)))
        values = [int(value) for _, value in rolls]
        self.assertTrue(all(1 <= value <= sides for value in values), result.stdout)
        totals = re.findall(r"^Total: (\d+)$", result.stdout, re.MULTILINE)
        self.assertEqual(totals, [str(sum(values))], result.stdout)
        return values

    def test_example(self):
        self.check_rolls(4, 6)

    def test_executable_and_independent_of_working_directory(self):
        self.check_rolls(3, 20, direct=True)

    def test_single_sided_dice(self):
        self.assertEqual(self.check_rolls(5, 1), [1] * 5)

    def test_bounds(self):
        for count, sides in [(1, 1), (1, 1000), (100, 1), (100, 1000)]:
            with self.subTest(count=count, sides=sides):
                self.check_rolls(count, sides)

    def test_repeated_roll_ranges_and_totals(self):
        for _ in range(20):
            self.check_rolls(8, 6)

    def test_help(self):
        result = self.run_script("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())

    def test_invalid_arguments(self):
        cases = [
            (), ("4",), ("4", "6", "extra"), ("--help", "6"),
            ("0", "6"), ("-1", "6"), ("101", "6"),
            ("4", "0"), ("4", "-6"), ("4", "1001"),
            ("one", "6"), ("4", "six"), ("1.5", "6"), ("4", "6.5"),
            ("04", "6"), ("4", "06"), ("+4", "6"),
            ("", "6"), ("4", ""), (" 4", "6"), ("4", "6 "),
            ("9" * 100, "6"), ("4", "9" * 100), ("1+1", "6"),
        ]
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_script(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(result.stderr.strip(), result.stdout)
                self.assertNotRegex(result.stdout, r"(?m)^Die \d+:")


if __name__ == "__main__":
    unittest.main(verbosity=2)
