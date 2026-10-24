# Dice roller

A Bash script for rolling dice for a game or a quick probability experiment. It prints every roll and the sum of all rolls.

## Usage

Run it from a Bash terminal:

```bash
./dice.sh 4 6
```

This rolls four six-sided dice. You can also run `bash dice.sh 4 6` or use `./dice.sh --help` for usage instructions.

The first argument is the number of dice, from **1 to 100**. The second is the number of sides per die, from **1 to 1000**. Both must be whole numbers without leading zeros. No input files, downloads, or dependencies beyond Bash are needed.

One possible result is:

```text
Rolling 4 dice with 6 sides each:
Die 1: 3
Die 2: 6
Die 3: 1
Die 4: 4
Total: 14
```

Results vary between runs. A one-sided die always rolls 1, so `./dice.sh 3 1` always has a total of 3.

These examples produce an error and a nonzero exit status:

```bash
./dice.sh        # Missing arguments
./dice.sh 0 6    # No dice
./dice.sh 4 six  # Not a number
./dice.sh 04 6   # Leading zero
./dice.sh 4 1001 # Too many sides
```

## How it works

- The command-line arguments choose the number and type of dice.
- `if` statements validate the arguments before any arithmetic.
- The `process_rolls` function contains a `for` loop that rolls each die and adds its value to the total.
- Bash's `$RANDOM` supplies random integers. A short `while` loop rejects the uneven remainder before mapping those integers to dice values, giving every side the same chance.
- `printf` displays the heading, individual rolls, and total.

## Tests

The GitHub Actions workflow checks Bash syntax, executable permissions, normal rolls, input errors, output ranges, and totals on Linux. You can run the same behavior tests with `python3 tests/test_dice.py` on Linux; Python is only needed for these optional tests, not for the dice roller itself.
